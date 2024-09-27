from dataclasses import dataclass, field
from app.constants.enums import *
from typing import Dict, List
import pickle


@dataclass
class Item:
    name: str = field(default_factory=str)
    description: str = field(default_factory=str)
    image: str = field(default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlJfnLgDiGKYaxVQApYVsxChexmtMbI42TYw&s")
    item_type: ItemType = field(init=False)
    effects: List[Dict[EffectType, Dict]] | None = field(default=None)


@dataclass
class EquippableItem(Item):
    weight: float = 0.0
    equippable_slots: List[SlotType] = field(default_factory=list)


@dataclass
class Scaling:
    STR: Scale = Scale.E
    DEX: Scale = Scale.E
    INT: Scale = Scale.E
    FTH: Scale = Scale.E


@dataclass
class OffensiveItem(EquippableItem):
    damage: int = 0
    damage_type: DamageType = DamageType.PHYSICAL
    scaling: Dict[StatEnum, Scale] = field(default_factory=dict)


@dataclass
class Weapon(OffensiveItem):
    weapon_type: WeaponType = field(default_factory=lambda: WeaponType.SWORD)
    two_handed: bool = field(default_factory=bool)
    max_targets: int = field(default_factory=int)

    def __post_init__(self):
        self.item_type = ItemType.WEAPON


@dataclass
class Spell(OffensiveItem):
    spell_type: SpellType = field(default_factory=SpellType)
    required_stat: Dict[StatEnum, int] = field(default_factory=dict)
    max_targets: int = field(default_factory=int)

    def __post_init__(self):
        self.item_type = ItemType.SPELL
        self.weight = 0


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
    defense: int = field(default_factory=int)
    defense_type_scaling: Dict[DamageType, Scale] = field(default_factory=dict)
    armor_type: ArmorType = field(default_factory=ArmorType)

    def __post_init__(self):
        self.item_type = ItemType.ARMOR


@dataclass
class Shield(EquippableItem):
    block_percentage: float = field(default_factory=float)
    stability: int = field(default_factory=int)

    def __post_init__(self):
        self.item_type = ItemType.SHIELD

    def can_block(self, attacker_damage: int, defender_stamina: int) -> bool:
        required_stamina = attacker_damage * (1 - self.block_percentage)
        return defender_stamina >= required_stamina


@dataclass
class Consumable(Item):
    quantity: int = field(default_factory=int)

    def __post_init__(self):
        self.item_type = ItemType.CONSUMABLE

    @property
    def is_empty(self) -> bool:
        return self.quantity <= 0

    def use(self, target) -> bool:
        if self.is_empty:
            return False

        self.apply_effects(target)
        self.quantity -= 1

        if self.is_empty:
            target.inventory.remove_item(self)

        return True

    def add_quantity(self, amount: int):
        self.quantity += amount
