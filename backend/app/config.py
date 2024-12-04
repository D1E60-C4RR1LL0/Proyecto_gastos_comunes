import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:Izipizi123.@localhost/gestion_gastos')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Izipizi123.'
