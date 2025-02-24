import logging
from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class Pgn(db.Model):
    __tablename__ = 'pgn'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _pgn = db.Column(db.String(255), nullable=False)
    _date = db.Column(db.String(255), nullable=False)
    _name = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, pgn, date, name, user_id=None):
        self._pgn = pgn
        self._date = date
        self._name = name
        self._user_id = user_id

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        user = User.query.get(self._user_id)
        return {
            'id': self.id,
            'pgn': self._pgn,
            'date': self._date,
            'name': self._name,
            "user_name": user.name if user else None
        }
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def patch(self):
        inputs = Pgn.query.get(self.id)

        if inputs._pgn:
            self._pgn = inputs._pgn
        if inputs._date:
            self._date = inputs._date
        if inputs._name:
            self._name = inputs._name

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            logging.warning(f"IntegrityError: Could not update pgn entry.")
            return None
        return self

    def update(self, data):

        # self._pgn = data.get('pgn', self.uid)
        # self._date = data.get('date', self.winner)
        # self._name = data.get('name', self.elo)
        # self._user_id = data.get('user_id', self.elo)
        # try:
        #     db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

    @staticmethod
    def restore(data):
        for pgn_data in data:
            _ = pgn_data.pop('id', None)  # Remove 'id' from post_data
            pgn_name = pgn_data.get("name", None)
            pgn = Pgn.query.filter_by(_name=pgn_name).first()
            if pgn:
                pgn.update(pgn_data)
            else:
                pgn = Pgn(**pgn_data)
                pgn.update(pgn_data)
                pgn.create()

def initPgn():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        p1 = Pgn(pgn='1. f3 c5 2. g4 d5 3. Na3 h5 4. b3 hxg4 5. c3 Nc6 6. d3 g6 7. b4 Nf6 8. Nb5 Bg7 9. Bd2 d4 10. cxd4 cxd4 11. Nxa7 Nxa7 12. Rc1 Kf8 13. Rxc8 Qxc8 14. a4 Qc7 15. b5 Qd8 16. a5 Qd5 17. b6 Qd6 18. bxa7 Kg8 19. a6 Rxa7 20. axb7 Kh7 21. h3', date='01/13/2025', name='Best game ever', user_id=3)
        files = [p1]

        for file in files:
            try:
                file.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
