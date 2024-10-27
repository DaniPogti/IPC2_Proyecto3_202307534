from flask import Flask, render_template, request, url_for, redirect
#from flask_cors import CORS
from xml.dom import minidom
from xml.dom.minidom import Document
import re

app = Flask(__name__)

#CORS(app)

Clasificaciones = []
Diccionarios = []
Positivos = []
Negativos = []
Empresas = []
Servicios = []
Alias = []
Mensajes = []

class CLasificacion:
    def __init__(self, diccionario, listaMensaje):
        self.diccionario = diccionario
        self.listaMensajes = listaMensaje
        
class Diccionario:
    def __init__(self, positivo, negativo, empresa):
        self.positivos = positivo
        self.negativos = negativo
        self.empresas = empresa

class Positivo:
    def __init__(self, palabra):
        self.palabra = palabra

class Negativo:
    def __init__(self, palabra):
        self.palabra = palabra
        
class Message():
    def __init__(self, mensaje):
        self.mensaje = mensaje
        
class Empresa():
    def __init__(self, nombre, servicios):
        self.nombre = nombre
        self.servicios = servicios
        
class Servicio:
    def __init__(self, nombre, alias):
        self.nombre = nombre
        self.alias = alias
        
class Alia():
    def __init__(self, alias):
        self.alias = alias

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/mostrar', methods=['GET'])
def mostrar():
    return 'hola'
 #archivo = request.files['archivo']
        #doc = minidom
        #doc = minidom.parse(archivo)

@app.route('/LeerXml', methods=['POST'])
def LeerXml():
    try:
        xml_content = request.data.decode('utf-8')
        doc = minidom.parseString(xml_content)
        root = doc.documentElement
        
        positive = [] 
        negative = [] 
        company = [] 
        msj = []
        
        diccionario = root.getElementsByTagName('diccionario')
        for dic in diccionario:
            positivos = dic.getElementsByTagName('sentimientos_positivos')
            negativos = dic.getElementsByTagName('sentimientos_negativos')
            emprezaAnalizar = dic.getElementsByTagName('empresas_analizar')
            
            for positivo in positivos:
                palabras = positivo.getElementsByTagName('palabra')
                for pal in palabras:
                    good = pal.firstChild.nodeValue.strip()
                    positive.append(Positivo(good))
                    #Positivos.append(good)
                    print(f"Positivo: {good}")
                    
            for negativo in negativos:
                palabras = negativo.getElementsByTagName('palabra')
                for pal in palabras:
                    bad = pal.firstChild.nodeValue.strip()
                    negative.append(Negativo(bad))
                    #Negativos.append(bad)
                    print(f"Negativo: {bad}")
            
            for emp in emprezaAnalizar:
                empresa = emp.getElementsByTagName('empresa')
                for emp in empresa:
                    nombre = emp.getElementsByTagName('nombre')
                    listServicios = []
                    for nom in nombre:
                        name = nom.firstChild.nodeValue.strip()
                        print(f"Empresa: {name}")
                    servicio = emp.getElementsByTagName('servicio')
                    for ser in servicio:
                        servicios = ser.getAttribute('nombre')
                        listAlias = []
                        print(f"Servicio: {servicios}")
                        alias = ser.getElementsByTagName('alias')
                        for ali in alias:
                            A_lias = ali.firstChild.nodeValue.strip()
                            listAlias.append(Alia(A_lias))
                            print(f"Alias: {A_lias}")
                        listServicios.append(Servicio(servicios, listAlias))
                    empre = Empresa(name, listServicios)
                    company.append(empre)
                    print(f"Empresa: {nombre}")
                    
        dictionary = Diccionario(positive, negative, company)
        Diccionarios.append(dictionary)
        
        listaMensajes = root.getElementsByTagName('lista_mensajes')
        for listaM in listaMensajes:
            mensaje = listaM.getElementsByTagName('mensaje')
            for mens in mensaje:
                txt = mens.firstChild.nodeValue.strip()
                msj.append(Message(txt))
                print(f"Mensaje: {txt}")
                Mensajes.append(txt)
                
        Clasificaciones.append
        Clasify= CLasificacion(dictionary, msj)
        Clasificaciones.append(Clasify)
        
                
        return "XML leído correctamente e impreso en la consola"
    
    except Exception as e:
        return str(e)

@app.route('/ConsultarDatos', methods=['GET'])
def ConsultarD():
    try:
        resultado = ""

        # Recorrer la lista de Clasificaciones
        for clasificacion in Clasificaciones:
            resultado += "======== Clasificación ========\n"
            
            # recorre diccionario dentro de clasificación
            diccionario = clasificacion.diccionario
            resultado += "------- Diccionario -------\n"
            
            # Mostrar positivos
            resultado += "-> Sentimientos Positivos:\n"
            for pos in diccionario.positivos:
                resultado += f"    {pos.palabra}\n"
                
            # Mostrar negativas
            resultado += "-> Sentimientos Negativos:\n"
            for neg in diccionario.negativos:
                resultado += f"    {neg.palabra}\n"
                
            # Mostrar empresas y sus servicios
            resultado += " -> Empresas:\n"
            for empresa in diccionario.empresas:
                resultado += f"    Nombre: {empresa.nombre}\n"
                for servicio in empresa.servicios:
                    resultado += f"      Servicio: {servicio.nombre}\n"
                    for alias in servicio.alias:
                        resultado += f"        Alias: {alias.alias}\n"
            
            # Acceder a los mensajes
            resultado += "------- Lista de Mensajes -------\n"
            for mensaje in clasificacion.listaMensajes:
                resultado += f"*  {mensaje.mensaje}\n"

        return resultado

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
    

@app.route('/ConsultarFecha', methods=['POST'])
def ConsultarF():
    pass

@app.route('/ConsultarRangoFechas', methods=['POST'])
def ConsultarRF():
    pass

@app.route('/ProcesarMensaje', methods=['POST'])
def Procesar():
    pass

@app.route('/Grafica', methods=['GET'])
def Graficar():
    pass

if __name__ == '__main__':
    app.run(debug=True)