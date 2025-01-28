from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db
from model.evaluation import Evaluation

evaluation_api = Blueprint('evaluation_api', __name__, url_prefix='/api')

api = Api(evaluation_api)

class EvaluationAPI:

    class _CRUD(Resource):
        def post(self):
            data = request.get_json()
            if not data or 'evaluation' not in data or 'move' not in data or 'move_number' not in data:
                return {'message': 'Move data is required.'}, 400

            evaluation = Evaluation(
                evaluation=data.get('evaluation'),
                move=data.get('move'),
                move_number=data.get('move_number')
            )

            try:
                evaluation.create()
                return jsonify(evaluation.read()), 201
            except Exception as e:
                return {'message': f'Error saving evaluation: {e}'}, 500

        def get(self):
            all_evaluations = Evaluation.query.all()
            return jsonify([evaluation.read() for evaluation in all_evaluations])

        def put(self):
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'ID is required to update the evaluation'}, 400

            evaluation = Evaluation.query.get(data['id'])
            if not evaluation:
                return {'message': 'Evaluation not found'}, 404

            try:
                # Update move as played
                evaluation.update(data)
                return jsonify(evaluation.read())
            except Exception as e:
                return {'message': f'Error updating evaluation: {e}'}, 500

        def delete(self):
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'ID is required for deletion'}, 400

            evaluation = Evaluation.query.get(data['id'])
            if not evaluation:
                return {'message': 'Evaluation not found'}, 404

            try:
                evaluation.delete()
                return {'message': 'Evaluation deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting evaluation: {e}'}, 500

    api.add_resource(_CRUD, '/evaluation')
