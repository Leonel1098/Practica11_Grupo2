from flask import Flask, redirect, url_for
from config import Config
from models import db
from routes import auth_routes, room_routes, reservation_routes, auth_routes

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar base de datos
db.init_app(app)

# Registrar rutas
app.register_blueprint(auth_routes.auth_routes, url_prefix='/auth')
app.register_blueprint(room_routes.rooms_routes, url_prefix='/rooms')
app.register_blueprint(reservation_routes.reservations_routes, url_prefix='/reservations')

@app.route('/')
def home():
    return redirect(url_for('auth.login')) 



if __name__ == "__main__":
    app.run(debug=True)
