from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from model.pgn import Pgn

pgn_api = Blueprint('pgn_api', __name__, url_prefix='/api')

api = Api(pgn_api)

### TODO: Implement on the Game Page after the game is finished to save the game.

class PgnAPI:
    class _BULK_CRUD(Resource):
        def get(self):
            pgns = Pgn.query.all()
            json_ready = []
            for pgn in pgns:
                pgn_data = pgn.read()
                json_ready.append(pgn_data)
            return jsonify(json_ready)

    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            body_pgn = body['pgn']
            body_name = body['name']
            body_id = body['user_id']

            ### TODO: Add error handling error for various input fields

            pgn_obj = Pgn(pgn=body['pgn'], date=body['date'], name=body['name'], user_id=body['user_id'])
            pgn_obj.create()
            # if not pgn:  # failure returns error message
            #     return {'message': f'Processed {body_pgn}, either a format error or User ID {body_id} is duplicate'}, 400

            return jsonify(pgn_obj.read())

        def delete(self):
            body = request.get_json()
            pgn = Pgn.query.get(body['id'])
            if not pgn:
                return {'message': 'Pgn not found'}, 404
            pgn.delete()
            return jsonify({"message": "pgn deleted"})

        def patch(self):
            body = request.get_json()
            pgn = Pgn.query.get(body['id'])
            if pgn is None:
                return {'message': 'Pgn not found'}, 404

            if 'name' in body:
                pgn._name = body['name']

            pgn.patch()
            return jsonify(pgn.read())

    api.add_resource(_BULK_CRUD, '/pgns')
    api.add_resource(_CRUD, '/pgn')