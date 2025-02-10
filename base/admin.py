from django.contrib import admin as a

from .models import *

class CustomerAdmin(a.ModelAdmin):

    list_display = ('website_type', 'name', 'email', 'phone', 'sent_at')

a.site.register(Customer, CustomerAdmin)
a.site.register(ButtonClick)