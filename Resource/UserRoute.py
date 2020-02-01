from Model.UserModel import UserModel
from flask_restful import Resource
from flask_restful import reqparse
# from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_claims
from Blacklist.blacklist import BLACKLIST
from flask_jwt_extended import *


def validate_user_data():
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Please enter valid name")
    parser.add_argument("email", type=str, required=True, help="Please enter valid email")
    parser.add_argument("password", type=str, help="Please enter valid password")
    parser.add_argument("role", type=str, help="Please enter valid role")
    return parser.parse_args()


def validate_login_detail():
    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str, required=True, help="Please enter valid email")
    parser.add_argument("password", type=str, required=True, help="Please enter valid password")
    return parser.parse_args()


class UserRoute(Resource):
    def post(self):
        user_detail = validate_user_data()
        if UserModel.get_by_email(user_detail["email"]):
            return {"message": "User detail already exists!", "status": False}
        user_model = UserModel(**user_detail)
        return user_model.save_user()

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Un-authorized"}, 401
        user_model = UserModel()
        user_details = user_model.get_all()
        if user_details:
            return {"message": user_details}
        else:
            return {"message": "No Record Found"}


class UserByIdRoute(Resource):
    @jwt_required
    def get(self, user_id):
        user_data = UserModel.get_by_id(user_id)
        if user_data:
            return {"message": user_data.json()}
        else:
            return {"message": "No Record Found"}

    @jwt_required
    def put(self, user_id):
        user_detail = UserModel.get_by_id(user_id)
        if user_detail:
            user_data = validate_user_data()
            user_detail.name = user_data["name"]
            user_detail.email = user_data["email"]
            return user_detail.save_user()
        else:
            return {"message": "No Record Found"}

    @jwt_required
    def delete(self, user_id):
        user_detail = UserModel.get_by_id(user_id)
        if user_detail:
            return user_detail.delete_user()
        else:
            return {"message": "No Record Found"}


class UserLogin(Resource):
    def post(self):
        user_data = validate_login_detail()
        user_credential = UserModel.get_by_email(user_data["email"])
        if user_credential:
            if user_credential.password == user_data["password"]:
                access_token = create_access_token(identity={"id": user_credential.id, "role": user_credential.role},
                                                   fresh=True)
                refresh_token = create_refresh_token(identity={"id": user_credential.id, "role": user_credential.role})
                return {"access_token": access_token, "refresh_token": refresh_token}
        else:
            return {"message": "Invalid Credential"}


class UserLogout(Resource):
    @jwt_required
    def post(self):
        token_id = get_raw_jwt()["jti"]  # This method will return the JWT unique id
        BLACKLIST.add(token_id)
        return {"message": "User logout success"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(current_user, fresh=False)
        return {"access_token": new_token}
