from os import environ

class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    MYSQL_USER = environ.get("MYSQL_USER")
    MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD")
    MYSQL_HOST = environ.get("MYSQL_HOST")
    MYSQL_DB = environ.get("MYSQL_DB")
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False