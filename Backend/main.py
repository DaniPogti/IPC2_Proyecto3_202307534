from flask import Flask, render_template, request, Response, url_for, redirect
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
        
def extract_dates(messages):
    date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    dates = []
    for message in messages:
        match = date_pattern.search(message)
        if match:
            dates.append(match.group())
    return dates

def count_messages_by_date(dates):
    date_counts = {}
    for date in dates:
        if date in date_counts:
            date_counts[date] += 1
        else:
            date_counts[date] = 1
    return date_counts

def classify_message(message):
    positive_count = sum(word in message for word in Positivos)
    negative_count = sum(word in message for word in Negativos)
    
    if positive_count == negative_count:
        return 'neutros'
    elif positive_count > negative_count:
        return 'positivos'
    else:
        return 'negativos'

def count_message_types_by_date(messages, dates):
    message_types_by_date = {}
    for message, date in zip(messages, dates):
        message_type = classify_message(message)
        if date not in message_types_by_date:
            message_types_by_date[date] = {'total': 0, 'positivos': 0, 'negativos': 0, 'neutros': 0}
        message_types_by_date[date]['total'] += 1
        if message_type == 'neutros':
            if message_types_by_date[date]['neutros'] == 0:
                message_types_by_date[date]['neutros'] = 1
        else:
            message_types_by_date[date][message_type] += 1
    return message_types_by_date

def dict_to_xml(message_types_by_date):
    doc = Document()
    root = doc.createElement('respuesta')
    doc.appendChild(root)
    
    for date, counts in message_types_by_date.items():
        date_element = doc.createElement('fecha')
        date_text = doc.createTextNode(date)
        date_element.appendChild(date_text)
        root.appendChild(date_element)
        
        messages_element = doc.createElement('mensajes')
        
        total_element = doc.createElement('total')
        total_text = doc.createTextNode(str(counts['total']))
        total_element.appendChild(total_text)
        
        positivos_element = doc.createElement('positivos')
        positivos_text = doc.createTextNode(str(counts['positivos']))
        positivos_element.appendChild(positivos_text)
        
        negativos_element = doc.createElement('negativos')
        negativos_text = doc.createTextNode(str(counts['negativos']))
        negativos_element.appendChild(negativos_text)
        
        neutros_element = doc.createElement('neutros')
        neutros_text = doc.createTextNode(str(counts['neutros']))
        neutros_element.appendChild(neutros_text)
        
        messages_element.appendChild(total_element)
        messages_element.appendChild(positivos_element)
        messages_element.appendChild(negativos_element)
        messages_element.appendChild(neutros_element)
        
        root.appendChild(messages_element)
    
    return doc.toprettyxml(encoding='utf-8')

@app.route('/countMessagesByDate', methods=['GET'])
def count_messages_by_date_endpoint():
    try:
        dates = extract_dates(Mensajes)
        message_types_by_date = count_message_types_by_date(Mensajes, dates)
        xml_response = dict_to_xml(message_types_by_date)
        return Response(xml_response, mimetype='application/xml')
    except Exception as e:
        print(f"Error: {e}")
        return Response("<error>Error al procesar los mensajes</error>", status=500, mimetype='application/xml')



@app.route('/')

def index():
    return render_template('index.html')
    
@app.route('/LeerXML', methods=['POST'])#para thunder client
def LeerXml1():
    try:
        xml_content = request.data.decode('utf-8')
        print("============Contenido XML recibido==============")
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
        print(f"Error: {e}")
        return "Error al procesar el archivo", 500

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
    

@app.route('/filtrarFechas', methods=['POST'])
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

@app.route('/mostrar', methods=['GET'])
def mostrar():
    return 'hola'
 #archivo = request.files['archivo']
        #doc = minidom
        #doc = minidom.parse(archivo)

#para backend
@app.route('/LeerXML1', methods=['POST'])
def LeerXml():
    try:
        xml_content = request.data.decode('utf-8')
        print("============Contenido XML recibido==============")
        data = minidom.parseString(xml_content)
        root = data.documentElement
        
        # Procesar el contenido del archivo XML aquí
        print(xml_content)
        print(root)
        return "Archivo procesado correctamente", 200
    except Exception as e:
        print(f"Error: {e}")
        return "Error al procesar el archivo", 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)