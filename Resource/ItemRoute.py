from Model.ItemModel import ItemModel
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt import jwt_required


def validate_item_data():
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Please enter valid name")
    parser.add_argument("price", type=float, required=True, help="Please enter valid price")
    parser.add_argument("store_id", type=int, required=True, help="Please enter valid store_id")
    return parser.parse_args()


class ItemRoute(Resource):

    @jwt_required()
    def post(self):
        item_data = validate_item_data()
        item_detail = ItemModel.get_item_by_name(item_data["name"])
        if item_detail:
            return {"message": "Item already exists"}
        item_detail = ItemModel(**item_data)
        return item_detail.save_item()

    @jwt_required()
    def get(self):
        item_model = ItemModel()
        items = item_model.get_items()
        if items:
            return items
        return {"message": "No Record Found"}


class ItemRouteById(Resource):

    @jwt_required()
    def get(self, item_id):
        item_model = ItemModel()
        items = item_model.get_item(item_id)
        if items:
            return items.json(), 200
        return {"message": "No Record Found"}, 204

    @jwt_required()
    def delete(self, item_id):
        item_model = ItemModel.get_item_by_id(item_id)
        if item_model:
            return item_model.delete_item()
        else:
            return {"message": "No Record Found"}

    @jwt_required()
    def put(self, item_id):
        item_model = ItemModel.get_item_by_id(item_id)
        if item_model:
            data = validate_item_data()
            item_model.name = data["name"]
            item_model.price = data["price"]
            item_model.store_id = data["store_id"]
            return item_model.save_item()
        else:
            return {"message": "No Record Found"}
