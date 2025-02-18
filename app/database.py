from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


# DeclarativeBase define un estilo declarativo para los modelos de SQLAlchemy.
# MappedAsDataclass habilita la funcionalidad de dataclass en los modelos.
class Base(DeclarativeBase, MappedAsDataclass):
    pass

# Crea la instancia de SQLAlchemy usando la clase base personalizada anterior.
db = SQLAlchemy(model_class=Base)
