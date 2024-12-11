from sqlite3 import IntegrityError
from __init__ import app, db

class personalInfo(db.Model):
    __tablename__ = 'personalInfo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _name = db.Column(db.String(255), nullable=False)
    _dob = db.Column(db.String(255), nullable=False)
    _color = db.Column(db.String(255), nullable=False)

    def __init__(self, name, dob, color):
        self._name = name
        self._dob = dob
        self._color = color

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
            'color': self._color
        }

    @staticmethod
    def insert_default_entries():
        try:
            # check empty
            existing_entries = personalInfo.query.count()
            if existing_entries == 0:
                default_entries = [
                    personalInfo(name="Nikhil Maturi", dob="01-20-2009", color="Black"),
                    personalInfo(name="Mihir Thaha", dob="04-09-2009", color="Purple"),
                    personalInfo(name="Aarush Gowda", dob="04-09-2009", color="Grey"),
                    personalInfo(name="Vasanth Rajasekaran", dob="06-27-2009", color="Black"),
                    personalInfo(name="Nikhil Narayan", dob="05-16-2009", color="Blue"),
                    personalInfo(name="Jowan Elzein", dob="07-02-2008", color="Purple"),
                ]
                db.session.bulk_save_objects(default_entries)
                db.session.commit()
                print("Default entries added to personalInfo table.")
            else:
                print("Table already contains entries. No defaults added.")
        except Exception as e:
            db.session.rollback()
            print(f"Error inserting default entries: {e}")