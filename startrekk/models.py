from datetime import datetime, timedelta
from startrekk  import db


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique= True)
    password = db.Column(db.String(80), nullable=False,unique = True)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)
    posts = db.relationship('Watchlist', backref='author', lazy=True)
    
    def __repr__(self):
        return '<USER %r>' % self.id

class Watchlist(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    content = db.Column(db.PickleType,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)

    def __repr__(self):
        return '<POST %r>' % self.id
