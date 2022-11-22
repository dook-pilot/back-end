from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import Company, LicensePlate, TargetImage, WorldBorder

class LicensePlateAdmin(admin.ModelAdmin):
    readonly_fields=('company', 'target_image',)

class TargetImageAdmin(admin.ModelAdmin):
    readonly_fields=('company',)


# Register your models here.
admin.site.register(Company)
admin.site.register(WorldBorder, GISModelAdmin)
admin.site.register(LicensePlate, LicensePlateAdmin)
admin.site.register(TargetImage, TargetImageAdmin)
