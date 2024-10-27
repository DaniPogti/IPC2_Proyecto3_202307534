from django.shortcuts import render
from .forms import FileForms
import requests

# Create your views here.

def index(request):
    ContenidoXml = None
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml})

def mostrar(request):
    ContenidoXml = ""
    
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml})

def subirXML(request):
    ContenidoXml = ""
    
    if request.method == 'POST':
        ContenidoXml = request.POST['archivo']
        print(ContenidoXml)
        
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml})   
    
 