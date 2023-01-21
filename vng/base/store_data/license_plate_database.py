from base.models import LicensePlate
from django.contrib.gis.geos import Point

def store_license_plate(license_number, target_image, lng, lat):
    licensePlate = LicensePlate(target_image=target_image)
    licensePlate.license_number = license_number
    pnt_license = Point(lng, lat)
    licensePlate.geom = pnt_license
    licensePlate.save()
    return license_number