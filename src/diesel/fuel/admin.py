'''
Created on Nov 13, 2010

@author: ktbaynes
'''
from django.contrib import admin
from diesel.fuel.models import Station, Vehicle, Announcement, FuelPrice,\
    StationUserComments

admin.site.register(Station)
admin.site.register(FuelPrice)
admin.site.register(Vehicle)
admin.site.register(Announcement)
admin.site.register(StationUserComments)