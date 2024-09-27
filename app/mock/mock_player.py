import random
from faker import Faker
from app.models.character import Player
from app.constants.constants import URL_DEFAULT_PFP
from app.models.inventory import InventoryBuilderRandom

faker = Faker()


def create_player(name: str = None):
    stats = {
        "STR": random.randrange(20),
        "DEX": random.randrange(20),
        "INT": random.randrange(20),
        "FTH": random.randrange(20),
        "CHA": random.randrange(20),
        "VIT": random.randrange(20),
        "END": random.randrange(20),
        "AGL": random.randrange(20),
    }
    if name is None:
        name = faker.name()
    mock_player = Player(
        name=name,
        stats=stats,
        photo=f"{URL_DEFAULT_PFP}",
        age=random.randrange(50),
        player_class=faker.job(),
        alignment="Neutral - Good",
        species="Human",
        gender=faker.passport_gender(),
        story=faker.sentence(),
    )

    random_item = InventoryBuilderRandom()

    mock_player.add_item_to_inventory(random_item.add_random_armor())  # Armure 1
    mock_player.add_item_to_inventory(random_item.add_random_armor())  # Armure 2
    mock_player.add_item_to_inventory(random_item.add_random_consumable())  # Consommable 1
    mock_player.add_item_to_inventory(random_item.add_random_consumable())  # Consommable 2
    mock_player.add_item_to_inventory(random_item.add_random_shield())  # Bouclier 1
    mock_player.add_item_to_inventory(random_item.add_random_shield())  # Bouclier 2
    mock_player.add_item_to_inventory(random_item.add_random_weapon())  # Arme 1
    mock_player.add_item_to_inventory(random_item.add_random_weapon())  # Arme 2
    mock_player.add_item_to_inventory(random_item.add_random_spell())  # Sort 1
    mock_player.add_item_to_inventory(random_item.add_random_spell())  # Sort 2
    mock_player.add_item_to_inventory(random_item.add_random_ring())  # Anneau 1
    mock_player.add_item_to_inventory(random_item.add_random_ring())  # Anneau 2
    return mock_player
