from flask import Blueprint, render_template, request, redirect, url_for, flash
from middleware import admin_required, login_required
from models.room import Room
from models import db

rooms_routes = Blueprint('rooms', __name__)

@rooms_routes.route('/rooms', methods=['GET'])
@login_required
def list_rooms():
    """Ruta para listar salas disponibles."""
    rooms = Room.query.filter_by(availability=True).all()
    return render_template('list_rooms.html', rooms=rooms)


@rooms_routes.route('/admin/rooms', methods=['GET', 'POST'])
@admin_required
def manage_rooms():
    """Ruta para que el administrador gestione las salas."""
    if request.method == 'POST':
        name = request.form['name']
        capacity = request.form['capacity']
        location = request.form['location']
        availability = request.form.get('availability') == 'on'

        new_room = Room(name=name, capacity=capacity, location=location, availability=availability)
        db.session.add(new_room)
        db.session.commit()
        flash('Sala creada exitosamente.', 'success')

    rooms = Room.query.all()
    return render_template('admin_manage.html', rooms=rooms)


@rooms_routes.route('/admin/rooms/delete/<int:room_id>', methods=['POST'])
@admin_required
def delete_room(room_id):
    """Ruta para que el administrador elimine una sala."""
    room = Room.query.get(room_id)
    if room:
        db.session.delete(room)
        db.session.commit()
        flash('Sala eliminada exitosamente.', 'success')
    else:
        flash('La sala no existe.', 'danger')
    return redirect(url_for('rooms.manage_rooms'))

@rooms_routes.route('/admin/rooms/update/<int:room_id>', methods=['GET', 'POST'])
@admin_required
def update_room(room_id):
    """Ruta para que el administrador modifique una sala."""
    room = Room.query.get_or_404(room_id)  # Obtén la sala, si no existe muestra un error 404

    if request.method == 'POST':
        room.name = request.form['name']
        room.capacity = request.form['capacity']
        room.location = request.form['location']
        room.availability = request.form.get('availability') == 'on'

        db.session.commit()  # Guarda los cambios en la base de datos
        flash('Sala actualizada exitosamente.', 'success')
        return redirect(url_for('rooms.manage_rooms'))  # Redirige a la vista de gestión de salas

    return render_template('modificar_sala.html', room=room)  # Muestra el formulario de actualización
