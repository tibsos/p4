from django.urls import path

from .views import *

urlpatterns = [

    path('', landing),

    path('t', save_leave_time),

    path('b', button_click),
    
    path('c', receive_contact_info),

    path('d', discount_timer),

    path('test', test),

]