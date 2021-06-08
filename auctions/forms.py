from .models import *

from django import forms
from django.forms import ModelForm

from django.db import models


class CreateNewListing(ModelForm):
    class Meta:
        model = NewListing
        fields = ('title', 'description', 'bid', 'image', 'category')

        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Type the title here...'}),
            'description': forms.Textarea(
                attrs={'class': "form-control", 'placeholder': 'Type the description here...'}),


        }


class AddComment(ModelForm):
    class Meta:
        model = Comment
        fields = ('__all__')

        widgets = {
            'body': forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Type the comment here...'}),

        }


class AddBid(ModelForm):
    class Meta:
        model = Bid
        fields = ('__all__')





class CloseBid(ModelForm):
    class Meta:

        model=NewListing
        fields=('title','openbid')
