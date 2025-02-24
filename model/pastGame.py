from flask import current_app
from flask_login import UserMixin
from datetime import date, datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from model.user import User
from flask_sqlalchemy import SQLAlchemy

from __init__ import app, db

""" Helper Functions """


class pastGame(db.Model):
    """
    pastGame Model

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database.
        id (Column): The primary key, an integer representing the unique identifier for the user.
        user_id (Column): A foreign key reference to the user.
        user_name (Column): The name of the user.
        number_of_wins (Column): An integer representing the number of times the user has beaten the bot.
        number_of_losses (Column): An integer representing the number of times the user has lost to the bot.
    """
    __tablename__= 'past_games'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    number_of_wins = db.Column(db.Integer, nullable=False)
    number_of_losses = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, number_of_wins, number_of_losses):
        self.user_id = user_id
        self.number_of_wins = number_of_wins
        self.number_of_losses = number_of_losses

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data):
        self.user_id = data.get('user_id', self.user_id)
        self.number_of_wins = data.get('number_of_wins', self.number_of_wins)
        self.number_of_losses = data.get('number_of_losses', self.number_of_losses)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def read(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "number_of_wins": self.number_of_wins,
            "number_of_losses": self.number_of_losses,
        }

    @staticmethod
    def restore(data):
        for game_data in data:
            _ = game_data.pop('id', None)  # Remove 'id' from post_data
            user_id = game_data.get("user_id", None)
            game = pastGame.query.filter_by(user_id=user_id).first()
            if game:
                game.update(game_data)
            else:
                game = pastGame(**game_data)
                game.update(game_data)
                game.create()

def initPastGames():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        past_games = [
            pastGame(user_id=1, number_of_wins=3, number_of_losses=1),
            pastGame(user_id=2, number_of_wins=2, number_of_losses=4),
            pastGame(user_id=3, number_of_wins=5, number_of_losses=2),
        ]
        for game in past_games:
            db.session.add(game)
        db.session.commit()
        print("Past Games table initialized.")
        return True
