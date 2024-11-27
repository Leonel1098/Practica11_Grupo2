from . import db
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200))
    availability = db.Column(db.Boolean, default=True)

     # Relación con User
    reservations = db.relationship('Reservation', back_populates='room')


    def __repr__(self):
        return f'<Room {self.name}>'

    

