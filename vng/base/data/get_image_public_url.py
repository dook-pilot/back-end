import boto3
from botocore.client import Config
from base.s3_config import config
from base.models import TargetImage


def get_img_url(image_id):
    s3 = boto3.resource(
        's3',
        region_name="eu-central-1",
        aws_access_key_id=config['ACCESS_KEY'],
        aws_secret_access_key=config['SECRET_KEY'],
        config=Config(signature_version='s3v4')
    )
    image_instance = TargetImage.objects.get(image_id=image_id)
    s3_url = image_instance.image.url
    s3_position = s3_url.index('media')
    key = s3_url[s3_position:]
    url = s3.meta.client.generate_presigned_url(
        "get_object", Params={'Bucket': config['BUCKET'], 'Key': key},
        ExpiresIn=3600
    )
    return url
