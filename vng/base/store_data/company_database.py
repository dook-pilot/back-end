from django.contrib.gis.geos import Point
from base.models import Company, TargetImage
from uuid import uuid4

def store_company(lng, lat, target_image, license_plate_company_data):
    id = uuid4()
    company = Company(target_image=target_image)
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
    company.longitude = lng
    company.latitude = lat
    point_company = Point(lng, lat)
    company.geom = point_company
    company.save()
    return id

def update_image_url(company_id, image_id):
    get_image = TargetImage.objects.get(image_id=image_id)
    updateCompanyImageUrl = Company.objects.get(company_id=company_id)
    updateCompanyImageUrl.image_url = get_image.image.url
    updateCompanyImageUrl.save()