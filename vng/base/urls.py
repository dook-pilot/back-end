from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload, name="upload"),
    path('get-history/<str:user_id>/', views.getHistory, name="get_history"),
    path('get-data/<str:id>', views.getData, name="getData"),
]
