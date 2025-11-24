from flask import Blueprint 
# Definimos el Blueprint del módulo de Productos 

productos_bp = Blueprint("productos", __name__, template_folder="templates")
# Importamos las rutas desde routes.py para que se registren en Flask

from . import routes # Importar las rutas (IMPORTANTE para registrar vistas)
# =============================== 
# Fin de productos/__init__.py

