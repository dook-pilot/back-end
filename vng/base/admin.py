from django.contrib import admin
from .models import Company, LicensePlate, User, TargetImage, LicenseDatabaseS3Link, History


class LicensePlateAdmin(admin.ModelAdmin):
    list_display = ['license_number']
    readonly_fields = ('target_image',)


class TargetImageAdmin(admin.ModelAdmin):
    list_display = ['image_id', 'title']
    readonly_fields = ('image', 'user',)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['hid', 'title']
    readonly_fields = ('user', 'image',)


class LicenseDatabaseS3LinkAdmin(admin.ModelAdmin):
    list_display = ['license_number']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_id', 'place_api_company_name']


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(User)
admin.site.register(LicensePlate, LicensePlateAdmin)
admin.site.register(TargetImage, TargetImageAdmin)
admin.site.register(LicenseDatabaseS3Link, LicenseDatabaseS3LinkAdmin)
