from base import s3_config
import boto3

def downloadRdwJson(file_name):
    print(file_name)
    s3 = boto3.client(
        's3', aws_access_key_id=s3_config.config["ACCESS_KEY"],
        aws_secret_access_key=s3_config.config["SECRET_KEY"])
    bucket = s3_config.config["BUCKET"]
    s3.download_file(bucket, 'license_data/' + str(file_name), file_name)