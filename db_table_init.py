from __init__ import app, db
from model.personalInfo import personalInfo
from sqlalchemy import inspect

def create_table():
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            if inspector.has_table(personalInfo.__tablename__):
                personalInfo.__table__.drop(db.engine)
                print(f"Table '{personalInfo.__tablename__}' dropped successfully.")

            personalInfo.__table__.create(db.engine)
            print(f"Table '{personalInfo.__tablename__}' created successfully.")

            personalInfo.insert_default_entries()

        except Exception as e:
            print(f"Error creating or dropping table '{personalInfo.__tablename__}': {e}")

if __name__ == "__main__":
    create_table()
