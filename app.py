from flask import Flask
from core.config import Config
from extensions.database import db, migrate 
from routes.__init__ import routes_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    #inicializar SQLAlchemy
    db.init_app(app)
    
    #Inicializar Migrate
    migrate.init_app(app, db)

    # Rotas
    routes_app(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000, debug=True)