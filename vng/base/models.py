from django.db import models
from django.contrib.gis.db import models
# Create your models here.

class Company(models.Model):
    place_api_company_name = models.CharField(max_length=255, null=True)
    bovag_matched_name = models.CharField(max_length=255, null=True)
    poitive_reviews = models.IntegerField(null=True)
    negative_reviews = models.IntegerField(null=True)
    rating = models.FloatField(null=True)
    duplicate_location = models.CharField(max_length=50, null=True)
    kvk_tradename = models.TextField(null=True)
    irregularities = models.CharField(max_length=50, null=True)
    duplicates_found = models.CharField(max_length=50, null=True)
    Bovag_registered = models.CharField(max_length=50, null=True)
    KVK_found = models.CharField(max_length=50, null=True)
    company_ratings = models.CharField(max_length=50, null=True)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    geom = models.PointField(srid=4326, spatial_index=True, null=True)
    createdAt = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.place_api_company_name
    class Meta:
        verbose_name_plural = "Companies"

class TargetImage(models.Model):
    image = models.FileField(upload_to='media/')
    image_name = models.CharField(max_length=255, null=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    def __str__(self):
        return self.image_name

class LicensePlate(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    target_image = models.ForeignKey(to=TargetImage, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.license_number
