from fastapi.responses import RedirectResponse
from app.ui.player_page import PlayerPage
from app.auth.middleware import *
from typing import Optional
from nicegui import app, ui
import app.ui.player_form as player_form
import pickle
import os

SAVE_FOLDER = "player_saves"

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


def save_player(player) -> None:
    if player is None:
        return
    username = app.storage.user.get("username")
    filename = os.path.join(SAVE_FOLDER, f"{username}.pkl")
    with open(filename, "wb") as f:
        pickle.dump(player, f)


def load_player(username):
    filename = os.path.join(SAVE_FOLDER, f"{username}.pkl")
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)
    return None


@ui.page("/")
def main_page() -> None:
    ui.add_head_html('<link rel="stylesheet" href="/css/style.css">')
    ui.colors(primary="#000000", secondary="#282A3A", accent="#735F32", positive="#C69749")

    def logout() -> None:
        player = get_current_user_player()
        if player:
            save_player(player)
        app.storage.user.clear()
        ui.navigate.to("/login")

    def get_current_user_player():
        user_data = app.storage.user
        username = user_data.get("username")
        if not username:
            return None
        player = load_player(username)
        if player is None:
            ui.navigate.to("/create_player")
            return None
        return player

    with ui.header().classes(replace="row items-center bg-inherit w-full justify-between"):
        with ui.row().classes("items-center"):
            with ui.tabs() as tabs:
                ui.tab("Fiche Personnage")
                ui.tab("Combat")
        ui.button("Se déconnecter", on_click=logout).classes("ml-auto")

    mock_player = get_current_user_player()

    with ui.column().classes("absolute-center items-center w-full bg-inherit"):
        with ui.tab_panels(tabs, value="Fiche Personnage").classes("w-full bg-inherit").style():
            with ui.tab_panel("Fiche Personnage"):
                if mock_player:
                    PlayerPage(mock_player).display_page()
                else:
                    ui.label("Aucun joueur correspondant trouvé.").classes("text-red-500")

            with ui.tab_panel("Combat"):
                ui.label("Fight")


@ui.page("/login")
def login() -> Optional[RedirectResponse]:
    ui.add_head_html('<link rel="stylesheet" href="/css/style.css">')
    ui.colors(primary="#000000", secondary="#282A3A", accent="#735F32", positive="#C69749")

    def try_login() -> None:
        if passwords.get(username.value) == password.value:
            app.storage.user.update({"username": username.value, "authenticated": True})
            ui.navigate.to("/")
        else:
            ui.notify("Mauvais identifiant ou mot de passe", color="negative")

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")
    with ui.card().classes("absolute-center p-4 gap-4"):
        username = ui.input("Nom d’utilisateur").on("keydown.enter", try_login)
        password = ui.input("Mot de passe", password=True, password_toggle_button=True).on("keydown.enter", try_login)
        ui.button("Connexion", on_click=try_login)
    return None


@app.on_disconnect
def on_disconnect():
    # Enregistrer le joueur ici, mais dans un contexte UI approprié
    pass


app.add_static_files(local_directory="app/static/css/", url_path="/css")
app.add_media_files(local_directory="app/static/assets", url_path="/assets")
app.add_media_files(local_directory="app/static/icons", url_path="/icons")
ui.run(storage_secret="VOTRE_SECRET_ICI")
