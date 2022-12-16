import cv2, os
import numpy as np
from paddleocr import PaddleOCR, draw_ocr
from transformers import YolosFeatureExtractor, YolosForObjectDetection
import matplotlib.pyplot as plt
import torch
from difflib import SequenceMatcher,get_close_matches
import re
from PIL import *
import pandas as pd
import numpy as np
import io
from PIL import Image
from deep_translator import GoogleTranslator
t = GoogleTranslator(source='auto', target='en')



class license_company_recognition_pipeline():
    def __init__(self, ocr_model_path='', detection_model_path='', feature_extractor_model_path='', csv_file_path=""):
        self.ocr_model_path = ocr_model_path
        self.detection_model_path = detection_model_path
        self.feature_extractor_model_path = feature_extractor_model_path
        self.csv_file_path = csv_file_path
        self.license_number = ""
    def load_models(self):
        model_dict = dict()
        # OCR Model
        if self.ocr_model_path == 'pretrained':
            model_dict['ocr_model'] = PaddleOCR(use_angle_cls=True, lang='en',
                                                ocr_version='PP-OCRv3')  # need to run only once to download and load model into memory
            # detection model
        if self.detection_model_path:
            model_dict['detection_model'] = YolosForObjectDetection.from_pretrained(
                'nickmuchi/yolos-small-rego-plates-detection')
            # feature extraction model
        if self.feature_extractor_model_path:
            model_dict['feature_extractor'] = YolosFeatureExtractor.from_pretrained(
                'nickmuchi/yolos-small-rego-plates-detection')
            # Translator model
        model_dict["translator"] = GoogleTranslator(source='auto', target='en')
        self.model_dict = model_dict
        return model_dict  # dictionary of loaded model
    def detectLicensePlate(self, image):
        image = image
        flag = False
        inputs = self.model_dict["feature_extractor"](images=image, return_tensors="pt")
        outputs = self.model_dict["detection_model"](**inputs)
        # model predicts bounding boxes and corresponding face mask detection classes
        logits = outputs.logits
        bboxes = outputs.pred_boxes
        target_sizes = torch.tensor([image.size[::-1]])
        results = self.model_dict["feature_extractor"].post_process(outputs, target_sizes=target_sizes)[0]
        plates = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            # let's only keep detections with score > 0.9
            if score > 0.7:
                if self.model_dict["detection_model"].config.id2label[label.item()] == 'license-plates':
                    # print(
                    # f"Detected {self.model_dict["detection_model"].config.id2label[label.item()]} with confidence "
                    # f"{round(score.item(), 3)} at location {box}.")
                    flag = True
                    bbox = box  # (center_x, center_y, width, height)
                    if flag == True:
                        r_box = [int(round(item, 0)) for item in bbox]
                        offset = 10
                        im1 = image.crop((bbox[0] - offset, bbox[1] - offset, bbox[2] + offset, bbox[3] + offset))
                        image_path = 'detected.jpg'
                        im1.save(image_path)
                        img = cv2.imread(image_path, 1)
                        img = cv2.resize(img, None, fx=10, fy=10, interpolation=cv2.INTER_CUBIC)
                        # (thresh, img) = cv2.threshold(img, 85, 255, cv2.THRESH_BINARY)
                        cv2.imwrite(image_path, img)
                        license_numberr = ''
                        result = (self.model_dict["ocr_model"]).ocr(image_path, cls=True)
                        # print(result)
                        ic = image.crop(r_box)
                        for i in range(30):  # with the BLUR filter, you can blur a few times to get the effect you're seeking
                            ic = ic.filter(ImageFilter.BLUR)
                        image.paste(ic, r_box)
                        license_numberr = str(result[0][1][0])
                        # for line in result:
                            # if len(line)>0:
                            #     print(line)
                            #     license_number = license_number + " " + str(line[1][0])
                        if license_numberr!= '':
                            plates.append(license_numberr.strip())
                            print(f"Vehicle Licence Number:  {license_numberr}\n\n")
                        else:
                            print('No license number is detected')
                    else:
                       print('No license number is detected')
                    self.license_number = license_numberr
        blurred_image_path = 'blurred_image.png'
        image.save(blurred_image_path)
        return plates, blurred_image_path
    def recognizeCompanyName(self, blurred_image_path):
        img = cv2.imread(blurred_image_path, 1)
        img = cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(blurred_image_path, img)
        text = ''
        result = self.model_dict["ocr_model"].ocr(blurred_image_path, cls=True)
        
        if len(result) != 0:
            print("OCR Result: {}".format(result[0]))
            # for line in result[0]:
            #     print(line)
            #     text = text + " " + str(line[0])
            for line in result:
                print(line)
                text = text +" " + line[1][0]
            text = text.replace(self.license_number, '')
            print("[+] TEXT: {}".format(text))
            return text
        else:
            print("No text data found!")
            return ""
    def finding_stopwords(self, df):
        word_counts = {}
        for name in df['place_api_company_name'].tolist():
            for word in name.split():
                if word in word_counts.keys():
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
        word_counts = {k.lower(): v for k, v in word_counts.items() if v > 5}
        stop_words = list(word_counts.keys())
        rms = ['kia', 'louwman', 'leiden', 'rotterdam', 'katwijk', 'noordwijk', 'leiderdorp', 'davo', 'zoetermeer']
        for w in rms:
            if w in stop_words:
                stop_words.remove(w)
        adds = ['repair', 'succes', 'class', 'haag', 'automobielen', 'sales', 'classic', 'classics',
                'Automobielbedrijf', 'automobielbedrijf', 'kerketuinen', 'forepark', 'motorhuis', 'brand', 'group',
                'dealer', 'automotives', 'Automotive company', 'automotive company', 'kerketuinen', 'forepark',
                'motor home', 'automobiles', 'cars', 'car', 'Car', 'Cars', 'car service',
                'autobedrijf', 'auto', 'company', 'AutoCenter', 'house', 'garage', 'the hague', 'autobedrijf',
                'company', 'corporal', 'bovag', 'BOVAG', 'smart', 'purchasing', 'sales', 'import', 'export',
                ' valuation', 'investing', ' is', 'bought', 'with', 'a', 'lease', 'financial', 'leasing', 'specialized',
                'in', 'mercedes', 'air', 'conditioning', 'repairs', 'maintenance', 'diagnosis',
                'body', 'tire', 'service', 'road', 'loan', 'service', 'leveling', 'systems']
        for w in adds:
            stop_words.append(w)
        return stop_words
    def stopwords_removal(self, text, stop_words):
        query = ''
        text = text.lower()
        text = ''.join(re.findall("[A-Za-z ]", text))
        for word in text.split():
            if word.lower() not in stop_words and len(word) > 3 and len(word) < 15:
                query = query + word.lower() + ' '
        return query
    def retrieving_final_results(self, detected_text):
        #print(self.csv_file_path)
        df = pd.read_csv(self.csv_file_path)
        stop_words = self.finding_stopwords(df)
        indices = []
        detected_text = self.stopwords_removal(
            self.model_dict["translator"].translate(self.stopwords_removal(detected_text, stop_words)), stop_words)
        name_lowers = [name.lower() for name in df['place_api_company_name'].tolist()]
        for token in detected_text.split():
            for i, name in enumerate(name_lowers):
                if token in name:
                    indices.append(i)
        # print(indices)
        similarities = [SequenceMatcher(a=self.stopwords_removal(detected_text, stop_words), b=name_lowers[i]).ratio()
                        for i in indices]
        # print(similarities)
        if len(similarities) == 0:
            return {'error': 'true'}
        else:
            response = df[
                ['place_api_company_name', 'bovag_matched_name', 'poitive_reviews', 'negative_reviews', 'rating',
                 'duplicate_location', 'kvk_tradename',
                 'irregularities', 'duplicates_found', 'Bovag_registered', 'KVK_found',
                 'company_ratings']].iloc[indices[np.argmax(similarities)]].to_dict()
            response['error'] = 'false'
            return (response)
    def run(self, image):
        models = self.load_models()  # load models
        plates, blurred_image_path = self.detectLicensePlate(image)
        text = self.recognizeCompanyName(blurred_image_path)
        results = self.retrieving_final_results(text)
        # print(text)
        return results, plates
data_directory = f'{os.getcwd()}/base/10-08-22'
companies_details_csv = f'{data_directory}/674_records_final_result_merged_with_updated_bovag_merged_reviews_and_irregularities.csv'#place_api_car_companies_indicators.csv'
pipeline = license_company_recognition_pipeline(ocr_model_path='pretrained',
                                                detection_model_path='nickmuchi/yolos-small-rego-plates-detection',
                                                feature_extractor_model_path='nickmuchi/yolos-small-rego-plates-detection' ,
                                                csv_file_path = companies_details_csv)
models = pipeline.load_models() # load models
def get_image_upload_license_company_res(imagee):
    #print('inside function license plate recognition')
    image = Image.open(io.BytesIO(imagee)).convert('RGB')
    # image = Image.open(imagee).convert('RGB')
    width, height = image.size
    print(image.size)
    raw_image_path = 'raw_image.jpg'
    if width >= 3000 or height >= 3000:
        # image = image.rotate(270, expand=True)
        image.save(raw_image_path)
        img=cv2.imread(raw_image_path)
        img = cv2.resize(img, None, fx = 0.50, fy = 0.50)
        cv2.imwrite(raw_image_path,img)
        im1 = Image.open(raw_image_path).rotate(270, expand=True).convert('RGB')
        # width = int(width/1.5)
        # height = int(height/1.5)
        # newsize = (width, height)
        # im1 = image.resize(newsize)
        print(im1.size)
        # plt.imshow(im1)
        # plt.show() 
        df_dict, plates = pipeline.run(im1)
        # pipeline.run(im1)
        df_dict['license_number'] = plates
        print(df_dict['license_number'])
        # df_dict["status"] = True
        # df_dict["errMsg"] = None
        return df_dict
    else:
        # pipeline.run(image)
        df_dict, plates = pipeline.run(image)
        df_dict['license_number'] = plates
        print(df_dict['license_number'])
        # df_dict["status"] = True
        # df_dict["errMsg"] = None
        return df_dict