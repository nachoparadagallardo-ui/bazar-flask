from app import create_app
from extensions import db

# Crear la app usando create_app()
app = create_app()

# Crear las tablas dentro del contexto de la aplicación
with app.app_context():
    db.create_all()
    print("Tablas creadas correctamente desde models.py")
