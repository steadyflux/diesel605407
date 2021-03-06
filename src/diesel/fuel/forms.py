'''
Created on Nov 21, 2010

@author: ktbaynes
'''
from django import forms
from django.contrib.localflavor.us.forms import USStateField, USZipCodeField
from diesel.fuel.models import DIESEL_TYPE

NUM_RESULTS = (
               ('5', '5'),
               ('10', '10'),
               ('20', '20'),
             )

class SearchForm(forms.Form):
    num_results = forms.ChoiceField(choices=NUM_RESULTS)
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = USStateField(required=False)
    zip = USZipCodeField(required=False)
    centane_rating = forms.ChoiceField(choices=DIESEL_TYPE)
    
class UploadFileForm(forms.Form):
    file  = forms.FileField()
    
class PriceForm(forms.Form):
    price = forms.CharField()
    
    