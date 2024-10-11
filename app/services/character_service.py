from app.models.character import Character
from typing import List
from nicegui import app
import pickle
import os


SAVE_FOLDER = "database/characters/"

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


def save_character(character: Character) -> None:
    if character is None:
        return
    username = character.name
    if character.is_player is True:
        username = app.storage.user.get("username")
    filename = os.path.join(SAVE_FOLDER, f"{username}.pkl")
    with open(filename, "wb") as f:
        pickle.dump(character, f)


def load_character(username):
    filename = os.path.join(SAVE_FOLDER, f"{username}.pkl")
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return None


def get_current_user_character():
    user_data = app.storage.user
    username = user_data.get("username")

    if not username:
        return None

    character = load_character(username)

    return character


def load_all_characters() -> List[Character]:
    characters = []

    if not os.path.exists(SAVE_FOLDER):
        return characters

    for filename in os.listdir(SAVE_FOLDER):
        if filename.endswith(".pkl"):
            filepath = os.path.join(SAVE_FOLDER, filename)
            try:
                with open(filepath, "rb") as f:
                    character =pickle.load(f)
                    character.update_stats()
                    characters.append(character)
            except Exception as e:
                print(f"Erreur lors du chargement du fichier {filename}: {e}")

    return characters
