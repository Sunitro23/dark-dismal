from typing import List
import pickle
import os

SAVE_FOLDER = "database/items/"


if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


def save_item(item) -> None:
    if item is None:
        return
    filename = os.path.join(SAVE_FOLDER, f"{item.name}.pkl")
    with open(filename, "wb") as f:
        pickle.dump(item, f)


def load_item(username):
    filename = os.path.join(SAVE_FOLDER, f"{username}.pkl")
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return None


def load_all_items() -> List:
    items = []
    if not os.path.exists(SAVE_FOLDER):
        return items
    for filename in os.listdir(SAVE_FOLDER):
        if filename.endswith(".pkl"):
            filepath = os.path.join(SAVE_FOLDER, filename)
            try:
                with open(filepath, "rb") as f:
                    items.append(pickle.load(f))
            except Exception as e:
                print(f"Erreur lors du chargement du fichier {filename}: {e}")
    return items
