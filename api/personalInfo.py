from flask import Blueprint, jsonify
from flask_restful import Api, Resource # used for REST API building

student_api = Blueprint('student_api', __name__, url_prefix='/api')

api = Api(student_api)

class StudentAPI:
    class _Nikhil(Resource):
        def get(self):
            data = {'DOB': '01-20-2009', 'Name': 'Nikhil Maturi', 'Favorite Color': 'Black'}
            return jsonify(data)

    class _Mihir(Resource):
        def get(self):
            data = {'DOB': '07-26-2009', 'Name': 'Mihir Thaha', 'Favorite Color': 'Green'}
            return jsonify(data)

    # building RESTapi endpoint
    api.add_resource(_Nikhil, '/student/nikhil')
    api.add_resource(_Mihir, '/student/mihir')