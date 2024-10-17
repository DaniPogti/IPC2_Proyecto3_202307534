from django import forms

class FileForms(forms.Form):
    file = forms.FileField(label='file')