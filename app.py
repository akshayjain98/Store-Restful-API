import os
from flask import Flask
from Resource.UserRoute import UserRoute, UserByIdRoute, UserLogin
from Resource.ItemRoute import ItemRoute, ItemRouteById
from Resource.StoreRoute import StoreRoute, StoreByNameRoute
from Security.Security import identity, authentication
from flask_jwt_extended import JWTManager
# from Model import CreateTableModel
from flask_restful import Api

app = Flask(__name__)

app.secret_key = "AKSHAYJAIN"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///store.db")
app.config["PROPAGATE_EXCEPTIONS"] = True
# JWT token generation
jwt = JWTManager(app)

# creating database with its table using SQLAlchemy


api = Api(app)


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
