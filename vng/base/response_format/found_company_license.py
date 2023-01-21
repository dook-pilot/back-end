def response(license_company_data, rdw):
    return ({
        "status": True,
        "errMsg": None,
        "license_plate_company_data": license_company_data, 
        "license_numbers_data": rdw if len(rdw) > 0 else None
    })