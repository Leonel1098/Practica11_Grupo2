from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.Enum('user', 'admin', name='roles'), default='user')

    reservations = db.relationship('Reservation', back_populates='user')

    def __repr__(self):
        return f'<User {self.name}>'
