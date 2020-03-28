from flask import Flask
from flask_restful import Api, Resource
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import reqparse


app = Flask(__name__)
api = Api(app)
limiter = Limiter(app=app, key_func=get_remote_address)
limiter.init_app(app=app)

parser = reqparse.RequestParser()
parser.add_argument('zipcode_arg', type=str, required=True, help="Please enter Zipcode")
parser.add_argument('city_arg', type=str, required=True, help="Please enter city")


class MyAPI(Resource):
    """ This is main class """

    def __init__(self):
        self.__zipcode = parser.parse_args().get('zipcode_arg', 'None')
        self.__city = parser.parse_args().get('city_arg', 'None')

    decorators = [limiter.limit("10/day")]

    def get(self):
        """ Gets the zipcode or city """
        if len(self.__zipcode) > 7 and self.__city != "":
            return{
                "response": 200,
                "result": True,
                "data": parser.parse_args()
            }


api.add_resource(MyAPI, '/weather')  # http://127.0.0.1:8001/weather

if __name__ == '__main__':
    app.run(port=8001, debug=True)
