from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_data, name="upload"),
    path('get-history/<str:user_id>/', views.getHistory, name="get_history"),
]
