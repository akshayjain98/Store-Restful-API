from Model.UserModel import UserModel


def authentication(username, password):
    user_detail = UserModel.get_by_email(username)
    return user_detail if user_detail and user_detail.password == password else None


def identity(payload):
    user_id = payload["identity"]
    return UserModel.get_by_id(user_id)
