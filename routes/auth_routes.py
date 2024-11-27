from flask import Blueprint, render_template, redirect, request, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models import db

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Buscar usuario por email
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash('Inicio de sesión exitoso', 'success')
            if user.role == 'admin':
                return redirect(url_for('rooms.manage_rooms'))
            return redirect(url_for('rooms.list_rooms'))
        else:
            flash('Email o contraseña incorrectos', 'danger')

    return render_template('login.html')


@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        # Validación de contraseñas
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.register'))

        # Validar si el email ya está registrado
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'danger')
            return redirect(url_for('auth.register'))

        # Crear un nuevo usuario
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password, role=role)

        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso, ahora puedes iniciar sesión', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_routes.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('auth.login'))
