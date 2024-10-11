from app.models.items import *
from typing import List, Optional
from dataclasses import dataclass, field


from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class BaseManager:
    equipped_items: List[Item] = field(default_factory=list)
    max_items: int = 4
    valid_slot: Optional[SlotType] = None

    def equip(self, item: Item) -> None:
        if self.valid_slot and self.valid_slot not in item.equippable_slots:
            raise ValueError(f"{item.name} cannot be equipped in {self.valid_slot}.")
        if len(self.equipped_items) >= self.max_items:
            raise ValueError(f"Cannot equip more than {self.max_items} items of this type.")
        self.equipped_items.append(item)

    def unequip(self, item: Item) -> None:
        if item in self.equipped_items:
            self.equipped_items.remove(item)

    def can_equip(self, item: Item) -> bool:
        return len(self.equipped_items) < self.max_items and item not in self.equipped_items

    def get_equipped_items(self) -> List[Item]:
        return self.equipped_items


@dataclass
class EquipmentManager(BaseManager):
    equipped_items: Dict[str, Item] = field(default_factory=dict)

    def equip(self, item: Item, slot: str) -> None:
        if not slot:
            raise ValueError("A slot must be specified for equippable items.")
        if slot not in item.equippable_slots:
            raise ValueError(f"{item.name} cannot be equipped in {slot}. Available slots: {item.equippable_slots}.")
        self.equipped_items[slot] = item

    def unequip(self, item: Item) -> None:
        self.equipped_items = {slot: equipped_item for slot, equipped_item in self.equipped_items.items() if equipped_item != item}

    def can_equip(self, item: Item) -> bool:
        return bool(item.equippable_slots) and item not in self.equipped_items.values()

    def get_equipped_items(self) -> List[Item]:
        return list(self.equipped_items.values())


@dataclass
class Inventory:
    items: List[Item] = field(default_factory=list)
    equipment_manager: EquipmentManager = field(default_factory=EquipmentManager)
    spell_manager: BaseManager = field(default_factory=lambda: BaseManager(max_items=4, valid_slot=SlotType.SPELL))
    ring_manager: BaseManager = field(default_factory=lambda: BaseManager(max_items=4, valid_slot=SlotType.RING))

    def get_items(self) -> List[Item]:
        return self.items

    def add_item(self, item: Item) -> None:
        if not isinstance(item, Item):
            raise ValueError("Invalid item")
        self.items.append(item)

    def remove_item(self, item: Item, character) -> None:
        if item in self.items:
            self.items.remove(item)
        self.unequip_item(item=item, character=character)

    def equip_item(self, item: Item, character, slot: Optional[str] = None) -> None:
        if not self.is_equippable(item):
            raise ValueError(f"Item {item.name} cannot be equipped.")
        if item.item_type == ItemType.SPELL:
            self.spell_manager.equip(item)
        elif item.item_type == ItemType.RING:
            self.ring_manager.equip(item)
        else:
            if not slot:
                raise ValueError(f"Slot must be provided for equipping {item.name}.")
            self.equipment_manager.equip(item, slot)
        character.apply_effects(item)

    def unequip_item(self, item: Item, character) -> None:
        if item.item_type == ItemType.SPELL:
            self.spell_manager.unequip(item)
        elif item.item_type == ItemType.RING:
            self.ring_manager.unequip(item)
        else:
            self.equipment_manager.unequip(item)
        character.apply_effects(item=item, remove=True)

    def is_equippable(self, item: Item) -> bool:
        if item.item_type == ItemType.SPELL:
            return self.spell_manager.can_equip(item)
        if item.item_type == ItemType.RING:
            return self.ring_manager.can_equip(item)
        return self.equipment_manager.can_equip(item)

    def get_equipped_items(self) -> List[Item]:
        return self.equipment_manager.get_equipped_items() + self.spell_manager.get_equipped_items() + self.ring_manager.get_equipped_items()

    def organize_by_category(self) -> Dict[str, List[Item]]:
        category_classes = {Weapon: "Armes", Armor: "Armures", Shield: "Boucliers", Spell: "Sorts", Consumable: "Consommables", Ring: "Anneaux", Item: "Autres"}
        categories = {label: [] for label in category_classes.values()}
        for item in self.items:
            for cls, label in category_classes.items():
                if isinstance(item, cls):
                    categories[label].append(item)
                    break
        return categories

    def get_inventory_items(self) -> List[Item]:
        return self.items

    def get_equipped_items_by_type(self, item_type: ItemType) -> List[Item]:
        all_equipped_items = self.get_equipped_items()
        return [item for item in all_equipped_items if item.item_type == item_type.value.upper()]

    def is_item_equipped(self, item_received: Item) -> bool:
        return item_received in self.get_equipped_items()

    def get_equipped_item_by_slot(self, slot: SlotType) -> Optional[Item]:
        return self.equipment_manager.equipped_items.get(slot)
