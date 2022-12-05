from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base.models import LicenseDatabaseS3Link
import json, os
from django.core.files import File

def rdw_scrapper(license):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    #driver =  webdriver.Chrome("/usr/bin/chromedriver", options=options)
    driver = webdriver.Chrome(options, service=Service(ChromeDriverManager().install()))
    driver.get('https://ovi.rdw.nl/default.aspx')
    search = driver.find_element(By.NAME, "ctl00$TopContent$txtKenteken").send_keys(license)
    submit = driver.find_element(By.XPATH, '//button[text()="Gegevens opvragen"]').click()
    try:
        element = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "myTable"))
    )
        # BRAND AND MODEL
        brand = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[1]/div/div[1]/h3[1]').get_attribute("innerHTML")
        brand = brand.strip()
        model = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[1]/div/div[1]/p[1]').get_attribute("innerHTML")
        model = model.strip()
        ########################################## CATEGORY BASIS ##################################################
        #
        # SECTION ALGEMEEN
        #
        # ROW 1
        algemeen_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[1]').get_attribute("innerHTML")
        algemeen_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[2]').get_attribute("innerHTML")
        algemeen_row_1_col_3 = driver.find_element(By.XPATH, '//*[@id="Voertuigsoort"]').get_attribute("innerHTML")
        algemeen_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[4]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        algemeen_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[5]').get_attribute("innerHTML")
        algemeen_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[6]').get_attribute("innerHTML")
        algemeen_row_2_col_3 = driver.find_element(By.XPATH, '//*[@id="CarrosserieOmschrijving"]').get_attribute("innerHTML")
        algemeen_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[6]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        algemeen_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[9]').get_attribute("innerHTML")
        algemeen_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[10]').get_attribute("innerHTML")
        algemeen_row_3_col_3 = driver.find_element(By.XPATH, '//*[@id="InrichtingCodeOmschrijving"]').get_attribute("innerHTML")
        algemeen_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[8]/div/div[2]').get_attribute("innerHTML")
        # ROW 4
        algemeen_row_4_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[13]').get_attribute("innerHTML")
        algemeen_row_4_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[14]').get_attribute("innerHTML")
        algemeen_row_4_col_3 = driver.find_element(By.XPATH, '//*[@id="Merk"]').get_attribute("innerHTML")
        algemeen_row_4_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[10]/div/div[2]').get_attribute("innerHTML")
        # ROW 5
        algemeen_row_5_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[17]').get_attribute("innerHTML")
        algemeen_row_5_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[18]').get_attribute("innerHTML")
        algemeen_row_5_col_3 = driver.find_element(By.XPATH, '//*[@id="Type"]').get_attribute("innerHTML")
        algemeen_row_5_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[12]/div/div[2]').get_attribute("innerHTML")
        # ROW 6
        algemeen_row_6_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[21]').get_attribute("innerHTML")
        algemeen_row_6_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[22]').get_attribute("innerHTML")
        algemeen_row_6_col_3 = driver.find_element(By.XPATH, '//*[@id="Variant"]').get_attribute("innerHTML")
        algemeen_row_6_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[14]/div/div[2]').get_attribute("innerHTML")
        # ROW 7
        algemeen_row_7_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[25]').get_attribute("innerHTML")
        algemeen_row_7_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[26]').get_attribute("innerHTML")
        algemeen_row_7_col_3 = driver.find_element(By.XPATH, '//*[@id="Uitvoering"]').get_attribute("innerHTML")
        algemeen_row_7_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[16]/div/div[2]').get_attribute("innerHTML")
        # ROW 8
        algemeen_row_8_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[29]').get_attribute("innerHTML")
        algemeen_row_8_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[30]').get_attribute("innerHTML")
        algemeen_row_8_col_3 = driver.find_element(By.XPATH, '//*[@id="Kleur"]').get_attribute("innerHTML")
        algemeen_row_8_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[18]/div/div[2]').get_attribute("innerHTML")
        # ROW 9
        algemeen_row_9_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[33]').get_attribute("innerHTML")
        algemeen_row_9_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[34]').get_attribute("innerHTML")
        algemeen_row_9_col_3 = driver.find_element(By.XPATH, '//*[@id="Handelsbenaming"]').get_attribute("innerHTML")
        algemeen_row_9_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[20]/div/div[2]').get_attribute("innerHTML")
        # ROW 10
        algemeen_row_10_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[37]').get_attribute("innerHTML")
        algemeen_row_10_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[38]').get_attribute("innerHTML")
        algemeen_row_10_col_3 = driver.find_element(By.XPATH, '//*[@id="Typegoedkeuring"]').get_attribute("innerHTML")
        algemeen_row_10_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[22]/div/div[2]').get_attribute("innerHTML")
        # ROW 11
        algemeen_row_11_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[41]').get_attribute("innerHTML")
        algemeen_row_11_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[42]').get_attribute("innerHTML")
        algemeen_row_11_col_3 = driver.find_element(By.XPATH, '//*[@id="PlaatsChassisOmschrijving"]').get_attribute("innerHTML")
        algemeen_row_11_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[24]/div/div[2]').get_attribute("innerHTML")
        # ROW 12
        algemeen_row_12_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[45]').get_attribute("innerHTML")
        algemeen_row_12_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[1]/div/div/div[46]').get_attribute("innerHTML")
        algemeen_row_12_col_3 = driver.find_element(By.XPATH, '//*[@id="Eigenaren"]').get_attribute("innerHTML")
        algemeen_row_12_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[26]/div/div[2]').get_attribute("innerHTML")

        #
        #SECTION VERVALDATA EN HISTORIE
        #
        # ROW 1
        vervaldata_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[1]').get_attribute("innerHTML")
        vervaldata_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[2]').get_attribute("innerHTML")
        vervaldata_row_1_col_3 = driver.find_element(By.XPATH, '//*[@id="VervaldatumApkKeuring"]').get_attribute("innerHTML")
        vervaldata_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[28]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        vervaldata_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[5]').get_attribute("innerHTML")
        vervaldata_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[6]').get_attribute("innerHTML")
        vervaldata_row_2_col_3 = driver.find_element(By.XPATH, '//*[@id="EersteAfgifteNederland"]').get_attribute("innerHTML")
        vervaldata_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[30]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        vervaldata_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[9]').get_attribute("innerHTML")
        vervaldata_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[10]').get_attribute("innerHTML")
        vervaldata_row_3_col_3 = driver.find_element(By.XPATH, '//*[@id="EersteToelatingsdatum"]').get_attribute("innerHTML")
        vervaldata_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[32]/div/div[2]').get_attribute("innerHTML")
        # ROW 4
        vervaldata_row_4_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[13]').get_attribute("innerHTML")
        vervaldata_row_4_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[14]').get_attribute("innerHTML")
        vervaldata_row_4_col_3 = driver.find_element(By.XPATH, '//*[@id="AfgDatKent"]').get_attribute("innerHTML")
        vervaldata_row_4_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[34]/div/div[2]').get_attribute("innerHTML")
        # ROW 5
        vervaldata_row_5_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[17]').get_attribute("innerHTML")
        vervaldata_row_5_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[18]').get_attribute("innerHTML")
        vervaldata_row_5_col_3 = driver.find_element(By.XPATH, '//*[@id="DatumGdk"]').get_attribute("innerHTML")
        vervaldata_row_5_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[36]/div/div[2]').get_attribute("innerHTML")
        # ROW 6
        vervaldata_row_6_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[21]').get_attribute("innerHTML")
        vervaldata_row_6_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[22]').get_attribute("innerHTML")
        vervaldata_row_6_col_3 = driver.find_element(By.XPATH, '//*[@id="DatumAanvangTenaamstelling"]').get_attribute("innerHTML")
        vervaldata_row_6_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[38]/div/div[2]').get_attribute("innerHTML")
        # ROW 7
        vervaldata_row_7_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[25]').get_attribute("innerHTML")
        vervaldata_row_7_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[2]/div/div/div[26]').get_attribute("innerHTML")
        vervaldata_row_7_col_3 = driver.find_element(By.XPATH, '//*[@id="TijdAanvangTenaamstelling"]').get_attribute("innerHTML")
        vervaldata_row_7_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[40]/div/div[2]').get_attribute("innerHTML")
        #
        # SECTION GEWICHTEN
        #
        # ROW 1
        gewichten_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[1]').get_attribute("innerHTML")
        gewichten_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[2]').get_attribute("innerHTML")
        gewichten_row_1_col_3 = driver.find_element(By.XPATH, '//*[@id="MassaBedrijfsklaar"]').get_attribute("innerHTML")
        gewichten_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[42]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        gewichten_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[5]').get_attribute("innerHTML")
        gewichten_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[6]').get_attribute("innerHTML")
        gewichten_row_2_col_3 = driver.find_element(By.XPATH, '//*[@id="MassaLedigVoertuig"]').get_attribute("innerHTML")
        gewichten_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[44]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        gewichten_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[9]').get_attribute("innerHTML")
        gewichten_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[10]').get_attribute("innerHTML")
        gewichten_row_3_col_3 = driver.find_element(By.XPATH, '//*[@id="TechnischeMaximumMassaVoertuig"]').get_attribute("innerHTML")
        gewichten_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[46]/div/div[2]').get_attribute("innerHTML")
        # ROW 4
        gewichten_row_4_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[13]').get_attribute("innerHTML")
        gewichten_row_4_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[14]').get_attribute("innerHTML")
        gewichten_row_4_col_3 = driver.find_element(By.XPATH, '//*[@id="MaximumMassaVoertuig"]').get_attribute("innerHTML")
        gewichten_row_4_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[48]/div/div[2]').get_attribute("innerHTML")
        # ROW 5
        gewichten_row_5_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[17]').get_attribute("innerHTML")
        gewichten_row_5_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[18]').get_attribute("innerHTML")
        gewichten_row_5_col_3 = driver.find_element(By.XPATH, '//*[@id="MaximumMassaSamenstel"]').get_attribute("innerHTML")
        gewichten_row_5_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[50]/div/div[2]').get_attribute("innerHTML")
        # ROW 6
        gewichten_row_6_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[21]').get_attribute("innerHTML")
        gewichten_row_6_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[22]').get_attribute("innerHTML")
        gewichten_row_6_col_3 = driver.find_element(By.XPATH, '//*[@id="MaximumMassaGeremd"]').get_attribute("innerHTML")
        gewichten_row_6_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[52]/div/div[2]').get_attribute("innerHTML")
        # ROW 7
        gewichten_row_7_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[25]').get_attribute("innerHTML")
        gewichten_row_7_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[3]/div/div/div[26]').get_attribute("innerHTML")
        gewichten_row_7_col_3 = driver.find_element(By.XPATH, '//*[@id="MaximumMassaOngeremd"]').get_attribute("innerHTML")
        gewichten_row_7_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[54]/div/div[2]').get_attribute("innerHTML")
        #
        # SECTION TELLERSTANDEN
        #
        # ROW 1
        tellerstanden_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[4]/div/div/div[1]').get_attribute("innerHTML")
        tellerstanden_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[4]/div/div/div[2]').get_attribute("innerHTML")
        tellerstanden_row_1_col_3 = driver.find_element(By.XPATH, '//*[@id="TellerstandDatum"]').get_attribute("innerHTML")
        tellerstanden_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[56]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        tellerstanden_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[4]/div/div/div[5]').get_attribute("innerHTML")
        tellerstanden_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[4]/div/div/div[6]').get_attribute("innerHTML")
        tellerstanden_row_2_col_3 = driver.find_element(By.XPATH, '//*[@id="TellerstandOordeel"]').get_attribute("innerHTML")
        tellerstanden_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[58]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        tellerstanden_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[4]/div/div/div[9]').get_attribute("innerHTML")
        tellerstanden_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[4]/div/div/div[10]').get_attribute("innerHTML")
        tellerstanden_row_3_col_3 = driver.find_element(By.XPATH, '//*[@id="TellerstandToelichting"]').get_attribute("innerHTML")
        tellerstanden_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[60]/div/div[2]').get_attribute("innerHTML")
        #
        # SECTION STATUS VAN HET VOERTULG
        #
        # ROW 1
        status_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[1]').get_attribute("innerHTML")
        status_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[2]').get_attribute("innerHTML")
        status_row_1_col_3 = driver.find_element(By.XPATH, '//*[@id="Gestolen"]').get_attribute("innerHTML")
        status_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[62]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        status_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[5]').get_attribute("innerHTML")
        status_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[6]').get_attribute("innerHTML")
        status_row_2_col_3 = driver.find_element(By.XPATH, '//*[@id="Geexporteerd"]').get_attribute("innerHTML")
        status_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[64]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        status_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[9]').get_attribute("innerHTML")
        status_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[10]').get_attribute("innerHTML")
        status_row_3_col_3 = driver.find_element(By.XPATH, '//*[@id="WAVerzekerd"]').get_attribute("innerHTML")
        status_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[66]/div/div[2]').get_attribute("innerHTML")
        # ROW 4
        status_row_4_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[13]').get_attribute("innerHTML")
        status_row_4_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[14]').get_attribute("innerHTML")
        status_row_4_col_3 = driver.find_element(By.XPATH, '//*[@id="WachtenOpKeuring"]').get_attribute("innerHTML")
        status_row_4_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[68]/div/div[2]').get_attribute("innerHTML")
        # ROW 5
        status_row_5_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[17]').get_attribute("innerHTML")
        status_row_5_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[5]/div/div/div[18]').get_attribute("innerHTML")
        status_row_5_col_3 = driver.find_element(By.XPATH, '//*[@id="TenaamstellenMogelijk"]').get_attribute("innerHTML")
        status_row_5_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[70]/div/div[2]').get_attribute("innerHTML")
        #
        # SECTION TERUGROEPACTIES
        #
        # ROW 1
        terug_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[6]/div/div/div[1]').get_attribute("innerHTML")
        terug_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[2]/div/div[6]/div/div/div[2]').get_attribute("innerHTML")
        terug_row_1_col_3 = driver.find_element(By.XPATH, '//*[@id="StatusTerugroepacties"]').get_attribute("innerHTML")
        terug_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[72]/div/div[2]').get_attribute("innerHTML")
        #
        ################################ CATEGORY MOTOR & MILIEU ##########################################
        #
        # SECTION MOTOR
        #
        # ROW 1
        motor_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[1]').get_attribute("innerHTML")
        motor_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]').get_attribute("innerHTML")
        motor_row_1_col_3 = driver.find_element(By.XPATH, '//*[@id="CilinderInhoud"]').get_attribute("innerHTML")
        motor_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[74]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        motor_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[5]').get_attribute("innerHTML")
        motor_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[6]').get_attribute("innerHTML")
        motor_row_2_col_3 = driver.find_element(By.XPATH, '//*[@id="AantalCilinders"]').get_attribute("innerHTML")
        motor_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[76]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        motor_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[9]').get_attribute("innerHTML")
        motor_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[10]').get_attribute("innerHTML")
        motor_row_3_col_3 = driver.find_element(By.XPATH, '//*[@id="TypeGasInstallatie"]').get_attribute("innerHTML")
        motor_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[78]/div/div[2]').get_attribute("innerHTML")
        # ROW 4
        motor_row_4_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[13]').get_attribute("innerHTML")
        motor_row_4_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[14]').get_attribute("innerHTML")
        motor_row_4_col_3 = driver.find_element(By.XPATH, '//*[@id="EmissieklasseDiesel"]').get_attribute("innerHTML")
        motor_row_4_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[80]/div/div[2]').get_attribute("innerHTML")
        #
        # SECTION MILIEUPRESTATIES
        #
        # ROW 1
        mili_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[1]').get_attribute("innerHTML")
        mili_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[2]').get_attribute("innerHTML")
        mili_row_1_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[4]').get_attribute("innerHTML")
        mili_row_1_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[5]').get_attribute("innerHTML")
        mili_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[82]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        mili_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[7]').get_attribute("innerHTML")
        mili_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[8]').get_attribute("innerHTML")
        mili_row_2_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[10]').get_attribute("innerHTML")
        mili_row_2_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[11]').get_attribute("innerHTML")
        mili_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[84]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        mili_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[13]').get_attribute("innerHTML")
        mili_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[14]').get_attribute("innerHTML")
        mili_row_3_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[16]').get_attribute("innerHTML")
        mili_row_3_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[17]').get_attribute("innerHTML")
        mili_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[86]/div/div[2]').get_attribute("innerHTML")
        # ROW 4
        mili_row_4_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[19]').get_attribute("innerHTML")
        mili_row_4_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[20]').get_attribute("innerHTML")
        mili_row_4_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[22]').get_attribute("innerHTML")
        mili_row_4_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[23]').get_attribute("innerHTML")
        mili_row_4_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[88]/div/div[2]').get_attribute("innerHTML")
        # ROW 5
        mili_row_5_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[25]').get_attribute("innerHTML")
        mili_row_5_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[26]').get_attribute("innerHTML")
        mili_row_5_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[28]').get_attribute("innerHTML")
        mili_row_5_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[29]').get_attribute("innerHTML")
        mili_row_5_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[90]/div/div[2]').get_attribute("innerHTML")
        # ROW 6
        mili_row_6_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[31]').get_attribute("innerHTML")
        mili_row_6_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[32]').get_attribute("innerHTML")
        mili_row_6_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[34]').get_attribute("innerHTML")
        mili_row_6_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[35]').get_attribute("innerHTML")
        mili_row_6_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[92]/div/div[2]').get_attribute("innerHTML")
        # ROW 7
        mili_row_7_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[37]').get_attribute("innerHTML")
        mili_row_7_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[38]').get_attribute("innerHTML")
        mili_row_7_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[40]').get_attribute("innerHTML")
        mili_row_7_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[41]').get_attribute("innerHTML")
        mili_row_7_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[94]/div/div[2]').get_attribute("innerHTML")
        # ROW 8
        mili_row_8_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[43]').get_attribute("innerHTML")
        mili_row_8_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[44]').get_attribute("innerHTML")
        mili_row_8_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[46]').get_attribute("innerHTML")
        mili_row_8_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[47]').get_attribute("innerHTML")
        mili_row_8_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[96]/div/div[2]').get_attribute("innerHTML")
        # ROW 9
        mili_row_9_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[49]').get_attribute("innerHTML")
        mili_row_9_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[50]').get_attribute("innerHTML")
        mili_row_9_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[52]').get_attribute("innerHTML")
        mili_row_9_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[53]').get_attribute("innerHTML")
        mili_row_9_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[98]/div/div[2]').get_attribute("innerHTML")
        # ROW 10
        mili_row_10_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[55]').get_attribute("innerHTML")
        mili_row_10_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[56]').get_attribute("innerHTML")
        mili_row_10_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[58]').get_attribute("innerHTML")
        mili_row_10_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[59]').get_attribute("innerHTML")
        mili_row_10_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[100]/div/div[2]').get_attribute("innerHTML")
        # ROW 11
        mili_row_11_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[61]').get_attribute("innerHTML")
        mili_row_11_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[62]').get_attribute("innerHTML")
        mili_row_11_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[64]').get_attribute("innerHTML")
        mili_row_11_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[65]').get_attribute("innerHTML")
        mili_row_11_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[102]/div/div[2]').get_attribute("innerHTML")
        # ROW 12
        mili_row_12_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[67]').get_attribute("innerHTML")
        mili_row_12_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[68]').get_attribute("innerHTML")
        mili_row_12_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[70]').get_attribute("innerHTML")
        mili_row_12_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[71]').get_attribute("innerHTML")
        mili_row_12_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[104]/div/div[2]').get_attribute("innerHTML")
        # ROW 13
        mili_row_13_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[73]').get_attribute("innerHTML")
        mili_row_13_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[74]').get_attribute("innerHTML")
        mili_row_13_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[76]').get_attribute("innerHTML")
        mili_row_13_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[77]').get_attribute("innerHTML")
        mili_row_13_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[106]/div/div[2]').get_attribute("innerHTML")
        # ROW 14
        mili_row_14_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[79]').get_attribute("innerHTML")
        mili_row_14_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[80]').get_attribute("innerHTML")
        mili_row_14_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[82]').get_attribute("innerHTML")
        mili_row_14_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[83]').get_attribute("innerHTML")
        mili_row_14_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[108]/div/div[2]').get_attribute("innerHTML")
        #
        # SECTION ULTSTOOT
        #
        # ROW 1
        ultstoot_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[1]').get_attribute("innerHTML")
        ultstoot_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[2]').get_attribute("innerHTML")
        ultstoot_row_1_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[4]').get_attribute("innerHTML")
        ultstoot_row_1_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[5]').get_attribute("innerHTML")
        ultstoot_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[82]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        ultstoot_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[7]').get_attribute("innerHTML")
        ultstoot_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[8]').get_attribute("innerHTML")
        ultstoot_row_2_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[10]').get_attribute("innerHTML")
        ultstoot_row_2_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[11]').get_attribute("innerHTML")
        ultstoot_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[112]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        ultstoot_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[13]').get_attribute("innerHTML")
        ultstoot_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[14]').get_attribute("innerHTML")
        ultstoot_row_3_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[16]').get_attribute("innerHTML")
        ultstoot_row_3_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[17]').get_attribute("innerHTML")
        ultstoot_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[114]/div/div[2]').get_attribute("innerHTML")  
        # ROW 4
        ultstoot_row_4_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[19]').get_attribute("innerHTML")
        ultstoot_row_4_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[20]').get_attribute("innerHTML")
        ultstoot_row_4_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[22]').get_attribute("innerHTML")
        ultstoot_row_4_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[23]').get_attribute("innerHTML")
        ultstoot_row_4_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[116]/div/div[2]').get_attribute("innerHTML") 
        # ROW 5
        ultstoot_row_5_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[25]').get_attribute("innerHTML")
        ultstoot_row_5_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[26]').get_attribute("innerHTML")
        ultstoot_row_5_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[28]').get_attribute("innerHTML")
        ultstoot_row_5_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[29]').get_attribute("innerHTML")
        ultstoot_row_5_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[118]/div/div[2]').get_attribute("innerHTML") 
        # ROW 6
        ultstoot_row_6_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[31]').get_attribute("innerHTML")
        ultstoot_row_6_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[32]').get_attribute("innerHTML")
        ultstoot_row_6_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[34]').get_attribute("innerHTML")
        ultstoot_row_6_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[35]').get_attribute("innerHTML")
        ultstoot_row_6_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[120]/div/div[2]').get_attribute("innerHTML")
        # ROW 7
        ultstoot_row_7_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[37]').get_attribute("innerHTML")
        ultstoot_row_7_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[38]').get_attribute("innerHTML")
        ultstoot_row_7_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[40]').get_attribute("innerHTML")
        ultstoot_row_7_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[41]').get_attribute("innerHTML")
        ultstoot_row_7_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[122]/div/div[2]').get_attribute("innerHTML")
        # ROW 8
        ultstoot_row_8_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[43]').get_attribute("innerHTML")
        ultstoot_row_8_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[44]').get_attribute("innerHTML")
        ultstoot_row_8_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[46]').get_attribute("innerHTML")
        ultstoot_row_8_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[47]').get_attribute("innerHTML")
        ultstoot_row_8_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[124]/div/div[2]').get_attribute("innerHTML")
        # ROW 9
        ultstoot_row_9_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[49]').get_attribute("innerHTML")
        ultstoot_row_9_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[50]').get_attribute("innerHTML")
        ultstoot_row_9_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[52]').get_attribute("innerHTML")
        ultstoot_row_9_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[53]').get_attribute("innerHTML")
        ultstoot_row_9_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[126]/div/div[2]').get_attribute("innerHTML")
        # ROW 10
        ultstoot_row_10_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[55]').get_attribute("innerHTML")
        ultstoot_row_10_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[56]').get_attribute("innerHTML")
        ultstoot_row_10_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[58]').get_attribute("innerHTML")
        ultstoot_row_10_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[59]').get_attribute("innerHTML")
        ultstoot_row_10_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[128]/div/div[2]').get_attribute("innerHTML")
        # ROW 11
        ultstoot_row_11_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[61]').get_attribute("innerHTML")
        ultstoot_row_11_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[62]').get_attribute("innerHTML")
        ultstoot_row_11_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[64]').get_attribute("innerHTML")
        ultstoot_row_11_col_4 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[65]').get_attribute("innerHTML")
        ultstoot_row_11_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[130]/div/div[2]').get_attribute("innerHTML")
        #
        ################################# CATEGORY TECHNISCH ########################################
        #
        # SECTION ELGENSCHAPPEN
        # ROW 1
        elgen_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[1]').get_attribute("innerHTML")
        elgen_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]').get_attribute("innerHTML")
        elgen_row_1_col_3 = driver.find_element(By.XPATH, '//*[@id="AantalZitplaatsen"]').get_attribute("innerHTML")
        elgen_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[132]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        elgen_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[5]').get_attribute("innerHTML")
        elgen_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[6]').get_attribute("innerHTML")
        elgen_row_2_col_3 = driver.find_element(By.XPATH, '//*[@id="AantalRolstoelplaatsen"]').get_attribute("innerHTML")
        elgen_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[134]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        elgen_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[9]').get_attribute("innerHTML")
        elgen_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[10]').get_attribute("innerHTML")
        elgen_row_3_col_3 = driver.find_element(By.XPATH, '//*[@id="AantalAssen"]').get_attribute("innerHTML")
        elgen_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[136]/div/div[2]').get_attribute("innerHTML")
        # ROW 4
        elgen_row_4_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[13]').get_attribute("innerHTML")
        elgen_row_4_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[14]').get_attribute("innerHTML")
        elgen_row_4_col_3 = driver.find_element(By.XPATH, '//*[@id="AantalWielen"]').get_attribute("innerHTML")
        elgen_row_4_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[138]/div/div[2]').get_attribute("innerHTML")
        # ROW 5
        elgen_row_5_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[17]').get_attribute("innerHTML")
        elgen_row_5_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[18]').get_attribute("innerHTML")
        elgen_row_5_col_3 = driver.find_element(By.XPATH, '//*[@id="Wielbasis"]').get_attribute("innerHTML")
        elgen_row_5_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[140]/div/div[2]').get_attribute("innerHTML")
        # ROW 6
        elgen_row_6_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[21]').get_attribute("innerHTML")
        elgen_row_6_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[1]/div/div/div[22]').get_attribute("innerHTML")
        elgen_row_6_col_3 = driver.find_element(By.XPATH, '//*[@id="AfstandVoorzijdeVrtgTotHartkoppeling"]').get_attribute("innerHTML")
        elgen_row_6_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[142]/div/div[2]').get_attribute("innerHTML")
        #
        # SECTION ASSEN
        #
        # ROW 1
        assen_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[2]').get_attribute("innerHTML")
        assen_row_1_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[4]').get_attribute("innerHTML")
        assen_row_1_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[5]').get_attribute("innerHTML")
        assen_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[144]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        assen_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[15]').get_attribute("innerHTML")
        assen_row_2_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[17]').get_attribute("innerHTML")
        assen_row_2_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[18]').get_attribute("innerHTML")
        assen_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[146]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        assen_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[28]').get_attribute("innerHTML")
        assen_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[30]').get_attribute("innerHTML")
        assen_row_3_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[31]').get_attribute("innerHTML")
        assen_row_3_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[148]/div/div[2]').get_attribute("innerHTML")
        # ROW 4
        assen_row_4_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[41]').get_attribute("innerHTML")
        assen_row_4_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[43]').get_attribute("innerHTML")
        assen_row_4_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[44]').get_attribute("innerHTML")
        assen_row_4_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[150]/div/div[2]').get_attribute("innerHTML")
        # ROW 5
        assen_row_5_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[54]').get_attribute("innerHTML")
        assen_row_5_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[56]').get_attribute("innerHTML")
        assen_row_5_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[57]').get_attribute("innerHTML")
        assen_row_5_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[152]/div/div[2]').get_attribute("innerHTML")
        # ROW 6
        assen_row_6_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[67]').get_attribute("innerHTML")
        assen_row_6_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[69]').get_attribute("innerHTML")
        assen_row_6_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[70]').get_attribute("innerHTML")
        assen_row_6_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[154]/div/div[2]').get_attribute("innerHTML")
        # ROW 7
        assen_row_7_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[80]').get_attribute("innerHTML")
        assen_row_7_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[82]').get_attribute("innerHTML")
        assen_row_7_col_3 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[83]').get_attribute("innerHTML")
        assen_row_7_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[156]/div/div[2]').get_attribute("innerHTML")
        #
        ################################# CATEGORY FLSCAAL ########################################
        #
        # SECTION FLSCAAL
        #
        # ROW 1
        flscaal_row_1_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[5]/div/div/div/div/div[2]').get_attribute("innerHTML")
        flscaal_row_1_col_2 = driver.find_element(By.XPATH, '//*[@id="BpmBedrag"]').get_attribute("innerHTML")
        flscaal_row_1_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[158]/div/div[2]').get_attribute("innerHTML")
        # ROW 2
        flscaal_row_2_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[5]/div/div/div/div/div[6]').get_attribute("innerHTML")
        flscaal_row_2_col_2 = driver.find_element(By.XPATH, '//*[@id="CatalogusPrijs"]').get_attribute("innerHTML")
        flscaal_row_2_info = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[160]/div/div[2]').get_attribute("innerHTML")
        # ROW 3
        flscaal_row_3_col_1 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[5]/div/div/div/div/div[10]').get_attribute("innerHTML")
        flscaal_row_3_col_2 = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[5]/div/div/div/div/div[12]/a').get_attribute("innerHTML")
        flscaal_row_3_link = driver.find_element(By.XPATH, '/html/body/div[1]/form/div[5]/div[2]/div[2]/div[5]/div/div/div/div/div[12]/a').get_attribute("href")
        flscaal_row_3_info = ""
        # CREATING RESPONSE DATA
        response_data = {
            "status": True,
            "errMsg": None,
            "title": license,
            "car_company": brand,
            "car_model": model,
            "categories": [
                {
                    "title": "Basis",
                    "sections": [
                        {
                            "title": "algemeen",
                            "data": [
                                {
                                    "col1": algemeen_row_1_col_1,
                                    "col2": algemeen_row_1_col_2,
                                    "col3": algemeen_row_1_col_3,
                                    "info": algemeen_row_1_info
                                },
                                {
                                    "col1": algemeen_row_2_col_1,
                                    "col2": algemeen_row_2_col_2,
                                    "col3": algemeen_row_2_col_3,
                                    "info": algemeen_row_2_info
                                },
                                {
                                    "col1": algemeen_row_3_col_1,
                                    "col2": algemeen_row_3_col_2,
                                    "col3": algemeen_row_3_col_3,
                                    "info": algemeen_row_3_info
                                },
                                {
                                    "col1": algemeen_row_4_col_1,
                                    "col2": algemeen_row_4_col_2,
                                    "col3": algemeen_row_4_col_3,
                                    "info": algemeen_row_4_info
                                },
                                {
                                    "col1": algemeen_row_5_col_1,
                                    "col2": algemeen_row_5_col_2,
                                    "col3": algemeen_row_5_col_3,
                                    "info": algemeen_row_5_info
                                },
                                {
                                    "col1": algemeen_row_6_col_1,
                                    "col2": algemeen_row_6_col_2,
                                    "col3": algemeen_row_6_col_3,
                                    "info": algemeen_row_6_info
                                },
                                {
                                    "col1": algemeen_row_7_col_1,
                                    "col2": algemeen_row_7_col_2,
                                    "col3": algemeen_row_7_col_3,
                                    "info": algemeen_row_7_info
                                },
                                {
                                    "col1": algemeen_row_8_col_1,
                                    "col2": algemeen_row_8_col_2,
                                    "col3": algemeen_row_8_col_3,
                                    "info": algemeen_row_8_info
                                },
                                {
                                    "col1": algemeen_row_9_col_1,
                                    "col2": algemeen_row_9_col_2,
                                    "col3": algemeen_row_9_col_3,
                                    "info": algemeen_row_9_info
                                },
                                {
                                    "col1": algemeen_row_10_col_1,
                                    "col2": algemeen_row_10_col_2,
                                    "col3": algemeen_row_10_col_3,
                                    "info": algemeen_row_10_info
                                },
                                {
                                    "col1": algemeen_row_11_col_1,
                                    "col2": algemeen_row_11_col_2,
                                    "col3": algemeen_row_11_col_3,
                                    "info": algemeen_row_11_info
                                },
                                {
                                    "col1": algemeen_row_12_col_1,
                                    "col2": algemeen_row_12_col_2,
                                    "col3": algemeen_row_12_col_3,
                                    "info": algemeen_row_12_info
                                },
                                
                            ]
                        },
                        {
                            "title": "Vervaldata en historie",
                            "data": [
                                {
                                    "col1": vervaldata_row_1_col_1,
                                    "col2": vervaldata_row_1_col_2,
                                    "col3": vervaldata_row_1_col_3,
                                    "info": vervaldata_row_1_info
                                },
                                {
                                    "col1": vervaldata_row_2_col_1,
                                    "col2": vervaldata_row_2_col_2,
                                    "col3": vervaldata_row_2_col_3,
                                    "info": vervaldata_row_2_info
                                },
                                {
                                    "col1": vervaldata_row_3_col_1,
                                    "col2": vervaldata_row_3_col_2,
                                    "col3": vervaldata_row_3_col_3,
                                    "info": vervaldata_row_3_info
                                },
                                {
                                    "col1": vervaldata_row_4_col_1,
                                    "col2": vervaldata_row_4_col_2,
                                    "col3": vervaldata_row_4_col_3,
                                    "info": vervaldata_row_4_info
                                },
                                {
                                    "col1": vervaldata_row_5_col_1,
                                    "col2": vervaldata_row_5_col_2,
                                    "col3": vervaldata_row_5_col_3,
                                    "info": vervaldata_row_5_info
                                },
                                {
                                    "col1": vervaldata_row_6_col_1,
                                    "col2": vervaldata_row_6_col_2,
                                    "col3": vervaldata_row_6_col_3,
                                    "info": vervaldata_row_6_info
                                },
                                {
                                    "col1": vervaldata_row_7_col_1,
                                    "col2": vervaldata_row_7_col_2,
                                    "col3": vervaldata_row_7_col_3,
                                    "info": vervaldata_row_7_info
                                }
                            ]
                        },
                        {
                            "title": "Gewichten",
                            "data": [
                                {
                                    "col1": gewichten_row_1_col_1,
                                    "col2": gewichten_row_1_col_2,
                                    "col3": gewichten_row_1_col_3,
                                    "info": gewichten_row_1_info
                                },
                                {
                                    "col1": gewichten_row_2_col_1,
                                    "col2": gewichten_row_2_col_2,
                                    "col3": gewichten_row_2_col_3,
                                    "info": gewichten_row_2_info
                                },
                                {
                                    "col1": gewichten_row_3_col_1,
                                    "col2": gewichten_row_3_col_2,
                                    "col3": gewichten_row_3_col_3,
                                    "info": gewichten_row_3_info
                                },
                                {
                                    "col1": gewichten_row_4_col_1,
                                    "col2": gewichten_row_4_col_2,
                                    "col3": gewichten_row_4_col_3,
                                    "info": gewichten_row_4_info
                                },
                                {
                                    "col1": gewichten_row_5_col_1,
                                    "col2": gewichten_row_5_col_2,
                                    "col3": gewichten_row_5_col_3,
                                    "info": gewichten_row_5_info
                                },
                                {
                                    "col1": gewichten_row_6_col_1,
                                    "col2": gewichten_row_6_col_2,
                                    "col3": gewichten_row_6_col_3,
                                    "info": gewichten_row_6_info
                                },
                                {
                                    "col1": gewichten_row_7_col_1,
                                    "col2": gewichten_row_7_col_2,
                                    "col3": gewichten_row_7_col_3,
                                    "info": gewichten_row_7_info
                                },
                            ]
                        },
                        {
                            "title": "Tellerstanden",
                            "data": [
                                {
                                    "col1": tellerstanden_row_1_col_1,
                                    "col2": tellerstanden_row_1_col_2,
                                    "col3": tellerstanden_row_1_col_3,
                                    "info": tellerstanden_row_1_info
                                },
                                {
                                    "col1": tellerstanden_row_2_col_1,
                                    "col2": tellerstanden_row_2_col_2,
                                    "col3": tellerstanden_row_2_col_3,
                                    "info": tellerstanden_row_2_info
                                },
                                {
                                    "col1": tellerstanden_row_3_col_1,
                                    "col2": tellerstanden_row_3_col_2,
                                    "col3": tellerstanden_row_3_col_3,
                                    "info": tellerstanden_row_3_info
                                },
                            ]
                        },
                        {
                            "title": "Status van het voertuig",
                            "data": [
                                {
                                    "col1": status_row_1_col_1,
                                    "col2": status_row_1_col_2,
                                    "col3": status_row_1_col_3,
                                    "info": status_row_1_info
                                },
                                {
                                    "col1": status_row_2_col_1,
                                    "col2": status_row_2_col_2,
                                    "col3": status_row_2_col_3,
                                    "info": status_row_2_info
                                },
                                {
                                    "col1": status_row_3_col_1,
                                    "col2": status_row_3_col_2,
                                    "col3": status_row_3_col_3,
                                    "info": status_row_3_info
                                },
                                {
                                    "col1": status_row_4_col_1,
                                    "col2": status_row_4_col_2,
                                    "col3": status_row_4_col_3,
                                    "info": status_row_4_info
                                },
                                {
                                    "col1": status_row_5_col_1,
                                    "col2": status_row_5_col_2,
                                    "col3": status_row_5_col_3,
                                    "info": status_row_5_info
                                },
                            ]
                        },
                        {
                            "title": "Terugroepacties",
                            "data": [
                                {
                                    "col1": terug_row_1_col_1,
                                    "col2": terug_row_1_col_2,
                                    "col3": terug_row_1_col_3,
                                    "info": terug_row_1_info
                                }
                            ]
                        }
                    ]
                },
                # category
                {
                    "title": "Motor & Milieu",
                    "sections": [
                        {
                            "title": "Motor",
                            "data": [
                                {
                                    "col1": motor_row_1_col_1,
                                    "col2": motor_row_1_col_2,
                                    "col3": motor_row_1_col_3,
                                    "info": motor_row_1_info
                                },
                                {
                                    "col1": motor_row_2_col_1,
                                    "col2": motor_row_2_col_2,
                                    "col3": motor_row_2_col_3,
                                    "info": motor_row_2_info
                                },
                                {
                                    "col1": motor_row_3_col_1,
                                    "col2": motor_row_3_col_2,
                                    "col3": motor_row_3_col_3,
                                    "info": motor_row_3_info
                                },
                                {
                                    "col1": motor_row_4_col_1,
                                    "col2": motor_row_4_col_2,
                                    "col3": motor_row_4_col_3,
                                    "info": motor_row_4_info
                                }
                            ]
                        },
                        {
                            "title": "Milieuprestaties",
                            "data": [
                                {
                                    "col1": mili_row_1_col_1,
                                    "col2": mili_row_1_col_2,
                                    "col3": mili_row_1_col_3,
                                    "col4": mili_row_1_col_4,
                                    "info": mili_row_1_info
                                },
                                {
                                    "col1": mili_row_2_col_1,
                                    "col2": mili_row_2_col_2,
                                    "col3": mili_row_2_col_3,
                                    "col4": mili_row_2_col_4,
                                    "info": mili_row_2_info
                                },
                                {
                                    "col1": mili_row_3_col_1,
                                    "col2": mili_row_3_col_2,
                                    "col3": mili_row_3_col_3,
                                    "col4": mili_row_3_col_4,
                                    "info": mili_row_3_info
                                },
                                {
                                    "col1": mili_row_4_col_1,
                                    "col2": mili_row_4_col_2,
                                    "col3": mili_row_4_col_3,
                                    "col4": mili_row_4_col_4,
                                    "info": mili_row_4_info
                                },
                                {
                                    "col1": mili_row_5_col_1,
                                    "col2": mili_row_5_col_2,
                                    "col3": mili_row_5_col_3,
                                    "col4": mili_row_5_col_4,
                                    "info": mili_row_5_info
                                },
                                {
                                    "col1": mili_row_6_col_1,
                                    "col2": mili_row_6_col_2,
                                    "col3": mili_row_6_col_3,
                                    "col4": mili_row_6_col_4,
                                    "info": mili_row_6_info
                                },
                                {
                                    "col1": mili_row_7_col_1,
                                    "col2": mili_row_7_col_2,
                                    "col3": mili_row_7_col_3,
                                    "col4": mili_row_7_col_4,
                                    "info": mili_row_7_info
                                },
                                {
                                    "col1": mili_row_8_col_1,
                                    "col2": mili_row_8_col_2,
                                    "col3": mili_row_8_col_3,
                                    "col4": mili_row_8_col_4,
                                    "info": mili_row_8_info
                                },
                                {
                                    "col1": mili_row_9_col_1,
                                    "col2": mili_row_9_col_2,
                                    "col3": mili_row_9_col_3,
                                    "col4": mili_row_9_col_4,
                                    "info": mili_row_9_info
                                },
                                {
                                    "col1": mili_row_10_col_1,
                                    "col2": mili_row_10_col_2,
                                    "col3": mili_row_10_col_3,
                                    "col4": mili_row_10_col_4,
                                    "info": mili_row_10_info
                                },
                                {
                                    "col1": mili_row_11_col_1,
                                    "col2": mili_row_11_col_2,
                                    "col3": mili_row_11_col_3,
                                    "col4": mili_row_11_col_4,
                                    "info": mili_row_11_info
                                },
                                {
                                    "col1": mili_row_12_col_1,
                                    "col2": mili_row_12_col_2,
                                    "col3": mili_row_12_col_3,
                                    "col4": mili_row_12_col_4,
                                    "info": mili_row_12_info
                                },
                                {
                                    "col1": mili_row_13_col_1,
                                    "col2": mili_row_13_col_2,
                                    "col3": mili_row_13_col_3,
                                    "col4": mili_row_13_col_4,
                                    "info": mili_row_13_info
                                },
                                {
                                    "col1": mili_row_14_col_1,
                                    "col2": mili_row_14_col_2,
                                    "col3": mili_row_14_col_3,
                                    "col4": mili_row_14_col_4,
                                    "info": mili_row_14_info
                                },
                            ]
                        },
                        {
                            "title": "Uitstoot",
                            "data": [
                                {
                                    "col1": ultstoot_row_1_col_1,
                                    "col2": ultstoot_row_1_col_2,
                                    "col3": ultstoot_row_1_col_3,
                                    "col4": ultstoot_row_1_col_4,
                                    "info": ultstoot_row_1_info
                                },
                                {
                                    "col1": ultstoot_row_2_col_1,
                                    "col2": ultstoot_row_2_col_2,
                                    "col3": ultstoot_row_2_col_3,
                                    "col4": ultstoot_row_2_col_4,
                                    "info": ultstoot_row_2_info
                                },
                                {
                                    "col1": ultstoot_row_3_col_1,
                                    "col2": ultstoot_row_3_col_2,
                                    "col3": ultstoot_row_3_col_3,
                                    "col4": ultstoot_row_3_col_4,
                                    "info": ultstoot_row_3_info
                                },
                                {
                                    "col1": ultstoot_row_4_col_1,
                                    "col2": ultstoot_row_4_col_2,
                                    "col3": ultstoot_row_4_col_3,
                                    "col4": ultstoot_row_4_col_4,
                                    "info": ultstoot_row_4_info
                                },
                                {
                                    "col1": ultstoot_row_5_col_1,
                                    "col2": ultstoot_row_5_col_2,
                                    "col3": ultstoot_row_5_col_3,
                                    "col4": ultstoot_row_5_col_4,
                                    "info": ultstoot_row_5_info
                                },
                                {
                                    "col1": ultstoot_row_6_col_1,
                                    "col2": ultstoot_row_6_col_2,
                                    "col3": ultstoot_row_6_col_3,
                                    "col4": ultstoot_row_6_col_4,
                                    "info": ultstoot_row_6_info
                                },
                                {
                                    "col1": ultstoot_row_7_col_1,
                                    "col2": ultstoot_row_7_col_2,
                                    "col3": ultstoot_row_7_col_3,
                                    "col4": ultstoot_row_7_col_4,
                                    "info": ultstoot_row_7_info
                                },
                                {
                                    "col1": ultstoot_row_8_col_1,
                                    "col2": ultstoot_row_8_col_2,
                                    "col3": ultstoot_row_8_col_3,
                                    "col4": ultstoot_row_8_col_4,
                                    "info": ultstoot_row_8_info
                                },
                                {
                                    "col1": ultstoot_row_9_col_1,
                                    "col2": ultstoot_row_9_col_2,
                                    "col3": ultstoot_row_9_col_3,
                                    "col4": ultstoot_row_9_col_4,
                                    "info": ultstoot_row_9_info
                                },
                                {
                                    "col1": ultstoot_row_10_col_1,
                                    "col2": ultstoot_row_10_col_2,
                                    "col3": ultstoot_row_10_col_3,
                                    "col4": ultstoot_row_10_col_4,
                                    "info": ultstoot_row_10_info
                                },
                                {
                                    "col1": ultstoot_row_11_col_1,
                                    "col2": ultstoot_row_11_col_2,
                                    "col3": ultstoot_row_11_col_3,
                                    "col4": ultstoot_row_11_col_4,
                                    "info": ultstoot_row_11_info
                                },
                            ]
                        },
                    ]
                },
                #category
                {
                    "title": "Technisch",
                    "sections": [
                        {
                            "title": "Eigenschappen",
                            "data": [
                                {
                                    "col1": elgen_row_1_col_1,
                                    "col2": elgen_row_1_col_2,
                                    "col3": elgen_row_1_col_3,
                                    "info": elgen_row_1_info
                                },
                                {
                                    "col1": elgen_row_2_col_1,
                                    "col2": elgen_row_2_col_2,
                                    "col3": elgen_row_2_col_3,
                                    "info": elgen_row_2_info
                                },
                                {
                                    "col1": elgen_row_3_col_1,
                                    "col2": elgen_row_3_col_2,
                                    "col3": elgen_row_3_col_3,
                                    "info": elgen_row_3_info
                                },
                                {
                                    "col1": elgen_row_4_col_1,
                                    "col2": elgen_row_4_col_2,
                                    "col3": elgen_row_4_col_3,
                                    "info": elgen_row_4_info
                                },
                                {
                                    "col1": elgen_row_5_col_1,
                                    "col2": elgen_row_5_col_2,
                                    "col3": elgen_row_5_col_3,
                                    "info": elgen_row_5_info
                                },
                                {
                                    "col1": elgen_row_6_col_1,
                                    "col2": elgen_row_6_col_2,
                                    "col3": elgen_row_6_col_3,
                                    "info": elgen_row_6_info
                                },
                            ]
                        },
                        {
                            "title": "Assen",
                            "data": [
                                {
                                    "col1": assen_row_1_col_1,
                                    "col2": assen_row_1_col_2,
                                    "col3": assen_row_1_col_3,
                                    "info": assen_row_1_info
                                },
                                {
                                    "col1": assen_row_2_col_1,
                                    "col2": assen_row_2_col_2,
                                    "col3": assen_row_2_col_3,
                                    "info": assen_row_2_info
                                },
                                {
                                    "col1": assen_row_3_col_1,
                                    "col2": assen_row_3_col_2,
                                    "col3": assen_row_3_col_3,
                                    "info": assen_row_3_info
                                },
                                {
                                    "col1": assen_row_4_col_1,
                                    "col2": assen_row_4_col_2,
                                    "col3": assen_row_4_col_3,
                                    "info": assen_row_4_info
                                },
                                {
                                    "col1": assen_row_5_col_1,
                                    "col2": assen_row_5_col_2,
                                    "col3": assen_row_5_col_3,
                                    "info": assen_row_5_info
                                },
                                {
                                    "col1": assen_row_6_col_1,
                                    "col2": assen_row_6_col_2,
                                    "col3": assen_row_6_col_3,
                                    "info": assen_row_6_info
                                },
                                {
                                    "col1": assen_row_7_col_1,
                                    "col2": assen_row_7_col_2,
                                    "col3": assen_row_7_col_3,
                                    "info": assen_row_7_info
                                },
                            ]
                        },
                    ]
                },
                #category
                {
                    "title": "Fiscaal",
                    "sections": [
                        {
                            "title": "Flscaal",
                            "data": [
                                {
                                    "col1": flscaal_row_1_col_1,
                                    "col2": flscaal_row_1_col_2,
                                    "info": flscaal_row_1_info
                                },
                                {
                                    "col1": flscaal_row_2_col_1,
                                    "col2": flscaal_row_2_col_2,
                                    "info": flscaal_row_2_info
                                },
                                {
                                    "col1": flscaal_row_3_col_1,
                                    "col2": flscaal_row_3_col_2,
                                    "link": flscaal_row_3_link,
                                    "info": flscaal_row_3_info
                                },
                            ]
                        }
                    ]
                }
            ]
        }
        # creating json file to upload to s3
        json_object = json.dumps(response_data, indent=4) #serializing
        with open('data.json', 'w') as outfile:
            outfile.write(json_object)
        # store rdw data into database and s3
        filename = str(license) + ".json"
        license_database = LicenseDatabaseS3Link()
        license_database.license_number = license
        license_database.license_data_json = File(file=open("data.json", 'rb'), name=filename)
        license_database.save()
        get_link = LicenseDatabaseS3Link.objects.last()
        url = get_link.license_data_json.url
        os.remove('data.json')
        return (response_data, url)
    except TimeoutException:
        driver.close()
        response_data = {
            "status": False,
            "title": license,
            "errMsg": "ASD is geen geldig kenteken. Voer een geldig kenteken in en klik op de knop 'Zoeken'."
        }
        return (response_data, None)