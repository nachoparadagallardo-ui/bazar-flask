class Config:
    # Clave necesaria para proteger formularios y sesiones (CSRF)
    SECRET_KEY = "clave_super_secreta"

    # Cadena de conexión a MySQL usando PyMySQL
    # FORMATO: mysql+pymysql://USUARIO:PASSWORD@HOST/BASE_DE_DATOS
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:12345@localhost/bazar"

    # Desactiva el seguimiento para optimizar rendimiento 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
# “El archivo config.py contiene la configuración principal de la aplicación Flask,
# incluyendo la clave secreta para seguridad y la cadena de conexión a la base de datos MySQL.
# También desactiva el seguimiento de modificaciones para mejorar el rendimiento.”  

   
