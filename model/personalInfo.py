from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class personalInfo(db.Model):
    __tablename__ = 'personalInfo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _name = db.Column(db.String(255), nullable=False)
    _dob = db.Column(db.String(255), nullable=False)
    _color = db.Column(db.String(255), nullable=False)
    _user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, dob, color, user_id):
        """
        Constructor, 1st step in object creation.

        Args:
            name (str): The name of the group.
            section_id (int): The section to which the group belongs.
            moderators (list, optional): A list of users who are the moderators of the group. Defaults to None.
        """
        self._name = name
        self._dob = dob
        self._color = color
        self._user_id = user_id

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        return {
            'id': self.id,
            'name': self._name,
            'dob': self._dob,
            'color': self._color,
            'user_id': self._user_id,
        }