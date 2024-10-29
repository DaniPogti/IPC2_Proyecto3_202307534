from flask import Flask, render_template, request, Response, url_for, redirect
from xml.dom import minidom
from xml.dom.minidom import Document
import re

app = Flask(__name__)

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
        
def extraerFechas(mensajes):
    fech = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    dates = []
    for msg in mensajes:
        match = fech.search(msg)
        if match:
            dates.append(match.group())
    return dates

def clasificarMensaje(msg):
    positivoCont = sum(word in msg for word in Positivos)
    negativoCont = sum(word in msg for word in Negativos)
    
    if positivoCont == negativoCont:
        return 'neutros'
    elif positivoCont > negativoCont:
        return 'positivos'
    else:
        return 'negativos'

def contadorFechMsg(mensajes, dates):
    mensajeByFecha = {}
    for msg, date in zip(mensajes, dates):
        tipoMsg = clasificarMensaje(msg)
        if date not in mensajeByFecha:
            mensajeByFecha[date] = {'total': 0, 'positivos': 0, 'negativos': 0, 'neutros': 0}
        mensajeByFecha[date]['total'] += 1
        if tipoMsg == 'neutros':
            if mensajeByFecha[date]['neutros'] == 0:
                mensajeByFecha[date]['neutros'] = 1
        else:
            mensajeByFecha[date][tipoMsg] += 1
    return mensajeByFecha

def contEmpresa(mensajes):
    companycont = {company.nombre: {'total': 0, 'positivos': 0, 'negativos': 0, 'neutros': 0} for company in Empresas}
    for msg in mensajes:
        tipoMsg = clasificarMensaje(msg)
        for company in Empresas:
            if company.nombre in msg:
                companycont[company.nombre]['total'] += 1
                if tipoMsg == 'neutros':
                    if companycont[company.nombre]['neutros'] == 0:
                        companycont[company.nombre]['neutros'] = 1
                else:
                    companycont[company.nombre][tipoMsg] += 1
    return companycont

def diccionarioXML(mensajeByFecha, companycont):
    doc = Document()
    root = doc.createElement('lista_respuestas')
    doc.appendChild(root)
    
    for date, counts in mensajeByFecha.items():
        respuesta_element = doc.createElement('respuesta')
        
        date_element = doc.createElement('fecha')
        date_text = doc.createTextNode(date)
        date_element.appendChild(date_text)
        respuesta_element.appendChild(date_element)
        
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
        
        respuesta_element.appendChild(messages_element)
        
        analysis_element = doc.createElement('analisis')
        
        for company, company_counts in companycont.items():
            company_element = doc.createElement('empresa')
            company_element.setAttribute('nombre', company)
            
            company_messages_element = doc.createElement('mensajes')
            
            total_element = doc.createElement('total')
            total_text = doc.createTextNode(str(company_counts['total']))
            total_element.appendChild(total_text)
            
            positivos_element = doc.createElement('positivos')
            positivos_text = doc.createTextNode(str(company_counts['positivos']))
            positivos_element.appendChild(positivos_text)
            
            negativos_element = doc.createElement('negativos')
            negativos_text = doc.createTextNode(str(company_counts['negativos']))
            negativos_element.appendChild(negativos_text)
            
            neutros_element = doc.createElement('neutros')
            neutros_text = doc.createTextNode(str(company_counts['neutros']))
            neutros_element.appendChild(neutros_text)
            
            company_messages_element.appendChild(total_element)
            company_messages_element.appendChild(positivos_element)
            company_messages_element.appendChild(negativos_element)
            company_messages_element.appendChild(neutros_element)
            
            company_element.appendChild(company_messages_element)
            
            services_element = doc.createElement('servicios')
            
            for empresa in Empresas:
                if empresa.nombre == company:
                    for serv in empresa.servicios:
                        service_element = doc.createElement('servicio')
                        service_element.setAttribute('nombre', serv.nombre)
                        
                        service_messages_element = doc.createElement('mensajes')
                        
                        service_total = 0
                        service_positives = 0
                        service_negatives = 0
                        service_neutros = 0
                        
                        for msg in Mensajes:
                            if any(alias.alias in msg for alias in serv.alias):
                                service_total += 1
                                tipoMsg = clasificarMensaje(msg)
                                if tipoMsg == 'positivos':
                                    service_positives += 1
                                elif tipoMsg == 'negativos':
                                    service_negatives += 1
                                elif tipoMsg == 'neutros':
                                    service_neutros += 1
                        
                        total_element = doc.createElement('total')
                        total_text = doc.createTextNode(str(service_total))
                        total_element.appendChild(total_text)
                        
                        positivos_element = doc.createElement('positivos')
                        positivos_text = doc.createTextNode(str(service_positives))
                        positivos_element.appendChild(positivos_text)
                        
                        negativos_element = doc.createElement('negativos')
                        negativos_text = doc.createTextNode(str(service_negatives))
                        negativos_element.appendChild(negativos_text)
                        
                        neutros_element = doc.createElement('neutros')
                        neutros_text = doc.createTextNode(str(service_neutros))
                        neutros_element.appendChild(neutros_text)
                        
                        service_messages_element.appendChild(total_element)
                        service_messages_element.appendChild(positivos_element)
                        service_messages_element.appendChild(negativos_element)
                        service_messages_element.appendChild(neutros_element)
                        
                        service_element.appendChild(service_messages_element)
                        services_element.appendChild(service_element)
            
            company_element.appendChild(services_element)
            analysis_element.appendChild(company_element)
        
        respuesta_element.appendChild(analysis_element)
        root.appendChild(respuesta_element)
    
    return doc.toprettyxml(encoding='utf-8')

@app.route('/EnvioXML', methods=['GET'])
def contFechaFunc():
    try:
        dates = extraerFechas(Mensajes)
        mensajeByFecha = contadorFechMsg(Mensajes, dates)
        companycont = contEmpresa(Mensajes)
        xml_response = diccionarioXML(mensajeByFecha, companycont)
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
                    Positivos.append(good)
                    print(f"Positivo: {good}")
                    
            for negativo in negativos:
                palabras = negativo.getElementsByTagName('palabra')
                for pal in palabras:
                    bad = pal.firstChild.nodeValue.strip()
                    negative.append(Negativo(bad))
                    Negativos.append(bad)
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
                    Empresas.append(empre)
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

@app.route('/Reset', methods=['POST'])
def vaciarListas():
    global Clasificaciones, Diccionarios, Positivos, Negativos, Empresas, Servicios, Alias, Mensajes
    Clasificaciones.clear()
    Diccionarios.clear()
    Positivos.clear()
    Negativos.clear()
    Empresas.clear()
    Servicios.clear()
    Alias.clear()
    Mensajes.clear()
    return "Todas las listas han sido vaciadas", 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
'''@app.route('/mostrar', methods=['GET'])
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
        return "Error al procesar el archivo", 500'''