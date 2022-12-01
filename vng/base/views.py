from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import s3_config
import os, boto3, base64
from . import write_uploaded_image
from .models import TargetImage
from .data import read_metadata, fetch_image_detail, fetch_license_detail, get_image_url
from .store_data import image_database, company_database, license_plate_database
from .response_format import invalid_gps, found_company_license, no_company_found
# Create your views here.

@api_view(['POST'])
def vngp1_predict_license_plate(request):
    file = request.data.get('file')
    print(file)
    if file == None:
        return Response({'error': "MemoryError: Please try with different image"})
    # SAVING IMAGE INTO LOCAL SYSTEM
    image_name, image_bytes = write_uploaded_image.get_image(file)
    # GET LATITUDE AND LONGITUDE FROM IMAGE
    lng, lat = read_metadata.coordinates(image_name)
    # GET IMAGE SCRAPED DATA
    license_plate_company_data = fetch_image_detail.company_license_data(image_bytes)
    # STORE IMAGE IN DATABASE AND S3 BUCKET
    image_instance_id = image_database.store_image(lng, lat, image_name)
    if image_instance_id == TypeError:
        return Response(invalid_gps.response())
    # FOREIGN KEY TARGET IMAGE
    foreign_key = TargetImage.objects.get(image_id=image_instance_id)
    # STORE COMPANY DETAILS IN DATABASE
    if license_plate_company_data['error'] == 'false':
        company_instance_id = company_database.store_company(lng, lat, foreign_key, license_plate_company_data)
    # STORE LICENSE NUMBERS IN DATABASE
    if len(license_plate_company_data['license_number']) > 0:
        for license_number in license_plate_company_data['license_number']:
            license_instance_id = license_plate_database.store_license_plate(license_number, foreign_key, lng, lat)
    os.remove(image_name)
    # PREPARE RESPONSE
    image_url = get_image_url.image_url(image_instance_id)
    rdw_scraped_response, json_file_urls = fetch_license_detail.license_detail(license_plate_company_data)
    if license_plate_company_data['error'] == 'false':
        return Response(found_company_license.response(json_file_urls, license_plate_company_data, rdw_scraped_response, image_url))
    else:
        return Response(no_company_found.response(license_plate_company_data, json_file_urls, rdw_scraped_response, image_url))
    
# get image file from s3
@api_view(['POST'])
def get_image(request):
    image_url = request.data.get('image_url')
    image_name = image_url.split('/', -1)[-1]
    s3 = boto3.client('s3', aws_access_key_id=s3_config.config["ACCESS_KEY"] , aws_secret_access_key=s3_config.config["SECRET_KEY"])
    bucket = s3_config.config["BUCKET"]
    try:
        s3.download_file(bucket,'media/'+str(image_name),image_name)
        with open(image_name, "rb") as file:
            encoded_image = base64.b64encode(file.read())
        os.remove(image_name)
        return Response({'image_base64_bytes': encoded_image})
    except:
        return Response({'status': False, 'errMsg': "File Not Found!"})
    

# get license data file from s3
@api_view(['POST'])
def get_license_data(request):
    license_url = request.data.get('license_url')
    license_data_name = license_url.split('/', -1)[-1]
    s3 = boto3.client('s3', aws_access_key_id=s3_config.config["ACCESS_KEY"] , aws_secret_access_key=s3_config.config["SECRET_KEY"])
    bucket = s3_config.config["BUCKET"]
    try:
        s3.download_file(bucket,'license_data/'+str(license_data_name),license_data_name)
        with open(license_data_name, "rb") as file:
            encoded_file = base64.b64encode(file.read())
        os.remove(license_data_name)
        return Response({'license_data_name': encoded_file})
    except:
        return Response({'status': False, 'errMsg': "File Not Found!"})