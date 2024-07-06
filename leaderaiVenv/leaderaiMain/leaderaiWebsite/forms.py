# forms.py

from django import forms
from .models import User

class SubscriptionForm(forms.Form):
    stripe_token = forms.CharField()
    subscription_type = forms.ChoiceField(choices=[('INSIGHT', 'Insight')])
