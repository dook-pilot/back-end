from django.contrib import admin
from .models import Company, LicensePlate, TargetImage

class LicensePlateAdmin(admin.ModelAdmin):
    readonly_fields=('company', 'target_image',)

class TargetImageAdmin(admin.ModelAdmin):
    readonly_fields=('company',)


# Register your models here.
admin.site.register(Company)
admin.site.register(LicensePlate, LicensePlateAdmin)
admin.site.register(TargetImage, TargetImageAdmin)