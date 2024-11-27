class Config:
    SECRET_KEY = 'mi_clave_secreta'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Leonel'
    MYSQL_DB = 'salas_conferencia'

    # URI de conexión para SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
