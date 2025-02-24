from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import db
from model.skill import Skill
from api.jwt_authorize import token_required

# Create Blueprint and API for Skills
skill_api = Blueprint('skill_api', __name__, url_prefix='/api')
api = Api(skill_api)

class SkillAPI:
    class _CRUD(Resource):
        # need to prohibit posting unless logged in somehow...
        def post(self):
            """
            Create a new skill entry.
            """
            data = request.get_json()

            # Validate required fields
            if not data or 'skill_name' not in data or 'skill_level' not in data or 'user_id' not in data:
                return {'message': 'Skill Name, Level, and User ID are required.'}, 400

            # Create a new skill
            skill = Skill(
                skill_name=data.get('skill_name'),
                skill_level=data.get('skill_level'),
                user_id=data.get('user_id')
            )
            try:
                skill.create()
                return jsonify(skill.read())
            except Exception as e:
                return {'message': f'Error saving skill: {e}'}, 500

        @token_required()
        def get(self):
            """
            Retrieve a skill by ID or all skills.
            """
            # skill_id = request.args.get('id')
            current_user = g.current_user
            print(current_user)
            print("user_id", current_user.id)

            # # Fetch a specific skill if ID is provided
            # if skill_id:
            #     skill = Skill.query.get(skill_id)
            #     if not skill:
            #         return {'message': 'Skill not found'}, 404
            #     return jsonify(skill.read())

            # Fetch all skills
            # all_skills = Skill.query.all()
            all_skills = Skill.query.filter_by(_user_id=current_user.id).all()
            return jsonify([skill.read() for skill in all_skills])

        def put(self):
            """
            Update an existing skill entry.
            """
            data = request.get_json()

            # Validate required fields
            if not data or 'id' not in data:
                return {'message': 'ID is required for updating a skill'}, 400

            # Find the skill by ID
            skill = Skill.query.get(data['id'])
            if not skill:
                return {'message': 'Skill not found'}, 404

            # Update the skill
            try:
                if 'skill_name' in data:
                    skill._skill_name = data['skill_name']
                if 'skill_level' in data:
                    skill._skill_level = data['skill_level']
                if 'user_id' in data:
                    skill._user_id = data['user_id']
                skill.create()  # Save changes
                return jsonify(skill.read())
            except Exception as e:
                return {'message': f'Error updating skill: {e}'}, 500

        def delete(self):
            """
            Delete a skill entry.
            """
            data = request.get_json()

            # Validate required fields
            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting a skill'}, 400

            # Find the skill by ID
            skill = Skill.query.get(data['id'])
            if not skill:
                return {'message': 'Skill not found'}, 404

            # Delete the skill
            try:
                skill.delete()
                return {'message': 'Skill deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting skill: {e}'}, 500

    # Add the CRUD Resource to the API
    api.add_resource(_CRUD, '/skill')
