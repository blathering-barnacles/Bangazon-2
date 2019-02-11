from django import forms
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.models import User
from ..models import

class DogForm(forms.Form):
  dog_name = forms.CharField(label='Dog name', max_length=20)
  breed = forms.CharField(label='Breed', max_length=20)
  chip_num = forms.IntegerField(label='Chip num')