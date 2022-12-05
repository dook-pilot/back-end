from base.models import TargetImage
from django.contrib.gis.geos import Point
from django.core.files import File
from uuid import uuid4

def store_image(lng, lat, image_name):
    image_id = uuid4()
    targetImage = TargetImage()
    targetImage.image_id = image_id
    targetImage.image = File(file=open(image_name, 'rb'), name=image_name)
    targetImage.image_name = image_name
    print(lng, lat)
    try:
        point_image = Point(lng, lat)
        targetImage.geom = point_image
    except TypeError:
        return TypeError
    targetImage.save()
    return image_id

