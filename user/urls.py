from django.urls import path

from .views import *

urlpatterns = [

    path('4d-log1n', log_in),
    path('logout', log_out),

]