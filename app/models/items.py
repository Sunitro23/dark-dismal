from app.services.item_service import save_item
from dataclasses import dataclass, field
from typing import Dict, List
from app.constants.enums import *


@dataclass
class Item:
    name: str = field(default_factory=str)
    description: str = field(default_factory=str)
    image: str = field(default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlJfnLgDiGKYaxVQApYVsxChexmtMbI42TYw&s")
    item_type: ItemType = field(init=False)
    effects: Dict[AllStat, int] = field(default=None)


@dataclass
class EquippableItem(Item):
    weight: float = 0.0
    equippable_slots: List[SlotType] = field(default_factory=list)
    improvement_level: int = 0

    def improve(self):
        if self.improvement_level < 15:
            self.improvement_level += 1
            self.update_stats()
        else:
            raise ValueError("L'item a dejà atteint le niveau maximum d'amelioration.")

    def update_stats(self):
        pass


@dataclass
class OffensiveItem(EquippableItem):
    damage: int = 0
    required_stat: Dict[StatEnum, int] = field(default_factory=dict)
    damage_type: DamageType = DamageType.PHYSICAL
    scaling: Dict[StatEnum, Scale] = field(default_factory=dict)
    max_targets: int = field(default_factory=int)
    range: int = 1

    def update_stats(self):
        self.damage += 1


@dataclass
class Weapon(OffensiveItem):
    weapon_type: WeaponType = field(default_factory=lambda: WeaponType.STRAIGHT_SWORD)
    two_handed: bool = field(default_factory=bool)

    def __post_init__(self):
        self.item_type = ItemType.WEAPON


@dataclass
class Spell(OffensiveItem):
    spell_type: SpellType = SpellType.SPELL
    max_uses: int = 1
    uses: int = 1

    def __post_init__(self):
        self.item_type = ItemType.SPELL
        self.weight = 0

    def use_spell(self):
        if self.uses > 0:
            self.uses -= 1


@dataclass
class Ring(EquippableItem):
    def __post_init__(self):
        self.item_type = ItemType.RING
        self.equippable_slots = [SlotType.RING]


@dataclass
class DefenseTypeScaling:
    physical: Scale = Scale.E
    magic: Scale = Scale.E
    fire: Scale = Scale.E
    lightning: Scale = Scale.E


@dataclass
class Armor(EquippableItem):
    defense: int = 0
    defense_type_scaling: Dict[DamageType, Scale] = field(default_factory=dict)

    def __post_init__(self):
        self.item_type = ItemType.ARMOR
        self.base_defense = self.defense

    def update_stats(self):
        self.defense = self.base_defense + self.improvement_level


@dataclass
class Shield(EquippableItem):
    block_percentage: float = field(default_factory=float)
    stability: int = field(default_factory=int)

    def __post_init__(self):
        self.item_type = ItemType.SHIELD
        self.base_stability = self.stability

    def update_stats(self):
        self.stability = self.base_stability + self.improvement_level

    def can_block(self, attacker_damage: int, defender_stamina: int) -> bool:
        required_stamina = attacker_damage * (1 - self.block_percentage)
        return defender_stamina >= required_stamina - self.improvement_level @ dataclass


@dataclass
class Consumable(Item):
    quantity: int = field(default=1)

    def __post_init__(self):
        self.item_type = ItemType.CONSUMABLE

    @property
    def is_empty(self) -> bool:
        return self.quantity <= 0

    def add_quantity(self, amount: int):
        self.quantity += amount


@dataclass
class Scaling:
    STR: Scale = Scale.E
    DEX: Scale = Scale.E
    INT: Scale = Scale.E
    FTH: Scale = Scale.E


@dataclass
class ItemFactory:
    @staticmethod
    def create_item(data: Dict) -> Item:
        if "quantity" in data and isinstance(data["quantity"], float):
            data["quantity"] = int(data["quantity"])

        item_type = data.pop("item_type", "").lower()

        if item_type == "weapon":
            item = Weapon(**data)
        elif item_type == "spell":
            item = Spell(**data)
        elif item_type == "armor":
            item = Armor(**data)
        elif item_type == "shield":
            item = Shield(**data)
        elif item_type == "consumable":
            item = Consumable(**data)
        elif item_type == "ring":
            item = Ring(**data)
        else:
            item = Item(**data)

        item.item_type = item_type.upper()
        save_item(item)
        return item
