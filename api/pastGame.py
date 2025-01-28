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
            try:
                # Step 1: Get JSON data from the request
                data = request.get_json()
                if not data:
                    return {"message": "No data provided in the request body"}, 400
                if 'id' not in data:
                    return {"message": "ID is required in the request body"}, 400

                # Debugging: Log the received data
                print(f"Received data: {data}")

                # Step 2: Fetch the game log by ID
                pastGame_log = pastGame.query.get(data['id'])

                # Debugging: Check if the query returned a result
                if not pastGame_log:
                    print(f"Game Log with ID {data['id']} not found in the database")
                    return {"message": "Game Log not found"}, 404

                print(f"Fetched Game Log: {pastGame_log}")

                # Step 3: Update fields if they are provided in the request
                if 'uid' in data:
                    print(f"Updating UID to: {data['uid']}")
                    pastGame_log._uid = data['uid']
                if 'winner' in data:
                    print(f"Updating Winner to: {data['winner']}")
                    pastGame_log._winner = data['winner']
                if 'elo' in data:
                    print(f"Updating ELO to: {data['elo']}")
                    pastGame_log._elo = data['elo']

                # Step 4: Commit changes to the database
                try:
                    # Assuming your `update` method handles committing changes
                    print("Attempting to update the game log in the database...")
                    pastGame_log.update(data)
                    print("Game log updated successfully")
                    return pastGame_log.read(), 200
                except Exception as e:
                    print(f"Error during database commit: {str(e)}")
                    return {"message": f"Failed to update game log during commit: {str(e)}"}, 500

            except Exception as e:
                # Catch unexpected exceptions and log them
                print(f"Unexpected error occurred: {str(e)}")
                return {"message": f"Unexpected error: {str(e)}"}, 500


        def delete(self):
            """Delete a game log."""
            try:
                # First, try to get UID from query parameters
                game_uid = request.args.get('uid')

                # If UID is not in query parameters, look for it in the request body
                if not game_uid:
                    data = request.get_json()
                    if data and 'uid' in data:
                        game_uid = data['uid']
                    else:
                        return {"message": "Game Log UID is required"}, 400

                # Fetch the game log by UID
                pastGame_log = pastGame.query.filter_by(uid=game_uid).first()
                if not pastGame_log:
                    return {"message": "Game Log not found"}, 404

                # Delete the game log
                pastGame_log.delete()
                return {"message": "Game Log deleted successfully"}, 200

            except Exception as e:
                # Handle unexpected errors
                print(f"Error deleting game log: {str(e)}")
                return {"message": f"Unexpected error: {str(e)}"}, 500




        
        
        def get(self):
            games = pastGame.query.all()
            json_ready = []
            for game in games:
                game_data = game.read()
                json_ready.append(game_data)
            return jsonify(json_ready)
        
# Register the resource
api.add_resource(pastGameAPI._CRUD, '/pastgame')