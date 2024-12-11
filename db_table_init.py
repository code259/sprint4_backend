from __init__ import app, db
from model.personalInfo import personalInfo
from sqlalchemy import inspect

def create_table():
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            if not inspector.has_table(personalInfo.__tablename__):
                personalInfo.__table__.create(db.engine)
                print(f"Table '{personalInfo.__tablename__}' created successfully.")
            else:
                print(f"Table '{personalInfo.__tablename__}' already exists.")
        except Exception as e:
            print(f"Error creating table '{personalInfo.__tablename__}': {e}")

if __name__ == "__main__":
    create_table()
