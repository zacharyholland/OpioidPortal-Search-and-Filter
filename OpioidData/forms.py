from django import forms

class SearchDrugsForm(forms.Form) :
    q = forms.CharField(label='Search', max_length=50)