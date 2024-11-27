from flask import session, redirect, url_for, flash

def login_required(func):
    """Middleware para verificar si el usuario está autenticado."""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión primero.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def admin_required(func):
    """Middleware para verificar si el usuario es administrador."""
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión primero.', 'danger')
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'admin':
            flash('No tienes permiso para acceder a esta página.', 'danger')
            return redirect(url_for('rooms.list_rooms'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
