from django.shortcuts import render

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
