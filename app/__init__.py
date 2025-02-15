from os import environ

from flask import Flask
from .config import Config
from .extensions import db
from .routes import api

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(api, url_prefix="/api")
db.init_app(app)
print(environ.get("MYSQL_USER")) # Debería imprimir 'root'
print(environ.get("MYSQL_PASSWORD")) # Debería imprimir 'root'
print(environ.get("MYSQL_HOST")) # Debería imprimir 'localhost'
print(environ.get("MYSQL_DB")) # Debería imprimir 'school'



