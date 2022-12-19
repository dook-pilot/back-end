from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import os, json
from . import write_uploaded_image
from .models import TargetImage, User, History, Company, LicensePlate
from .data import get_image_public_url, read_metadata, download_rdw_s3
from .store_data import history_database, user_database, image_database
from .response_format import no_company_found, found_company_license
# Create your views here.

@api_view(['GET'])
def getHistory(request, user_id):
    history_instance = History.objects.filter(user__uid=user_id).values()
    response = [{'status': True, 'documents': []}]
    for value in history_instance:
        history = History.objects.get(hid=value['hid'])
        image_url = get_image_public_url.get_img_url(value['image_id'])
        history.image_url = image_url
        datetime = str(value['date']) + " at " + str(value['time'])
        response[0]['documents'].append({
            'id': value['image_id'],
            'title': value['title'],
            'image': image_url,
            'datetime': datetime,
            'latitude': value['latitude'],
            'longitude': value['longitude'],
            'isProcessed': value['isProcessed'],
        },)
        history.save()
    return Response(response[0])

@api_view(['POST'])
def upload(request):
    file = request.data.get('file')
    user_id = request.data.get('user_id')
    title = request.data.get('title') if request.data.get('title') is not "" else ""
    if user_id == "":
        return Response({'status': False, 'message': "No User ID"})
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

@api_view(['GET'])
def getData(request, id):
    image = TargetImage.objects.get(image_id=id)
    history = History.objects.get(image=image)
    license_numbers = []
    if history.isProcessed == False:
        return Response({
            'status': False,
            'message': 'Data is processing, try again later.'
        })
    try:
        company = Company.objects.get(target_image=image)
    except:
        company = None
    try:
        license_numbers = LicensePlate.objects.filter(target_image=image)
    except:
        license_numbers = []
    # GET LICENSE NUMBERS
    license_nums = []
    rdw_response = []
    if len(license_numbers) > 0:
        for license_number in license_numbers:
            license_nums.append(license_number.license_number)
            json_filename = license_number.license_number+".json"
            if " " in json_filename:
                json_filename = json_filename.replace(" ", "_")
            # DOWNLOAD RDW JSON FILE
            download_rdw_s3.downloadRdwJson(json_filename)
            # STORE RDW RESPONSE
            j_file = open(json_filename)
            rdw_data = json.load(j_file)
            rdw_response.append(rdw_data)
            j_file.close()
            os.remove(json_filename)
    # GET COMPANY DATA
    if company is not None:
        company_data = {
            "status": False,
            "errMsg": None,
            "place_api_company_name": company.place_api_company_name,
            "bovag_matched_name": company.bovag_matched_name,
            "poitive_reviews": company.poitive_reviews,
            "negative_reviews": company.negative_reviews, 
            "rating": company.rating,
            "duplicate_location": company.duplicate_location,
            "kvk_tradename": company.kvk_tradename,
            "irregularities": company.irregularities,
            "duplicates_found": company.duplicates_found,
            "Bovag_registered": company.Bovag_registered,
            "KVK_found": company.KVK_found,
            "company_ratings": company.company_ratings,
            "license_number": license_nums if len(license_nums) > 0 else None
            }
        return Response(found_company_license.response(company_data, rdw_response))
    else:
        company_data = {"license_number": license_nums}
        return Response(no_company_found.response(company_data, rdw_response))
    
    return Response("DONE")