from flask import Blueprint, jsonify
from flask_restful import Api, Resource # used for REST API building
intro_api = Blueprint('intro_api', __name__,
                   url_prefix='/api')
# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(intro_api)
class IntroApi:
    class _Phrases(Resource):
        def get(self):
            prompt_data = {
                "Questions": [
                    "What's your favorite chess opening?",
                    "Do you prefer playing as White or Black?",
                    "How long have you been playing chess?",
                    "What’s the most exciting chess game you’ve ever played?",
                    "Have you ever tried solving chess puzzles?",
                    "Which chess piece do you think is the most powerful and why?",
                    "Do you enjoy fast-paced blitz games or longer, strategic matches?",
                    "What’s your go-to strategy for the endgame?",
                    "Who’s your favorite chess player or grandmaster?",
                    "What’s one chess skill you’d like to improve?"
                ]

            }
            return jsonify(prompt_data)
    # building RESTapi endpoint
    api.add_resource(_Phrases, '/intro/phrases')
