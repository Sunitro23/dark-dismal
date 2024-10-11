from app.ui.components.character.character_inventory import CharacterInventory
from app.ui.components.character.character_card import CharacterCard
from app.ui.components.character.fight import FightDisplay
from app.constants.constants import head_html
from app.models.character import Character
from nicegui import ui


class MainPage:
    def __init__(self, character):
        self.character: Character = character

    @ui.refreshable
    def display(self):
        self.set_ui_colors()
        self.display_menu()
        self.display_fight()

        if not self.character:
            ui.navigate.to("/create_character")

    def set_ui_colors(self):
        ui.add_head_html(head_html)
        ui.colors(primary="#000000", secondary="#000000", accent="#F58840", positive="#B85252")

    def display_menu(self):
        with ui.row().classes("bg-black p-2 gap-x-4 flex items-center w-full"):
            self.display_character_info()
            self.display_menu_buttons()
            self.display_health_bar()
            self.display_stamina_bar()
            self.display_mental_bar()

    def display_character_info(self):
        with ui.row().classes("items-center gap-2"):
            ui.image("icons/level.png").classes("h-8 w-8")
            ui.label(f"{self.character.level}").classes("text-[#EADEDE] text-lg font-semibold")
            ui.image("icons/souls.png").classes("h-8 w-8")
            ui.label(f"{self.character.souls}").classes("text-[#EADEDE] text-lg font-semibold")

    def display_menu_buttons(self):
        with ui.row().classes("ml-auto gap-2"):
            ui.button(icon="info", on_click=self.show_character_card).classes("text-[#EADEDE] rounded-full h-8 w-8 flex items-center justify-center")
            ui.button(icon="inventory", on_click=self.show_character_inventory).classes("text-[#EADEDE] rounded-full h-8 w-8 flex items-center justify-center")

    def display_health_bar(self):
        with ui.row().classes("relative w-40 h-8"):
            ui.linear_progress(value=self.character.stats_manager.current_hp / self.character.stats_manager.max_hp, size="100%", show_value=False, color="#B85252").classes("w-full h-full")
            ui.label(f"{self.character.stats_manager.current_hp}/{self.character.stats_manager.max_hp}").classes("absolute inset-0 text-center text-[#EADEDE]").style("line-height: 2rem")

    def display_stamina_bar(self):
        with ui.row().classes("relative w-40 h-8"):
            ui.linear_progress(value=self.character.stats_manager.current_stamina / self.character.stats_manager.max_stamina, size="100%", show_value=False, color="#008000").classes("w-full h-full")
            ui.label(f"{self.character.stats_manager.current_stamina}/{self.character.stats_manager.max_stamina}").classes("absolute inset-0 text-center text-[#EADEDE]").style("line-height: 2rem")

    def display_mental_bar(self):
        with ui.row().classes("relative w-40 h-8"):
            ui.linear_progress(value=self.character.stats_manager.current_stamina / self.character.stats_manager.max_stamina, size="100%", show_value=False, color="#5a5a5a").classes("w-full h-full")
            ui.label(f"{self.character.stats_manager.current_mh}/{self.character.stats_manager.max_mh}").classes("absolute inset-0 text-center text-[#EADEDE]").style("line-height: 2rem")

    def display_fight(self):
        FightDisplay(character=self.character).display_fight()

    def show_character_card(self):
        with ui.dialog() as dialog:
            CharacterCard(self.character).display()
        dialog.open()

    def show_character_inventory(self):
        with ui.dialog() as dialog:
            with ui.card().classes("w-4/5 max-w-max h-4/5 content-start bg-[#000000]").style("max-width: max-content !important;"):
                CharacterInventory(self.character).display()
        dialog.open()
