from app.constants.constants import *
from app.models.items import *
from typing import Dict, Union


class BaseFieldExtractor:
    @staticmethod
    def extract(item):
        data = {**BaseFieldExtractor.get_effect_info(item.effects)}
        if isinstance(item, EquippableItem):
            try:
                weight = float(item.weight)
                if weight > 0:
                    data[ICON_WEIGHT] = weight
            except ValueError:
                print(f"Invalid weight value: {item.weight}")
        return data

    @staticmethod
    def get_effect_info(effects: Dict[int, AllStat]) -> Dict[str, str]:
        if not effects:
            return {}
        effects_info = ", ".join(f"{stat} {'+' if amount > 0 else ''}{int(amount)}" for stat, amount in effects.items())
        return {"": effects_info}


class WeaponFieldExtractor(BaseFieldExtractor):
    @staticmethod
    def extract(item: Weapon):
        return {**BaseFieldExtractor.extract(item), IconMapping.get_damage_icon(item.damage_type): item.damage, **ScalingInfoExtractor.get_scaling_info(item.scaling)}


class ArmorFieldExtractor(BaseFieldExtractor):
    @staticmethod
    def extract(item: Armor):
        return {**BaseFieldExtractor.extract(item), ICON_DEFENSE: item.defense, **ScalingInfoExtractor.get_scaling_info(item.defense_type_scaling, is_armor=True)}


class ShieldFieldExtractor(BaseFieldExtractor):
    @staticmethod
    def extract(item: Shield):
        return {**BaseFieldExtractor.extract(item), ICON_BLOCK_PERCENTAGE: f"{int(item.block_percentage * 100)}%", ICON_STABILITY: item.stability}


class SpellFieldExtractor(BaseFieldExtractor):
    @staticmethod
    def extract(item: Spell):
        return {
            **BaseFieldExtractor.extract(item),
            IconMapping.get_damage_icon(item.damage_type): item.damage,
            **ScalingInfoExtractor.get_scaling_info(item.scaling),
            **RequiredStatInfoExtractor.get_required_stat_info(item.required_stat),
        }


class ConsumableFieldExtractor(BaseFieldExtractor):
    @staticmethod
    def extract(item: Consumable):
        return {**BaseFieldExtractor.extract(item), "Quantité": f"{item.quantity} restants"}


class RingFieldExtractor(BaseFieldExtractor):
    @staticmethod
    def extract(item: Ring):
        return BaseFieldExtractor.extract(item)


class ScalingInfoExtractor:
    @staticmethod
    def get_scaling_info(scaling: Dict[StatEnum, Scale], is_armor=False):
        icons = (
            {
                StatEnum.STR: ICON_SCALING_STR,
                StatEnum.DEX: ICON_SCALING_DEX,
                StatEnum.INT: ICON_SCALING_INT,
                StatEnum.FTH: ICON_SCALING_FTH,
            }
            if not is_armor
            else {
                DamageType.PHYSICAL: ICON_ARMOR_SCALING_PHYSICAL,
                DamageType.FIRE: ICON_ARMOR_SCALING_FIRE,
                DamageType.MAGIC: ICON_ARMOR_SCALING_MAGIC,
                DamageType.LIGHTNING: ICON_ARMOR_SCALING_LIGHTNING,
            }
        )
        return {icons[key]: scale.value if isinstance(scale, Scale) else scale for key, scale in scaling.items() if key in icons}


class RequiredStatInfoExtractor:
    @staticmethod
    def get_required_stat_info(required_stats: Dict[StatEnum, int]):
        icons = {
            StatEnum.INT: ICON_REQUIRED_INT,
            StatEnum.FTH: ICON_REQUIRED_FTH,
            StatEnum.STR: ICON_REQUIRED_STR,
            StatEnum.DEX: ICON_REQUIRED_DEX,
        }
        return {icons[stat]: value for stat, value in required_stats.items() if stat in icons}


class IconMapping:
    @staticmethod
    def get_damage_icon(damage_type: DamageType):
        icons = {
            DamageType.PHYSICAL: ICON_DAMAGE_PHYSICAL,
            DamageType.FIRE: ICON_DAMAGE_FIRE,
            DamageType.MAGIC: ICON_DAMAGE_MAGIC,
            DamageType.LIGHTNING: ICON_DAMAGE_LIGHTNING,
        }
        return icons.get(damage_type, ICON_DAMAGE_PHYSICAL)


class ItemFieldsService:
    extractors = {
        Weapon: WeaponFieldExtractor,
        Armor: ArmorFieldExtractor,
        Shield: ShieldFieldExtractor,
        Spell: SpellFieldExtractor,
        Consumable: ConsumableFieldExtractor,
        Ring: RingFieldExtractor,
    }

    def get_item_fields(self, item):
        extractor = self.extractors.get(type(item), BaseFieldExtractor)
        return extractor.extract(item)
