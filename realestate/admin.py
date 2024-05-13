from django.contrib import admin
from .models import Event, Property, PropertyType, Neighborhood, SearchHistory

admin.site.register(Event)
admin.site.register(Property)
admin.site.register(PropertyType)
admin.site.register(Neighborhood)
admin.site.register(SearchHistory)


