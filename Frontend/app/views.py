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
        
        response = requests.post(api + '/LeerXML', data=limpiarXML)
        
        if response.status_code == 200:
            mensaje = "Datos enviados correctamente. Respuesta del servidor: " + response.text
        else:
            mensaje = f"Error al enviar los datos. Código de estado: {response.status_code} - {response.reason}"
    
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml, 'mensaje': mensaje})

def mandarXML(request):
    response = requests.get(api + '/EnvioXML')
    
    if response.status_code == 200:
        mensaje = response.text  # Pasar el contenido del XML al mensaje
    else:
        mensaje = f"Error al obtener los datos. Código de estado: {response.status_code} - {response.reason}"
    
    ContenidoXml = request.GET.get('xml', '')

    return render(request, 'index.html', {'ContenidoXml': ContenidoXml, 'mensaje': mensaje})

def Ayuda(request):
    return render(request, 'ayuda.html')

def Reset(request):
    response = requests.post(api + '/Reset')
    ContenidoXml = None
    
    if response.status_code == 200:
        mensaje = 'Datos reseteados correctamente'
    else:
        mensaje = f"Error al resetear: {response.status_code} - {response.reason}"

    
    return render(request, 'index.html', {'ContenidoXml': ContenidoXml, 'mensaje': mensaje})
