from app.models.items import Armor, EquippableItem, Spell, Weapon
from app.constants.enums import DamageType, StatEnum, WeaponType
from app.constants.constants import stamina_values
from app.models.character import Character
import random


SCALE_WEAPON_MULTIPLIER = {"S": 1.0, "A": 0.8, "B": 0.6, "C": 0.4, "E": 0.0}

ARMOR_SCALING_MULTIPLIER = {"S": 1.5, "A": 1.25, "B": 1.0, "C": 0.75, "E": 0.5}


class CombatCalculator:
    @staticmethod
    def get_weapon_multiplier(scaling_stat: str) -> int:
        return SCALE_WEAPON_MULTIPLIER.get(scaling_stat.upper(), 0.0)

    @staticmethod
    def calculate_weapon_damage(weapon: Weapon, stats: dict) -> int:
        base_damage = weapon.damage
        total_damage = base_damage
        for stat_name, scaling_level in weapon.scaling.items():
            if stat_name in stats:
                stat_value = stats[stat_name]
                multiplier = CombatCalculator.get_weapon_multiplier(scaling_level)
                total_damage += (stat_value - 10) * multiplier
        return total_damage

    @staticmethod
    def get_weapon_damage_types(right_weapon: Weapon, left_weapon: Weapon) -> tuple[DamageType, DamageType]:
        damage_type_right = right_weapon.damage_type if right_weapon else None
        damage_type_left = left_weapon.damage_type if left_weapon else None
        return damage_type_right, damage_type_left

    @staticmethod
    def calculate_attack_damage(weapons: list, stats: dict) -> int:
        total_damage = 0
        for weapon in weapons:
            if weapon:
                damage = CombatCalculator.calculate_weapon_damage(weapon, stats)
                total_damage += damage
        return total_damage

    @staticmethod
    def calculate_total_weight(equipped_items: list[EquippableItem]) -> int:
        return sum(item.weight for item in equipped_items)

    @staticmethod
    def calculate_max_weight(endurance: int) -> int:
        return endurance * 2.5

    @staticmethod
    def calculate_dodge_penalty(current_weight: int, max_weight: int) -> int:
        weight_ratio = current_weight / max_weight
        if weight_ratio > 0.75:
            return -5
        elif weight_ratio > 0.5:
            return -2
        elif weight_ratio > 0.25:
            return -1
        else:
            return 0

    @staticmethod
    def roll_dice(dice_size: int, number_of_dice: int) -> int:
        return sum(random.randint(1, dice_size) for _ in range(number_of_dice))

    @staticmethod
    def roll_dodge(character: Character) -> int:
        base_roll = CombatCalculator.roll_dice(20, 1)
        current_weight = CombatCalculator.calculate_total_weight(character.inventory.get_equipped_items())
        max_weight = CombatCalculator.calculate_max_weight(character.stats.get(StatEnum.END))
        penalty = CombatCalculator.calculate_dodge_penalty(current_weight, max_weight)
        return base_roll + penalty

    @staticmethod
    def calculate_initiative(character: Character) -> int:
        agility = character.stats.get(StatEnum.AGL, 0)
        return (agility - 10) / 2 + random.randint(1, 20)

    @staticmethod
    def calculate_spell_damage(spell: Spell, stats: dict) -> int:
        base_damage = spell.damage
        total_damage = base_damage
        for stat_name, scaling_level in spell.scaling.items():
            if stat_name in stats:
                stat_value = stats[stat_name]
                multiplier = CombatCalculator.get_weapon_multiplier(scaling_level)
                total_damage += (stat_value - 10) * multiplier
        return total_damage

    @staticmethod
    def calculate_damage_received(attack_damage: int, armor_pieces: list[Armor], damage_type: DamageType) -> int:
        if not armor_pieces:
            return attack_damage
        total_defense = 0
        for armor in armor_pieces:
            scaling_level = armor.defense_type_scaling.get(damage_type, "B")
            multiplier = ARMOR_SCALING_MULTIPLIER.get(scaling_level.upper(), 1.0)
            total_defense += armor.defense * multiplier
        if total_defense < attack_damage:
            damage_received = attack_damage - total_defense
        else:
            damage_received = 1
        return damage_received

    @staticmethod
    def stamina_required_to_block(attack_damage: int, stability: int) -> int:
        return attack_damage - stability

    @staticmethod
    def damage_after_block(attack_damage: int, block_percentage: int) -> int:
        return attack_damage * (1 - block_percentage / 100)

    @staticmethod
    def can_block(stamina: int, stamina_required: int) -> bool:
        return stamina >= stamina_required

    @staticmethod
    def calculate_dual_wield_damage(right_weapon, left_weapon, stats: dict[StatEnum, int]) -> float:
        if right_weapon and left_weapon:
            damage_right = CombatCalculator.calculate_weapon_damage(right_weapon, stats)
            damage_left = CombatCalculator.calculate_weapon_damage(left_weapon, stats)
            return damage_right + damage_left
        elif right_weapon:
            return CombatCalculator.calculate_weapon_damage(right_weapon, stats)
        elif left_weapon:
            return CombatCalculator.calculate_weapon_damage(left_weapon, stats)
        else:
            return 4

    @staticmethod
    def get_stamina_consumption(weapons: list[Weapon]) -> float:
        if all(weapon is None for weapon in weapons):
            return stamina_values.get(WeaponType.FIST, 3)

        total_stamina = 0
        for weapon in weapons:
            weapon_type = weapon.weapon_type if weapon else WeaponType.FIST
            total_stamina += stamina_values.get(weapon_type, 3)

        return total_stamina
