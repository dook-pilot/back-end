from django.contrib import admin
from .models import Company, LicensePlate, TargetImage

class LicensePlateAdmin(admin.ModelAdmin):
    list_display=['id', 'license_number', 'company']
    readonly_fields=('company', 'target_image',)

class TargetImageAdmin(admin.ModelAdmin):
    list_display=['id', 'image_name']
    readonly_fields=('company',)

class CompanyAdmin(admin.ModelAdmin):
    list_display=['id', 'place_api_company_name']
# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(LicensePlate, LicensePlateAdmin)
admin.site.register(TargetImage, TargetImageAdmin)
