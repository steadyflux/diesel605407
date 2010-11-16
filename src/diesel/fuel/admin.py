'''
Created on Nov 13, 2010

@author: ktbaynes
'''
from django.contrib import admin
from diesel.fuel.models import Station, Vehicle, Announcement

admin.site.register(Station)
admin.site.register(Vehicle)
admin.site.register(Announcement)