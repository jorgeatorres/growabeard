# encoding: utf-8
from django import forms
from .models import CampaignEntry


class UploadForm(forms.Form):
    image = forms.ImageField()
