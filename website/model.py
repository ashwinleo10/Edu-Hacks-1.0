from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User model
class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Game model
class Game(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    levels = db.relationship('Level', backref='game', lazy=True)

    def __repr__(self):
        return f"<Game {self.name}>"

# Level model
class Level(db.Model):
    id = db.Column(db.String, primary_key=True)
    level_name = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50))
    game_id = db.Column(db.String, db.ForeignKey('game.id'), nullable=False)
    challenges = db.relationship('Challenge', backref='level', lazy=True)

    def __repr__(self):
        return f"<Level {self.level_name}>"

# Challenge model
class Challenge(db.Model):
    id = db.Column(db.String, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    solution = db.Column(db.String(200), nullable=False)
    level_id = db.Column(db.String, db.ForeignKey('level.id'), nullable=False)

    def __repr__(self):
        return f"<Challenge {self.question}>"

# Score model
class Score(db.Model):
    id = db.Column(db.String, primary_key=True)
    score_value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.String, db.ForeignKey('game.id'), nullable=False)

    def __repr__(self):
        return f"<Score {self.score_value} by User {self.user_id}>"
