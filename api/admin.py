from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from model.userstats import UserStats
from model.user import User

data_api = Blueprint('data_api', __name__, url_prefix='/api')
api = Api(data_api)

class _GetUserStats(Resource):
    def get(self, user_id):
        user_stats = UserStats.query.filter_by(user_id=user_id).first()
        if not user_stats:
            return {'error': 'User not found'}, 404
        
        return jsonify(user_stats.read()), 200  # Now returns "name"


class UserStatsAPI:
    class _UpdateScore(Resource):
        def post(self):
            data = request.get_json()
            name = data.get('name')
            result = data.get('result')

            if not name or result not in ['win', 'loss']:
                return jsonify({'error': 'Valid Name and result (win/loss) are required'}), 400

            user = User.query.filter_by(_name=name).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404

            user_stats = UserStats.query.filter_by(user_id=user.id).first()
            if not user_stats:
                return jsonify({'error': 'User stats not found'}), 404

            try:
                if result == 'win':
                    user_stats.wins += 1
                else:
                    user_stats.losses += 1

                user_stats.update()
                return jsonify({'message': 'User stats updated successfully', 'data': user_stats.read()}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    class _AdminUser(Resource):
        def patch(self):
            data = request.get_json()
            name = data.get('name')
            wins = data.get('wins')
            losses = data.get('losses')

            if not name:
                return jsonify({'error': 'Name is required'}), 400

            user = User.query.filter_by(_name=name).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404

            user_stats = UserStats.query.filter_by(user_id=user.id).first()
            if not user_stats:
                return jsonify({'error': 'User stats not found'}), 404

            if wins is not None:
                user_stats.wins = wins
            if losses is not None:
                user_stats.losses = losses

            try:
                user_stats.update()
                return jsonify({'message': 'User stats updated successfully', 'data': user_stats.read()}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    class _GetUserStats(Resource):
        def get(self, name):
            user = User.query.filter_by(_name=name).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404

            user_stats = UserStats.query.filter_by(user_id=user.id).first()
            if not user_stats:
                return jsonify({'error': 'User stats not found'}), 404

            return jsonify(user_stats.read()), 200

api.add_resource(UserStatsAPI._UpdateScore, '/user_stats/update_score')
api.add_resource(UserStatsAPI._AdminUser, '/admin/user')
api.add_resource(UserStatsAPI._GetUserStats, '/user_stats/<string:name>')
