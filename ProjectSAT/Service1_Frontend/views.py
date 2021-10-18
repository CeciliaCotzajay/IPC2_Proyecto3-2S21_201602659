from django.shortcuts import render

# Create your views here.


def index(request):
    mensaje = "SAT  -  Proyecto3"
    title = "Proyecto_2-IPC2"
    variables = {
        "mensaje": mensaje,
        "title": title,
        "mostrarbarra": False
    }
    return render(request, "index.html", variables)