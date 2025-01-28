from flask import Blueprint, request, g, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.pastGame import pastGame
# Blueprint and API
pastGame_api = Blueprint('pastGame_api', __name__, url_prefix='/api')
api = Api(pastGame_api)
class pastGameAPI:
    class _CRUD(Resource):

        def post(self):
            """create the new game entry"""

            data = request.get_json()
            # Validate input
            if not data or 'winner' not in data or 'elo' not in data:
                return {"message": "Game winner and elo are required"}, 400
            # Create a new game log
            new_pastGame_log = pastGame(
                winner=data['winner'],
                elo=data['elo'],
                uid=data['uid']
            )
            created_log = new_pastGame_log.create()
            if created_log:
                return {"message": "Game History logged successfully", "pastGame_log_id": created_log.id}, 201
            return {"message": "Failed to create game history"}, 500
        

        
        def put(self):
            """Update an existing game log."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {"message": "Game Log ID is required"}, 400
            pastGame_log = pastGame.query.get(data['id'])
            updated_log = pastGame_log.update(data)
            return updated_log.read(), 200

        def delete(self):
            """Delete a game log."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {"message": "Game Log ID is required"}, 400
            pastGame_log = pastGame.query.get(data['id'])
            pastGame_log.delete()
            return {"message": "Game Log deleted successfully"}, 200
        
        
        def get(self):
            games = pastGame.query.all()
            json_ready = []
            for game in games:
                game_data = game.read()
                json_ready.append(game_data)
            return jsonify(json_ready)
        
# Register the resource
api.add_resource(pastGameAPI._CRUD, '/pastgame')