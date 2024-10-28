from django import forms

class FileForms(forms.Form):
    archivo = forms.FileField(label='archivo')