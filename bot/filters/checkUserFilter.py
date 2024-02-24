from config import db


class CheckUserFilter:


    def __call__(self, message) -> bool:
        user_id = str(message.from_user.id)
        return db.check_user_id(user_id)