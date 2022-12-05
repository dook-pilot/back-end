from base.models import LicensePlate
from django.contrib.gis.geos import Point
from uuid import uuid4

def store_license_plate(license_number, target_image, lng, lat):
    license_id = uuid4()
    licensePlate = LicensePlate(target_image=target_image)
    licensePlate.license_number = license_number
    licensePlate.license_plate_id = license_id
    pnt_license = Point(lng, lat)
    licensePlate.geom = pnt_license
    licensePlate.save()
    return license_id