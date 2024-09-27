from typing import Dict, Type
from enum import Enum


class CharAlignment(Enum):
    LAWFUL_GOOD = "Loyal Bon"
    NEUTRAL_GOOD = "Bon"
    CHAOTIC_GOOD = "Bon Chaotique"
    LAWFUL_NEUTRAL = "Loyal Neutre"
    TRUE_NEUTRAL = "Neutre"
    CHAOTIC_NEUTRAL = "Neutre Chaotique"
    LAWFUL_EVIL = "Loyal Mauvais"
    NEUTRAL_EVIL = "Mauvais"
    CHAOTIC_EVIL = "Mauvais Chaotique"


class StatEnum(Enum):
    VIT = "VIT"
    STR = "STR"
    DEX = "DEX"
    INT = "INT"
    FTH = "FTH"
    END = "END"
    AGL = "AGL"
    CHA = "CHA"


class SlotType(Enum):
    HELMET = "helmet"
    CHESTPLATE = "chestplate"
    BOOTS = "boots"
    GLOVES = "gloves"
    RIGHT_HAND = "right_hand"
    LEFT_HAND = "left_hand"
    SPELL = "spell"
    RING = "ring"


class ItemType(Enum):
    WEAPON = "weapon"
    SHIELD = "shield"
    SPELL = "spell"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    RING = "ring"
    OTHER = "other"


class ArmorType(Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


class ArmorSlot(Enum):
    HELMET = "helmet"
    CHESTPLATE = "chestplate"
    BOOTS = "boots"
    GLOVES = "gloves"


class WeaponType(Enum):
    SWORD = "sword"
    AXE = "axe"
    MACE = "mace"
    BOW = "bow"
    CROSSBOW = "crossbow"
    STAFF = "staff"
    WAND = "wand"


class DamageType(Enum):
    PHYSICAL = "physical"
    MAGIC = "magic"
    FIRE = "fire"
    LIGHTNING = "lightning"


class Scale(Enum):
    E = "E"
    D = "D"
    C = "C"
    B = "B"
    A = "A"
    S = "S"


class SpellType(Enum):
    SPELL = "spell"
    MIRACLE = "miracle"
    PYROMANCY = "pyromancy"


class EffectType(Enum):
    RESTORE_HP = "restore_hp"
    RESTORE_STA = "restore_sta"
    BOOST_STAT = "boost_stat"


class Class(Enum):
    WARRIOR = "Guerrier"
    KNIGHT = "Chevalier"
    WANDERER = "Vagabond"
    THIEF = "Voleur"
    BANDIT = "Bandit"
    HUNTER = "Chasseur"
    SORCERER = "Sorcier"
    PYROMANCER = "Pyromancien"
    CLERIC = "Clerc"
    DEPRIVED = "Défavorisé"
