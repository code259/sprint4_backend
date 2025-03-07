from flask import Blueprint, request, jsonify
from __init__ import db
from model.pastGame import pastGame
from flask_cors import cross_origin

admin_update_api = Blueprint('admin_update_api', __name__, url_prefix='/api/admin')

@admin_update_api.route('/update_user_stats', methods=['PUT'])
@cross_origin()  # Allows CORS for this endpoint
def update_user_stats():
    """
    Update a user's game stats in the past_games table using their numeric user_id.
    Expected JSON payload:
    {
      "user_id": <integer>,   # Numeric ID of the user
      "wins": <integer>,
      "losses": <integer>
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"error": "Missing user_id"}), 400

    # Find the pastGame record using user_id
    record = pastGame.query.filter_by(user_id=user_id).first()
    if not record:
        return jsonify({"error": f"No pastGame record found for user_id '{user_id}'"}), 404

    # Update wins and losses if provided
    if "wins" in data:
        record.number_of_wins = data["wins"]
    if "losses" in data:
        record.number_of_losses = data["losses"]

    try:
        db.session.commit()
        return jsonify({
            "message": "User stats updated successfully",
            "data": record.read()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
