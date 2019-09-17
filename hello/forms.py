from django import forms

class UrlForm(forms.Form):
    Url = forms.CharField(
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Url'}))
    Email = forms.CharField(widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Email Address'}))
    Price = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Price'}))