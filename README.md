# Introduction
A django project to scrap information from websites and images. Built with django rest framework. This contains all the API need to run the VNG-DOOK Pilot project for web and mobile application.
# Installation
pip install -r requirements.txt
run the project by: python manage.py runserver
# Directory Structure
![directory_structure](https://i.ibb.co/3NgvPg2/dir.png)
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
# API function rdw:
This function accepts GET request only and it also requires a license number from the user. It finds the data of with the license number on [rdw](https://ovi.rdw.nl/default.aspx) website and scraps all the information. It then send that information back in json format.
