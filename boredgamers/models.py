from boredgamers import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(60))
    age = db.Column(db.Integer)
    favourite_games = db.Column(db.String(300))
    about = db.Column(db.String(1000))
    availability = db.Column(db.String)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer, unique=True, nullable=False)
    bgg_url = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    min_players = db.Column(db.Integer)
    max_players = db.Column(db.Integer)
    average_time = db.Column(db.Integer)
    min_time = db.Column(db.Integer)
    max_time = db.Column(db.Integer)
    year = db.Column(db.Integer)
    average_rating = db.Column(db.Float)
    geek_rating = db.Column(db.Float)
    num_votes = db.Column(db.Integer)
    image_url = db.Column(db.String, unique=True)
    age = db.Column(db.Integer)
    mechanic = db.Column(db.String)
    owned = db.Column(db.Integer)
    category = db.Column(db.String)
    designer = db.Column(db.String)

    def __repr__(self):
        return f"Game: {self.name}"