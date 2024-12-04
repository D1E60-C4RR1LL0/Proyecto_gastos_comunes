import sys
import os

# Agregar el directorio raíz del proyecto al sys.path
BASE_DIR = "C:\\Duoc\\Proyecto_gastos_comunes"
sys.path.append(BASE_DIR)

from backend.app import db
from flask import Flask
from sqlalchemy.sql import text


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Izipizi123.@localhost/gestion_gastos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    try:
        # Intenta conectarte a la base de datos usando text()
        db.session.execute(text('SELECT 1'))
        print("¡Conexión exitosa con la base de datos!")
    except Exception as e:
        print("Error al conectar con la base de datos:", str(e))

