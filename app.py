import os
from flask import Flask, jsonify
from Resource.UserRoute import UserRoute, UserByIdRoute, UserLogin, TokenRefresh, UserLogout
from Resource.ItemRoute import ItemRoute, ItemRouteById
from Resource.StoreRoute import StoreRoute, StoreByNameRoute
from Security.Security import identity, authentication
# from flask_jwt_extended import JWTManager
from Blacklist.blacklist import BLACKLIST
from flask_jwt_extended import *
from flask_restful import Api

app = Flask(__name__)

app.secret_key = "AKSHAYJAIN"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///store.db")
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECK"] = {"access", "refresh"}

# JWT token generation
jwt = JWTManager(app)

# creating database with its table using SQLAlchemy


api = Api(app)


@jwt.revoked_token_loader
def revoked_token():
    return jsonify({
        "description": "This token is already revoked"
    }), 401


@jwt.needs_fresh_token_loader
def fresh_token_required():
    return jsonify({
        "description": "You required fresh token to perform task"
    }), 401


@jwt.expired_token_loader
def expired_token():
    return jsonify({
        "description": "TYour token is expired please re-generate token"
    }), 401


@jwt.invalid_token_loader
def invalid_token(error):
    return jsonify({
        "description": "Please enter valid token",
        "error": error
    }), 401


@jwt.unauthorized_loader
def unauthorized(error):
    return jsonify({
        "description": "You are not authorised to access this",
        "error": error
    }), 401


@jwt.token_in_blacklist_loader
def block_blacklisted_token(decrypted_data):
    # This will use when we want to block the user ID
    # return decrypted_data["identity"]["id"] in BLACKLIST

    return decrypted_data["jti"] in BLACKLIST



@app.before_first_request
def create_tables():
    db.create_all()


@jwt.user_claims_loader
def add_more_claims(identity):
    if identity["role"] == "a":
        return {"is_admin": True}
    return {"is_admin": False}


# Calling User Route
api.add_resource(UserRoute, "/user")
api.add_resource(UserByIdRoute, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

# Calling Item Route
api.add_resource(ItemRoute, "/item")
api.add_resource(ItemRouteById, "/item/<item_id>")

# Calling Store Route
api.add_resource(StoreRoute, "/store")
api.add_resource(StoreByNameRoute, "/store/<name>")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    # Server running at default port 5000
    app.run(debug=True)
