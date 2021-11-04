from xml.etree import ElementTree as ET

import requests as req
from django.shortcuts import render, redirect
from reportlab.pdfgen import canvas

# Create your views here.

firstXML = ""
secondXML = ""
XML2 = ""


# ##################################################### CLASES #########################################################
class DatosNIT:

    def __init__(self, fecha=None, nitEmisor=None, ivaE=None, nitReceptor=None, ivaR=None):
        self.fecha = fecha
        self.nitEmisor = nitEmisor
        self.nitReceptor = nitReceptor
        self.ivaE = ivaE
        self.ivaR = ivaR


class ListaDatosNit:
    def __init__(self):
        self.lista_datosNit = []

    def add(self, datoNit):
        self.lista_datosNit.append(datoNit)

    def devolverTamanio(self):
        return len(self.lista_datosNit)

    # def buscarNitEmisor(self, ):
    #     if self.lista_datosNit:
    #         for d in self.lista_datosNit:
    #             if d.fecha == fecha and d.nitEmisor == nitEmisor:
    #
    #     return False


li = ListaDatosNit()


def index(request):
    mensaje = "SAT  -  Proyecto3"
    title = "Proyecto_3-IPC2"
    variables = {
        "mensaje": mensaje,
        "title": title,
        "mostrarbarra": False
    }
    return render(request, "index.html", variables)


def Principal(request):
    mensaje = "Carga de Archivo"
    title = "Proyecto_3-IPC2"
    variables = {
        "mensaje": mensaje,
        "title": title,
        "mostrarbarra": True
    }
    return render(request, "Principal.html", variables)


def acercaDe(request):
    mensaje = "Acerda de..."
    title = "Proyecto_3-IPC2"
    variables = {
        "mensaje": mensaje,
        "title": title,
        "mostrarbarra": True
    }
    return render(request, "acercaDe.html", variables)


def recibirXML(request):
    texto = ""
    mostrarWarning = False
    textoAviso = None
    if request.method == 'POST':
        # ARCHIVO DE SOLICITUDES
        try:
            data = request.FILES["solicitudes"]
            decode_file = data.read().decode("utf-8").splitlines()
            for linea in decode_file:
                texto += linea + "\n"
        # print(data)
        # print(decode_file)
        # texto = str(data) + "\n" + str(decode_file)
        except:
            print("NO SE HA ELEGIDO NINGÚN ARCHIVO")
            mostrarWarning = True
            textoAviso = "- No se ha elegido ningún archivo!!- "
    mensaje = "Información"
    title = "Proyecto_3-IPC2"
    variables = {
        "mostrarbarra": True,
        "mensaje": mensaje,
        "title": title,
        "texto": texto,
        "mostrarWarning": mostrarWarning,
        "textoAviso": textoAviso
    }
    return render(request, 'Principal.html', variables)


def resetear(request):
    global firstXML, secondXML, XML2, li
    texto = ""
    mostrarWarning = False
    textoAviso = None
    if request.method == 'POST':
        req.post('http://127.0.0.1:5000/reset', 'reset')
        firstXML = ""
        secondXML = ""
        XML2 = ""
        li = None
        mostrarWarning = True
        textoAviso = "Sistema Reseteado!!- "
        print("**************DONE--Django-POST-RESET-********************************************")
    mensaje = "Carga de Archivos"
    title = "Proyecto_3-IPC2"
    variables = {
        "mostrarbarra": True,
        "mensaje": mensaje,
        "title": title,
        "texto": texto,
        "mostrarWarning": mostrarWarning,
        "textoAviso": textoAviso
    }
    return render(request, 'Principal.html', variables)


def enviarXML(request):
    global firstXML
    if request.method == 'POST':
        xml_envio = request.POST["textEnvioXML"]
        firstXML = xml_envio
        # print(xml_envio)
        req.post('http://127.0.0.1:5000/process_xml', xml_envio)
        print("**************DONE--Django-POST-********************************************")
    return redirect('Principal')


def traerXML(request):
    global firstXML, secondXML
    texto2 = ""
    if request.method == 'GET':
        xml_data = req.get('http://localhost:5000/process_xml')
        xml_text = xml_data.text
        secondXML = xml_text
        texto2 = xml_text
    texto = firstXML
    mensaje = "Resultados de Análisis"
    title = "Proyecto_3-IPC2"
    variables = {
        "mostrarbarra": True,
        "mensaje": mensaje,
        "title": title,
        "texto": texto,
        "texto2": texto2
    }
    print("**************DONE--Django-GET-XML-********************************************")
    return render(request, 'Principal.html', variables)


def Reportes(request):
    mensaje = "Reportes"
    title = "Proyecto_3-IPC2"
    variables = {
        "mensaje": mensaje,
        "title": title,
        "mostrarbarra": True
    }
    return render(request, "Reportes.html", variables)


def segundoXML(request):
    global XML2
    if request.method == 'GET':
        xml_data = req.get('http://localhost:5000/segundoXML')
        xml_text = xml_data.text
        XML2 = xml_text
    texto = "Ingrese una Fecha dd/mm/yyyy"
    mensaje = "Reportes"
    title = "Proyecto_3-IPC2"
    variables = {
        "mostrarbarra": True,
        "mensaje": mensaje,
        "title": title,
        "texto": texto,
    }
    print("**************DONE--Django-GET-XML-2-********************************************")
    return render(request, 'Reportes.html', variables)


def Reportesini(request):
    # REPORTE2----------------------------------------------------------------------------------------------------------
    global XML2, li

    root = ET.fromstring(XML2)
    for dte in root:
        fecha = dte.find('FECHA').text
        nitEmisor = dte.find('NIT_EMISOR').text
        nitReceptor = dte.find('NIT_RECEPTOR').text
        valor = dte.find('IVA_EMISOR').text
        iva = dte.find('IVA_RECEPTOR').text
        li.add(DatosNIT(fecha, nitEmisor, nitReceptor, valor, iva))

    # import numpy as np
    # import matplotlib.pyplot as plt
    # # dataset
    # bars = contenido
    # y_pos = np.arange(len(contenido))
    # # bars
    # plt.bar(y_pos, cantidad)
    # # names on the x-axis
    # plt.xticks(y_pos, bars)
    # # Save image
    # plt.savefig('static/img/grafica1.jpg')
    # plt.close()

    return redirect('Reportes')


def pdf(request):
    global firstXML
    if request.method == 'POST':
        xml_envio = request.POST["pdf"]
        c = canvas.Canvas(str(xml_envio)+".pdf")
        c.drawString(90, 900, "Texto Resulatdo")
        c.drawString(90, 600, str(XML2))
        c.save()
        print("**************DONE--Django-POST-PDF-********************************************")
    return redirect('Reportes')
