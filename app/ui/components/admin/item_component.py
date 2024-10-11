from app.ui.components.character.display_item import ItemDisplayComponent
from app.services.item_service import load_all_items, save_item
from app.services.character_service import save_character
from app.ui.components.admin.item_form import ItemForm
from app.models.items import EquippableItem, Item
from app.models.character import Character
from dataclasses import dataclass, field
from typing import List, Optional
from nicegui import ui


@dataclass
class ItemComponent:
    character: Optional[Character] = None
    items: List[Item] = field(default_factory=list)
    item_display_component = ItemDisplayComponent()

    @ui.refreshable
    def display(self):
        if self.character is None:
            ui.label("Aucun personnage selectionne. Veuillez selectionner un personnage.").classes("text-red-500 text-lg font-semibold")
            return

        ui.label(f"Gestion des Items pour {self.character.name}").classes("text-white text-lg font-semibold")
        self.items = load_all_items()

        ui.button("Creer un item", on_click=self.open_item_form).classes("mt-4 bg-green-500 text-white")

        if not self.items:
            ui.label("Aucun item trouve dans la base de donnees").classes("text-gray-500")
        else:
            with ui.element().classes("grid gap-4 w-full py-4") as grid_container:
                grid_container.classes("sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 xl:grid-cols-10")
                for item in self.items:
                    if isinstance(item, EquippableItem):
                        self.display_item_card(item)

    def display_item_card(self, item: EquippableItem):
        self.item_display_component.display_item_with_dialog(item=item, character=self.character, refresh_callback=self.get_refresh_callback(), big_card=False)

    def open_item_form(self):
        with ui.dialog() as dialog:
            with ui.card().classes("p-8 gap-4 w-96 bg-charsheet"):
                ItemForm()
        dialog.open()

    def get_refresh_callback(self):
        return lambda: self.display.refresh()
