from sqlalchemy import Column, Integer, String, Float
from __init__ import db, app

class Skill(db.Model):
    # Defines skills model, and specifies the different columns and their data types

    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    _skill_name = db.Column(db.String(50), nullable=False)  # Skill name (e.g., "Tactics", "Blitz")
    _skill_level = db.Column(db.String(10), nullable=False)  # "High" or "Low"
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Links skill to a user in the table

    def __init__(self, skill_name, skill_level, user_id):
    # Making the class and establishing the attributes
        self._skill_name = skill_name
        self._skill_level = skill_level
        self._user_id = user_id

    def create(self):
    # Adds a new skill entry to the database
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
    # Access the skill information as a dictionary
        return {
            "id": self.id,
            "skill_name": self._skill_name,
            "skill_level": self._skill_level,
            "user_id": self._user_id
        }

    def delete(self):
    # Deletes the current skill entry from the database
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initSkills():
    # Function to initialize the "skills" table and add test data
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Sample data for table for testing purposes
        skills = [
            Skill(skill_name='Tactics', skill_level='High', user_id=1),
            Skill(skill_name='Blitz', skill_level='Low', user_id=2),
        ]

        for skill in skills:
        # Loop through the sample data and add each skill to the database
            try:
                db.session.add(skill)
                db.session.commit()
                print(f"Record created: {repr(skill)}")
                # Prints success message
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate or error: {repr(skill)}")
                # Print error message
