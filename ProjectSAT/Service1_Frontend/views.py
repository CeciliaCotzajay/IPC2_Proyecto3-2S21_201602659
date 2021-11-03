from xml.dom import minidom

from django.shortcuts import render, redirect
import requests as req


# Create your views here.


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
    texto = ""
    mostrarWarning = False
    textoAviso = None
    if request.method == 'POST':
        req.post('http://127.0.0.1:5000/reset', 'reset')
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
    if request.method == 'POST':
        xml_envio = request.POST["textEnvioXML"]
        # print(xml_envio)
        req.post('http://127.0.0.1:5000/process_xml', xml_envio)
        print("**************DONE--Django-POST-********************************************")
    return redirect('Principal')