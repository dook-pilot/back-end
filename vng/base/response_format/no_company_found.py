def response(license_company_data, license_file_urls, rdw, image_url):
    return ({
            "status": True,
            "errMsg": None,
            "image_url": image_url,
            "license_data_urls": license_file_urls if len(license_file_urls) > 0 else None,
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
            "license_number": license_company_data['license_number'] if len(license_company_data['license_number']) > 0 else None
            }, 
            "license_numbers_data": rdw if len(rdw) > 0 else None
            })