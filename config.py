import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI','mysql://root:Leonel@localhost/salas_conferencia') 



