from django import forms

class HomeForm(forms.Form):
    City_Name = forms.CharField(label = "City Name:" )
class BasicForm(forms.Form):
    pass
