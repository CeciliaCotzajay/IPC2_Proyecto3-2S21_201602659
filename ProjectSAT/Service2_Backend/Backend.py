import re
import xml

from flask import Flask, request
from flask_cors import CORS
from xml.dom import minidom

from Seeds.DTE import DTE
from Seeds.ListaDTE import ListaDTE
from Seeds.ListaErrores import ListaErrores

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})

listaDTE = ListaDTE()
listaErrores = ListaErrores()


def quitarCaracteresEspeciales(cadenaEvaluar):
    copia = cadenaEvaluar.replace("\n", "")
    copia2 = copia.replace("\t", "")
    copia3 = copia2.replace("\f", "")
    copia4 = copia3.replace("\t", "")
    cadenaRetornar = copia4.strip()
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
    lista_dte = solicitud.getElementsByTagName("DTE")
    for dte in lista_dte:
        t0 = dte.getElementsByTagName("TIEMPO")[0]
        tiempo = quitarCaracteresEspeciales(str(t0.firstChild.data))
        # ######################## EXPRESION REGULAR ###################################################################
        obj = re.search('(0[1-9]|[1|2][\d]|3[0|1])/(0[1-9]|1[\d])/(2[\d]{3})', tiempo)
        if obj is None:
            print("Fecha No Coincide: ", tiempo)
        else:
            tiempo = str(obj[0][0]) + "/" + str(obj[0][1]) + "/" + str(obj[0][2])
        # ######################## FIN EXPRESION REGULAR ###############################################################
        r0 = dte.getElementsByTagName("REFERENCIA")[0]
        referencia = quitarCaracteresEspeciales(str(r0.firstChild.data))
        if listaDTE.buscarReferencia(referencia):
            listaErrores.actualizarReferencia(tiempo)
            print("Referencia repetida:", referencia, tiempo)
            pass
        nE0 = dte.getElementsByTagName("NIT_EMISOR")[0]
        nitEmisor = quitarCaracteresEspeciales(str(nE0.firstChild.data))
        if listaDTE.validarNit(nitEmisor):
            listaErrores.actualizarNitEmisor(tiempo)
            print("Error Nit Emisor:", nitEmisor, tiempo)
            pass
        nR0 = dte.getElementsByTagName("NIT_RECEPTOR")[0]
        nitReceptor = quitarCaracteresEspeciales(str(nR0.firstChild.data))
        if listaDTE.validarNit(nitReceptor):
            listaErrores.actualizarReceptor(tiempo)
            print("Error Nit Receptor:", nitReceptor, tiempo)
            pass
        v0 = dte.getElementsByTagName("VALOR")[0]
        valor = quitarCaracteresEspeciales(str(v0.firstChild.data))
        objV = re.search('[\d]{1,15}.[\d]{2}', valor)
        if objV is None:
            print("Valor No es (+,2):", valor, tiempo)
            pass
        else:
            valor = float(objV.group(0))
        i0 = dte.getElementsByTagName("IVA")[0]
        iva = float(quitarCaracteresEspeciales(str(i0.firstChild.data)))
        i = valor * 0.12
        ivaResultado = "{0:.2f}".format(i)
        if iva != ivaResultado:
            listaErrores.actualizarIVA(tiempo)
            print("IVA mal calculado:", iva, tiempo)
            pass
        tt0 = dte.getElementsByTagName("TOTAL")[0]
        total = float(quitarCaracteresEspeciales(str(tt0.firstChild.data)))
        totalResultado = valor + iva
        if total != totalResultado:
            listaErrores.actualizarTotal(tiempo)
            print("Total mal calculado:", total, tiempo)
            pass
        listaDTE.add(DTE(tiempo, referencia, nitEmisor, nitReceptor, valor, iva, total))
    print("**************DONE--Flask-POST-********************************************")
    return ''


if __name__ == '__main__':
    app.run(debug=True, port=5000)
