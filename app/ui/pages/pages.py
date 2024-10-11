from app.services.character_service import get_current_user_character
from app.ui.pages.character_form_page import CharacterCreationForm
from app.auth.middleware import AuthMiddleware
from app.ui.pages.login_page import LoginPage
from app.ui.pages.admin_page import AdminPage
from app.constants.constants import head_html
from app.ui.pages.main_page import MainPage
from nicegui import app, ui

middleware = AuthMiddleware(app)


@ui.page("/")
@middleware.require_authentication
def main_page():
    character = get_current_user_character()
    if character is None:
        ui.navigate.to("/create_character")
    else:
        MainPage(character).display()


@ui.page("/admin")
@middleware.require_admin
def admin_page_view():
    ui.add_head_html(head_html)
    ui.colors(primary="#000000", secondary="#282A3A", accent="#735F32", positive="#C69749")
    admin_page = AdminPage()
    admin_page.display()


@ui.page("/login")
def login():
    ui.add_head_html(head_html)
    ui.colors(primary="#000000", secondary="#282A3A", accent="#735F32", positive="#C69749")
    LoginPage()


@ui.page("/create_character")
@middleware.require_authentication
def create_character_page():
    ui.add_head_html(head_html)
    ui.colors(primary="#000000", secondary="#282A3A", accent="#735F32", positive="#C69749")
    CharacterCreationForm()
