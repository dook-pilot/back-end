from base.models import TargetImage

def image_url(target_image_id):
    target_image = TargetImage.objects.get(image_id=target_image_id)
    return target_image.image.url