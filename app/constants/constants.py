from app.constants.enums import Scale, SlotType


SCALE_DEFENSE_MULTIPLIER = {
    Scale.S: 0.5,
    Scale.A: 0.7,
    Scale.B: 0.9,
    Scale.C: 1.1,
    Scale.D: 1.3,
    Scale.E: 1.5,
}

SCALE_WEAPON_MULTIPLIER = {
    Scale.S: 1,
    Scale.A: 0.5,
    Scale.B: 0.33,
    Scale.C: 0.25,
    Scale.D: 0.2,
    Scale.E: 0,
}
URL_DEFAULT_PFP = "https://upload.wikimedia.org/wikipedia/commons/d/de/Facebook_head.png"
FILE_ICONS = "icons"


# ICONS
ICON_DEFENSE = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/icon-darkdef.png"
ICON_BLOCK_PERCENTAGE = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/physical_defense-shield-icon.jpg"
ICON_STABILITY = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/magic_defense-shield-icon.jpg"
ICON_DAMAGE_PHYSICAL = "https://darksouls.wiki.fextralife.com/file/Dark-Souls/physical_damage_dark_souls.jpg"
ICON_DAMAGE_FIRE = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/icon-firebonus.png"
ICON_DAMAGE_MAGIC = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/icon-magicbonus.png"
ICON_DAMAGE_LIGHTNING = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/icon-lightningbonus.png"
ICON_SCALING_STR = f"{FILE_ICONS}/icon-str.png"
ICON_SCALING_DEX = f"{FILE_ICONS}/icon-dex.png"
ICON_SCALING_INT = f"{FILE_ICONS}/icon-int.png"
ICON_SCALING_FTH = f"{FILE_ICONS}/icon-fth.png"
ICON_ARMOR_SCALING_PHYSICAL = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/icon-physicaldef.png"
ICON_ARMOR_SCALING_MAGIC = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/icon-magicdef.png"
ICON_ARMOR_SCALING_FIRE = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/icon-firedef.png"
ICON_ARMOR_SCALING_LIGHTNING = "https://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/icon-lightningdef.png"
ICON_REQUIRED_INT = f"{FILE_ICONS}/icon-int-req.png"
ICON_REQUIRED_FTH = f"{FILE_ICONS}/icon-fth-req.png"
ICON_WEIGHT = "https://darksouls.wiki.fextralife.com/file/Dark-Souls/icon_other_weig.png"

icon_tooltips = {
    ICON_DAMAGE_PHYSICAL: "Dégâts Physiques",
    ICON_DAMAGE_FIRE: "Dégâts de Feu",
    ICON_DAMAGE_MAGIC: "Dégâts Magiques",
    ICON_DAMAGE_LIGHTNING: "Dégâts de Foudre",
    ICON_SCALING_STR: "Échelonnage de Force",
    ICON_SCALING_DEX: "Échelonnage de Dextérité",
    ICON_SCALING_INT: "Échelonnage d'Intelligence",
    ICON_SCALING_FTH: "Échelonnage de Foi",
    ICON_ARMOR_SCALING_PHYSICAL: "Échelonnage de Défense Physique",
    ICON_ARMOR_SCALING_FIRE: "Échelonnage de Défense de Feu",
    ICON_ARMOR_SCALING_MAGIC: "Échelonnage de Défense Magique",
    ICON_ARMOR_SCALING_LIGHTNING: "Échelonnage de Défense de Foudre",
    ICON_DEFENSE: "Défense",
    ICON_BLOCK_PERCENTAGE: "Pourcentage de Blocage",
    ICON_STABILITY: "Stabilité",
    ICON_REQUIRED_INT: "Intelligence Requise",
    ICON_REQUIRED_FTH: "Foi Requise",
    ICON_WEIGHT: "Poids",
}
texts = {
    "not_equippable": "This item cannot be equipped.",
    "select_slot_label": "Choose a slot to equip.",
    "equip_confirmation": "Are you sure that you want to equip this item : ",
    "equip_confirmation_slot": "On your : ",
}

readable_slot_names = {
    SlotType.HELMET: "Casque",
    SlotType.CHESTPLATE: "Plastron",
    SlotType.BOOTS: "Bottes",
    SlotType.GLOVES: "Gants",
    SlotType.RIGHT_HAND: "Main Droite",
    SlotType.LEFT_HAND: "Main Gauche",
}
readable_effect_names = {
    "restore": "+",
    "boost": "+",
    "heal_status": "Soigne l'effet",
}
