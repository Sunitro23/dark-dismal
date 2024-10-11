from app.services.character_service import save_character
from app.models.items import Item, SlotType, ItemType, Consumable
from app.constants.constants import readable_slot_names
from app.auth.middleware import AuthMiddleware
from app.models.character import Character
from typing import List, Optional
from nicegui import ui, app
import copy

from app.services.dynamic_form import EditDynamicForm
from app.services.item_service import save_item


class ItemActionService:
    def __init__(self, item: Item, character: Character, refresh_callback):
        self.item = item
        self.character = character
        self.inventory = character.inventory
        self.refresh_callback = refresh_callback

    def get_actions(self):
        actions = []
        if any(self.item is inventory_item for inventory_item in self.inventory.get_inventory_items()):
            if isinstance(self.item, Consumable):
                actions.append(("Utiliser", self.use_item))
            elif self.inventory.is_item_equipped(self.item):
                actions.append(("Desequiper", self.unequip_item))
            elif self.inventory.is_equippable(self.item):
                if self.item.item_type == ItemType.SPELL:
                    actions.append(("Equiper sort", self.equip_item))
                elif len(self.item.equippable_slots) == 1:
                    slot = self.item.equippable_slots[0]
                    print(slot)
                    slot_name = readable_slot_names.get(slot)
                    actions.append((f"Equiper dans {slot_name}", lambda: self.equip_item(slot)))
                else:
                    actions.extend(self.generate_slot_actions(self.item.equippable_slots))
            actions.append(("Jeter", self.throw_item))
            if AuthMiddleware(app).is_admin() and hasattr(self.item, "improvement_level"):
                actions.append(("Ameliorer l'item", self.improve_item))
        else:
            actions.append(("Ajouter à l'inventaire", self.add_to_inventory))
            actions.append(("Modifier", self.edit_item))

        return actions

    def generate_slot_actions(self, slot_options: List[SlotType]):
        return [(f"Equiper {readable_slot_names.get(slot)}", lambda s=slot: self.equip_item(s)) for slot in slot_options]

    def equip_item(self, slot: Optional[str] = None):
        try:
            self.character.inventory.equip_item(item=self.item, slot=slot, character=self.character)
            self.refresh_callback()
            save_character(self.character)
        except ValueError as e:
            raise ValueError(f"Erreur d'equipement: {str(e)}")

    def unequip_item(self):
        try:
            self.character.inventory.unequip_item(self.item, self.character)
            self.refresh_callback()
            save_character(self.character)
        except ValueError as e:
            raise ValueError(f"Erreur de desequipement: {str(e)}")

    def use_item(self):
        self.item.use(self.character)
        self.refresh_callback()
        self.character.apply_effects(self.item)
        save_character(self.character)

    def throw_item(self):
        self.inventory.remove_item(self.item, self.character)
        self.refresh_callback()
        save_character(self.character)

    def add_to_inventory(self):
        try:
            item_copy = copy.deepcopy(self.item)
            self.character.add_item_to_inventory(item_copy)
            self.refresh_callback()
            save_character(self.character)
        except ValueError as e:
            raise ValueError(f"Erreur d'ajout à l'inventaire: {str(e)}")

    def improve_item(self):
        if hasattr(self.item, "improvement_level"):
            self.item.improve()
            self.refresh_callback()
            save_character(self.character)

    def edit_item(self):
        self.dialog = ui.dialog()
        with self.dialog:
            with ui.card().classes("p-8 gap-4 w-96 bg-charsheet"):
                ui.label(f"Modification de {self.item.name}").classes("text-xl font-bold text-center mb-4")
                self.form_container = ui.element().classes("w-full")
                excluded_fields = ["stats_manager", "effect_manager", "inventory"]
                self.dynamic_form = EditDynamicForm(self.form_container, self.submit_form, existing_object=self.item, excluded_fields=excluded_fields)
                self.dynamic_form.create_form()
        self.dialog.open()

    def submit_form(self, form_data):
        if self.dynamic_form.existing_object:
            item = self.dynamic_form.existing_object
            for key, value in form_data.items():
                setattr(item, key, value)
            save_item(item=item)
            ui.notify(f"ITem  '{self.item.name}' modifié avec succès!", color="positive")
            self.form_container.clear()
            self.display.refresh()
            self.dialog.close()
