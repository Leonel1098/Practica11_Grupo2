from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.room import Room, db
from models.user import User

bp = Blueprint('rooms', __name__)

# Ruta para listar todas las salas disponibles
@bp.route('/', methods=['GET'])
def get_rooms():
    rooms = Room.query.filter_by(availability=True).all()
    return jsonify([{'id': room.id, 'name': room.name, 'capacity': room.capacity, 'location': room.location} for room in rooms]), 200

# Ruta para agregar una nueva sala (Solo admin)
@bp.route('/', methods=['POST'])
@jwt_required()
def add_room():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'admin':
        return jsonify({"msg": "Permission denied"}), 403
    
    data = request.get_json()
    name = data.get('name')
    capacity = data.get('capacity')
    location = data.get('location')

    if not name or not capacity or not location:
        return jsonify({"msg": "Missing required fields"}), 400

    new_room = Room(name=name, capacity=capacity, location=location, availability=True)
    db.session.add(new_room)
    db.session.commit()

    return jsonify({"msg": "Room added successfully"}), 201

# Ruta para editar una sala (Solo admin)
@bp.route('/<int:room_id>', methods=['PUT'])
@jwt_required()
def update_room(room_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'admin':
        return jsonify({"msg": "Permission denied"}), 403
    
    room = Room.query.get_or_404(room_id)
    data = request.get_json()

    room.name = data.get('name', room.name)
    room.capacity = data.get('capacity', room.capacity)
    room.location = data.get('location', room.location)

    db.session.commit()
    return jsonify({"msg": "Room updated successfully"}), 200

# Ruta para eliminar una sala (Solo admin)
@bp.route('/<int:room_id>', methods=['DELETE'])
@jwt_required()
def delete_room(room_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'admin':
        return jsonify({"msg": "Permission denied"}), 403

    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()

    return jsonify({"msg": "Room deleted successfully"}), 200
