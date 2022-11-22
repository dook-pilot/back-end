from django.urls import path
from . import views

urlpatterns = [
    path('license-plate/', views.vngp1_predict_license_plate, name="license_plate"),
    path('mvt-tiles/<int:zoom>/<int:x>/<int:y>', views.mvt_tiles, name="mvt-tiles"),
    path('companies-irregularities/<str:place_type>/', views.vngp1_predict_pre_extracted, name="place_type"),
]