from typing import Dict
from app.constants.enums import *
from app.models.items import *
from app.constants.constants import *


def get_scaling_info(scaling: Dict[str, Scale], is_armor=False):
    if is_armor:
        icons = {
            DamageType.PHYSICAL: ICON_ARMOR_SCALING_PHYSICAL,
            DamageType.FIRE: ICON_ARMOR_SCALING_FIRE,
            DamageType.MAGIC: ICON_ARMOR_SCALING_MAGIC,
            DamageType.LIGHTNING: ICON_ARMOR_SCALING_LIGHTNING,
        }
        return {icons[damage_type]: scale.value for damage_type, scale in scaling.items() if damage_type in icons}
    else:
        icons = {"STR": ICON_SCALING_STR, "DEX": ICON_SCALING_DEX, "INT": ICON_SCALING_INT, "FTH": ICON_SCALING_FTH}
        scaling_info = {}
        for stat, icon in icons.items():
            if stat in scaling:
                scaling_info[icon] = scaling[stat].value
            else:
                scaling_info[icon] = Scale.E.value
        return scaling_info


def get_damage_icon(damage_type: DamageType):
    icons = {
        DamageType.PHYSICAL: ICON_DAMAGE_PHYSICAL,
        DamageType.FIRE: ICON_DAMAGE_FIRE,
        DamageType.MAGIC: ICON_DAMAGE_MAGIC,
        DamageType.LIGHTNING: ICON_DAMAGE_LIGHTNING,
    }
    return icons.get(damage_type, ICON_DAMAGE_PHYSICAL)


def get_required_stat_info(required_stats: Dict[str, int]):
    icons = {
        "INT": ICON_REQUIRED_INT,
        "FTH": ICON_REQUIRED_FTH,
    }
    required_stats_info = {}
    for stat, value in required_stats.items():
        icon = icons.get(stat)
        if icon:
            required_stats_info[icon] = value
    return required_stats_info


def get_weapon_fields(item: Weapon):
    weapon_type = item.weapon_type.value.capitalize()
    scaling_info = get_scaling_info(item.scaling)
    damage_icon = get_damage_icon(item.damage_type)
    effect_info = get_effect_info(item.effects)
    return {None: weapon_type, ICON_WEIGHT: item.weight, damage_icon: item.damage, **scaling_info, **effect_info}


def get_armor_fields(item: Armor):
    armor_type_and_slot = f"{item.armor_type.value.title()} {item.equippable_slots[0].value.title()}"
    defense_info = get_scaling_info(item.defense_type_scaling, is_armor=True)
    effect_info = get_effect_info(item.effects)
    return {None: armor_type_and_slot, ICON_WEIGHT: item.weight, ICON_DEFENSE: item.defense, **defense_info, **effect_info}


def get_shield_fields(item: Shield):
    block_percentage = f"{int(item.block_percentage * 100)}%"
    effect_info = get_effect_info(item.effects)
    return {ICON_WEIGHT: item.weight, ICON_BLOCK_PERCENTAGE: block_percentage, ICON_STABILITY: item.stability, **effect_info}


def get_spell_fields(item: Spell):
    scaling_info = get_scaling_info(item.scaling)
    required_stats_info = get_required_stat_info(item.required_stat)
    damage_icon = get_damage_icon(item.damage_type)
    effect_info = get_effect_info(item.effects)
    return {None: item.spell_type.value.title(), damage_icon: item.damage, **scaling_info, **required_stats_info, **effect_info}


def get_effect_info(effects: List[Dict[EffectType, List]]):
    if not effects:
        return {}
    effect_info = ", ".join(
        [
            f"{next((readable_effect for effect_key, readable_effect in readable_effect_names.items() if effect_key in effect_type), effect_type)} {value['value']} {value['stat']}"
            for effect in (effects or [])
            for effect_type, value in effect.items()
        ]
    )
    return effect_info


def get_item_fields(item: Item):
    if isinstance(item, Weapon):
        return get_weapon_fields(item)
    elif isinstance(item, Armor):
        return get_armor_fields(item)
    elif isinstance(item, Shield):
        return get_shield_fields(item)
    elif isinstance(item, Spell):
        return get_spell_fields(item)
    elif isinstance(item, Consumable):
        return {"": get_effect_info(item.effects), None: f"/ {item.quantity} restants"}
    elif isinstance(item, Ring):
        return {"": get_effect_info(item.effects)}
    else:
        return {}
