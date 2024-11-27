import select
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_jwt_extended import current_user
from middleware import login_required
from models.reservation import Reservation
from models import db
from models.room import Room
from models.user import User

reservations_routes = Blueprint('reservations', __name__)

@reservations_routes.route('/reservations', methods=['GET'])
def list_reservations():
    user_id = session.get('user_id')
    
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    
    if user.role == 'admin':
        reservations = Reservation.query.all()
    else:
        reservations = Reservation.query.filter_by(user_id=user.id).all()

    return render_template('listar_reservaciones.html', reservations=reservations)


# Ruta para crear una reserva
@reservations_routes.route('/reservations/create', methods=['GET', 'POST'])
def create_reservation():
    # Obtener datos de sesión
    user_id = session.get('user_id')
    user_role = session.get('role')

    # Verificar autenticación y permisos
    if user_id is None:
        flash("Debes iniciar sesión para crear una reserva", "danger")
        return redirect(url_for('auth.login'))  # Redirige al login si no está autenticado

    if user_role != 'user':
        flash("No tienes permisos para crear una reserva", "danger")
        return redirect(url_for('reservations.list_reservations'))

    # Manejo de formulario para creación de reservas
    if request.method == 'POST':
        nombre_cliente = request.form.get('nombre_cliente')
        fecha_reserva = request.form.get('fecha_reserva')
        hora_reserva = request.form.get('hora_reserva')

        # Validar que los campos no estén vacíos (opcional)
        if not (nombre_cliente and fecha_reserva and hora_reserva):
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('reservations.create_reservation'))

        # Crear una nueva reserva
        new_reservation = Reservation(
            nombre_cliente=nombre_cliente,
            fecha_reserva=fecha_reserva,
            hora_reserva=hora_reserva,
            user_id=user_id
        )
        db.session.add(new_reservation)
        db.session.commit()
        flash("Reserva creada exitosamente!", "success")
        return redirect(url_for('reservations.list_reservations'))

    # Renderizar el formulario de creación de reservas
    return render_template('crear_reservacion.html')


# Ruta para editar una reserva
@reservations_routes.route('/reservations/edit/<int:reservation_id>', methods=['GET', 'POST'])
def edit_reservation(reservation_id):
    # Verificar si el usuario está autenticado
    user_id = session.get('user_id')
    user_role = session.get('role')

    if not user_id:
        flash("Debes iniciar sesión para editar una reserva", "danger")
        return redirect(url_for('auth.login'))

    reservation = Reservation.query.get_or_404(reservation_id)

    # Verificar si el usuario tiene permisos para editar la reserva
    if reservation.user_id != user_id and user_role != 'admin':
        flash("No tienes permiso para editar esta reserva", "danger")
        return redirect(url_for('reservations.list_reservations'))

    if request.method == 'POST':
        reservation.nombre_cliente = request.form['nombre_cliente']
        reservation.fecha_reserva = request.form['fecha_reserva']
        reservation.hora_reserva = request.form['hora_reserva']

        db.session.commit()
        flash("Reserva actualizada exitosamente", "success")
        return redirect(url_for('reservations.list_reservations'))

    return render_template('editar_reserva.html', reservation=reservation)

# Ruta para eliminar una reserva
@reservations_routes.route('/reservations/delete/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    # Verificar si el usuario está autenticado
    user_role = session.get('role')

    if not user_role:
        flash("Debes iniciar sesión para eliminar una reserva", "danger")
        return redirect(url_for('auth.login'))

    reservation = Reservation.query.get_or_404(reservation_id)

    # Verificar si el usuario tiene permisos para eliminar la reserva
    if user_role != 'admin':
        flash("No tienes permiso para eliminar esta reserva", "danger")
        return redirect(url_for('reservations.list_reservations'))

    db.session.delete(reservation)
    db.session.commit()
    flash("Reserva eliminada exitosamente", "success")
    return redirect(url_for('reservations.list_reservations'))

