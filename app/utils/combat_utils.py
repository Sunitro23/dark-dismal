from app.constants.constants import SCALE_DEFENSE_MULTIPLIER, SCALE_WEAPON_MULTIPLIER
import random


def calculate_attack_damage(base_damage: int, stats: dict, scaling):
    total_damage = base_damage
    for stat, value in stats.items():
        weapon_multiplier = get_weapon_multiplier(scaling[stat])
        total_damage += (value - 10) * weapon_multiplier
    return total_damage


def get_weapon_multiplier(scaling_stat: str):
    return SCALE_WEAPON_MULTIPLIER.get(scaling_stat, 0.0)


def calculate_total_damage(attack_damage: int, defense_pieces: list, total_defense: int):
    if not defense_pieces:
        average_defense_multiplier = 0
    else:
        average_defense_multiplier = sum(get_defense_multiplier(piece) for piece in defense_pieces) / len(defense_pieces)
    total_damage = max(0, attack_damage * average_defense_multiplier - total_defense)
    return total_damage


def get_defense_multiplier(defense_stat: str):
    return SCALE_DEFENSE_MULTIPLIER.get(defense_stat, 1.5)


def calculate_armor_class(equipped_armor, character_stats):
    if not equipped_armor:
        return 8
    total_bonus = 0
    for armor in equipped_armor:
        total_bonus += get_armor_bonus(armor["type"], character_stats)
    armor_class = total_bonus / len(equipped_armor)
    return armor_class


def get_armor_bonus(armor_type, stats):
    if armor_type == "light":
        return stats["DEX"] + stats["AGL"] / 2
    elif armor_type == "medium":
        return (stats["INT"] + stats["FTH"]) / 2
    elif armor_type == "heavy":
        return (stats["STR"] + stats["END"]) / 2
    else:
        return 8


def calculate_roll_bonus(stat_value):
    return (stat_value - 10) // 2


def roll_dice(dice_size: int, number_of_dice: int):
    return sum(random.randint(1, dice_size) for _ in range(number_of_dice))


def stat_roll(stat, player):
    return roll_dice(20, 1) + calculate_roll_bonus(player.stats[stat])
