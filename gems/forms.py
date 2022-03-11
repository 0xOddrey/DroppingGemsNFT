from django import forms

from .models import *

class gemSearchForm(forms.Form):
    tokenId = forms.IntegerField()