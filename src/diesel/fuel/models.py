from django.db import models
from django.contrib.localflavor.us.forms import USStateField
from django.contrib.localflavor.us.forms import USZipCodeField
from django.forms.models import ModelForm
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)

    vehicles = models.ManyToManyField('Vehicle')
    lucky_number = models.IntegerField(blank=True, null=True)

class Station(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=128, verbose_name='Address')
    city = models.CharField(max_length=64, verbose_name='City')
    state = models.CharField(max_length=32, verbose_name='State')
    zip = models.CharField(max_length=10, verbose_name='Zip')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ('address', #This form uses a subset of fields from the model
                  'city',
                  'state',
                  'zip',
                  'phone')
        widgets = {
                  'zip'    : USZipCodeField(),
                  'state'  : USStateField(),
        }

class Vehicle(models.Model):
    
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