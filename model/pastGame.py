# user.py
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
        _uid (Column): A unique string identifier for the user, cannot be null.
        _winner (Column): A string representing the path to the user's profile picture. It can be null.
        _elo (Column): A string representing the path to the user's profile picture. It can be null.

    """
    __tablename__= 'past_games'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(100), nullable=False)
    winner = db.Column(db.String(100), nullable=False)
    elo = db.Column(db.String(100), nullable=False)
    # timestamp = db.Column(db.String(100), default=str(datetime.ctime))


    def __init__(self, uid, winner, elo):
        self.uid = uid
        self.winner = winner
        self.elo = elo

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, data):

        self.uid = data.get('uid', self.uid)
        self.winner = data.get('winner', self.winner)
        self.elo = data.get('elo', self.elo)
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
            "uid": self.uid,
            "winner": self.winner,
            "elo": self.elo,
            # "timestamp": self.timestamp
        }

    @staticmethod
    def restore(data):
        for game_data in data:
            _ = game_data.pop('id', None)  # Remove 'id' from post_data
            uid = game_data.get("uid", None)
            game = pastGame.query.filter_by(uid=uid).first()
            if game:
                game.update(game_data)
            else:
                game = pastGame(**game_data)
                game.update(game_data)
                game.create()

def initPastGames():
    with app.app_context():
        # Drop the existing table if it exists
        db.drop_all()
        # Create all tables
        db.create_all()
        
        past_games = [
            pastGame(uid="niko", winner="winner1", elo="elo100"),
            pastGame(uid="john", winner="winner2", elo="elo2000"),
            pastGame(uid="shane", winner="winner3", elo="elo300"),
        ]
        for game in past_games:
            db.session.add(game)
        db.session.commit()
        print("Past Games table initialized.")
        return True
