import re
import xml

from flask import Flask, request
from flask_cors import CORS
from xml.dom import minidom

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})


# ######################################################################################################################
# ##################################################### CLASES #########################################################
class DTE:

    def __init__(self, fecha=None, referencia=None, nitEmisor=None, nitReceptor=None, valor=None, iva=None,
                 total=None):
        self.fecha = fecha
        self.referencia = referencia
        self.nitEmisor = nitEmisor
        self.nitReceptor = nitReceptor
        self.valor = valor
        self.iva = iva
        self.total = total


class Error:

    def __init__(self, fecha=None, cantNitEmisor=None, cantNitReceptor=None, cantIva=None, cantTotal=None,
                 CantReferencia=None):
        self.fecha = fecha
        self.cantNitEmisor = cantNitEmisor
        self.cantNitReceptor = cantNitReceptor
        self.cantIva = cantIva
        self.cantTotal = cantTotal
        self.CantReferencia = CantReferencia


class Aprobacion:

    def __init__(self, referencia=None, nitEmisor=None, codigoAprobacion=None):
        self.referencia = referencia
        self.nitEmisor = nitEmisor
        self.codigoAprobacion = codigoAprobacion


# ##################################################### CLASES #########################################################
class ListaDTE:
    def __init__(self):
        self.lista_dte = []

    def add(self, dte):
        self.lista_dte.append(dte)

    def buscarReferencia(self, referencia):
        if self.lista_dte:
            for dte in self.lista_dte:
                if dte.referencia == referencia:
                    return True
        return False

    def devolverTamanio(self):
        return len(self.lista_dte)

    def validarNit(self, nit):
        listaCaracter = []
        for c in nit:
            listaCaracter.append(c)
        tam = len(listaCaracter)
        pos = 0
        paso1 = 0
        while tam > 1:
            paso1 += int(listaCaracter[pos]) * tam
            tam -= 1
            pos += 1
        paso3 = paso1 % 11
        paso4 = 11 - paso3
        paso5 = paso4 % 11
        ultimoCaracter = listaCaracter.pop()
        if paso5 == 10:
            if ultimoCaracter == 'K' or ultimoCaracter == 'k':
                return False
            else:
                return True
        else:
            if paso5 == int(ultimoCaracter):
                return False
            else:
                return True

    def NoEncontrarNitEmisor(self, nit):
        if self.lista_dte:
            for dte in self.lista_dte:
                if dte.nitEmisor == nit:
                    return False
        return True

    def NoEncontrarNitReceptor(self, nit):
        if self.lista_dte:
            for dte in self.lista_dte:
                if dte.nitReceptor == nit:
                    return False
        return True


# ##################################################### CLASES #########################################################
class ListaErrores:
    def __init__(self):
        self.lista_errores = []

    def add(self, error):
        self.lista_errores.append(error)

    def devolverTamanio(self):
        return len(self.lista_errores)

    def actualizarReferencia(self, fecha):
        encontrado = 0
        if self.lista_errores:
            for e in self.lista_errores:
                if e.fecha == fecha:
                    e.CantReferencia += 1
                    encontrado = 1
        if encontrado == 0:
            self.add(Error(fecha, 0, 0, 0, 0, 1))

    def actualizarNitEmisor(self, fecha):
        encontrado = 0
        if self.lista_errores:
            for e in self.lista_errores:
                if e.fecha == fecha:
                    e.cantNitEmisor += 1
                    encontrado = 1
        if encontrado == 0:
            self.add(Error(fecha, 1, 0, 0, 0, 0))

    def actualizarReceptor(self, fecha):
        encontrado = 0
        if self.lista_errores:
            for e in self.lista_errores:
                if e.fecha == fecha:
                    e.cantNitReceptor += 1
                    encontrado = 1
        if encontrado == 0:
            self.add(Error(fecha, 0, 1, 0, 0, 0))

    def actualizarIVA(self, fecha):
        encontrado = 0
        if self.lista_errores:
            for e in self.lista_errores:
                if e.fecha == fecha:
                    e.cantIva += 1
                    encontrado = 1
        if encontrado == 0:
            self.add(Error(fecha, 0, 0, 1, 0, 0))

    def actualizarTotal(self, fecha):
        encontrado = 0
        if self.lista_errores:
            for e in self.lista_errores:
                if e.fecha == fecha:
                    e.cantTotal += 1
                    encontrado = 1
        if encontrado == 0:
            self.add(Error(fecha, 0, 0, 0, 1, 0))


# ##################################################### CLASES #########################################################
class ListaAprobacion:
    def __init__(self):
        self.lista_aprobacion = []

    def add(self, aprobacion):
        self.lista_aprobacion.append(aprobacion)

    def devolverTamanio(self):
        return len(self.lista_aprobacion)


# ##################################################### OBJETOS ########################################################
listaDTE = ListaDTE()
listaErrores = ListaErrores()
listaAprobaciones = ListaAprobacion()
cantFac_Correctas = 0
canEmisores = 0
canReceptores = 0


# ##################################################### OBJETOS ########################################################
# ######################################################################################################################

def quitarCaracteresEspeciales(cadenaEvaluar):
    copia = cadenaEvaluar.replace("\n", "")
    copia2 = copia.replace("\t", "")
    copia3 = copia2.replace("\f", "")
    copia4 = copia3.replace("\t", "")
    cadenaRetornar = copia4.strip()
    return cadenaRetornar


def CrearAprobacion(referencia, nitEmisor, dia, mes, anio):
    global cantFac_Correctas, listaAprobaciones, listaDTE, listaErrores
    tex = str(cantFac_Correctas)
    cerosRestantes = 8 - len(tex)
    cadena = ""
    while cerosRestantes > 0:
        cadena += "0"
        cerosRestantes -= 1
    parte2 = cadena + str(cantFac_Correctas)
    codigoAprobacion = anio + mes + dia + parte2
    aprobacion = Aprobacion(referencia, nitEmisor, codigoAprobacion)
    listaAprobaciones.add(aprobacion)
    # print("dte:", listaDTE.devolverTamanio, "error:", listaErrores.devolverTamanio, "apro:",
    #       listaAprobaciones.devolverTamanio)


@app.route('/')
def index():
    title = "Servidor_2_FLASK"
    return title


@app.route('/process_xml', methods=['POST'])
def post_xml():
    # xml_cadena = request.data.decode("utf-8")
    global listaDTE, listaErrores, cantFac_Correctas, canEmisores, canReceptores
    xml_cadena = request.data.decode("ISO-8859-1")
    print(xml_cadena)
    errorArchivo = 0
    xml_data = xml.dom.minidom.parseString(xml_cadena)
    solicitud = xml_data.getElementsByTagName("SOLICITUD_AUTORIZACION")[0]
    lista_dte = solicitud.getElementsByTagName("DTE")
    for dte in lista_dte:
        t0 = dte.getElementsByTagName("TIEMPO")[0]
        tiempo = quitarCaracteresEspeciales(str(t0.firstChild.data))
        # print(tiempo)
        # ######################## EXPRESION REGULAR ###################################################################
        obj = re.findall('(0[1-9]|[1|2][\d]|3[0|1])/(0[1-9]|1[\d])/(2[\d]{3})', tiempo)
        if len(obj) == 0:
            print("Fecha No Coincide: ", tiempo)
        else:
            tiempo = str(obj[0][0]) + "/" + str(obj[0][1]) + "/" + str(obj[0][2])
            # print(tiempo)
        # print(tiempo)
        # ######################## FIN EXPRESION REGULAR ###############################################################
        r0 = dte.getElementsByTagName("REFERENCIA")[0]
        referencia = quitarCaracteresEspeciales(str(r0.firstChild.data))
        if listaDTE.buscarReferencia(referencia):
            listaErrores.actualizarReferencia(tiempo)
            print("Referencia repetida:", referencia, '-', tiempo)
            errorArchivo = 1
        nE0 = dte.getElementsByTagName("NIT_EMISOR")[0]
        nitEmisor = quitarCaracteresEspeciales(str(nE0.firstChild.data))
        if listaDTE.validarNit(nitEmisor):
            listaErrores.actualizarNitEmisor(tiempo)
            print("Error Nit Emisor:", nitEmisor, '-', tiempo)
            errorArchivo = 1
        if listaDTE.NoEncontrarNitEmisor(nitEmisor):
            canEmisores += 1
        nR0 = dte.getElementsByTagName("NIT_RECEPTOR")[0]
        nitReceptor = quitarCaracteresEspeciales(str(nR0.firstChild.data))
        if listaDTE.validarNit(nitReceptor):
            listaErrores.actualizarReceptor(tiempo)
            print("Error Nit Receptor:", nitReceptor, '-', tiempo)
            errorArchivo = 1
        if listaDTE.NoEncontrarNitReceptor(nitReceptor):
            canReceptores += 1
        v0 = dte.getElementsByTagName("VALOR")[0]
        valor = quitarCaracteresEspeciales(str(v0.firstChild.data))
        objV = re.search('[\d]{1,15}.[\d]{2}', valor)
        if objV is None:
            print("Valor No es (+,2):", valor, '-', tiempo)
            errorArchivo = 1
        else:
            valor = float(objV.group(0))
        i0 = dte.getElementsByTagName("IVA")[0]
        iva = float(quitarCaracteresEspeciales(str(i0.firstChild.data)))
        i = valor * 0.12
        ivaResultado = float("{0:.2f}".format(i))
        if iva != ivaResultado:
            listaErrores.actualizarIVA(tiempo)
            print("IVA mal calculado:", iva, '-', tiempo)
            errorArchivo = 1
        tt0 = dte.getElementsByTagName("TOTAL")[0]
        total = float(quitarCaracteresEspeciales(str(tt0.firstChild.data)))
        totalResultado = valor + iva
        if total != totalResultado:
            listaErrores.actualizarTotal(tiempo)
            print("Total mal calculado:", total, '-', tiempo)
            errorArchivo = 1
        # #SI NO CUENTA CON ERRORES SE ALMACENA#
        if errorArchivo == 0:
            listaDTE.add(DTE(tiempo, referencia, nitEmisor, nitReceptor, valor, iva, total))
            cantFac_Correctas += 1
            CrearAprobacion(referencia, nitEmisor, str(obj[0][0]), str(obj[0][1]), str(obj[0][2]))
    print("**************DONE--Flask-POST-********************************************")
    return ''


@app.route('/reset', methods=['POST'])
def reset():
    texto = request.data.decode("ISO-8859-1")
    if str(texto) == 'reset':
        global listaDTE, listaErrores, cantFac_Correctas, canEmisores, canReceptores, listaAprobaciones
        listaDTE = None
        listaErrores = None
        listaAprobaciones = None
        cantFac_Correctas = 0
        canEmisores = 0
        canReceptores = 0
        print("**************DONE--Flask-POST-RESET-********************************************")
    return ''


if __name__ == '__main__':
    app.run(debug=True, port=5000)
