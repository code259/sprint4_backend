from flask import Flask, jsonify, request
from flask_cors import CORS

# initialize a flask application (app)
app = Flask(__name__)
CORS(app, supports_credentials=True, origins='*')  # Allow all origins (*)

# ... your existing Flask

@app.route('/check-auth')
def check_auth():
    token = request.cookies.get('jwt_python_flask')
    if token:
        return jsonify({'isAuthenticated': True})
    return jsonify({'isAuthenticated': False})

# add an api endpoint to flask app
@app.route('/api/john')
def get_data():
    # start a list, to be used like a information database
    InfoDb = []

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "John",
        "LastName": "Mortensen",
        "DOB": "October 21",
        "Residence": "San Diego",
        "Email": "jmortensen@powayusd.com",
        "Owns_Cars": ["2015-Fusion", "2011-Ranger", "2003-Excursion", "1997-F350", "1969-Cadillac"]
    })

    # add a row to list, an Info record
    InfoDb.append({
        "FirstName": "Shane",
        "LastName": "Lopez",
        "DOB": "February 27",
        "Residence": "San Diego",
        "Email": "slopez@powayusd.com",
        "Owns_Cars": ["2021-Insight"]
    })

    return jsonify(InfoDb)

# class ChessFact(Base):
#     __tablename__ = 'chess_facts'
#     id = Column(Integer, primary_key=True)
#     fact = Column(String, nullable=False)


# # Populate the database with facts if empty
# if not session.query(ChessFact).first():
#     facts = [
#         ChessFact(fact="The longest chess game theoretically possible is 5,949 moves."),
#         ChessFact(fact="The first chessboard with alternating light and dark squares appeared in Europe in 1090."),
#         ChessFact(fact="The word 'checkmate' comes from the Persian phrase 'Shah Mat,' meaning 'the king is helpless.'"),
#         ChessFact(fact="Chess originated in India around the 6th century as a game called 'Chaturanga.'"),
#         ChessFact(fact="The first modern chess tournament was held in London in 1851."),
#         ChessFact(fact="The first world chess champion was Wilhelm Steinitz in 1886."),
#         ChessFact(fact="The shortest possible chess game is called Fool's Mate, which can be achieved in just two moves."),
#         ChessFact(fact="Chess became a part of the Olympic Games in 1924."),
#         ChessFact(fact="The number of possible unique chess games is greater than the number of atoms in the observable universe."),
#         ChessFact(fact="Bobby Fischer, an American chess prodigy, became the youngest U.S. Chess Champion at the age of 14.")
#     ]
#     session.add_all(facts)
#     session.commit()


@app.route('/api/chess/history', methods=['GET'])
def chess_history():
    """Endpoint to provide a brief history of chess."""
    return jsonify({"message": "Chess is a game that dates back over 1,500 years, originating in India. It evolved into its current form in the 15th century in Europe."})

@app.route('/api/chess/random_fact', methods=['GET'])
def random_fact():
    """Endpoint to fetch a random chess fact."""
    fact = session.query(ChessFact).order_by(func.random()).first()
    return jsonify({"fact": fact.fact})

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    # starts flask server on default port, http://127.0.0.1:5001
    app.run(port=5001)