from db import db


class UserModel(db.Model):
    __tablename__ = "user_tbl"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(255))
    password = db.Column(db.String(16))
    role = db.Column(db.String(1))

    def __init__(self, _id=None, name=None, email=None, password=None, role=None):
        self.id = _id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "password": self.password, "role": self.role}

    @classmethod
    def get_by_id(cls, user_id):
        try:
            return cls.query.filter_by(id=user_id).first()
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}

    def save_user(self):
        try:
            db.session.add(self)
            db.session.commit()
            return {"message": "User detail saved", "status": True}, 200
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}, 500

    @classmethod
    def get_by_email(cls, email):
        try:
            return cls.query.filter_by(email=email).first()
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}

    def delete_user(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return {"message": "User detail removed", "status": True}, 200
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}

    def get_all(self):
        try:
            user_details = self.query.all()
            if user_details:
                return [user.json() for user in user_details]
        except:
            return {"error": "An error has been occur, Please restart it again!", "status": False}
