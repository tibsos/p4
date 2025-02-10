from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('get_data_by_date/', views.get_data_by_date, name='get_data_by_date'),
]
