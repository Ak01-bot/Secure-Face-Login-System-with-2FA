# app/__init__.py

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from app.routes import main

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Allow up to 2 MB
    
    # Load secret key from file
    with open('secret.key', 'rb') as f:
        app.secret_key = f.read()

    app.register_blueprint(main)
    return app
