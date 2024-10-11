from app.constants.constants import head_html
from app.auth.middleware import passwords
from nicegui import app, ui


class LoginPage:
    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        ui.add_head_html(head_html)
        ui.colors(primary="#000000", secondary="#282A3A", accent="#735F32", positive="#C69749")

        if app.storage.user.get("authenticated", False):
            ui.navigate.to("/")
            return

        with ui.card().classes("absolute-center p-4 gap-4"):
            self.username = ui.input("Nom d’utilisateur").on("keydown.enter", self.try_login)
            self.password = ui.input("Mot de passe", password=True, password_toggle_button=True).on("keydown.enter", self.try_login)
            ui.button("Connexion", on_click=self.try_login)

    def try_login(self):
        if passwords.get(self.username.value) == self.password.value:
            app.storage.user.update({"username": self.username.value, "authenticated": True})
            if self.username.value == "Sun":
                ui.navigate.to("/admin")
            else:
                ui.navigate.to("/")
        else:
            ui.notify("Mauvais identifiant ou mot de passe", color="negative")
