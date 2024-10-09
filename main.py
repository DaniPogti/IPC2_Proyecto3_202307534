from flask import Flask, render_template, request, url_for, redirect
from xml.dom import minidom
from xml.dom.minidom import Document

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')


@app.route('/LeerXml', methods=['POST'])
def LeerXml():
    try:
        archivo = request.files['archivo']
        doc = minidom
        doc = minidom.parse(archivo)
        root = doc.documentElement
        print(root.tagName)
        
        solicitud = root.getElementsByTagName('solicitud_clasificacion')
        for raiz in solicitud:
            diccionario = raiz.getElementsByTagName('diccionario')
            for dic in diccionario:
                positivos = dic.getElementsByTagName('sentimientos_positivos')
                negativos = dic.getElementsByTagName('sentimientos_negativos')
                emprezaAnalizar = dic.getElementsByTagName('empresas_analizar')
                
                for positivo in positivos:
                    palabra = positivo.getElementsByTagName('palabra')
                    for pal in palabra:
                        good = pal.firstChild.nodeValue()
                        
                for negativo in negativos:
                    palabra = negativo.getElementsByTagName('palabra')
                    for pal in palabra:
                        bad = pal.firstChild.nodeValue()
                
                for emp in emprezaAnalizar:
                    empresa = emp.getElementsByTagName('empresa')
                    for emp in empresa:
                        nombre = emp.getElementsByTagName('nombre')
                        for nom in nombre:
                            name = nom.firstChild.nodeValue()
                        servicio = emp.getElementsByTagName('servicios')
                        for ser in servicio:
                            servicios = ser.getAttribute('nombre')
                            alias = ser.getElementsByTagName()
                            for ali in alias:
                                A_lias = ali.firstChild.nodeValue() 
            
            listaMensajes = raiz.getElementsByTagName('lista_mensajes')
            for listaM in listaMensajes:
                mensaje = listaM.getElementsByTagName('mensaje')
                for mens in mensaje:
                    txt = mens.firstChild.nodeValue()
               
    except Exception as e:
        return str(e)

@app.route('/ConsultarDatos', methods=['GET'])
def ConsultarD():
    pass

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