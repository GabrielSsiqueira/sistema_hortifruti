from .admin import admin_blueprint
from .hortifruti import hortifruti_blueprint

def routes_app(app):
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(hortifruti_blueprint)