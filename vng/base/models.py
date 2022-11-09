from django.db import models

# Create your models here.

class LicensePlateCompanyData(models.Model):
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
    license_number = models.TextField(null=True)
    image = models.FileField(upload_to='media/')
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.place_api_company_name
