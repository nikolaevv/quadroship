from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sender = db.Column(db.Integer)
    receiver = db.Column(db.Integer)
    
    sendLat = db.Column(db.Float)
    sendLon = db.Column(db.Float)
    recvLat = db.Column(db.Float)
    recvLon = db.Column(db.Float)

    status = db.Column(db.Integer)
    comment = db.Column(db.String(500))

    way = db.Column(db.Integer)
    minutes = db.Column(db.Integer)
    date_create = db.Column(db.DateTime)