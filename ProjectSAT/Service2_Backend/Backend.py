import xml

from flask import Flask, request
from flask_cors import CORS
from xml.dom import minidom

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})


def quitarCaracteresEspeciales(cadenaEvaluar):
    copia = cadenaEvaluar.replace("\n", "")
    copia2 = copia.replace("\t", "")
    copia3 = copia2.replace("\f", "")
    cadenaRetornar = copia3.replace("\t", "")
    return cadenaRetornar


@app.route('/')
def index():
    title = "Servidor_2_FLASK"
    return title


@app.route('/process_xml', methods=['POST'])
def post_xml():
    # xml_cadena = request.data.decode("utf-8")
    xml_cadena = request.data.decode("ISO-8859-1")
    print(xml_cadena)
    xml_data = xml.dom.minidom.parseString(xml_cadena)
    solicitud = xml_data.getElementsByTagName("SOLICITUD_AUTORIZACION")[0]
    lista_dte = xml_data.getElementsByTagName("DTE")
    # print(lista_dte, "*******************************************")
    for dte in lista_dte:
        t0 = dte.getElementsByTagName("TIEMPO")[0]
        tiempo = quitarCaracteresEspeciales(str(t0.firstChild.data))
        r0 = dte.getElementsByTagName("REFERENCIA")[0]
        referencia = quitarCaracteresEspeciales(str(r0.firstChild.data))
        nE0 = dte.getElementsByTagName("NIT_EMISOR")[0]
        nitEmisor = quitarCaracteresEspeciales(str(nE0.firstChild.data))
        nR0 = dte.getElementsByTagName("NIT_RECEPTOR")[0]
        nitReceptor = quitarCaracteresEspeciales(str(nR0.firstChild.data))
        v0 = dte.getElementsByTagName("VALOR")[0]
        valor = quitarCaracteresEspeciales(str(v0.firstChild.data))
        i0 = dte.getElementsByTagName("IVA")[0]
        iva = quitarCaracteresEspeciales(str(i0.firstChild.data))
        tt0 = dte.getElementsByTagName("TOTAL")[0]
        total = quitarCaracteresEspeciales(str(tt0.firstChild.data))
    print("**************DONE--Flask-POST-********************************************")
    return ''





if __name__ == '__main__':
    app.run(debug=True, port=5000)