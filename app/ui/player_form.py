import os
from app.constants.enums import CharAlignment, Class
from app.models.character import Player
from main import SAVE_FOLDER
from nicegui import app, ui
import pickle


def create_player(name, stats, player_class, alignment, species, gender, story, age, photo_url):
    player = Player(name=name, stats=stats, photo=photo_url, player_class=player_class, alignment=alignment, species=species, gender=gender, story=story, age=int(age))
    save_player(player=player)
    ui.notify(f"Joueur {player.name} créé avec succès !")
    ui.navigate.to("/")
    return player


def save_player(player) -> None:
    if player is None:
        return
    username = app.storage.user.get("username")
    filename = os.path.join(SAVE_FOLDER, f"{username}.pkl")
    with open(filename, "wb") as f:
        pickle.dump(player, f)


@ui.page("/create_player")
def create_player_form() -> None:
    ui.add_head_html('<link rel="stylesheet" href="/css/style.css">')
    ui.colors(primary="#000000", secondary="#282A3A", accent="#735F32", positive="#C69749")
    points_available = 27
    initial_value = 8
    stats = {"VIT": initial_value, "END": initial_value, "STR": initial_value, "DEX": initial_value, "INT": initial_value, "FTH": initial_value, "AGL": initial_value, "CHA": initial_value}

    def update_stat(stat_name: str, change: int):
        nonlocal points_available
        if (points_available - change >= 0) and (stats[stat_name] + change >= initial_value):
            stats[stat_name] += change
            points_available -= change
            points_label.set_text(f"Points disponibles : {points_available}")
        else:
            ui.notify("Pas assez de points disponibles ou valeur minimale atteinte", color="negative")
        refresh_stats()

    def refresh_stats():
        for stat_name in stats:
            labels[stat_name].set_text(f"{stat_name} : {stats[stat_name]}")

    labels = {}

    with ui.element().classes("w-full h-full flex items-center justify-center bg-inherit"):
        with ui.card().classes("p-8 gap-6 w-96 bg-charsheet"):
            ui.label("Création de Joueur").classes("text-xl font-bold text-center mb-4")

            name = ui.input("Nom du joueur").classes("w-full").props("autofocus")

            player_class = ui.select([c.value for c in Class], label="Classe").classes("w-full")

            species = ui.input("Espèce").classes("w-full")
            alignment = ui.select([c.value for c in CharAlignment], label="Alignement").classes("w-full")
            gender = ui.input("Genre").classes("w-full")
            age = ui.number("Âge", value=25, min=1, max=100).classes("w-full")
            photo_url = ui.input("URL de la photo").classes("w-full")
            story = ui.textarea("Histoire").classes("w-full h-24 textarea-expand").props("autogrow")
            ui.label("Attribution des statistiques").classes("text-lg font-semibold text-center mt-4")

            with ui.row().classes("w-full"):
                points_label = ui.label(f"Points disponibles : {points_available}").classes("font-bold")

            with ui.column().classes("w-full space-y-4"):
                stats_list = list(stats.keys())
                for i in range(0, len(stats_list), 2):
                    with ui.row().classes("w-full flex justify-between"):
                        for stat in stats_list[i : i + 2]:
                            with ui.column().classes("flex-1 space-y-2 items-center text-center"):
                                labels[stat] = ui.label(f"{stat} : {stats[stat]}").classes("text-sm")
                                with ui.row().classes("flex justify-center space-x-2"):
                                    ui.button("+", on_click=lambda s=stat: update_stat(s, 1)).classes("h-2 w-2")
                                    ui.button("-", on_click=lambda s=stat: update_stat(s, -1)).classes("h-2 w-2")
            ui.button("Créer le joueur", on_click=lambda: create_player(name.value, stats, player_class.value, alignment.value, species.value, gender.value, story.value, age.value, photo_url.value))
