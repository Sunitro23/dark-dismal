from app.constants.enums import AllStat, Class, EffectType
from app.models.items import Item
from typing import Dict


class EffectManager:
    class_bonuses = {
        Class.WARRIOR: {"STR": 1, "END": 1},
        Class.KNIGHT: {"END": 2},
        Class.WANDERER: {"DEX": 1, "END": 1},
        Class.THIEF: {"DEX": 1, "AGL": 1},
        Class.BANDIT: {"STR": 2},
        Class.HUNTER: {"DEX": 2},
        Class.SORCERER: {"INT": 2},
        Class.PYROMANCER: {"INT": 1, "FTH": 1},
        Class.CLERIC: {"FTH": 2},
        Class.DEPRIVED: {"CHA": 2},
    }

    @staticmethod
    def apply_class_bonus(character_class: str, stats: Dict[str, int]) -> Dict[str, int]:
        if character_class in EffectManager.class_bonuses:
            for stat, bonus in EffectManager.class_bonuses[character_class].items():
                stats[stat] = stats.get(stat, 0) + bonus
        return stats

    @staticmethod
    def apply_item_effects(item: Item, target, remove: bool = False):
        multiplier = -1 if remove else 1
        if item.effects:
            for stat, value in item.effects.items():
                adjusted_value = value * multiplier
                if stat == AllStat.HP:
                    target.restore_hp(adjusted_value)
                elif stat == AllStat.STA:
                    target.restore_stamina(adjusted_value)
                else:
                    target.increase_stat(stat=stat, amount=adjusted_value)

    @staticmethod
    def apply_all_effects(character_class: str, item: Item, stats: Dict[str, int], target):
        stats = EffectManager.apply_class_bonus(character_class, stats)
        EffectManager.apply_item_effects(item, target)
        return stats
