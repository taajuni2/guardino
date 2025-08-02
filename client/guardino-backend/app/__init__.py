from flask import Flask
from routes.routes import ping_bp
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Blueprints registrieren
    app.register_blueprint(ping_bp, url_prefix="/api")

    return app