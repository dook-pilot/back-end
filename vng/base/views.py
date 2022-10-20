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
import numpy as np
import ast
import io
import os
from geopy.geocoders import Nominatim
from .scrap_functions import license_number_with_company_name
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
    if file == "":
        return Response({'error': 'No file'})
    image_bytes = file.read()
    license_plate_company_data = license_number_with_company_name.get_image_upload_license_company_res(image_bytes)
    return Response(license_plate_company_data)
@api_view(['GET'])
def rdw(request, license):
    data = rdw_scrapper.rdw_scrapper(license)
    return Response(data)

