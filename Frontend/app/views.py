from django.shortcuts import render
from .forms import FileForms
import requests

# Create your views here.

def index(request):
    ContenidoXml = None
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml})

def mostrar(request):
    ContenidoXml = ""
    
    if request.method == 'POST':
        form = FileForms(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.cleaned_data['file']
            ContenidoXml = file.read().decode('utf-8')
        else:
            print(form.errors)
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml})
 