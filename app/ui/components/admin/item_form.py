from app.services.dynamic_form import DynamicForm
from app.models.items import ItemFactory
from app.models.items import *
from nicegui import ui
import re

item_type_dict = {"Weapon": Weapon, "Spell": Spell, "Armor": Armor, "Shield": Shield, "Ring": Ring, "Consumable": Consumable, "Item": Item}


class ItemForm:
    def __init__(self):
        self.current_item = None
        self.dynamic_form = None
        self.submit_button = None
        self.form_container = None
        self.stat_inputs = {}
        self.setup_ui()

    def setup_ui(self):
        ui.label("Creation d'Item").classes("text-xl font-bold text-center mb-4")
        self.item_type_dropdown = ui.select(
            ["Weapon", "Spell", "Armor", "Shield", "Ring", "Consumable", "Item"], value="Weapon", label="Type d'item", validation={"Le type est requis": lambda v: bool(v)}
        ).classes("w-full")
        self.item_type_dropdown.on_value_change(self.on_type_change)
        self.form_container = ui.element().classes("w-full")
        excluded_fields = ["item_type", "improvement_level"]
        self.dynamic_form = DynamicForm(self.form_container, self.submit_form, excluded_fields=excluded_fields)
        self.create_form(self.item_type_dropdown.value)

    def on_type_change(self, event):
        self.create_form(event.value)

    def create_form(self, selected_object_type):
        self.current_item = selected_object_type.lower()
        self.stat_inputs.clear()
        self.dynamic_form.create_form(object_class=item_type_dict.get(selected_object_type))

    def submit_form(self, form_data):
        form_data["item_type"] = self.current_item
        try:
            created_item = ItemFactory.create_item(form_data)
            ui.notify(f"Item '{created_item.name}' de type {type(created_item).__name__} cree avec succès!", color="positive")
        except Exception as e:
            ui.notify(f"Erreur lors de la creation de l'item : {str(e)}", color="negative")

    def validate_url(self, url):
        regex = re.compile(r"^(?:http|ftp)s?://(?:\S+)$", re.IGNORECASE)
        return bool(regex.match(url))
