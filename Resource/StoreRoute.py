from Model.StoreModel import StoreModel
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required


def validate_store_detail():
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Please enter valid name")
    return parser.parse_args()


class StoreRoute(Resource):
    @jwt_required
    def get(self):
        store_model = StoreModel()
        result_store_detail = store_model.get_all()
        return {"store": result_store_detail, "status": True} if result_store_detail else {"message": "No Record Found",
                                                                                           "status": False}

    @jwt_required
    def post(self):
        store_data = validate_store_detail()
        result_store_detail = StoreModel.get_by_name(store_data["name"])
        if result_store_detail:
            return {"message": "Store detail already exists!", "status": False}
        store_model = StoreModel(**store_data)
        return store_model.save_store()


class StoreByNameRoute(Resource):
    @jwt_required
    def get(self, name):
        result_store_detail = StoreModel.get_by_name(name)
        return {"store": result_store_detail, "status": True} if result_store_detail else {"message": "No Record Found",
                                                                                           "status": False}

    @jwt_required
    def delete(self, name):
        result_store_detail = StoreModel.get_by_name(name)
        return result_store_detail.delete_store() if result_store_detail else {"message": "No Record Found",
                                                                               "status": False}

    @jwt_required
    def put(self, name):
        store_model = StoreModel.get_by_name(name)
        if store_model:
            store_data = validate_store_detail()
            store_model.name = store_data["name"]
            return store_model.save_store()
        else:
            return {"message": "No Record Found"}
