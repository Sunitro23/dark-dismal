from enum import Enum


class CharAlignment(str, Enum):
    LAWFUL_GOOD = "Loyal Bon"
    NEUTRAL_GOOD = "Bon"
    CHAOTIC_GOOD = "Bon Chaotique"
    LAWFUL_NEUTRAL = "Loyal Neutre"
    TRUE_NEUTRAL = "Neutre"
    CHAOTIC_NEUTRAL = "Neutre Chaotique"
    LAWFUL_EVIL = "Loyal Mauvais"
    NEUTRAL_EVIL = "Mauvais"
    CHAOTIC_EVIL = "Mauvais Chaotique"


class StatEnum(str, Enum):
    VIT = "VIT"
    STR = "STR"
    DEX = "DEX"
    INT = "INT"
    FTH = "FTH"
    END = "END"
    AGL = "AGL"
    CHA = "CHA"


class SlotType(str, Enum):
    HELMET = "helmet"
    CHESTPLATE = "chestplate"
    BOOTS = "boots"
    GLOVES = "gloves"
    RIGHT_HAND = "right_hand"
    LEFT_HAND = "left_hand"
    SPELL = "spell"
    RING = "ring"


class ItemType(str, Enum):
    WEAPON = "weapon"
    SHIELD = "shield"
    SPELL = "spell"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    RING = "ring"
    OTHER = "other"


class ArmorSlot(str, Enum):
    HELMET = "helmet"
    CHESTPLATE = "chestplate"
    BOOTS = "boots"
    GLOVES = "gloves"


class WeaponType(str, Enum):
    AXE = "axe"
    CATALYST = "catalyst"
    CURVED_GREATSWORD = "curved greatsword"
    CURVED_SWORD = "curved sword"
    DAGGER = "dagger"
    FIST = "fist"
    GREAT_HAMMER = "great hammer"
    GREATAXE = "greataxe"
    GREATSWORD = "greatsword"
    HALBERD = "halberd"
    HAMMER = "hammer"
    KATANA = "katana"
    PYROMANCY_FLAME = "pyromancy flame"
    SPEAR = "spear"
    STRAIGHT_SWORD = "straight sword"
    TALISMAN = "talisman"
    THRUSTING_SWORD = "thrusting sword"
    ULTRA_GREATSWORD = "ultra greatsword"
    WHIP = "whip"


class DamageType(str, Enum):
    PHYSICAL = "physical"
    MAGIC = "magic"
    FIRE = "fire"
    LIGHTNING = "lightning"


class Scale(str, Enum):
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S = "S"


class SpellType(str, Enum):
    SPELL = "spell"
    MIRACLE = "miracle"
    PYROMANCY = "pyromancy"


class EffectType(str, Enum):
    RESTORE = "restore"
    BOOST = "boost"


class Class(str, Enum):
    WARRIOR = "Guerrier"
    KNIGHT = "Chevalier"
    WANDERER = "Vagabond"
    THIEF = "Voleur"
    BANDIT = "Bandit"
    HUNTER = "Chasseur"
    SORCERER = "Sorcier"
    PYROMANCER = "Pyromancien"
    CLERIC = "Clerc"
    DEPRIVED = "Defavorise"


class AllStat(str, Enum):
    VIT = "VIT"
    STR = "STR"
    DEX = "DEX"
    INT = "INT"
    FTH = "FTH"
    END = "END"
    AGL = "AGL"
    CHA = "CHA"
    HP = "HP"
    STA = "STA"
