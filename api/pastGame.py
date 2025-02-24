from flask import Blueprint, request, g, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.pastGame import pastGame
import requests
from model.user import User

# Blueprint and API
pastGame_api = Blueprint('pastGame_api', __name__, url_prefix='/api')
api = Api(pastGame_api)

class pastGameAPI:
    class _CRUD(Resource):

        def post(self):
            """Create a new game entry"""
            data = request.get_json()
            if not data or 'user_id' not in data or 'number_of_wins' not in data or 'number_of_losses' not in data:
                return {"message": "User ID, User Name, Number of Wins, and Number of Losses are required"}, 400

            new_pastGame_log = pastGame(
                user_id=data['user_id'],
                number_of_wins=data['number_of_wins'],
                number_of_losses=data['number_of_losses']
            )
            created_log = new_pastGame_log.create()
            if created_log:
                return {"message": "Game History logged successfully", "pastGame_log_id": created_log.id}, 201
            return {"message": "Failed to create game history"}, 500

        def put(self):
            """Update an existing game log."""
            try:
                data = request.get_json()
                if not data or 'id' not in data:
                    return {"message": "ID is required in the request body"}, 400
                
                pastGame_log = pastGame.query.get(data['id'])
                if not pastGame_log:
                    return {"message": "Game Log not found"}, 404

                pastGame_log.update(data)
                return pastGame_log.read(), 200
            except Exception as e:
                return {"message": f"Unexpected error: {str(e)}"}, 500

        def delete(self):
            """Delete a game log by User ID."""
            try:
                data = request.get_json()
                if not data or "user_id" not in data:
                    return {"message": "User ID is required"}, 400

                game_log = pastGame.query.filter_by(user_id=data["user_id"]).first()
                if not game_log:
                    return {"message": "Game Log not found"}, 404

                game_log.delete()
                return {"message": "Game Log deleted successfully"}, 200
            except Exception as e:
                return {"message": f"Unexpected error: {str(e)}"}, 500
            

        # def get_user_name(self, user_id):
        #     """Fetch user name based on the user_id"""
        #     try:
        #         # Fetch all users from the API
                

        #         current_user = g.current_user
        #         print(current_user)

        #         # Find the user by the user_id
        #         user = next((user for user in users if user['user_id'] == user_id), None)
        #         if not user:
        #             return {"message": "User not found"}, 404
                
                
        #         # Return the name of the user
        #         return user['name'], 200
        #     except Exception as e:
        #         return {"message": f"Unexpected error: {str(e)}"}, 500
    

        def get(self):
            """Get all past game records with user names"""
            games = pastGame.query.all()
            json_ready = []
            for game in games:
                game_data = game.read()

                # Fetch the user associated with the game
                user = User.query.filter_by(id=game_data['user_id']).first()
                if user:
                    # Add user_name to the game data
                    game_data['user_name'] = user.name
                else:
                    game_data['user_name'] = "Unknown"  # Fallback if user is not found

                json_ready.append(game_data)

            return jsonify(json_ready)

# Register the resource
api.add_resource(pastGameAPI._CRUD, '/pastgame')
