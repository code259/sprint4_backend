from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from model.personalInfo import personalInfo

student_api = Blueprint('student_api', __name__, url_prefix='/api')

api = Api(student_api)

class StudentAPI:
    class _NikhilM(Resource):
        def get(self):
            data = {'DOB': '01-20-2009', 'Name': 'Nikhil Maturi', 'Favorite Color': 'Black'}
            return jsonify(data)
    class _Mihir(Resource):
        def get(self):
            data = {'DOB': '04-09-2009', 'Name': 'Mihir Thaha', 'Favorite Color': 'Purple'}
            return jsonify(data)

    class _Aarush(Resource):
        def get(self):
            data = {'DOB': '04-09-2009', 'Name': 'Aarush Gowda', 'Favorite Color': 'Grey'}
            return jsonify(data)
    class _Vasanth(Resource):
        def get(self):
            data = {'DOB': '06-27-2009', 'Name': 'Vasanth Rajasekaran', 'Favorite Color': 'Black'}
            return jsonify(data)

    class _NikhilN(Resource):
        def get(self):
            data = {'DOB': '05-16-2009', 'Name': 'Nikhil Narayan', 'Favorite Color': 'Blue'}
            return jsonify(data)
        
    class _Jowan(Resource):
        def get(self):
            data = {'DOB': '07-02-2008', 'Name': 'Jowan Elzein', 'Favorite Color': 'Purple'}
            return jsonify(data)

    class _BULK_STATIC(Resource):
        def get(self):
            data = {'Nikhilm': {'DOB': '01-20-2009', 'Name': 'Nikhil Maturi', 'Favorite Color': 'Black'}, 'Mihir': {'DOB': '04-09-2009', 'Name': 'Mihir Thaha', 'Favorite Color': 'Purple'}, 'Nikhiln': {'DOB': '05-16-2009', 'Name': 'Nikhil Narayan', 'Favorite Color': 'Blue'}, 'Aarush': {'DOB': '04-09-2009', 'Name': 'Aarush Gowda', 'Favorite Color': 'Grey'}, 'Vasanth': {'DOB': '06-27-2009', 'Name': 'Vasanth Rajasekaran', 'Favorite Color': 'Black'}, 'Jowan': {'DOB': '07-02-2008', 'Name': 'Jowan Elzein', 'Favorite Color': 'Purple'}}
            return jsonify(data)

    class _BULK_DYNAMIC(Resource):
        def get(self):
            infos = personalInfo.query.all()
            json_ready = []
            for info in infos:
                info_data = info.read()
                json_ready.append(info_data)
            return jsonify(json_ready)

    api.add_resource(_NikhilM, '/student/nikhilm')
    api.add_resource(_Mihir, '/student/mihir')
    api.add_resource(_Aarush, '/student/aarush')
    api.add_resource(_NikhilN, '/student/nikhiln')
    api.add_resource(_Jowan, '/student/jowan')
    api.add_resource(_Vasanth, '/student/vasanth')
    api.add_resource(_BULK_STATIC, '/student/bulk_static')
    api.add_resource(_BULK_DYNAMIC, '/student/bulk_dynamic')
