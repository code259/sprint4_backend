# imports from flask
import json
import os
from urllib.parse import urljoin, urlparse
from flask import abort, redirect, render_template, request, send_from_directory, url_for, jsonify  # import render_template from "public" flask libraries
from flask_login import current_user, login_user, logout_user
from flask.cli import AppGroup
from flask_login import current_user, login_required
from flask import current_app
from werkzeug.security import generate_password_hash
import shutil
from stockfish import Stockfish
import platform
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func



# import "objects" from "this" project
from __init__ import app, db, login_manager  # Key Flask objects 
# API endpoints
from api.user import user_api 
from api.pfp import pfp_api
from api.nestImg import nestImg_api # Justin added this, custom format for his website
from api.post import post_api
from api.channel import channel_api
from api.group import group_api
from api.section import section_api
from api.nestPost import nestPost_api # Justin added this, custom format for his website
from api.messages_api import messages_api # Adi added this, messages for his website
from api.carphoto import car_api
from api.carChat import car_chat_api
from api.personalInfo import student_api
from api.intro import intro_api
from api.vote import vote_api
# database Initialization functions
from model.carChat import CarChat
from model.user import User, initUsers
from model.section import Section, initSections
from model.group import Group, initGroups
from model.channel import Channel, initChannels
from model.post import Post, initPosts
from model.nestPost import NestPost, initNestPosts # Justin added this, custom format for his website
from model.vote import Vote, initVotes
# server only Views

# register URIs for api endpoints
app.register_blueprint(messages_api) # Adi added this, messages for his website
app.register_blueprint(user_api)
app.register_blueprint(pfp_api)
app.register_blueprint(post_api)
app.register_blueprint(channel_api)
app.register_blueprint(group_api)
app.register_blueprint(section_api)
app.register_blueprint(car_chat_api)
# Added new files to create nestPosts, uses a different format than Mortensen and didn't want to touch his junk
app.register_blueprint(nestPost_api)
app.register_blueprint(nestImg_api)
app.register_blueprint(vote_api)
app.register_blueprint(car_api)
app.register_blueprint(student_api)
app.register_blueprint(intro_api)
# Tell Flask-Login the view function name of your login route
login_manager.login_view = "login"

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login', next=request.path))

# register URIs for server pages
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Helper function to check if the URL is safe for redirects
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    next_page = request.args.get('next', '') or request.form.get('next', '')
    if request.method == 'POST':
        user = User.query.filter_by(_uid=request.form['username']).first()
        if user and user.is_password(request.form['password']):
            login_user(user)
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page or url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template("login.html", error=error, next=next_page)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    print("Home:", current_user)
    return render_template("index.html")


@app.route('/get-move', methods=["POST"])
def get_move():
    data = request.get_json()
    fen = data["fen"]
    elo = data.get("elo", 1200)
    print("this is the elo requested", elo)

    system = platform.system()

    if system == "Darwin":
        stockfish_path = "./stockfish"
    elif system == "Windows":
        stockfish_path = "./stockfish-windows.exe"
    else:
        pass

    stockfish = Stockfish(stockfish_path)
    stockfish.set_fen_position(fen)
    stockfish.set_elo_rating(elo)
    best_move = stockfish.get_best_move()
    return jsonify({"move": best_move}), 200



Base = declarative_base()
class ChessFact(Base):
    __tablename__ = 'chess_facts'
    id = Column(Integer, primary_key=True)
    fact = Column(String, nullable=False)

engine = create_engine('sqlite:///chess_facts.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# Populate the database with facts if empty
if not session.query(ChessFact).first():
    facts = [
        ChessFact(fact="The longest chess game theoretically possible is 5,949 moves."),
        ChessFact(fact="The first chessboard with alternating light and dark squares appeared in Europe in 1090."),
        ChessFact(fact="The word 'checkmate' comes from the Persian phrase 'Shah Mat,' meaning 'the king is helpless.'"),
        ChessFact(fact="Chess originated in India around the 6th century as a game called 'Chaturanga.'"),
        ChessFact(fact="The first modern chess tournament was held in London in 1851."),
        ChessFact(fact="The first world chess champion was Wilhelm Steinitz in 1886."),
        ChessFact(fact="The shortest possible chess game is called Fool's Mate, which can be achieved in just two moves."),
        ChessFact(fact="Chess became a part of the Olympic Games in 1924."),
        ChessFact(fact="The number of possible unique chess games is greater than the number of atoms in the observable universe."),
        ChessFact(fact="Bobby Fischer, an American chess prodigy, became the youngest U.S. Chess Champion at the age of 14.")
    ]
    session.add_all(facts)
    session.commit()


@app.route('/api/chess/history', methods=['GET'])
def chess_history():
    """Endpoint to provide a brief history of chess."""
    return jsonify({"message": "Chess is a game that dates back over 1,500 years, originating in India. It evolved into its current form in the 15th century in Europe."})

@app.route('/api/chess/random_fact', methods=['GET'])
def random_fact():
    """Endpoint to fetch a random chess fact."""
    fact = session.query(ChessFact).order_by(func.random()).first()
    return jsonify({"fact": fact.fact})


@app.route('/test', methods=["POST"])
def test():
    return jsonify({"message": "Test successful"}), 200

@app.route('/analyze-move', methods=["POST"])
def analyze_move():
    data = request.get_json()
    fen = data["fen"]
    last_eval = data.get("last_evaluation", 0.0) #must be sent by client, and is the evaluation after previous move

    system = platform.system()

    if system == "Darwin":
        stockfish_path = "./stockfish"
    elif system == "Windows":
        stockfish_path = "./stockfish-windows.exe"
    else:
        pass

    stockfish = Stockfish(stockfish_path)
    stockfish.set_fen_position(fen)
    evaluation = stockfish.get_evaluation()
    evaluation = evaluation['value'] / 100.0 #converting from centipawns to pawns

    status = ""
    if evaluation - last_eval > 1.0:
        status = "Brilliant"
    if evaluation - last_eval > 0.5:
        status = "Excellent"
    if evaluation - last_eval > 0:
        status = "Good"
    if evaluation - last_eval < -0.5:
        status = "Inaccurate"
    if evaluation - last_eval < -1.0:
        status = "Mistake"
    if evaluation - last_eval < -3.0:
        status = "Blunder"
    else:
        status = "Neutral"

    best_move = stockfish.get_best_move()
    return jsonify({"evaluation": evaluation, "best move": best_move, "status": status}), 200

@app.route('/check-auth')
def check_auth():
    token = request.cookies.get('jwt_python_flask')
    if token:
        return jsonify({'isAuthenticated': True})
    return jsonify({'isAuthenticated': False})

@app.route('/users/table')
@login_required
def utable():
    users = User.query.all()
    return render_template("utable.html", user_data=users)

@app.route('/users/table2')
@login_required
def u2table():
    users = User.query.all()
    return render_template("u2table.html", user_data=users)

# Helper function to extract uploads for a user (ie PFP image)
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@app.route('/users/delete/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.delete()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/reset_password/<int:user_id>', methods=['GET'])
@login_required
def reset_password(user_id):
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Set the new password
    if user.update({"password": app.config['DEFAULT_PASSWORD']}):
        return jsonify({'message': 'Password reset successfully'}), 200
    return jsonify({'error': 'Password reset failed'}), 500

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to run the data generation functions
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initSections()
    initGroups()
    initChannels()
    initPosts()
    initNestPosts()
    initVotes()
    
# Backup the old database
def backup_database(db_uri, backup_uri):
    """Backup the current database."""
    if backup_uri:
        db_path = db_uri.replace('sqlite:///', 'instance/')
        backup_path = backup_uri.replace('sqlite:///', 'instance/')
        shutil.copyfile(db_path, backup_path)
        print(f"Database backed up to {backup_path}")
    else:
        print("Backup not supported for production database.")

# Extract data from the existing database
def extract_data():
    data = {}
    with app.app_context():
        data['users'] = [user.read() for user in User.query.all()]
        data['sections'] = [section.read() for section in Section.query.all()]
        data['groups'] = [group.read() for group in Group.query.all()]
        data['channels'] = [channel.read() for channel in Channel.query.all()]
        data['posts'] = [post.read() for post in Post.query.all()]
    return data

# Save extracted data to JSON files
def save_data_to_json(data, directory='backup'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for table, records in data.items():
        with open(os.path.join(directory, f'{table}.json'), 'w') as f:
            json.dump(records, f)
    print(f"Data backed up to {directory} directory.")

# Load data from JSON files
def load_data_from_json(directory='backup'):
    data = {}
    for table in ['users', 'sections', 'groups', 'channels', 'posts']:
        with open(os.path.join(directory, f'{table}.json'), 'r') as f:
            data[table] = json.load(f)
    return data

# Restore data to the new database
def restore_data(data):
    with app.app_context():
        users = User.restore(data['users'])
        _ = Section.restore(data['sections'])
        _ = Group.restore(data['groups'], users)
        _ = Channel.restore(data['channels'])
        _ = Post.restore(data['posts'])
    print("Data restored to the new database.")

# Define a command to backup data
@custom_cli.command('backup_data')
def backup_data():
    data = extract_data()
    save_data_to_json(data)
    backup_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_BACKUP_URI'])

# Define a command to restore data
@custom_cli.command('restore_data')
def restore_data_command():
    data = load_data_from_json()
    restore_data(data)

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# this runs the flask application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="9000")
