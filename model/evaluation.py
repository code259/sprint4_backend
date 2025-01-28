from sqlalchemy import Column, Integer, String, Float
from __init__ import db, app

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True)
    move_number = Column(Integer, nullable=False)
    move = Column(String, nullable=False)
    evaluation = Column(Float, nullable=False)

    # CRUD methods
    def create(self):
        """
        Adds the evaluation object to the database and commits the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Returns a dictionary representation of the evaluation object.
        """
        return {
            "id": self.id,
            "move_number": self.move_number,
            "move": self.move,
            "evaluation": self.evaluation
        }

    def update(self, data):
        """
        Updates the evaluation object with the provided data and commits the transaction.
        """
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """
        Deletes the evaluation object from the database and commits the transaction.
        """
        db.session.delete(self)
        db.session.commit()

def initEvaluation():
    if Evaluation.query.count() == 0:
        evaluations = [
            Evaluation(move_number=1, move="e4", evaluation=0.5),
            Evaluation(move_number=2, move="e5", evaluation=0.3),
            Evaluation(move_number=3, move="Nf3", evaluation=0.2),
            Evaluation(move_number=4, move="Nc6", evaluation=0.1),
            Evaluation(move_number=5, move="Bc4", evaluation=0.4),
            Evaluation(move_number=6, move="d6", evaluation=0.3),
            Evaluation(move_number=7, move="d3", evaluation=0.2),
            Evaluation(move_number=8, move="Qe7", evaluation=0.1),
            Evaluation(move_number=9, move="Qe2", evaluation=0.4),
            Evaluation(move_number=10, move="O-O", evaluation=0.3),
            Evaluation(move_number=11, move="O-O", evaluation=0.2),
            Evaluation(move_number=12, move="Re1", evaluation=0.1),
            Evaluation(move_number=13, move="Re8", evaluation=0.4),
            Evaluation(move_number=14, move="Bd2", evaluation=0.3),
            Evaluation(move_number=15, move="Bd7", evaluation=0.2),
            Evaluation(move_number=16, move="c3", evaluation=0.1),
            Evaluation(move_number=17, move="c6", evaluation=0.4),
            Evaluation(move_number=18, move="b4", evaluation=0.3),
            Evaluation(move_number=19, move="b5", evaluation=0.2),
            Evaluation(move_number=20, move="a4", evaluation=0.1),
        ]
        db.session.add_all(evaluations)
        db.session.commit()

def remove_duplicates():
    """
    Removes duplicate entries from the evaluations table.
    """
    subquery = db.session.query(
        db.func.min(Evaluation.id).label('min_id')
    ).group_by(
        Evaluation.move_number, Evaluation.move, Evaluation.evaluation
    ).subquery()

    db.session.query(Evaluation).filter(
        Evaluation.id.notin_(db.session.query(subquery.c.min_id))
    ).delete(synchronize_session=False)

    db.session.commit()

# Create the tables, initialize data, and remove duplicates
with app.app_context():
    db.create_all()
    initEvaluation()
    remove_duplicates()