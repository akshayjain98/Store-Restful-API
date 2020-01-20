from db import db


class ItemModel(db.Model):
    __tablename__ = "item_tbl"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey("store_tbl.id"))
    store = db.relationship("StoreModel")

    def __init__(self, _id=None, name=None, price=None, store_id=None):
        self.id = _id
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"id": self.id, "item_name": self.name, "item_price": self.price, "store_id": self.store_id}

    def save_item(self):
        try:
            result_item_detail = self.get_item_by_name(self.name)
            if result_item_detail:
                return {"message": "Item already exists", "status": False}, 200
            db.session.add(self)
            db.session.commit()
            return {"message": "Success", "status": True}, 200
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}, 500

    def get_item(self, item_id):
        try:
            return self.query.filter_by(id=item_id).first()
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}

    def delete_item(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return {"message": "Item removed success", "status": True}, 200
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}, 500

    def get_items(self):
        try:
            items = self.query.all()
            if items:
                return [item.json() for item in items]
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}

    def get_item_by_name(self, name):
        try:
            return self.query.filter_by(name=name).first()
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}, 500

    @classmethod
    def get_item_by_id(cls, id):
        try:
            return cls.query.filter_by(id=id).first()
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}, 500