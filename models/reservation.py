from . import db
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('active', 'cancelled'), default='active', nullable=False)

    user = db.relationship('User', back_populates='reservations')
    # Relación con Room (si existe)
    room = db.relationship('Room', back_populates='reservations')
