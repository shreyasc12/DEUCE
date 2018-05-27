from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms
from .models import Event


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "event_name",
            "sport",
            "Required_Players",
            "Available_Players",
            "date",
            "in_time",
            "out_time",
        ]
#class AddMember(forms.ModelForm):
#    class Meta:
#        model = Member
#        fields = [
#           "team",
#        ]
