from app.constants.constants import readable_slot_names
from dataclasses import dataclass, field
from typing import List, Optional
from app.models.items import *
from faker import Faker
import random


@dataclass
class Inventory:
    items: List[Item] = field(default_factory=list)
    equipped_items: Dict[str, Item] = field(default_factory=dict)
    equipped_rings: List[Item] = field(default_factory=list)
    equipped_spells: List[Item] = field(default_factory=list)
    MAX_RINGS: int = 4
    MAX_SPELLS: int = 4

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        if item in self.items:
            self.items.remove(item)
        if item in self.equipped_spells:
            self.equipped_spells.remove(item)
        if item in self.equipped_rings:
            self.equipped_rings.remove(item)
        self.equipped_items = {slot: equipped_item for slot, equipped_item in self.equipped_items.items() if equipped_item != item}

    def equip_item(self, item: Item, slot: Optional[str] = None) -> None:
        if item.item_type == ItemType.SPELL:
            self._equip_spell(item)
        elif item.item_type == ItemType.RING:
            self._equip_ring(item)
        else:
            self._equip_item(item, slot)

    def _equip_spell(self, item: Item) -> None:
        if len(self.equipped_spells) >= self.MAX_SPELLS:
            raise ValueError(f"Cannot equip more than {self.MAX_SPELLS} spells.")
        if item in self.equipped_spells:
            raise ValueError(f"{item.name} is already equipped.")
        self.equipped_spells.append(item)

    def _equip_ring(self, item: Item) -> None:
        if len(self.equipped_rings) >= self.MAX_RINGS:
            raise ValueError(f"Cannot equip more than {self.MAX_RINGS} rings.")
        if item in self.equipped_rings:
            raise ValueError(f"{item.name} is already equipped.")
        self.equipped_rings.append(item)

    def _equip_item(self, item: Item, slot: str) -> None:
        if not slot:
            raise ValueError("A slot must be specified for equippable items.")
        if slot not in item.equippable_slots:
            raise ValueError(f"{item.name} cannot be equipped in {slot}.")
        self.equipped_items[slot] = item

    def unequip_item(self, item: EquippableItem) -> None:
        if item in self.equipped_spells:
            self.equipped_spells.remove(item)
        elif item in self.equipped_rings:
            self.equipped_rings.remove(item)
        else:
            self.equipped_items = {slot: equipped_item for slot, equipped_item in self.equipped_items.items() if equipped_item != item}

    def is_item_equipped(self, item: EquippableItem) -> bool:
        return item in self.equipped_spells or item in self.equipped_rings or item in self.equipped_items.values()

    def is_equippable(self, item: EquippableItem) -> bool:
        if item.item_type == ItemType.SPELL:
            return len(self.equipped_spells) < self.MAX_SPELLS and not self.is_item_equipped(item)
        if item.item_type == ItemType.RING:
            return len(self.equipped_rings) < self.MAX_RINGS and not self.is_item_equipped(item)
        return len(item.equippable_slots) > 0 and not self.is_item_equipped(item)

    def get_equipped_items(self) -> List[Item]:
        return list(self.equipped_items.values()) + self.equipped_spells + self.equipped_rings

    def get_inventory_items(self) -> List[Item]:
        equipped = self.get_equipped_items()
        return [item for item in self.items if item not in equipped]

    def organize_by_category(self) -> Dict[str, List[Item]]:
        category_classes = {Weapon: "Armes", Armor: "Armures", Shield: "Boucliers", Spell: "Sorts", Consumable: "Consommables", Ring: "Anneaux", Item: "Autres"}
        categories = {label: [] for label in category_classes.values()}
        for item in self.items:
            for cls, label in category_classes.items():
                if isinstance(item, cls):
                    categories[label].append(item)
                    break
        return categories

    def organize_equipped_by_slot(self) -> Dict[str, List[Item]]:
        equipped_by_slot = {readable_slot_names.get(slot, slot): [] for slot in readable_slot_names.keys()}
        for slot, item in self.equipped_items.items():
            slot_name = readable_slot_names.get(slot, slot)
            equipped_by_slot[slot_name].append(item)
        equipped_by_slot["Sorts"] = self.equipped_spells
        equipped_by_slot["Anneaux"] = self.equipped_rings
        return equipped_by_slot


faker = Faker()


class InventoryBuilderRandom:

    def add_random_weapon(self):
        name = faker.word().capitalize() + " Sword"
        description = faker.sentence()
        damage = random.randint(5, 20)
        damage_type = random.choice([DamageType.PHYSICAL, DamageType.FIRE, DamageType.MAGIC])
        weapon_type = random.choice([WeaponType.SWORD, WeaponType.AXE])
        scaling = {"STR": random.choice([Scale.A, Scale.B, Scale.C]), "DEX": random.choice([Scale.A, Scale.B, Scale.C])}
        weight = random.randint(2, 6)
        equippable_slots = [SlotType.LEFT_HAND, SlotType.RIGHT_HAND]
        return Weapon(name=name, description=description, damage=damage, damage_type=damage_type, weapon_type=weapon_type, scaling=scaling, weight=weight, equippable_slots=equippable_slots)

    def add_random_armor(self):
        name = faker.word().capitalize() + " Armor"
        description = faker.sentence()
        defense = random.randint(1, 5)
        defense_type_scaling = {DamageType.PHYSICAL: random.choice([Scale.A, Scale.B, Scale.C]), DamageType.MAGIC: random.choice([Scale.A, Scale.B, Scale.C])}
        armor_type = random.choice([ArmorType.LIGHT, ArmorType.HEAVY])
        weight = random.randint(2, 6)
        equippable_slots = [random.choice([SlotType.BOOTS, SlotType.CHESTPLATE, SlotType.GLOVES, SlotType.HELMET])]
        return Armor(name=name, description=description, defense=defense, defense_type_scaling=defense_type_scaling, armor_type=armor_type, weight=weight, equippable_slots=equippable_slots)

    def add_random_shield(self):
        name = faker.word().capitalize() + " Shield"
        description = faker.sentence()
        block_percentage = random.uniform(0.5, 1.0)
        stability = random.randint(2, 8)
        weight = random.randint(2, 6)
        equippable_slots = [SlotType.LEFT_HAND, SlotType.RIGHT_HAND]
        return Shield(name=name, description=description, block_percentage=block_percentage, stability=stability, weight=weight, equippable_slots=equippable_slots)

    def add_random_spell(self):
        name = faker.word().capitalize() + " Spell"
        description = faker.sentence()
        damage = random.randint(10, 30)
        damage_type = random.choice([DamageType.FIRE, DamageType.MAGIC, DamageType.LIGHTNING])
        required_stat = {"INT": random.randint(8, 20)}
        scaling = {"INT": random.choice([Scale.A, Scale.B, Scale.C])}
        spell_type = random.choice([SpellType.MIRACLE, SpellType.PYROMANCY, SpellType.SPELL])
        return Spell(name=name, description=description, damage=damage, damage_type=damage_type, spell_type=spell_type, required_stat=required_stat, scaling=scaling)

    def add_random_consumable(self):
        name = faker.word().capitalize() + " Potion"
        description = faker.sentence()
        effects = [{"restore_hp": {"value": random.randint(10, 50), "stat": "PV"}}]
        quantity = random.randint(1, 5)
        return Consumable(name=name, description=description, effects=effects, quantity=quantity)

    def add_random_ring(self):
        name = faker.word().capitalize() + " Ring"
        description = faker.sentence()
        effects = [{"boost_stat": {"stat": random.choice(["STR", "DEX", "INT"]), "value": random.randint(1, 5)}}]
        weight = random.randint(2, 6)
        return Ring(name=name, description=description, weight=weight, effects=effects)

    def build(self):
        return self.items
