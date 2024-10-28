from django.shortcuts import render
from .forms import FileForms
import requests

# Create your views here.

api = 'http://localhost:5000'

def index(request):
    ContenidoXml = None
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml})
    
def leerArchivoXML(request):
    ContenidoXml = ""
    
    if request.method == 'POST':
        form = FileForms(request.POST, request.FILES)
        
        if form.is_valid():
            archivo = form.cleaned_data['archivo']
            ContenidoXml = archivo.read().decode('utf-8')
            
            print(ContenidoXml)
        else:
            print(form.errors)
    
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml})
def subirXML(request):
    ContenidoXml = ""
    mensaje = ""
    
    if request.method == 'POST':
        ContenidoXml = request.POST.get('xml', '')
        
        limpiarXML = ContenidoXml.encode('utf-8')
        
        try:
            response = requests.post(api + '/LeerXML', data={'xml': ContenidoXml})  # comunica con backend
            if response.status_code == 200:
                mensaje = "Archivo enviado correctamente"
                print("Archivo enviado correctamente")
                print(ContenidoXml)
            else:
                mensaje = "Error al enviar el archivo"
                print("Error al enviar el archivo")
        except requests.ConnectionError as e:
            mensaje = f"Error de conexión: {e}"
            print(f"Error de conexión: {e}")
    
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml, 'mensaje': mensaje})
