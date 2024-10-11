from app.models.items import Spell
from app.ui.components.character.character_bar_display import CharacterBarDisplay
from app.models.fight_manager import CombatEvent, CombatManager
from app.models.character import Character
from app.models.action import AttackAction, CastSpellAction
from nicegui import ui


class FightDisplay:
    def __init__(self, character: Character):
        self.character_name = character.name
        self.combat_manager = CombatManager()
        self.character = self.combat_manager.get_character_by_name(self.character_name)
        self.logs_visible = False
        self.is_in_combat = self.character is not None
        if self.is_in_combat and not self.combat_manager.turn_order:
            self.combat_manager.initialize_turn_order()

    @ui.refreshable
    def display_fight(self):
        if not self.is_in_combat:
            return

        with ui.column().classes("p-6 space-y-6 h-full w-full"):
            self.display_info_bar()
            self.display_character_grid()
            self.display_logs()
            self.display_toggle_logs_button()

    def display_info_bar(self):
        current_character = self.combat_manager.get_current_turn_character()
        with ui.row().classes("info-bar bg-[#000000] p-4 shadow-md items-center justify-between w-full rounded-lg"):
            with ui.column().classes("w-1/2"):
                ui.label(f"Combat en cours").classes("text-3xl text-[#F58840]")
                ui.label(f"Personnage : {self.character.name}").classes("text-[#EADEDE] text-xl")

            with ui.column().classes("w-1/2 items-end"):
                if self.is_in_combat and current_character:
                    ui.label(f"Tour actuel : {current_character.name}").classes("text-2xl text-[#F58840] underline")
                    pass_turn_button = ui.button("Passer le tour", on_click=self.pass_turn).classes("bg-[#F58840] text-[#000000] py-2 px-4 rounded-lg")
                    pass_turn_button.bind_enabled_from(self, "is_player_turn")

    def display_character_grid(self):
        player_team_number = 1 if self.character in [char for _, char in self.combat_manager.get_team_characters(1)] else 2
        first_team, first_team_label = (1, "Équipe 1") if player_team_number == 1 else (2, "Équipe 2")
        second_team, second_team_label = (2, "Équipe 2") if player_team_number == 1 else (1, "Équipe 1")
        with ui.row().classes("w-full h-full"):
            with ui.splitter().classes("h-full w-full") as splitter:
                with splitter.before:
                    with ui.column().classes("w-full h-full justify-start"):
                        self.display_team_column(first_team, first_team_label)
                with splitter.separator:
                    ui.element().classes("bg-[#EADEDE] h-full w-[1px]")
                with splitter.after:
                    with ui.column().classes("w-full h-full justify-end items-end"):
                        self.display_team_column(second_team, second_team_label)

    def display_logs(self):
        if not self.logs_visible:
            return
        logs = CombatEvent().get_logs()
        with ui.element().classes("fixed top-10 right-0 w-1/6 p-2 h-full rounded-l-lg shadow-md overflow-y-auto bg-charsheet"):
            ui.label("Journal de Combat").classes("text-2xl mb-2")
            for log in logs:
                ui.label(log).classes("text-sm")

    def display_toggle_logs_button(self):
        icon = "chevron_right" if not self.logs_visible else "chevron_left"
        tooltip = "Afficher logs" if not self.logs_visible else "Masquer logs"
        with ui.element().classes("fixed bottom-4 right-4"):
            ui.button(icon=icon, on_click=self.toggle_logs_visibility).classes("bg-[#F58840] text-[#000000] p-2 rounded-full shadow-lg").tooltip(tooltip)

    def toggle_logs_visibility(self):
        self.logs_visible = not self.logs_visible
        self.refresh_display()

    def display_team_column(self, team_number: int, team_label: str):
        team_characters = self.combat_manager.get_team_characters(team_number)
        if not team_characters:
            ui.label(f"{team_label} n'a pas de personnages.").classes("text-[#EADEDE] text-lg text-center w-full")
        else:
            ui.label(team_label).classes("text-center text-[#EADEDE] text-lg font-bold mb-4")
            for _, character in team_characters:
                self.display_character_card(character)

    def display_character_card(self, character: Character):
        if not self.is_in_combat:
            return
        stats_display = CharacterBarDisplay(character)
        with ui.card().classes("bg-[#000000] cursor-pointer shadow-lg border border-[#EADEDE] rounded-md justify-center relative") as card:
            with ui.element().classes("w-[180px] p-2"):
                stats_display.display_character_image()
                stats_display.display_health_bar()
                stats_display.display_stamina_bar()
            with ui.button(icon="menu").classes("absolute top-0 left-0 opacity-70 z-10").bind_enabled_from(self, "is_player_turn"):
                with ui.menu() as menu:
                    ui.menu_item("Attaquer", on_click=lambda: self.initiate_attack(character))
                    self.add_spells_to_menu(menu, character)

            card.on("contextmenu", lambda e: menu.open(e.page.x, e.page.y))

    def add_spells_to_menu(self, menu, character: Character):
        spell = self.character.inventory.equipment_manager.equipped_items.get("SPELL")
        if spell:
            ui.menu_item(spell.name, on_click=lambda: self.cast_spell(spell=spell, attacker=self.character, target=character))

    def initiate_attack(self, target_character: Character):
        attack_action = AttackAction(attacker=self.character, target=target_character, refresh_callback=self.refresh_display)
        result_message = attack_action.execute()
        ui.notify(result_message)
        self.refresh_display()

    def cast_spell(self, spell, attacker, target):
        cast_spell_action = CastSpellAction(spell=spell, attacker=attacker, target=target, refresh_callback=self.refresh_display)
        result_message = cast_spell_action.execute()
        ui.notify(result_message)
        self.refresh_display()

    def pass_turn(self):
        self.combat_manager.next_turn()
        self.refresh_display()

    def refresh_display(self):
        self.display_fight.refresh()

    @property
    def is_player_turn(self):
        return self.combat_manager.is_player_turn(self.character)
