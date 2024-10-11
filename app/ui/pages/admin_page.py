from app.ui.components.admin.character_component import CharacterComponent
from app.ui.components.admin.item_component import ItemComponent
from app.constants.constants import head_html
from app.ui.pages.main_page import MainPage
from app.models.character import Character
from dataclasses import dataclass, field
from typing import Optional
from nicegui import ui


@dataclass
class AdminPage:
    item_component: ItemComponent = field(default_factory=ItemComponent)
    character_component: CharacterComponent = field(default_factory=CharacterComponent)
    selected_character: Optional[Character] = None

    @ui.refreshable
    def display(self):
        ui.add_head_html(head_html)
        ui.colors(primary="#000000", secondary="#282A3A", accent="#735F32", positive="#C69749")
        with ui.tabs().classes("bg-zinc-800 w-full text-white") as self.tabs:
            ui.tab("Personnages")
            ui.tab("Items").bind_enabled(self, "is_player_selected")
            ui.tab("Inventory").bind_enabled(self, "is_player_selected")

        with ui.tab_panels(self.tabs, value="Personnages").classes("bg-inherit w-full"):
            with ui.tab_panel("Personnages"):
                self.character_component.select_callback = self.select_character
                self.character_component.display()

            with ui.tab_panel("Items"):
                if self.selected_character:
                    self.item_component.character = self.selected_character
                    self.item_component.display()

            with ui.tab_panel("Inventory"):
                if self.selected_character:
                    MainPage(self.selected_character).display()

    def select_character(self, character: Character):
        self.selected_character = character
        self.display.refresh()
        ui.notify(f"Personnage {character.name} sélectionné!")

    @property
    def is_player_selected(self):
        return self.selected_character is not None
