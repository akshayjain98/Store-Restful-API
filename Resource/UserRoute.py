from Model.UserModel import UserModel
from flask_restful import Resource
from flask_restful import reqparse


def validate_user_data():
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Please enter valid name")
    parser.add_argument("email", type=str, required=True, help="Please enter valid email")
    parser.add_argument("password", type=str, required=True, help="Please enter valid password")
    return parser.parse_args()


class UserRoute(Resource):
    def post(self):
        user_detail = validate_user_data()
        user_model = UserModel(**user_detail)
        return user_model.register_user()
