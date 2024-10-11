from app.models.character import Character
from nicegui import ui


class CharacterBarDisplay:
    def __init__(self, character: Character):
        self.character = character

    def display_health_bar(self):
        with ui.row().classes("relative w-full h-8 mb-2 mx-auto"):
            ui.linear_progress(value=self.get_health_percentage(), size="100%", show_value=False, color="#B85252").classes("w-full h-full rounded")
            ui.label(f"{self.character.stats_manager.current_hp}/{self.character.stats_manager.max_hp}").classes("absolute inset-0 text-center text-[#EADEDE] text-sm").style("line-height: 2rem;")

    def display_stamina_bar(self):
        with ui.row().classes("relative w-full h-8 mb-2 mx-auto"):
            ui.linear_progress(value=self.get_stamina_percentage(), size="100%", show_value=False, color="#F58840").classes("w-full h-full rounded")
            ui.label(f"{self.character.stats_manager.current_stamina}/{self.character.stats_manager.max_stamina}").classes("absolute inset-0 text-center text-[#EADEDE] text-sm").style(
                "line-height: 2rem"
            )

    def get_health_percentage(self):
        return self.character.stats_manager.current_hp / self.character.stats_manager.max_hp

    def get_stamina_percentage(self):
        return self.character.stats_manager.current_stamina / self.character.stats_manager.max_stamina

    def display_character_image(self):
        with ui.element().classes("w-full aspect-square"):
            ui.image(self.character.photo).classes("w-full h-full object-cover rounded-lg")
        ui.label(f"{self.character.name}").classes("text-xl font-semibold text-center text-[#EADEDE] w-full")
