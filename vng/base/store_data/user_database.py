from base.models import User


def store_user(user_id):
    user_instance = User()
    user_instance.uid = user_id
    user_instance.save()
    return user_id
