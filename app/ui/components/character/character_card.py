from app.services.character_service import save_character
from app.constants.constants import FILE_ICONS
from app.models.character import Character
from app.constants.enums import StatEnum
from dataclasses import dataclass
from nicegui import ui


@dataclass
class CharacterCard:
    character: Character
    attributes: list = None
    infos: list = None

    def __post_init__(self):
        self.attributes = self.get_attributes()
        self.infos = self.get_infos()

    def increment_attribute(self, attribute_name):
        if self.character.points_available > 0:
            self.character.stats[attribute_name] += 1
            self.character.points_available -= 1
            self.character.update_stats()
            save_character(self.character)
            self.attributes = self.get_attributes()
            self.refresh_display()
        else:
            ui.notify("Vous n'avez plus de points à attribuer.", color="negative")

    @ui.refreshable
    def display(self):
        with ui.card().tight().classes("w-full flex-col items-stretch box-border overflow-hidden bg-charsheet"):
            self.display_header()
            self.display_info_section()
            self.display_story()

    def display_header(self):
        with ui.row().classes("w-full h-2/5 justify-between items-stretch"):
            with ui.column().classes("w-1/2 h-full p-2"):
                ui.image(self.character.photo).classes("w-full h-full object-cover rounded-lg shadow-xl")
            with ui.column().classes("w-1/2 h-full p-2"):
                self.display_attributes()

    def display_info_section(self):
        with ui.column().classes("h-1/5 w-full"):
            with ui.grid(columns=2).classes("w-full h-full p-4"):
                for label, value in self.infos:
                    with ui.column().classes("w-full"):
                        with ui.row().classes("items-center justify-between"):
                            ui.label(f"{label} :").classes("font-bold text-[clamp(0.75rem,1vw,1rem)] whitespace-nowrap overflow-visible text-ellipsis shrink-0")
                            ui.label(f"{value}").classes("text-[clamp(0.75rem,1vw,1rem)] whitespace-nowrap overflow-visible text-right grow")
                        ui.separator().classes("my-2 bg-black w-3/4 h-[1px]")

    def display_story(self):
        with ui.column().classes("h-2/5 w-full overflow-y-auto story-content"):
            ui.label(self.character.story).classes("text-justify story-content w-full p-4")

    def display_attributes(self):
        with ui.column().classes("bg-black text-white rounded-md shadow-xl w-full h-full p-2"):
            with ui.column().classes("w-full h-[12%]"):
                with ui.row().classes("w-full justify-between"):
                    ui.label("Attributs").classes("font-bold text-left text-[clamp(0.75rem,1vw,1rem)]")
                    ui.label(f"{self.character.points_available}").classes("text-left text-[clamp(0.75rem,1vw,1rem)]")
                ui.separator().classes("bg-white h-[1px] my-1")

            with ui.column().classes("w-full h-[88%] flex flex-col justify-between"):
                for attribute, icon_url, value in self.attributes:
                    modifier = self.calculate_modifier(value)
                    self.display_single_attribute(attribute, icon_url, value, modifier)

    def display_single_attribute(self, attribute, icon_url, value, modifier):
        with ui.row().classes("items-center justify-between w-full h-[11%]"):
            with ui.row().classes("items-center h-full"):
                ui.image(icon_url).classes("h-full w-auto aspect-square")
                ui.label(attribute).classes("ml-2 text-left text-[clamp(0.75rem,1vw,1rem)]")
            with ui.row().classes("items-center"):
                ui.label(int(value)).classes("text-right text-[clamp(0.75rem,1vw,1rem)]")
                ui.label(f"({int(modifier):+d})").classes("ml-2 text-gray-400 text-right text-[clamp(0.75rem,1vw,1rem)]")
                ui.label("+").classes("text-white cursor-pointer aspect-square mx-2").on("click", lambda e, attr=attribute: self.increment_attribute(attr))

    def refresh_display(self):
        self.display.refresh()

    def get_attributes(self):
        return [
            ("VIT", f"{FILE_ICONS}/icon-vit.png", self.character.stats[StatEnum.VIT.value]),
            ("STR", f"{FILE_ICONS}/icon-str.png", self.character.stats[StatEnum.STR.value]),
            ("DEX", f"{FILE_ICONS}/icon-dex.png", self.character.stats[StatEnum.DEX.value]),
            ("INT", f"{FILE_ICONS}/icon-int.png", self.character.stats[StatEnum.INT.value]),
            ("END", f"{FILE_ICONS}/icon-end.png", self.character.stats[StatEnum.END.value]),
            ("CHA", f"{FILE_ICONS}/icon-char.png", self.character.stats[StatEnum.CHA.value]),
            ("AGL", f"{FILE_ICONS}/icon-agl.png", self.character.stats[StatEnum.AGL.value]),
            ("FTH", f"{FILE_ICONS}/icon-fth.png", self.character.stats[StatEnum.FTH.value]),
        ]

    def get_infos(self):
        return [
            ("Nom", self.character.name),
            ("Âge", f"{self.character.age} ans"),
            ("Classe", self.character.character_class.value),
            ("Espèce", self.character.species),
            ("Alignement", self.character.alignment.value),
            ("Genre", self.character.gender),
        ]

    def calculate_modifier(self, value):
        return (value - 10) // 2
