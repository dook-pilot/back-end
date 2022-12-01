def response(license_file_urls, license_company_data, rdw, image_url):
    return ({
        "status": True,
        "errMsg": None,
        "image_url": image_url,
        "license_data_urls": license_file_urls if len(license_file_urls) > 0 else None,
        "license_plate_company_data": license_company_data, 
        "license_numbers_data": rdw if len(rdw) > 0 else None
    })