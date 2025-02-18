# python
from flask import Flask
from flask_cors import CORS
from .config import Config
from .database import db
from .routes import api

# Instancia la aplicación
app = Flask(__name__)

# Habilita CORS en la app
CORS(app)

# Carga la configuración de la clase Config
app.config.from_object(Config)

# Registra el blueprint del módulo api bajo el prefijo /api
app.register_blueprint(api, url_prefix="/api")

# Inicializa la base de datos con la aplicación
db.init_app(app)