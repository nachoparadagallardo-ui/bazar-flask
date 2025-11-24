# Importar dependencias
from flask import Flask, render_template
from config import Config
from extensions import db

# Importar blueprints (uno por módulo)
from productos import productos_bp
from proveedores import proveedores_bp
from compras import compras_bp
from ventas import ventas_bp
from balance import balance_bp

def create_app():
    app = Flask(__name__) # Crear instancia de Flask 

    # Cargar configuración desde config.py
    app.config.from_object(Config)

    # Inicializar la extensión de base de datos
    db.init_app(app)

    # ==============================
    #   REGISTRO DE BLUEPRINTS
    # ==============================

    # Registro de blueprints con sus prefijos de URL
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(proveedores_bp, url_prefix="/proveedores")  
    app.register_blueprint(compras_bp, url_prefix="/compras")
    app.register_blueprint(ventas_bp, url_prefix="/ventas")
    app.register_blueprint(balance_bp, url_prefix="/balance")
    

    # ==============================
    #   RUTA DE INICIO
    # ==============================
    @app.route("/")
    def index():
        return render_template("inicio.html")  # Archivo en templates/

    return app

# Ejecutar app (solo si se llama directamente)
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


# “El archivo app.py es el que inicializa toda la aplicación Flask.
#Cuando lo ejecuto, crea la app, registra los blueprints, se conecta a la base de datos y levanta el servidor web.
#Es el punto de entrada principal de la aplicación.”