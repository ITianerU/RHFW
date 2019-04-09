from django import forms

class JobForm(forms.Form):
    position = forms.CharField(max_length=10)
    city = forms.CharField(max_length=10)
