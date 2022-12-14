from django.contrib import admin
from .models import Company, LicensePlate, TargetImage, LicenseDatabaseS3Link

class LicensePlateAdmin(admin.ModelAdmin):
    list_display=['license_plate_id', 'license_number']
    readonly_fields=('target_image',)

class TargetImageAdmin(admin.ModelAdmin):
    list_display=['image_id', 'image_name']
    readonly_fields=('image',)
class LicenseDatabaseS3LinkAdmin(admin.ModelAdmin):
    list_display=['id', 'license_number']

class CompanyAdmin(admin.ModelAdmin):
    list_display=['company_id', 'place_api_company_name']
# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(LicensePlate, LicensePlateAdmin)
admin.site.register(TargetImage, TargetImageAdmin)
admin.site.register(LicenseDatabaseS3Link, LicenseDatabaseS3LinkAdmin)
