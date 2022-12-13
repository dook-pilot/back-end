# Introduction

A django project to scrap information from websites and images. Built with django rest framework. This contains all the API need to run the VNG-DOOK Pilot project for web and mobile application.

# Installing PaddleOCR library

1. clone the paddleOCR repository from here: https://github.com/PaddlePaddle/PaddleOCR.git
2. activate python virtual environment
3. go to paddleOCR directory
4. python setup.py install
   run the project by: python manage.py runserver

# Installation

First create a python environement.
Python version should be: python >= 3.4
pip install -r requirements.txt
All libraries can be installed by pip.

# Directory Structure

```
VNG/
├─ vng/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
├─ base/
│  ├─ scrap_functions/
│  │  ├─ license_number_with_company_name.py
│  │  ├─ rdw_scrapper.py
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
├─ requirements.txt
├─ manage.py
```

vng/ is the root directory of project. Inside root directory there are project directory (vng/) and application directory (base/).
The project directory vng/ contains configurations of our project.
The base/ directory contains all of the scraping logics and functions. Inside base/ directory there is a folder called scrap_functions/ which contains two files.
One file rdw_scrapper.py is scraping the information from [rdw](https://ovi.rdw.nl/default.aspx) website. license_number_with_company_name.py file is scraping data from image.

# RDW Scrapper

rdw_scrapper.py file is scraping the information from [rdw](https://ovi.rdw.nl/default.aspx) website with selenium.

# license_number_with_company_name.py

This file is scraping data from image with help of paddleocr library. If paddleocr library make problems to install, try to install it from it's [repository](https://github.com/PaddlePaddle/PaddleOCR).

# views.py

views.py file contains the APIs which are returning json object as a response.

# API function vngp1_predict_pre_extracted:

This API accepts a GET request only. It also requires a parameter which is "place_type". It takes place type from a user and scraps the data from csv file locating inside 10-08-22/ directory.

# API function vngp1_predict_license_plate:

This API accepts POST request only. It requires an image through the form from front-end side. It scraps the data from image using license_number_with_company_name.py file and send back the response in a json format.
The RDW scrap function is called inside this API. When the data from image is extracted, the rdw scrap function will be called for each license number
found in extracted data of image.

```
back-end
├─ .git
└─ vng
   ├─ base
   │  ├─ 10-08-22
   │  │  └─ 674_records_final_result_merged_with_updated_bovag_merged_reviews_and_irregularities.csv
   │  ├─ __init__.py
   │  ├─ admin.py
   │  ├─ apps.py
   │  ├─ data
   │  │  ├─ fetch_image_detail.py
   │  │  ├─ fetch_license_detail.py
   │  │  ├─ get_image_url.py
   │  │  └─ read_metadata.py
   │  ├─ migrations
   │  │  ├─ 0001_initial.py
   │  │  ├─ 0002_alter_company_rating.py
   │  │  └─ __init__.py
   │  ├─ models.py
   │  ├─ read_exifdata.py
   │  ├─ response_format
   │  │  ├─ found_company_license.py
   │  │  ├─ invalid_gps.py
   │  │  └─ no_company_found.py
   │  ├─ scrap_functions
   │  │  ├─ license_number_with_company_name.py
   │  │  └─ rdw_scrapper.py
   │  ├─ store_data
   │  │  ├─ company_database.py
   │  │  ├─ image_database.py
   │  │  └─ license_plate_database.py
   │  ├─ tests.py
   │  ├─ urls.py
   │  ├─ views.py
   │  ├─ views.py.old
   │  └─ write_uploaded_image.py
   ├─ db.sqlite3
   ├─ manage.py
   ├─ requirements.txt
   └─ vng
      ├─ __init__.py
      ├─ asgi.py
      ├─ settings.py
      ├─ urls.py
      └─ wsgi.py

```
