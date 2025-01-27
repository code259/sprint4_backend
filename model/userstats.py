from __init__ import db, app

class UserStats(db.Model):
    """
    UserStats Model
    This model represents user statistics including wins and losses.
    """
    __tablename__ = 'user_stats'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    wins = db.Column(db.Integer, default=0, nullable=False)
    losses = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, user_id, wins=0, losses=0):
        """
        Initialize the UserStats object.
        
        Args:
            user_id (int): The user's unique identifier.
            wins (int, optional): The number of wins. Defaults to 0.
            losses (int, optional): The number of losses. Defaults to 0.
        """
        self.user_id = user_id
        self.wins = wins
        self.losses = losses

    def create(self):
        """
        Add the user stats to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the user stats as a dictionary.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "wins": self.wins,
            "losses": self.losses
        }

    def update(self, data):
        """
        Update the user stats with the provided dictionary.
        
        Args:
            data (dict): A dictionary containing the new data for the user stats.
        """
        try:
            self.wins = data.get('wins', self.wins)
            self.losses = data.get('losses', self.losses)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Remove the user stats from the database and commit the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initUserStats():
    """
    Initialize the UserStats table with sample data.
    """
    stats = [
        UserStats(user_id=1, wins=5, losses=2),
        UserStats(user_id=2, wins=3, losses=4),
        UserStats(user_id=3, wins=10, losses=0)
    ]

    with app.app_context():
        try:
            db.drop_all()  # Drop all tables for a clean start
            db.create_all()  # Create all tables
            print("Database tables created.")

            for stat in stats:
                stat.create()
                print(f"Added User Stats: User ID {stat.user_id} with {stat.wins} wins and {stat.losses} losses")

        except Exception as e:
            print(f"Error initializing UserStats: {e}")
