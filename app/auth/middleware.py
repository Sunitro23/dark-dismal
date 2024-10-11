from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app, ui

passwords = {"Kaelith": "léna&mimi", "RavenarLeSublime": "ilovefurries37", "vladlovesfishy": "blessedby69skibidis", "Sun": "S0l41r3"}
unrestricted_page_routes = {"/login"}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get("authenticated", False):
            if not request.url.path.startswith("/_nicegui") and request.url.path not in unrestricted_page_routes:
                app.storage.user["referrer_path"] = request.url.path
                return RedirectResponse("/login")
        return await call_next(request)

    def is_authenticated(self):
        return app.storage.user.get("authenticated", False)

    def is_admin(self):
        return app.storage.user.get("username") == "Sun"

    def require_authentication(self, page_function):
        def wrapper():
            if not self.is_authenticated():
                ui.navigate.to("/login")
                return
            return page_function()

        return wrapper

    def require_admin(self, page_function):
        def wrapper():
            if not self.is_authenticated() or not self.is_admin():
                ui.navigate.to("/login")
                return
            return page_function()

        return wrapper


app.add_middleware(AuthMiddleware)


def logout():
    app.storage.user.clear
