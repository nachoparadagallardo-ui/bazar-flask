from flask_sqlalchemy import SQLAlchemy

# Instancia global de SQLAlchemy, pero aún NO está vinculada a la app
# Esto permite importarla en cualquier archivo sin generar importaciones circulares
db = SQLAlchemy()

# Aquí se pueden agregar otras extensiones en el futuro (por ejemplo, Flask-Migrate, Flask-Login, etc.)
# Cada extensión debe ser inicializada en app.py dentro de create_app()
