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
    def __str__(self):
        return self.place_api_company_name
    class Meta:
        verbose_name_plural = "Companies"

class TargetImage(models.Model):
    image = models.FileField(upload_to='media/')
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    def __str__(self):
        return self.company.place_api_company_name

class LicensePlate(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    target_image = models.ForeignKey(to=TargetImage, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.license_number


class WorldBorder(models.Model):
    fips = models.CharField(max_length=2)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    un = models.IntegerField()
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.BigIntegerField()
    region = models.IntegerField()
    subregion = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)


# Auto-generated `LayerMapping` dictionary for WorldBorder model
worldborder_mapping = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'geom': 'MULTIPOLYGON',
}
