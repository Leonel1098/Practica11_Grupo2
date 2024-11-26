from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.reservation import Reservation, db
from models.room import Room
from models.user import User

bp = Blueprint('reservations', __name__)

# Ruta para hacer una reserva
@bp.route('/', methods=['POST'])
@jwt_required()
def create_reservation():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    user = User.query.get(current_user_id)
    room_id = data.get('room_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not room_id or not start_time or not end_time:
        return jsonify({"msg": "Missing required fields"}), 400

    room = Room.query.get_or_404(room_id)

    # Verificar disponibilidad de la sala
    if not room.availability:
        return jsonify({"msg": "Room not available"}), 400

    new_reservation = Reservation(user_id=user.id, room_id=room.id, start_time=start_time, end_time=end_time)
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({"msg": "Reservation created successfully"}), 201

# Ruta para ver las reservas de un usuario
@bp.route('/', methods=['GET'])
@jwt_required()
def get_user_reservations():
    current_user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=current_user_id).all()
    return jsonify([{
        'id': reservation.id,
        'room_id': reservation.room_id,
        'start_time': reservation.start_time,
        'end_time': reservation.end_time,
        'status': reservation.status
    } for reservation in reservations]), 200

# Ruta para cancelar una reserva
@bp.route('/<int:reservation_id>', methods=['DELETE'])
@jwt_required()
def cancel_reservation(reservation_id):
    current_user_id = get_jwt_identity()
    reservation = Reservation.query.get_or_404(reservation_id)

    if reservation.user_id != current_user_id:
        return jsonify({"msg": "Permission denied"}), 403

    reservation.status = 'cancelled'
    db.session.commit()

    return jsonify({"msg": "Reservation cancelled successfully"}), 200
