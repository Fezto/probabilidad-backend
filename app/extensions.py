# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


# La instancia de SQLAlchemy se crea a nivel de módulo,
# por lo que se comporta como un singleton en la aplicación.
class Base(DeclarativeBase, MappedAsDataclass):
  pass

db = SQLAlchemy(model_class=Base)
