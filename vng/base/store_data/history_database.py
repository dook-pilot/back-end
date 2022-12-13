from base.models import History
from uuid import uuid4


def store_history(user_instance, image_instance, title, image_url, lng, lat):
    history_id = uuid4()
    history_instance = History(user=user_instance, image=image_instance)
    history_instance.hid = history_id
    history_instance.title = title
    history_instance.image_url = image_url
    history_instance.longitude = lng
    history_instance.latitude = lat
    history_instance.isProcessed = False
    history_instance.save()
    return history_id
