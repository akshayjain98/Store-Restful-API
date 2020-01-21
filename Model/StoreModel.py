from db import db


class StoreModel(db.Model):
    __tablename__ = "store_tbl"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, _id=None, name=None):
        self.id = _id
        self.name = name

    def json(self):
        return {"store_id": self.id, "name": self.name, "items": [item.json() for item in self.items.all()]}

    def save_store(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {"message": "Store detail saved successfully!", "status": True}
        except:
            return {"message": "An error has been occure!", "status": False}

    @classmethod
    def get_by_name(cls, name):
        try:
            store_data = cls.query.filter_by(name=name).first()
            if store_data:
                return store_data
            return None
        except:
            return {"message": "An error has been occure!", "status": False}

    def get_all(self):
        try:
            stores = self.query.all()
            if len(stores):
                return [store.json() for store in stores]
            else:
                return None
        except:
            return {"message": "An error has been occure!", "status": False}

    def delete_store(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return {"message": "Store detail removed successfully!", "status": True}
        except:
            return {"message": "An error has been occure!", "status": False}
