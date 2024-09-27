from app.models.character import Player
from app.constants.constants import *
from dataclasses import dataclass
from app.utils.ui_utils import *
from typing import Dict, List
from nicegui import ui


@dataclass
class CharacterCard:
    player: Player
    attributes: list = None
    infos: list = None

    @ui.refreshable
    def display(self):
        self.setup()
        with ui.card().tight().classes("flex flex-col items-stretch box-border overflow-hidden shadow-2xl bg-charsheet"):
            self.display_header()
            self.display_info_section()
            self.display_story()

    def setup(self):
        self.attributes = [
            ("Vitalité", f"{FILE_ICONS}/icon-vit.png", self.player.stats["VIT"]),
            ("Force", f"{FILE_ICONS}/icon-str.png", self.player.stats["STR"]),
            ("Dextérité", f"{FILE_ICONS}/icon-dex.png", self.player.stats["DEX"]),
            ("Intelligence", f"{FILE_ICONS}/icon-int.png", self.player.stats["INT"]),
            ("Endurance", f"{FILE_ICONS}/icon-end.png", self.player.stats["END"]),
            ("Charisme", f"{FILE_ICONS}/icon-char.png", self.player.stats["CHA"]),
            ("Agilité", f"{FILE_ICONS}/icon-agl.png", self.player.stats["AGL"]),
            ("Foi", f"{FILE_ICONS}/icon-fth.png", self.player.stats["FTH"]),
        ]
        self.infos = [
            ("Nom", self.player.name),
            ("Âge", f"{self.player.age} ans"),
            ("Classe", self.player.player_class),
            ("Espèce", self.player.species),
            ("Alignement", self.player.alignment),
            ("Genre", self.player.gender),
        ]

    def display_header(self):
        with ui.row().classes("w-full h-[40%] flex justify-between items-stretch"):
            with ui.column().classes("w-[50%] aspect-square p-2"):
                ui.image(self.player.photo).classes("w-full h-full object-cover rounded-lg shadow-xl")
            with ui.column().classes("w-[50%] aspect-square"):
                self.display_attributes()

    def display_info_section(self):
        with ui.column().classes("h-[20%] w-full"):
            with ui.grid(columns=2).classes("w-full h-full p-4"):
                for label, value in self.infos:
                    with ui.column().classes("w-full"):
                        with ui.row().classes("flex items-center justify-between"):
                            ui.label(f"{label} :").classes("font-bold text-xs sm:text-sm md:text-base whitespace-nowrap overflow-visible text-ellipsis shrink-0")
                            ui.label(f"{value}").classes("text-xs sm:text-sm md:text-base whitespace-nowrap overflow-visible text-right grow")
                        ui.separator().classes("my-2 bg-black w-[75%] sm:w-[90%] h-[1px]")

    def display_story(self):
        with ui.column().classes("h-[40%] w-full overflow-y-auto story-content"):
            ui.label(self.player.story).classes("text-justify story-content w-full p-4")

    def display_attributes(self):
        with ui.row().classes("w-full h-full p-2"):
            with ui.column().classes("bg-black text-white rounded-md shadow-xl w-full h-full p-2"):
                ui.label("Attributs").classes("font-bold text-left")
                ui.separator().classes("my-1 bg-white")
                with ui.column().classes("w-full h-full flex flex-col justify-between"):
                    for attribute, icon_url, value in self.attributes:
                        modifier = (value - 10) // 2
                        self.display_single_attribute(attribute, icon_url, value, modifier)

    def display_single_attribute(self, attribute, icon_url, value, modifier):
        with ui.row().classes("flex items-center justify-between gap-1 h-1/8"):
            with ui.row().classes("flex items-center gap-1"):
                ui.image(icon_url).classes("w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6")
                ui.label(attribute).classes("text-left text-xs sm:text-sm md:text-base")
            with ui.row().classes("flex justify-end gap-1"):
                ui.label(str(value)).classes("text-right text-xs sm:text-sm md:text-base")
                ui.label(f"({modifier:+d})").classes("text-gray-400 text-right text-xs sm:text-sm md:text-base")

    def refresh_display(self):
        self.display.refresh()


class CharInventory:
    def __init__(self, player: Player, refresh_callback):
        self.player = player
        self.current_tab = "Equipé"
        self.refresh_callback = refresh_callback

    @ui.refreshable
    def display(self):
        with ui.column().classes("text-white w-full"):
            self.display_categories()

    def display_categories(self):
        equipped_items_by_slot = self.player.inventory.organize_equipped_by_slot()
        categories = {"Equipé": equipped_items_by_slot}
        categories.update(self.player.inventory.organize_by_category())

        with ui.card().classes("bg-inherit h-full"):
            with ui.tabs(on_change=self.on_tab_change) as tabs:
                for label in categories.keys():
                    ui.tab(label)

            with ui.tab_panels(tabs, value=self.current_tab).classes("bg-inherit w-full"):
                for label, items in categories.items():
                    with ui.tab_panel(label):
                        if isinstance(items, dict):
                            self.display_equipped_by_slot(items)
                        elif items:
                            with ui.column().classes("w-full gap-2"):
                                for item in items:
                                    display_item_with_dialog(item, self.player, self.refresh_callback)
                        else:
                            ui.label("Aucun item dans cette catégorie.").classes("text-gray-500")

    def display_equipped_by_slot(self, equipped_by_slot: Dict[str, List[Item]]):
        for slot, items in equipped_by_slot.items():
            slot_name = readable_slot_names.get(slot, slot.capitalize())
            with ui.column().classes("w-full gap-2"):
                ui.label(f"{slot_name}").classes("text-lg font-bold")
                if items:
                    for item in items:
                        display_item_with_dialog(item, self.player, self.refresh_callback)
                else:
                    ui.label(f"Aucun objet équipé dans {slot_name}.").classes("text-gray-500")

    def refresh_display(self):
        self.display.refresh()

    def on_tab_change(self, event):
        self.current_tab = event.value


@dataclass
class PlayerPage:
    player: Player
    character_card: CharacterCard = None
    char_inventory: CharInventory = None

    def __post_init__(self):
        self.character_card = CharacterCard(player=self.player)
        self.char_inventory = CharInventory(player=self.player, refresh_callback=self.refresh_display_all)

    @ui.refreshable
    def display_page(self):
        with ui.row().classes("w-full justify-evenly items-start flex-wrap md:flex-nowrap"):
            with ui.column().classes("w-full md:w-1/2 flex-shrink-0 max-w-full"):
                self.character_card.display()
            with ui.column().classes("w-full md:w-1/2 flex-shrink-0 max-w-full"):
                self.char_inventory.display()

    def refresh_display_all(self):
        print("Refresh All")
        self.character_card.refresh_display()
        self.char_inventory.refresh_display()
        self.display_page.refresh()
