from django import forms
from .models import Category

class AuctionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label="Description")
    image = forms.ImageField(required=False)
    category = forms.ChoiceField(choices=Category.choices, initial=Category.OTHER, widget=forms.Select(attrs={'class': 'form-control'}))
    start_bid = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))

class BidForm(forms.Form):
    bid_price = forms.DecimalField(min_value=0, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'autofocus': 'autofucus'}))