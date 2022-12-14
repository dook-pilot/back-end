from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from . import write_uploaded_image
from .models import TargetImage, User, History
from .data import get_image_public_url, read_metadata
from .store_data import history_database, user_database, image_database
# Create your views here.

@api_view(['GET'])
def getHistory(request, user_id):
    history_instance = History.objects.filter(user__uid=user_id).values()
    response = [{'status': True, 'documents': []}]
    for value in history_instance:
        datetime = str(value['date']) + " at " + str(value['time'])
        response[0]['documents'].append({
            'id': value['image_id'],
            'title': value['title'],
            'image': value['image_url'],
            'datetime': datetime,
            'time': value['time'],
            'latitude': value['latitude'],
            'longitude': value['longitude'],
            'isProcessed': value['isProcessed'],
        },)
    return Response(response)

@api_view(['POST'])
def upload(request):
    file = request.data.get('file')
    user_id = request.data.get('user_id')
    title = request.data.get('title')
    if user_id == "" or title == "":
        return Response({'status': False, 'message': "No title, No User ID"})
    if file == None or file == "":
        return Response({'status': False, 'message': "No File: Upload a file or try with different image."})
    # SAVING IMAGE INTO LOCAL SYSTEM
    image_name, image_bytes = write_uploaded_image.get_image(file)
    # GET LATITUDE AND LONGITUDE FROM IMAGE
    lng, lat = read_metadata.coordinates(image_name)
    # STORE USER ID IN DATABASE
    uid = user_database.store_user(user_id)
    # STORE IMAGE IN DATABASE AND S3 BUCKET
    img_id = image_database.store_image(
        lng, lat, image_name, title, uid)
    if(img_id == TypeError):
        return Response({'status': False, "message": "No GPS Data Found!"})
    # GET IMAGE URL
    image_url = get_image_public_url.get_img_url(img_id)
    # STORE HISTORY DATA
    history_id = history_database.store_history(
        uid, img_id, title, image_url, lng, lat
    )
    os.remove(image_name)
    return Response({"status": True, "message": "Successfully uploaded"})