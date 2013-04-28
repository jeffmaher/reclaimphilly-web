from django import forms
from reclaimcities.apps.web.models import Location

# TODO plusjeff make some of the values in this class constants to be used between forms and models

class AddLocation(forms.ModelForm):
    class Meta:
        model = Location
