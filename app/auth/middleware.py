from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app, ui

passwords = {"Kaelith": "léna&mimi", "RavenarLeSublime": "ilovefurries37", "vladlovesfishy": "blessedby69skibidis"}
unrestricted_page_routes = {"/login"}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get("authenticated", False):
            if not request.url.path.startswith("/_nicegui") and request.url.path not in unrestricted_page_routes:
                app.storage.user["referrer_path"] = request.url.path
                return RedirectResponse("/login")
        return await call_next(request)


app.add_middleware(AuthMiddleware)
