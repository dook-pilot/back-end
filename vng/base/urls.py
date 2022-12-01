from django.urls import path
from . import views

urlpatterns = [
    path('get-image-data/', views.get_image, name="get_image_license_data"),
    path('get-license-data/', views.get_license_data, name="get_license_data"),
    path('license-plate/', views.vngp1_predict_license_plate, name="license_plate"),
]