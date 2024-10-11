from app.services.combat_calculator import CombatCalculator
from typing import ClassVar, List, Optional, Tuple
from app.models.character import Character


class CombatEvent:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CombatEvent, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def add_log(self, message: str):
        self.logs.append(message)
        self.write_log_to_file(message)

    def get_logs(self) -> List[str]:
        return self.logs[-10:]

    def clear_logs(self):
        self.logs.clear()

    def write_log_to_file(self, message: str, filename: str = "combat_logs.txt"):
        with open(filename, "a") as log_file:
            log_file.write(f"{message}\n")


class CombatManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.teams = {1: [], 2: []}
            cls._instance.turn_order = []
            cls._instance.current_turn_index = 0
            cls._instance.turn_number = 1
        return cls._instance

    def add_character(self, character: "Character", team: int, turn_order: int = 0):
        if team not in self.teams:
            raise ValueError(f"L'équipe {team} n'existe pas.")
        self.teams[team].append((turn_order, character))
        self._log_event(f"{character.name} a rejoint l'équipe {team}.")
        self._update_turn_order()

    def remove_character(self, character: "Character"):
        for team in self.teams.values():
            team[:] = [char_tuple for char_tuple in team if char_tuple[1] != character]
        self._update_turn_order()
        self._log_event(f"{character.name} a été retiré du combat.")

    def get_character_by_name(self, name: str) -> Optional["Character"]:
        return next((char for _, char in [char for team in self.teams.values() for char in team] if char.name == name), None)

    def get_team_characters(self, team: int) -> List[Tuple[int, "Character"]]:
        return self.teams.get(team, [])

    def initialize_turn_order(self):
        all_characters = [char for team in self.teams.values() for _, char in team]
        if not all_characters:
            raise ValueError("Aucun personnage trouvé dans les équipes.")
        self.turn_order = sorted(all_characters, key=lambda char: CombatCalculator()._calculate_initiative(character=char), reverse=True)
        self.current_turn_index = 0
        self.turn_number = 1

    def next_turn(self):
        if not self.turn_order:
            raise ValueError("Le combat n'a pas été initialisé ou il n'y a pas de personnages.")
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        if self.current_turn_index == 0:
            self.turn_number += 1
            self._restore_stamina_for_all()
        self._log_event(f"Tour {self.turn_number} : C'est au tour de {self.get_current_turn_character().name}.")
        return self.get_current_turn_character()

    def get_current_turn_character(self):
        if not self.turn_order:
            raise ValueError("Le combat n'a pas été initialisé ou il n'y a pas de personnages.")
        return self.turn_order[self.current_turn_index]

    def reset_combat(self):
        for team in self.teams:
            self.teams[team].clear()
        self.turn_order.clear()
        self.current_turn_index = 0
        self.turn_number = 1

    def is_player_turn(self, character: "Character") -> bool:
        return character == self.get_current_turn_character()

    def _restore_stamina_for_all(self):
        for character in self.turn_order:
            character.stats_manager.restore_stamina(99)

    def _update_turn_order(self):
        self.turn_order = sorted([char for team in self.teams.values() for _, char in team], key=lambda char: CombatCalculator().calculate_initiative(character=char), reverse=True)

    def _log_event(self, message: str):
        CombatEvent().add_log(message)
