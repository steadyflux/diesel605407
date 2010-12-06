from django.db import models
from django.contrib.localflavor.us.forms import USStateField
from django.contrib.localflavor.us.forms import USZipCodeField
from django.forms.models import ModelForm
from django.contrib.auth.models import User

DIESEL_TYPE = (
               ("Unknown","-"),
               ("ULSD_40","Ultra Low Sulfer Diesel 40 Centane"),
               ("ULSD_OVER_40","Ultra Low Sulfer Diesel Above 40 Centane"),
               ("LSD","Low Sulfer Diesel"),
              )

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)

    vehicles = models.ManyToManyField('Vehicle')
    lucky_number = models.IntegerField(blank=True, null=True)

class Station(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128, verbose_name='Address', blank=True, null=True)
    city = models.CharField(max_length=64, verbose_name='City', blank=True, null=True)
    state = models.CharField(max_length=32, verbose_name='State', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, null=True)
    
    has_separate_diesel_pumps = models.NullBooleanField()
    is_not_gas_station = models.NullBooleanField()
    diesel_grade = models.CharField(max_length=128, choices=DIESEL_TYPE, default='Unknown') 

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def current_price(self):
        try:
            return FuelPrice.objects.filter(station=self).latest('created').price
        except:
            return '-'

    def __unicode__(self):
        return self.name + " - " + self.address + " " + self.city + ", " + self.state

class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ['address', #This form uses a subset of fields from the model
                  'city',
                  'state',
                  'zip',
                  'phone']
        widgets = {
                  'zip'    : USZipCodeField(),
                  'state'  : USStateField(),
        }

class StationUserComments(models.Model):
    station = models.ForeignKey(Station)
    user = models.ForeignKey(User, unique=False)
    created = models.DateTimeField(auto_now_add=True) 
    text = models.TextField()

class StationUserCommentsForm(ModelForm):
    class Meta:
        model = StationUserComments
        fields = ['text']   

class FuelPrice(models.Model):
    station = models.ForeignKey(Station)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)   
    
    def __unicode__(self):
        return str(self.station.name) + " - $%(num).2f - " % {"num" : self.price} + self.created.strftime("%m/%d/%Y")

class Vehicle(models.Model):
    owner = models.ManyToManyField('UserProfile')
    
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    color = models.CharField(max_length=20)
    trim = models.CharField(max_length=20)
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.make

class Announcement(models.Model):
    title = models.CharField(max_length=20)
    text = models.TextField()
    created_by = models.ForeignKey(User)    
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        exclude = ('created_by',)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
     
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user','vehicles']