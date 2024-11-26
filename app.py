from flask import Flask, render_template, redirect, url_for, request, flash
from models import db
from models.user import User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.password == password: 
            flash('Login exitoso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Correo electrónico o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        user = User(name=name, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Cuenta creada exitosamente!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
