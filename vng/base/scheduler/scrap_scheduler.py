from apscheduler.schedulers.background import BackgroundScheduler
from base.models import TargetImage, Company, LicensePlate, History
from base.data import download_img_s3, read_metadata, fetch_image_detail
# download_rdw_s3, , fetch_license_detail, , get_image_url
from base.store_data import company_database, license_plate_database
from base.scrap_functions import rdw_scrapper
import os, json
from base.response_format import found_company_license, no_company_found

def job():
    images = TargetImage.objects.all()
    for image in images:
        history = History.objects.get(image=image)
        if image.isScraped == False:
            # DOWNLOAD IMAGE FROM S3 AND DO SCRAPING
            image_url = image.image.url
            image_name = image_url.split('/', -1)[-1]
            download_img_s3.download_image(image_name)
            # GET LATITUDE AND LONGITUDE FROM IMAGE
            lng, lat = read_metadata.coordinates(image_name)
            image_file = open(image_name, 'rb')
            image_bytes = image_file.read()
            # GET IMAGE SCRAPED DATA
            # try:
            license_plate_company_data = fetch_image_detail.company_license_data(
                image_bytes)
            # STORE COMPANY DETAILS IN DATABASE
            if license_plate_company_data['error'] == 'false':
                company_instance_id = company_database.store_company(
                    lng, lat, image, license_plate_company_data)
            os.remove(image_name)
            # STORE LICENSE NUMBERS IN DATABASE
            if len(license_plate_company_data['license_number']) > 0:
                for license_number in license_plate_company_data['license_number']:
                    license = license_plate_database.store_license_plate(
                        license_number, image, lng, lat)
                    # SCRAP RDW DATA ON EACH LICENSE NUMBER
                    rdw_response = rdw_scrapper.rdw_scrapper(license_number)
            history.isProcessed = True
            image.isScraped = True
            history.save()
            image.save()
            # except:
            #     pass
            
            
            
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds=2, id="0", replace_existing=True)
    scheduler.start()