from app.ui.components.character.display_item import ItemDisplayComponent
from app.constants.constants import readable_slot_names
from app.models.inventory import Inventory
from app.models.character import Character
from typing import Any, Dict, List
from app.models.items import Item
from nicegui import ui



class CharacterInventory:
    def __init__(self, character: Character):
        self.character = character
        self.current_tab = "Equipe"
        self.item_display_component = ItemDisplayComponent()

    @ui.refreshable
    def display(self):
        with ui.column().classes("text-white w-full"):
            self.display_categories()

    def display_categories(self):
        if not hasattr(self.character, "inventory") or not isinstance(self.character.inventory, Inventory):
            self.character.inventory = Inventory()

        equipped_items_by_slot = self.character.inventory.get_equipped_items()
        categories = self.get_categories(equipped_items_by_slot)
        category_icons = self.get_category_icons()

        with ui.card().classes("bg-inherit h-full w-full"):
            with ui.tabs(on_change=self.on_tab_change).classes("w-full flex") as tabs:
                self.create_tabs(categories, category_icons)
            with ui.tab_panels(tabs, value=self.current_tab).classes("bg-inherit w-full"):
                self.create_tab_panels(categories)

    def get_categories(self, equipped_items_by_slot: Dict[str, List[Item]]):
        categories = {"Equipe": equipped_items_by_slot}
        categories.update(self.character.inventory.organize_by_category())
        return categories

    def get_category_icons(self):
        return {
            "Equipe": "icons/equipped.png",
            "Armes": "icons/weapons.png",
            "Armures": "icons/armors.png",
            "Boucliers": "icons/shields.png",
            "Sorts": "icons/spells.png",
            "Consommables": "icons/consumables.png",
            "Anneaux": "icons/rings.png",
            "Autres": "icons/others.png",
        }

    def create_tabs(self, categories: Dict[str, Any], category_icons: Dict[str, str]):
        for label in categories.keys():
            image_src = category_icons.get(label)
            with ui.tab(name=label, label="").classes("flex-1"):
                ui.image(image_src).classes("aspect-square w-16 h-16 mx-auto")
                ui.tooltip(f"{label}").classes("absolute")

    def create_tab_panels(self, categories: Dict[str, Any]):
        for label, items in categories.items():
            with ui.tab_panel(label):
                if isinstance(items, dict):
                    self.display_equipped_by_slot(items)
                elif items:
                    self.display_items_list(items)
                else:
                    ui.label("Aucun item dans cette categorie.").classes("text-gray-500")

    def display_equipped_by_slot(self, equipped_by_slot: Dict[str, List[Item]]):
        for slot, items in equipped_by_slot.items():
            slot_name = readable_slot_names.get(slot, slot.capitalize())
            with ui.column().classes("w-full gap-2"):
                ui.label(f"{slot_name}").classes("text-lg font-bold")
                if items:
                    self.display_items_list(items)
                else:
                    ui.label(f"Aucun objet equipe dans {slot_name}.").classes("text-gray-500")

    def display_items_list(self, items: List[Item]):
        with ui.column().classes("w-full gap-2"):
            for item in items:
                self.item_display_component.display_item_with_dialog(item=item, character=self.character, refresh_callback=self.get_refresh_callback())

    def on_tab_change(self, event):
        if self.current_tab != event.value:
            self.current_tab = event.value
            self.display.refresh()

    def get_refresh_callback(self):
        return lambda: self.display.refresh()
