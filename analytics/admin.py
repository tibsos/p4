from django.contrib import admin as a

from .models import Visit, Event

class VisitAdmin(a.ModelAdmin):

    list_display = ['mobile', 'entered_at', 'left_at']

a.site.register(Visit, VisitAdmin)

a.site.register(Event)