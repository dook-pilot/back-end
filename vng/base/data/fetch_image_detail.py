from base.scrap_functions import license_number_with_company_name
def company_license_data(image_bytes):
    license_plate_company_data = license_number_with_company_name.get_image_upload_license_company_res(image_bytes)
    license_plate_company_data["status"] = True
    license_plate_company_data["errMsg"] = None
    return license_plate_company_data