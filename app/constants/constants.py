from app.constants.enums import Scale, SlotType, WeaponType


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
ICON_REQUIRED_STR = f"{FILE_ICONS}/icon-str-req.png"
ICON_REQUIRED_DEX = f"{FILE_ICONS}/icon-dex-req.png"
ICON_WEIGHT = "https://darksouls.wiki.fextralife.com/file/Dark-Souls/icon_other_weig.png"

icon_tooltips = {
    ICON_DAMAGE_PHYSICAL: "Degats Physiques",
    ICON_DAMAGE_FIRE: "Degats de Feu",
    ICON_DAMAGE_MAGIC: "Degats Magiques",
    ICON_DAMAGE_LIGHTNING: "Degats de Foudre",
    ICON_SCALING_STR: "Echelonnage de Force",
    ICON_SCALING_DEX: "Echelonnage de Dexterite",
    ICON_SCALING_INT: "Echelonnage d'Intelligence",
    ICON_SCALING_FTH: "Echelonnage de Foi",
    ICON_ARMOR_SCALING_PHYSICAL: "Echelonnage de Defense Physique",
    ICON_ARMOR_SCALING_FIRE: "Echelonnage de Defense de Feu",
    ICON_ARMOR_SCALING_MAGIC: "Echelonnage de Defense Magique",
    ICON_ARMOR_SCALING_LIGHTNING: "Echelonnage de Defense de Foudre",
    ICON_DEFENSE: "Defense",
    ICON_BLOCK_PERCENTAGE: "Pourcentage de Blocage",
    ICON_STABILITY: "Stabilite",
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
    "HELMET": "Casque",
    "CHESTPLATE": "Plastron",
    "BOOTS": "Bottes",
    "GLOVES": "Gants",
    "RIGHT_HAND": "Main Droite",
    "LEFT_HAND": "Main Gauche",
    "SPELL": "Sorts",
    "RING": "Anneaux"
}


head_html = '<link rel="stylesheet" href="/css/style.css">'
stamina_values = {
    WeaponType.AXE: 8,
    WeaponType.CATALYST: 5,
    WeaponType.CURVED_GREATSWORD: 10,
    WeaponType.CURVED_SWORD: 6,
    WeaponType.DAGGER: 4,
    WeaponType.FIST: 6,
    WeaponType.GREAT_HAMMER: 11,
    WeaponType.GREATAXE: 11,
    WeaponType.GREATSWORD: 10,
    WeaponType.HALBERD: 10,
    WeaponType.HAMMER: 8,
    WeaponType.KATANA: 8,
    WeaponType.PYROMANCY_FLAME: 5,
    WeaponType.SPEAR: 8,
    WeaponType.STRAIGHT_SWORD: 6,
    WeaponType.TALISMAN: 5,
    WeaponType.THRUSTING_SWORD: 6,
    WeaponType.ULTRA_GREATSWORD: 15,
    WeaponType.WHIP: 8,
}
