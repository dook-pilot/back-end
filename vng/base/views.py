from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import s3_config
import os
import boto3
import base64
from . import write_uploaded_image
from .models import TargetImage, User
from .data import get_image_public_url, read_metadata, fetch_image_detail, fetch_license_detail, get_image_url
from .store_data import history_database, user_database, image_database, company_database, license_plate_database
from .response_format import invalid_gps, found_company_license, no_company_found
# Create your views here.

@api_view(['POST'])
def upload_data(request):
    file = request.data.get('file')
    if file == None:
        return Response({'status': False, 'message': "MemoryError: Please try with different image"})
    user_id = request.data.get('user_id')
    title = request.data.get('title')
    if user_id == "" or title == "":
        return Response({'status': False, 'message': "No title, No User ID"})
    # SAVING IMAGE INTO LOCAL SYSTEM
    image_name, image_bytes = write_uploaded_image.get_image(file)
    # GET LATITUDE AND LONGITUDE FROM IMAGE
    lng, lat = read_metadata.coordinates(image_name)
    # STORE USER ID IN DATABASE
    uid = user_database.store_user(user_id)
    # GET USER INSTANCE
    user_instance = User.objects.get(uid=uid)
    # STORE IMAGE IN DATABASE AND S3 BUCKET
    image_instance_id = image_database.store_image(
        lng, lat, image_name, title, user_instance)
    # GET IMAGE INSTANCE
    image_instance = TargetImage.objects.get(image_id=image_instance_id)
    # GET IMAGE URL
    image_url = get_image_public_url.get_img_url(image_instance_id)
    # STORE HISTORY DATA
    history_id = history_database.store_history(
        user_instance, image_instance, title, image_url, lng, lat
    )
    os.remove(image_name)
    return Response({"status": True, "message": "Successfully uploaded"})
