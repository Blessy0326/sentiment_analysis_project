from django import forms
from django.forms import ModelForm
from .models import Review_added,Product
class RateForm(ModelForm):
    class Meta:
        model = Review_added
        fields = ('product_selected','review')
        labels = {
            'product_selected':'',
            'review': 'Review',

        }
        widgets = {
            'product_selected':forms.TextInput(attrs={'class': 'form-control','placeholder':'enter product name'}),
            'review': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your feedback'}),
        }
