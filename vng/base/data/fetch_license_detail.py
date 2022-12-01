from base.scrap_functions import rdw_scrapper
def license_detail(license_plate_company_data):
    rdw_scrapped_response = []
    license_data_links = []
    license_data_links_without_null = []
    for license_number in license_plate_company_data['license_number']:
        rdw_scraped_data, license_data_link = rdw_scrapper.rdw_scrapper(license_number)
        rdw_scrapped_response.append(rdw_scraped_data)
        license_data_links.append(license_data_link)
    if len(license_data_links) > 0:
        for link in license_data_links:
            if link != None:
                license_data_links_without_null.append(link)
    return (rdw_scrapped_response, license_data_links_without_null)