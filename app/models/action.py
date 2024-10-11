from typing import List
from app.models.items import Spell, Weapon
from app.services.combat_calculator import CombatCalculator
from app.models.fight_manager import CombatEvent
from app.models.character import Character
from app.constants.enums import DamageType, ItemType, SpellType, WeaponType


class Action:
    def __init__(self, attacker: Character, target: Character, refresh_callback):
        self.attacker = attacker
        self.target = target
        self.refresh_callback = refresh_callback

    def execute(self):
        raise NotImplementedError("This method should be overridden by subclasses")


class AttackAction(Action):
    def __init__(self, attacker, target, refresh_callback):
        super().__init__(attacker, target, refresh_callback)
        self.right_hand = attacker.inventory.get_equipped_item_by_slot("right_hand")
        self.left_hand = attacker.inventory.get_equipped_item_by_slot("left_hand")

    def execute(self):
        stamina_to_use = self._get_stamina_usage()

        if not self._has_enough_stamina(stamina_to_use):
            message = f"{self.attacker.name} n'a pas l'énergie pour faire cette action."
            CombatEvent().add_log(message)
            return message

        total_damage = self._calculate_total_damage()
        self._execute_attack(total_damage, stamina_to_use)
        message = f"{self.attacker.name} inflige {total_damage} points de dégâts à {self.target.name}."
        CombatEvent().add_log(message)
        return message

    def _calculate_attack_damage(self):
        damage = CombatCalculator.calculate_dual_wield_damage(self.right_hand, self.left_hand, self.attacker.stats)
        return damage

    def _calculate_total_damage(self):
        attack_damage = self._calculate_attack_damage()
        defense_pieces = self.target.inventory.get_equipped_items_by_type(ItemType.ARMOR)
        damage_type = CombatCalculator.get_weapon_damage_types(self.right_hand, self.left_hand)
        total_damage = CombatCalculator.calculate_damage_received(attack_damage, defense_pieces, damage_type)
        return total_damage

    def _get_stamina_usage(self):
        stamina_usage = CombatCalculator.get_stamina_consumption([self.right_hand, self.left_hand])
        return stamina_usage

    def _has_enough_stamina(self, stamina_to_use):
        has_stamina = self.attacker.stats_manager.current_stamina >= stamina_to_use
        return has_stamina

    def _execute_attack(self, total_damage, stamina_to_use):
        self.target.take_damage(total_damage)
        self.attacker.stats_manager.use_stamina(stamina_to_use)
        CombatEvent().add_log(f"{self.attacker.name} utilise {stamina_to_use} points d'endurance pour attaquer {self.target.name}.")
        self.refresh_callback()


class CastSpellAction(Action):
    def __init__(self, attacker: Character, target: Character, spell: Spell, refresh_callback):
        super().__init__(attacker, target, refresh_callback)
        self.spell = spell

    def execute(self):
        total_damage = self._calculate_total_damage()
        self._execute_cast(total_damage)
        message = f"{self.attacker.name} lance {self.spell.name} et inflige {total_damage} points de dégâts à {self.target.name}."
        self.spell.use_spell()
        CombatEvent().add_log(message)
        return message

    def _calculate_spell_damage(self):
        return CombatCalculator.calculate_spell_damage(self.spell, self.attacker.stats)

    def _calculate_total_damage(self):
        spell_damage = self._calculate_spell_damage()
        defense_pieces = self.target.inventory.get_equipped_items_by_type(ItemType.ARMOR)
        damage_type = self.spell.damage_type
        total_damage = CombatCalculator.calculate_damage_received(spell_damage, defense_pieces, damage_type)
        return total_damage

    def _has_enough_stamina(self, stamina_to_use):
        return self.attacker.stats_manager.current_stamina >= stamina_to_use

    def _execute_cast(self, total_damage):
        self.target.take_damage(total_damage)
        CombatEvent().add_log(f"{self.attacker.name} lance {self.spell.name} sur {self.target.name}.")
        self.refresh_callback()
