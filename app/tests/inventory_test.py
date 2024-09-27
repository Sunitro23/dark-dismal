import pytest
from app.models.inventory import Inventory
from app.models.items import Weapon, Spell, Shield, Armor, Consumable
from app.constants.enums import ItemType, WeaponType, SpellType, StatEnum, DamageType, Scale, SlotType, ArmorType, ArmorSlot
from unittest.mock import Mock


@pytest.fixture
def inventory():
    return Inventory()


@pytest.fixture
def sword():
    return Weapon(
        name="Sword",
        description="A sharp blade",
        image="sword.png",
        damage=50,
        damage_type=DamageType.PHYSICAL,
        scaling={StatEnum.STR: Scale.C, StatEnum.DEX: Scale.E},
        weapon_type=WeaponType.SWORD,
        equippable_slots=[SlotType.RIGHT_HAND, SlotType.LEFT_HAND],
    )


@pytest.fixture
def shield():
    return Shield(name="Shield", description="A strong shield", image="shield.png", block_percentage=0.75, stability=5, equippable_slots=[SlotType.LEFT_HAND])


@pytest.fixture
def spell():
    return Spell(
        name="Fireball",
        description="A ball of fire",
        image="fireball.png",
        damage=100,
        damage_type=DamageType.FIRE,
        scaling={StatEnum.INT: Scale.B},
        spell_type=SpellType.SPELL,
        required_stat={StatEnum.INT: 15},
        equippable_slots=[],
    )


@pytest.fixture
def another_spell():
    return Spell(
        name="Iceball",
        description="A ball of ice",
        image="iceball.png",
        damage=80,
        damage_type=DamageType.MAGIC,
        scaling={StatEnum.INT: Scale.B},
        spell_type=SpellType.SPELL,
        required_stat={StatEnum.INT: 15},
        equippable_slots=[],
    )


@pytest.fixture
def armor():
    return Armor(
        name="Iron Chestplate",
        description="A sturdy chestplate",
        image="armor.png",
        defense=30,
        defense_type_scaling={DamageType.PHYSICAL: Scale.B, DamageType.FIRE: Scale.E},
        armor_type=ArmorType.HEAVY,
        armor_slot=ArmorSlot.CHESTPLATE,
        equippable_slots=[SlotType.CHESTPLATE],
    )


@pytest.fixture
def consumable():
    return Consumable(name="Healing Potion", description="Restores health", image="potion.png", effect={"restore_hp": 50}, quantity=3, equippable_slots=[])


# Test adding items
def test_add_item(inventory, sword):
    inventory.add_item(sword)
    assert sword in inventory.items


# Test equipping a weapon
def test_equip_weapon(inventory, sword):
    inventory.add_item(sword)
    inventory.equip_item(sword, SlotType.RIGHT_HAND)
    assert inventory.equipped_items[SlotType.RIGHT_HAND] == sword


# Test equipping a shield
def test_equip_shield(inventory, shield):
    inventory.add_item(shield)
    inventory.equip_item(shield, SlotType.LEFT_HAND)
    assert inventory.equipped_items[SlotType.LEFT_HAND] == shield


# Test equipping armor
def test_equip_armor(inventory, armor):
    inventory.add_item(armor)
    inventory.equip_item(armor, SlotType.CHESTPLATE)
    assert inventory.equipped_items[SlotType.CHESTPLATE] == armor


# Test equipping in an invalid slot
def test_equip_invalid_slot(inventory, sword):
    inventory.add_item(sword)
    with pytest.raises(ValueError, match="cannot be equipped in slot"):
        inventory.equip_item(sword, SlotType.HELMET)


# Test equipping when the slot is occupied
def test_equip_item_in_occupied_slot(inventory, sword, shield):
    inventory.add_item(sword)
    inventory.add_item(shield)
    inventory.equip_item(sword, SlotType.LEFT_HAND)
    with pytest.raises(ValueError, match="An item is already equipped in the SlotType.LEFT_HAND slot"):
        inventory.equip_item(shield, SlotType.LEFT_HAND)


# Test unequipping items
def test_unequip_item(inventory, sword):
    inventory.add_item(sword)
    inventory.equip_item(sword, SlotType.RIGHT_HAND)
    inventory.unequip_item(sword, SlotType.RIGHT_HAND)
    assert SlotType.RIGHT_HAND not in inventory.equipped_items


# Test equipping a spell
def test_equip_spell(inventory, spell):
    inventory.add_item(spell)
    inventory.equip_item(spell)
    assert spell in inventory.equipped_spells


# Test equipping duplicate spell
def test_equip_duplicate_spell(inventory, spell):
    inventory.add_item(spell)
    inventory.equip_item(spell)
    with pytest.raises(ValueError, match="is already equipped as a spell"):
        inventory.equip_item(spell)


# Test equipping more spells than allowed
def test_equip_max_spells(inventory, spell, another_spell):
    inventory.MAX_SPELLS = 1  # Set max spells to 1 for testing
    inventory.add_item(spell)
    inventory.add_item(another_spell)
    inventory.equip_item(spell)
    with pytest.raises(ValueError, match="Cannot equip more than 1 spells"):
        inventory.equip_item(another_spell)


def test_use_consumable(inventory, consumable):
    mock_target = Mock()  # Simulate the target of the consumable
    inventory.add_item(consumable)
    consumable.use(mock_target)
    assert consumable.quantity == 2  # Check if quantity is reduced


def test_equip_two_spells(inventory, spell, another_spell):
    inventory.MAX_SPELLS = 2  # Set max spells to 2 for this test
    inventory.add_item(spell)
    inventory.add_item(another_spell)

    # Equip the first spell
    inventory.equip_item(spell)
    assert spell in inventory.equipped_spells  # Verify the first spell is equipped

    # Equip the second spell
    inventory.equip_item(another_spell)
    assert another_spell in inventory.equipped_spells  # Verify the second spell is equipped

    # Verify that both spells are equipped
    assert len(inventory.equipped_spells) == 2
