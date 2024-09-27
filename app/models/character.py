from app.models.stats_manager import StatsManager
from app.constants.enums import Class, EffectType
from app.models.inventory import Inventory
from dataclasses import dataclass, field
from app.models.items import Item
from typing import Dict, Optional


@dataclass
class Character:
    name: str
    stats: Dict[str, int]
    photo: str
    inventory: Inventory = field(default_factory=Inventory)
    stats_manager: StatsManager = field(init=False)

    def __post_init__(self):
        vit = self.stats.get("VIT", 10)
        end = self.stats.get("END", 10)
        self.stats_manager = StatsManager(max_hp=vit, max_stamina=end)

    def apply_or_remove_effects(self, item: Item, target=None, remove: bool = False):
        target = target or self
        multiplier = -1 if remove else 1
        if hasattr(item, "effects") and item.effects:
            for effect in item.effects:
                for effect_type, value in effect.items():
                    if effect_type == EffectType.RESTORE_HP.value:
                        target.restore_hp(value["value"] * multiplier)
                    elif effect_type == EffectType.RESTORE_STA.value:
                        target.restore_stamina(value["value"] * multiplier)
                    elif effect_type == EffectType.BOOST_STAT.value:
                        target.increase_stat(value["stat"], value["value"] * multiplier)

    def increase_stat(self, stat_to_boost: str, boost_value: int):
        self.stats[stat_to_boost] = self.stats.get(stat_to_boost, 0) + boost_value

    def check_if_dead(self) -> bool:
        if self.stats_manager.current_hp <= 0:
            self.status = "dead"
            return True
        return False

    def take_damage(self, amount: int) -> bool:
        self.stats_manager.take_damage(amount)
        return self.check_if_dead()

    def restore_hp(self, amount: int):
        self.stats_manager.restore_hp(amount)

    def restore_stamina(self, amount: int):
        self.stats_manager.restore_stamina(amount)

    def use_stamina(self, amount: int) -> bool:
        return self.stats_manager.use_stamina(amount)

    def add_item_to_inventory(self, item: Item):
        self.inventory.add_item(item)

    def remove_item_from_inventory(self, item: Item):
        self.inventory.remove_item(item)

    def equip(self, item: Item, slot: str):
        self.inventory.equip_item(item, slot)
        self.apply_or_remove_effects(item=item)

    def unequip(self, item: Item):
        self.inventory.unequip_item(item)
        self.apply_or_remove_effects(item=item, remove=True)

    def show_inventory(self):
        return self.inventory.get_inventory_items()

    def show_equipment(self):
        return self.inventory.get_equipped_items()

    def get_equipped_in_slot(self, slot: str) -> Optional[Item]:
        return self.inventory.equipment_slots.get(slot)


class Player(Character):
    player_class: Class
    alignment: str
    username: str
    species: str
    gender: str
    story: str
    age: int

    def __init__(self, name: str, stats: Dict[str, int], photo: str, player_class: str, alignment: str, species: str, gender: str, story: str, age: int):
        super().__init__(name=name, stats=stats, photo=photo)
        self.player_class = player_class
        self.alignment = alignment
        self.species = species
        self.gender = gender
        self.story = story
        self.age = age

        # Dictionnaire des bonus par classe
        class_stat_bonus = {
            Class.WARRIOR: {"STR": 1, "END": 1},
            Class.KNIGHT: {"END": 2},
            Class.WANDERER: {"DEX": 1, "END": 1},
            Class.THIEF: {"DEX": 1, "AGL": 1},
            Class.BANDIT: {"STR": 2},
            Class.HUNTER: {"DEX": 2},
            Class.SORCERER: {"INT": 2},
            Class.PYROMANCER: {"INT": 1, "FTH": 1},
            Class.CLERIC: {"FTH": 2},
            Class.DEPRIVED: {"CHA": 2},
        }
        if player_class in class_stat_bonus:
            for stat, bonus in class_stat_bonus[player_class].items():
                self.stats[stat] = self.stats.get(stat, 0) + bonus
        self.stats_manager = StatsManager(max_hp=self.stats.get("VIT", 10), max_stamina=self.stats.get("END", 10))
