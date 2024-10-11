from app.constants.enums import CharAlignment, Class, StatEnum
from app.models.effect_manager import EffectManager
from app.models.stats_manager import StatsManager
from app.models.inventory import Inventory
from dataclasses import dataclass, field
from app.models.items import Item
from typing import Dict



@dataclass
class Character:
    photo: str = "https://www.belloflostsouls.net/wp-content/uploads/2022/01/monster-factory-squirtle.jpg"
    effect_manager: EffectManager = field(default_factory=EffectManager)
    inventory: Inventory = field(default_factory=Inventory)
    character_class: Class = field(default_factory=lambda: Class.WARRIOR)
    stats: Dict[StatEnum, int] = field(default_factory=lambda: {stat: 8 for stat in StatEnum})
    stats_manager: StatsManager = field(init=False)
    alignment: CharAlignment = field(default=CharAlignment.TRUE_NEUTRAL)
    story: str = field(default_factory=str)
    species: str = "Humain"
    is_player: bool = False
    name: str = field(default_factory=str)
    gender: str = "Homme"
    age: int = 25
    points_available: int = 27
    souls: int = 0
    level: int = 1

    def __post_init__(self):
        self.stats_manager = StatsManager(max_hp=self.stats.get(StatEnum.VIT, 8), max_stamina=self.stats.get(StatEnum.VIT, 8), max_mh=self.stats.get(StatEnum.CHA, 8))

    def __eq__(self, other):
        if not isinstance(other, Character):
            return False
        return self.name == other.name

    def apply_effects(self, item: Item, remove: bool = False):
        self.effect_manager.apply_item_effects(item, self, remove)

    def remove_effects(self, item: Item):
        self.effect_manager.apply_item_effects(item, self, True)

    def add_item_to_inventory(self, item: Item):
        self.inventory.add_item(item)

    def equip_item(self, item: Item, slot: str):
        self.inventory.equip_item(item, slot)
        self.apply_effects(item)

    def unequip_item(self, item: Item):
        self.inventory.unequip_item(item)
        self.remove_effects(item)

    def take_damage(self, amount: int) -> bool:
        self.stats_manager.take_damage(amount)
        return self.stats_manager.is_dead()

    def restore_hp(self, amount: int):
        self.stats_manager.restore_hp(amount)

    def restore_stamina(self, amount: int):
        self.stats_manager.restore_stamina(amount)

    def get_inventory_items(self):
        return self.inventory.get_items()

    def get_equipped_items(self):
        return self.inventory.get_equipped_items()

    def get_total_defense(self):
        return sum(item.defense for item in self.inventory.get_armor() if item)

    def update_stats(self):
        from app.services.character_service import save_character
        self.stats_manager.update_stats(max_hp=self.stats.get(StatEnum.VIT, 8), max_stamina=self.stats.get(StatEnum.END, 8), max_mental=self.stats.get(StatEnum.CHA, 8))
        save_character(character=self)

    def increase_stat(self, stat: StatEnum, amount: int):
        if stat in self.stats:
            self.stats[stat] += amount
            if self.stats[stat] < 0:
                self.stats[stat] = 0
        else:
            print(f"Statistique {stat} non reconnue pour ce personnage.")
