from base.models import History, User, TargetImage
from uuid import uuid4


def store_history(uid, img_id, title, image_url, lng, lat):
    history_id = uuid4()
    user = User.objects.get(uid=uid)
    image = TargetImage(image_id=img_id)
    history_instance = History(user=user, image=image)
    history_instance.hid = history_id
    history_instance.title = title
    history_instance.image_url = image_url
    history_instance.longitude = lng
    history_instance.latitude = lat
    history_instance.isProcessed = False
    history_instance.save()
    return history_id
