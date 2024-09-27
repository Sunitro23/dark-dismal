from app.constants.constants import icon_tooltips
from app.utils.item_utils import get_item_fields
from app.models.inventory import Inventory
from app.models.character import Player
from app.models.items import Item
from app.ui.menus import ItemMenu
from nicegui import ui


def render_icon_with_tooltip(icon, tooltip_text, image_size="h-4 w-4"):
    with ui.row().classes(f"items-center {image_size}"):
        ui.image(icon)
        ui.tooltip(tooltip_text).classes("bg-gray-800 text-white")


def display_item(item: Item, fields: dict, image_size="h-8 w-8", inventory: Inventory = None):
    with ui.element("div").classes("relative bg-black p-2 w-full"):
        with ui.row().classes("items-center justify-between"):
            with ui.row().classes("items-center space-x-4"):
                with ui.element("div").classes("relative"):
                    ui.image(item.image).classes(image_size)
                    ui.tooltip(item.description).classes("bg-gray-800 text-white")
                    if inventory and inventory.is_item_equipped(item):
                        ui.element("div").classes("absolute bottom-0 left-0 w-3 h-3 bg-red-500 rounded-full opacity-70")

                ui.label(item.name).classes("text-white text-base font-semibold text-left")

            with ui.row().classes("items-center space-x-2 justify-end"):
                for field_icon, value in fields.items():
                    with ui.row().classes("items-center space-x-1"):
                        if field_icon:
                            tooltip_text = icon_tooltips.get(field_icon, "")
                            render_icon_with_tooltip(field_icon, tooltip_text)
                        ui.label(str(value)).classes("text-gray-400 text-base text-right")


def display_item_with_dialog(item: Item, player: Player, refresh_callback):
    with ui.element("div").classes("bg-black p-2 w-full cursor-pointer relative") as item_element:
        fields = get_item_fields(item)
        display_item(item, fields, inventory=player.inventory)
    item_element.on("mousedown", lambda: show_item_menu(item_element, item, player, refresh_callback))


def show_item_menu(container_element, item: Item, player: Player, refresh_callback):
    with container_element:
        ItemMenu(item, player, refresh_callback).show()
