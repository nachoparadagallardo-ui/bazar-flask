from flask import Blueprint # ===============================
# Definimos el Blueprint del módulo de Proveedores
#
proveedores_bp = Blueprint("proveedores", __name__, template_folder="templates") # Importamos las rutas para registrar las vistas

from . import routes # ===============================
