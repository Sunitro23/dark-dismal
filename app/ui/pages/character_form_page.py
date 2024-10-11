from app.services.character_service import save_character
from app.services.dynamic_form import DynamicForm
from app.constants.constants import head_html
from app.models.character import Character
from nicegui import ui


class CharacterCreationForm:
    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        ui.add_head_html(head_html)
        ui.colors(primary="#000000", secondary="#282A3A", accent="#735F32", positive="#C69749")
        with ui.element().classes("w-full h-full flex items-center justify-center"):
            with ui.card().classes("p-8 gap-4 w-96 bg-charsheet"):
                self.form_container = ui.element().classes("w-full")
                excluded_fields = ["stats_manager", "inventory", "is_player", "stats", "effect_manager", "level", "points_available", "souls"]
                self.dynamic_form = DynamicForm(self.form_container, self.submit_form, excluded_fields=excluded_fields)
                self.dynamic_form.create_form(object_class=Character)

    def submit_form(self, form_data):
        new_character = Character(**form_data, is_player=True)
        save_character(new_character)
        ui.notify(f"Personnage '{new_character.name}' créé avec succès!", color="positive")
        ui.navigate.to("/")
