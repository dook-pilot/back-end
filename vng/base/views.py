from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scrap_functions import rdw_scrapper
from flask import Flask, request, jsonify
from flask import request, abort
from functools import wraps
from base64 import encodebytes
from joblib import dump, load
import pandas as pd
from PIL import Image
from . import read_exifdata, s3_config
import numpy as np
import os, uuid, boto3, ast, io, base64
from django.contrib.gis.geos import Point
from PIL.ExifTags import TAGS
from .scrap_functions import license_number_with_company_name
from .models import Company, LicensePlate, TargetImage
from django.core.files import File

# Create your views here.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm', 'tif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def get_response_image(image_path):
    pil_img = Image.fromarray(np.uint8(image_path)).convert('RGB') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('utf-8') # encode as base64
    return encoded_img
def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)
        return wrapper
    return decorator
# Companies and map irregularities API
@api_view(['GET'])
def vngp1_predict_pre_extracted(request, place_type):
    if (len(place_type) == 0):
        return Response({'error': 'Data is not correct. Please make a search again'})
    output_dir = ''
    data_directory = f'{os.getcwd()}/base/10-08-22'
    companies_details_csv = f'{data_directory}/674_records_final_result_merged_with_updated_bovag_merged_reviews_and_irregularities.csv'#place_api_car_companies_indicators.csv'

    companies_df = pd.read_csv(companies_details_csv)

    companies_df["lat_lng"] = [[geometry['location']['lat'], geometry['location']['lng']] for geometry in
                        [ast.literal_eval(i) for i in companies_df["geometry"]]]
    
    if place_type != 'all':
        companies_df = companies_df[companies_df['types'].str.contains(place_type)]
    companies_indicators_dict = companies_df.fillna(0).to_dict('r')

    response_dict = {'status': 'new',
                        'compnaies_indicators_dict': companies_indicators_dict,
                        }
    return Response(response_dict)

@api_view(['POST'])
def vngp1_predict_license_plate(request):
    file = request.data.get('file')
    image_name = str(uuid.uuid4())+".jpg"
    print(file)
    if file == None:
        return Response({'error': "Server Error: Please try with different image"})
    image_bytes = file.read()
    with open("image.jpg", "wb") as img:
        img.write(image_bytes)
        
    license_plate_company_data = license_number_with_company_name.get_image_upload_license_company_res(image_bytes)
    license_plate_company_data["status"] = True
    license_plate_company_data["errMsg"] = None
    # read metadata
    coordinates = read_exifdata.image_coordinates("image.jpg")
    lat = coordinates[0]
    lng = coordinates[1]
    rdw_scrapped_response = []
    license_data_links = []
    license_data_links_without_null = []
    if license_plate_company_data['license_number'] != "":
        for license_number in license_plate_company_data['license_number']:
            rdw_scraped_data, license_data_link = rdw_scrapper.rdw_scrapper(license_number)
            rdw_scrapped_response.append(rdw_scraped_data)
            license_data_links.append(license_data_link)
            # rdw_scrapped_response.append(rdw_scrapper.rdw_scrapper(license_number))
    if len(license_data_links) > 0:
        for link in license_data_links:
            if link != None:
                license_data_links_without_null.append(link)
    # storing into database
    try:
        id = uuid.uuid4()
        company = Company()
        company.company_id = id
        company.place_api_company_name = license_plate_company_data['place_api_company_name']
        company.bovag_matched_name = license_plate_company_data['bovag_matched_name']
        company.poitive_reviews = license_plate_company_data['poitive_reviews']
        company.negative_reviews = license_plate_company_data['negative_reviews']
        company.rating = license_plate_company_data['rating']
        company.duplicate_location = license_plate_company_data['duplicate_location']
        company.kvk_tradename = license_plate_company_data['kvk_tradename']
        company.irregularities = license_plate_company_data['irregularities']
        company.duplicates_found = license_plate_company_data['duplicates_found']
        company.Bovag_registered = license_plate_company_data['Bovag_registered']
        company.KVK_found = license_plate_company_data['KVK_found']
        company.company_ratings = license_plate_company_data['company_ratings']
        company.latitude = lat
        company.longitude = lng
        
        try:
            pnt_company = Point(lat, lng)
            print(pnt_company)
            company.geom = pnt_company
        except ValueError:
            return Response({
                "status": False,
                "errMsg": "No GPS Data Found! Please Upload Another Image."
            })
        company.save()
        image_id = uuid.uuid4()
        targetImage = TargetImage(company=company)
        targetImage.image_id = image_id
        targetImage.image = File(file=open("image.jpg", 'rb'), name=image_name)
        targetImage.image_name = image_name
        try:
            pnt_image = Point(lat, lng)
            targetImage.geom = pnt_image
        except ValueError:
            return Response({
                "status": False,
                "errMsg": "No GPS Data Found! Please Upload Another Image."
            })
        targetImage.save()
        get_image = TargetImage.objects.get(image_id=image_id)
        updateCompanyImageUrl = Company.objects.get(company_id=id)
        updateCompanyImageUrl.image_url = get_image.image.url
        updateCompanyImageUrl.save()
        if license_plate_company_data['license_number'] != "":
            for license_number in license_plate_company_data['license_number']:
                license_id = uuid.uuid4()
                licensePlate = LicensePlate(company=company, target_image=targetImage)
                licensePlate.license_number = license_number
                licensePlate.license_plate_id = license_id
                try:
                    pnt_license = Point(lat, lng)
                    licensePlate.geom = pnt_license
                except ValueError:
                    return Response({
                        "status": False,
                        "errMsg": "No GPS Data Found! Please Upload Another Image."
                    })
                licensePlate.save()
        os.remove("image.jpg")
        return Response({
        "status": True,
        "errMsg": None,
        "image_url": get_image.image.url,
        "license_data_urls": license_data_links_without_null if len(license_data_links_without_null) > 0 else None,
        "license_plate_company_data": license_plate_company_data, 
        "license_numbers_data": rdw_scrapped_response if len(rdw_scrapped_response) > 0 else None 
        })
    except KeyError:
        id = uuid.uuid4()
        license_plate_company_data["status"] = False
        license_plate_company_data["errMsg"] = "No company data found!"
        company = Company()
        company.company_id = id
        company.place_api_company_name = ""
        company.bovag_matched_name = ""
        company.poitive_reviews = 0
        company.negative_reviews = 0
        company.rating = 0
        company.duplicate_location = ""
        company.kvk_tradename = ""
        company.irregularities = ""
        company.duplicates_found = ""
        company.Bovag_registered = ""
        company.KVK_found = ""
        company.company_ratings = ""
        company.latitude = lat
        company.longitude = lng
        try:
            pnt = Point(float(lat), float(lng))
            company.geom = pnt
        except ValueError:
            return Response({
                "status": False,
                "errMsg": "No GPS Data Found! Please Upload Another Image."
            })
        company.save()
        image_id = uuid.uuid4()
        targetImage = TargetImage(company=company)
        targetImage.image_id = image_id
        targetImage.image = File(file=open("image.jpg", 'rb'), name=image_name)
        targetImage.image_name = image_name
        targetImage.save()
        get_image = TargetImage.objects.get(image_id=image_id)
        updateCompanyImageUrl = Company.objects.get(company_id=id)
        updateCompanyImageUrl.image_url = get_image.image.url
        updateCompanyImageUrl.save()
        if license_plate_company_data['license_number'] != "":
            for license_number in license_plate_company_data['license_number']:
                licensePlate = LicensePlate(company=company, target_image=targetImage)
                licensePlate.license_number = license_number
                licensePlate.save()
        os.remove("image.jpg")
        return Response({
            "status": True,
            "errMsg": None,
            "image_url": get_image.image.url,
            "license_data_urls": license_data_links_without_null if len(license_data_links_without_null) > 0 else None,
            "license_plate_company_data": {
            "status": False,
            "errMsg": "No company data found!",
            "place_api_company_name": "",
            "bovag_matched_name": None,
            "poitive_reviews": 0,
            "negative_reviews": 0, 
            "rating": "",
            "duplicate_location": "",
            "kvk_tradename": "",
            "irregularities": "",
            "duplicates_found": "",
            "Bovag_registered": "",
            "KVK_found": "",
            "company_ratings": "",
            "license_number": license_plate_company_data['license_number'] if len(license_plate_company_data['license_number']) > 0 else None
            }, 
            "license_numbers_data": rdw_scrapped_response if len(rdw_scrapped_response) > 0 else None
            })

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