from base.read_exifdata import image_coordinates
from base.write_uploaded_image import get_image

def coordinates(image_name):
    coordinates = image_coordinates(image_name)
    lat = coordinates[0]
    lng = coordinates[1]
    return (lng, lat)