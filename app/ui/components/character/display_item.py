from app.services.item_field_extractor import ItemFieldsService
from app.services.item_action_service import ItemActionService
from app.models.character import Character
from app.models.inventory import Inventory
from app.constants.constants import *
from app.models.items import Item
from typing import List, Optional
from nicegui import ui


class IconRenderer:
    @staticmethod
    def render_icon_with_tooltip(icon, tooltip_text, image_size="h-4 w-4"):
        with ui.row().classes(f"items-center {image_size}"):
            ui.image(str(icon))
            ui.tooltip(tooltip_text).classes("bg-gray-800 text-white")


class ItemDisplayComponent:
    def __init__(self):
        self.item_service = ItemFieldsService()

    def display_item(self, item: Item, image_size="h-16 w-16", inventory: Optional[Inventory] = None, big_card=True):
        with ui.element("div").classes("p-2 w-full"):
            with ui.row().classes("items-center justify-between" if big_card else "flex-col"):
                self.display_item_image_and_name(item, image_size, inventory, big_card)
                if big_card:
                    fields = self.item_service.get_item_fields(item)
                    self.display_item_fields(fields)

    def display_item_image_and_name(self, item: Item, image_size, inventory: Inventory, big_card):
        with ui.row().classes("items-center w-auto h-full space-x-4" if big_card else "flex-col items-center justify-center w-full"):
            with ui.element("div").classes("relative flex items-center justify-center"):
                ui.image(item.image).classes(image_size)
                ui.tooltip(item.description).classes("bg-gray-800 text-white")
                if inventory and inventory.is_item_equipped(item):
                    ui.element("div").classes("absolute bottom-0 left-0 w-3 h-3 bg-red-500 rounded-full opacity-70")
            item_name = item.name
            if hasattr(item, "improvement_level") and item.improvement_level > 0:
                item_name += f" +{item.improvement_level}"
            if big_card:
                ui.label(item_name).classes("text-white text-base font-semibold text-left")
            else:
                ui.label(item_name).classes("text-white text-sm font-semibold text-center truncate w-full")

    def display_item_fields(self, fields: dict):
        with ui.row().classes("items-center space-x-2 justify-end"):
            for field_icon, value in fields.items():
                with ui.row().classes("items-center space-x-1"):
                    if field_icon:
                        tooltip_text = icon_tooltips.get(field_icon, "")
                        IconRenderer.render_icon_with_tooltip(field_icon, tooltip_text)
                    ui.label(str(value)).classes("text-gray-400 text-base text-right")

    def display_item_with_dialog(self, item: Item, character: Optional[Character], refresh_callback, big_card=True):
        with ui.element("div").classes(f"bg-black p-2 {'w-full' if big_card else 'w-32 h-32'} cursor-pointer relative") as item_element:
            self.display_item(item, inventory=character.inventory if character else None, big_card=big_card)
        if character:
            item_element.on("mousedown", lambda: ItemActionMenu.show(item_element, item, character, refresh_callback))


class ItemActionMenu:
    @staticmethod
    def show(container_element, item: Item, character: Character, refresh_callback):
        action_service = ItemActionService(item, character, refresh_callback)
        actions = action_service.get_actions()

        with container_element:
            with ui.menu().props("auto-close").classes("bg-transparent"):
                for label, method in actions:
                    ui.menu_item(label, on_click=lambda m=method: ItemActionMenu.handle_action(m)).classes("bg-[#282A3A] text-white")

    @staticmethod
    def handle_action(action_method):
        try:
            action_method()
        except ValueError as e:
            ui.notify(str(e), color="negative")
