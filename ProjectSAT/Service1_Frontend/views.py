from django.shortcuts import render

# Create your views here.


def index(request):
    mensaje = "CHET  -  Proyecto_2"
    title = "Proyecto_2-IPC2"
    variables = {
        "mensaje": mensaje,
        "title": title
    }
    return render(request, "index.html", variables)