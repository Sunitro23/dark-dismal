from app.constants.constants import readable_slot_names
from app.models.items import Consumable, Item
from app.constants.enums import ItemType, SlotType
from app.models.character import Player
from typing import List, Optional
from nicegui import ui


class ItemMenu:
    def __init__(self, item: Item, player: Player, refresh_callback):
        self.item = item
        self.player = player
        self.refresh_callback = refresh_callback
        self.inventory = player.inventory
        self.actions = self.get_actions()

    def show(self):
        with ui.menu().props("auto-close").classes("bg-transparent"):
            for label, method in self.actions:
                ui.menu_item(label, on_click=method).classes("bg-[#282A3A] text-white")

    def get_actions(self):
        actions = []
        if isinstance(self.item, Consumable):
            actions.append(("Utiliser", self.use_item))
        elif self.inventory.is_item_equipped(self.item):
            actions.append(("Déséquiper", self.unequip_item))
        elif self.inventory.is_equippable(self.item):
            if self.item.item_type == ItemType.SPELL:
                actions.append(("Équiper sort", self.equip_item))
            elif len(self.item.equippable_slots) == 1:
                slot = self.item.equippable_slots[0]
                slot_name = readable_slot_names.get(slot, slot.value)
                actions.append((f"Équiper dans {slot_name}", lambda: self.equip_item(slot)))
            else:
                actions.extend(self.generate_slot_actions(self.item.equippable_slots))
        actions.append(("Jeter", self.throw_item))
        return actions

    def generate_slot_actions(self, slot_options: List[SlotType]):
        return [(f"Équiper {readable_slot_names.get(slot, slot.value)}", lambda s=slot: self.equip_item(s)) for slot in slot_options]

    def equip_item(self, slot: Optional[str] = None):
        try:
            self.player.equip(self.item, slot)
            self.refresh_callback()
        except ValueError as e:
            ui.notify(str(e))

    def unequip_item(self):
        try:
            self.player.unequip(self.item)
            self.refresh_callback()
        except ValueError as e:
            ui.notify(str(e))

    def use_item(self):
        self.item.use(self.player)
        self.refresh_callback()

    def throw_item(self):
        self.inventory.remove_item(self.item)
        self.refresh_callback()
