from db import db


class UserModel(db.Model):
    __tablename__ = "user_tbl"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(255))
    password = db.Column(db.String(16))

    def __init__(self, _id=None, name=None, email=None, password=None):
        self.id = _id
        self.name = name
        self.email = email
        self.password = password

    def json(self):
        return {"user_id": self.id, "name": self.name, "email": self.email, "password": self.password}

    @classmethod
    def get_by_id(cls, user_id):
        try:
            return cls.query().filter_by(id=user_id)
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}

    def register_user(self):
        try:
            # Check user exists or not
            result_user_detail = UserModel.get_by_email(self.email)
            if result_user_detail:
                return {"message": "User already exists", "status": result_user_detail}, 200
            db.session.add(self)
            db.session.commit()
            return {"message": "User registered Success", "status": True, "user_id": result_user_detail}, 200
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}, 500

    @classmethod
    def get_by_email(cls, email):
        try:
            return cls.query.filter_by(email=email).first()
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}
