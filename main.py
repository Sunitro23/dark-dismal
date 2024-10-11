from nicegui import app, ui

if __name__ in {"__main__", "__mp_main__"}:
    app.add_static_files(local_directory="app/static/css", url_path="/css")
    app.add_media_files(local_directory="app/static/assets", url_path="/assets")
    app.add_media_files(local_directory="app/static/icons", url_path="/icons")
    app.add_media_files(local_directory="app/static/fonts", url_path="/fonts")
    ui.run(storage_secret="VOTRE_SECRET_ICI")

import app.ui.pages.pages
