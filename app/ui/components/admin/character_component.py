from app.models.fight_manager import CombatManager
from app.services.character_service import load_all_characters, save_character
from app.services.dynamic_form import DynamicForm, EditDynamicForm
from app.models.character import Character
from nicegui import ui


class CharacterComponent:
    def __init__(self):
        self.dynamic_form = None
        self.form_container = None
        self.dialog = None
        self.select_callback = None

    @ui.refreshable
    def display(self):
        ui.label("Gestion des Personnages").classes("text-xl text-white font-bold text-center mb-4")
        ui.button("Creer un nouveau personnage", on_click=self.open_form_dialog).classes("mt-4 bg-green-500 text-white")
        self.display_characters()

    def display_characters(self):
        characters = load_all_characters()
        if not characters:
            ui.label("Aucun personnage trouvé").classes("text-gray-500")
        else:
            with ui.element().classes("grid py-4 gap-4 w-full") as grid_container:
                grid_container.classes("sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-10")
                for character in characters:
                    self.display_character_card(character)

    def display_character_card(self, character: Character):
        with ui.card().classes("bg-black w-36 h-36 flex flex-col items-center justify-center") as character_card:
            ui.image(character.photo).classes("h-24 w-24 object-cover rounded-full mb-2")
            ui.label(f"{character.name}").classes("text-white text-base font-semibold text-center")
            with ui.menu() as character_menu:
                ui.menu_item("Sélectionner", on_click=lambda: self.select_character(character))
                ui.menu_item("Modifier", on_click=lambda: self.open_edit_form_dialog(character))
                if CombatManager().get_character_by_name(character.name) is not None:
                    ui.menu_item("Retirer du Combat", on_click=lambda: self.remove_from_combat(character))
                else:
                    ui.menu_item("Ajouter Equipe 1", on_click=lambda: self.add_to_combat(character, 1))
                    ui.menu_item("Ajouter Equipe 2", on_click=lambda: self.add_to_combat(character, 2))
            character_card.on("click", character_menu.open)

    def select_character(self, character: Character):
        self.select_callback(character)
        self.display.refresh()

    def add_to_combat(self, character: Character, team: int):
        CombatManager().add_character(character=character, team=team)
        self.display.refresh()

    def remove_from_combat(self, character: Character):
        CombatManager().remove_character(character=character)
        self.display.refresh()

    # FORM
    def open_form_dialog(self):
        self.dialog = ui.dialog()
        with self.dialog:
            with ui.card().classes("p-8 gap-4 w-96 bg-charsheet"):
                ui.label("Création de Personnage").classes("text-xl font-bold text-center mb-4")
                self.form_container = ui.element().classes("w-full")
                excluded_fields = ["stats_manager", "inventory", "is_player", "stats", "effect_manager", "level"]
                self.dynamic_form = DynamicForm(self.form_container, self.submit_form, excluded_fields=excluded_fields)
                self.dynamic_form.create_form(object_class=Character)
        self.dialog.open()

    def open_edit_form_dialog(self, character: Character):
        self.dialog = ui.dialog()
        with self.dialog:
            with ui.card().classes("p-8 gap-4 w-96 bg-charsheet"):
                ui.label(f"Modification de {character.name}").classes("text-xl font-bold text-center mb-4")
                self.form_container = ui.element().classes("w-full")
                excluded_fields = ["stats_manager", "effect_manager", "inventory"]
                self.dynamic_form = EditDynamicForm(self.form_container, self.submit_form, existing_object=character, excluded_fields=excluded_fields)
                self.dynamic_form.create_form()
        self.dialog.open()

    def submit_form(self, form_data):
        try:
            if hasattr(self.dynamic_form, "existing_object") and self.dynamic_form.existing_object:
                character = self.dynamic_form.existing_object
                for key, value in form_data.items():
                    setattr(character, key, value)
                save_character(character)
                ui.notify(f"Personnage '{character.name}' modifié avec succès!", color="positive")
            else:
                new_character = Character(**form_data)
                save_character(new_character)
                ui.notify(f"Personnage '{new_character.name}' créé avec succès!", color="positive")

            self.form_container.clear()
            self.display.refresh()
            self.dialog.close()
        except Exception as e:
            print(f"Erreur lors de la création ou la modification du personnage : {str(e)}")
            ui.notify(f"Erreur lors de la création ou la modification du personnage : {str(e)}", color="negative")
