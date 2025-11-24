# ==============================
# Blueprint del módulo VENTAS
# ==============================
from flask import Blueprint

ventas_bp = Blueprint("ventas", __name__, template_folder="templates")

# Importar las rutas (IMPORTANTE para registrar vistas)
from . import routes
