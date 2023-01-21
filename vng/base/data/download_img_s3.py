from base import s3_config
import boto3

def download_image(image_name):
    s3 = boto3.client(
        's3', aws_access_key_id=s3_config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=s3_config.AWS_SECRET_ACCESS_KEY)
    bucket = s3_config.AWS_STORAGE_BUCKET_NAME #config["BUCKET"]
    s3.download_file(bucket, 'media/'+str(image_name), image_name)