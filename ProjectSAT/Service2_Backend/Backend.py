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

    def __init__(self, fecha=None, referencia=None, nitEmisor=None, codigoAprobacion=None):
        self.fecha = fecha
        self.referencia = referencia
        self.nitEmisor = nitEmisor
        self.codigoAprobacion = codigoAprobacion


class DatosGenerales:

    def __init__(self, fecha=None, cantFacturasRecibidas=None, cantFacturasCorrectas=None, cantEmisores=None,
                 cantReceptores=None):
        self.fecha = fecha
        self.cantFacturasRecibidas = cantFacturasRecibidas
        self.cantFacturasCorrectas = cantFacturasCorrectas
        self.cantEmisores = cantEmisores
        self.cantReceptores = cantReceptores


# ##################################################### CLASES #########################################################
class ListaDTE:
    def __init__(self):
        self.lista_dte = []

    def add(self, dte):
        self.lista_dte.append(dte)

    def buscarReferencia(self, referencia, fecha):
        if self.lista_dte:
            for dte in self.lista_dte:
                if dte.referencia == referencia and dte.fecha == fecha:
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
class ListaDatosGenerales:
    def __init__(self):
        self.lista_datosGen = []

    def add(self, error):
        self.lista_datosGen.append(error)

    def devolverTamanio(self):
        return len(self.lista_datosGen)

    def actualizarCantFacturasRecibidas(self, fecha):
        encontrado = 0
        if self.lista_datosGen:
            for e in self.lista_datosGen:
                if e.fecha == fecha:
                    e.cantFacturasRecibidas += 1
                    encontrado = 1
        if encontrado == 0:
            self.add(DatosGenerales(fecha, 1, 0, 0, 0))

    def actualizarCantFacturasCorrectas(self, fecha):
        encontrado = 0
        if self.lista_datosGen:
            for e in self.lista_datosGen:
                if e.fecha == fecha:
                    e.cantFacturasCorrectas += 1
                    encontrado = 1
        if encontrado == 0:
            self.add(DatosGenerales(fecha, 0, 1, 0, 0))

    def actualizarCantEmisores(self, fecha):
        encontrado = 0
        if self.lista_datosGen:
            for e in self.lista_datosGen:
                if e.fecha == fecha:
                    e.cantEmisores += 1
                    encontrado = 1
        if encontrado == 0:
            self.add(DatosGenerales(fecha, 0, 0, 1, 0))

    def actualizarCantReceptores(self, fecha):
        encontrado = 0
        if self.lista_datosGen:
            for e in self.lista_datosGen:
                if e.fecha == fecha:
                    e.cantReceptores += 1
                    encontrado = 1
        if encontrado == 0:
            self.add(DatosGenerales(fecha, 0, 0, 0, 1))

    def obtenerFacturasCorrectas(self, fecha):
        cantidad = 0
        if self.lista_datosGen:
            for e in self.lista_datosGen:
                if e.fecha == fecha:
                    cantidad = e.cantFacturasCorrectas
        return cantidad


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
listaDatosGenerales = ListaDatosGenerales()


# cantFac_Total = 0
# cantFac_Correctas = 0
# canEmisores = 0
# canReceptores = 0


# ##################################################### OBJETOS ########################################################
# ######################################################################################################################

def quitarCaracteresEspeciales(cadenaEvaluar):
    copia = cadenaEvaluar.replace("\n", "")
    copia2 = copia.replace("\t", "")
    copia3 = copia2.replace("\f", "")
    copia4 = copia3.replace("\t", "")
    cadenaRetornar = copia4.strip()
    return cadenaRetornar


def CrearAprobacion(fecha, referencia, nitEmisor, dia, mes, anio):
    global listaAprobaciones, listaDTE, listaErrores, listaDatosGenerales
    tex = str(listaDatosGenerales.obtenerFacturasCorrectas(fecha))
    cerosRestantes = 8 - len(tex)
    cadena = ""
    while cerosRestantes > 0:
        cadena += "0"
        cerosRestantes -= 1
    parte2 = cadena + tex
    codigoAprobacion = anio + mes + dia + parte2
    aprobacion = Aprobacion(fecha, referencia, nitEmisor, codigoAprobacion)
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
    global listaDTE, listaErrores, listaDatosGenerales
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
        listaDatosGenerales.actualizarCantFacturasRecibidas(tiempo)
        r0 = dte.getElementsByTagName("REFERENCIA")[0]
        referencia = quitarCaracteresEspeciales(str(r0.firstChild.data))
        if listaDTE.buscarReferencia(referencia, tiempo):
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
            listaDatosGenerales.actualizarCantEmisores(tiempo)
        nR0 = dte.getElementsByTagName("NIT_RECEPTOR")[0]
        nitReceptor = quitarCaracteresEspeciales(str(nR0.firstChild.data))
        if listaDTE.validarNit(nitReceptor):
            listaErrores.actualizarReceptor(tiempo)
            print("Error Nit Receptor:", nitReceptor, '-', tiempo)
            errorArchivo = 1
        if listaDTE.NoEncontrarNitReceptor(nitReceptor):
            listaDatosGenerales.actualizarCantReceptores(tiempo)
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
        i = float(valor) * 0.12
        ivaResultado = float("{0:.2f}".format(i))
        if iva != ivaResultado:
            listaErrores.actualizarIVA(tiempo)
            print("IVA mal calculado:", iva, '-', tiempo)
            errorArchivo = 1
        tt0 = dte.getElementsByTagName("TOTAL")[0]
        total = float(quitarCaracteresEspeciales(str(tt0.firstChild.data)))
        totalResultado = float(valor) + float(iva)
        if total != totalResultado:
            listaErrores.actualizarTotal(tiempo)
            print("Total mal calculado:", total, '-', tiempo)
            errorArchivo = 1
        # #SI NO CUENTA CON ERRORES SE ALMACENA#
        if errorArchivo == 0:
            listaDTE.add(DTE(tiempo, referencia, nitEmisor, nitReceptor, valor, iva, total))
            listaDatosGenerales.actualizarCantFacturasCorrectas(tiempo)
            CrearAprobacion(tiempo, referencia, nitEmisor, str(obj[0][0]), str(obj[0][1]), str(obj[0][2]))
        errorArchivo = 0
    print("**************DONE--Flask-POST-********************************************")
    return ''


@app.route('/reset', methods=['POST'])
def reset():
    texto = request.data.decode("ISO-8859-1")
    if str(texto) == 'reset':
        global listaDTE, listaErrores, listaAprobaciones, listaDatosGenerales
        listaDTE = None
        listaErrores = None
        listaAprobaciones = None
        listaDatosGenerales = None
        print("**************DONE--Flask-POST-RESET-********************************************")
    return ''


@app.route('/process_xml', methods=['GET'])
def get_xml():
    global listaDTE, listaDatosGenerales, listaAprobaciones, listaErrores
    document = minidom.Document()
    root = document.createElement('LISTA_AUTORIZACIONES')
    for dte in listaDTE.lista_dte:
        fechaDTE = dte.fecha
        autorizacion = document.createElement('AUTORIZACION')
        root.appendChild(autorizacion)

        fechaDoc = document.createElement('FECHA')
        fechaDoc.appendChild(document.createTextNode(fechaDTE))
        autorizacion.appendChild(fechaDoc)

        for dg in listaDatosGenerales.lista_datosGen:
            if dg.fecha == fechaDTE:
                facturasTotales = document.createElement('FACTURAS_RECIBIDAS')
                facturasTotales.appendChild(document.createTextNode(str(dg.cantFacturasRecibidas)))
                autorizacion.appendChild(facturasTotales)
        errores = document.createElement('ERRORES')
        autorizacion.appendChild(errores)
        er = 0
        for e in listaErrores.lista_errores:
            if e.fecha == fechaDTE:
                er = 1
                nitEmisor = document.createElement('NIT_EMISOR')
                nitEmisor.appendChild(document.createTextNode(str(e.cantNitEmisor)))
                errores.appendChild(nitEmisor)
                nitReceptor = document.createElement('NIT_RECEPTOR')
                nitReceptor.appendChild(document.createTextNode(str(e.cantNitReceptor)))
                errores.appendChild(nitReceptor)
                iva = document.createElement('IVA')
                iva.appendChild(document.createTextNode(str(e.cantIva)))
                errores.appendChild(iva)
                total = document.createElement('TOTAL')
                total.appendChild(document.createTextNode(str(e.cantTotal)))
                errores.appendChild(total)
                referencia = document.createElement('REFERENCIA_DUPLICADA')
                referencia.appendChild(document.createTextNode(str(e.CantReferencia)))
                errores.appendChild(referencia)
        if er == 0:
            nitEmisor = document.createElement('NIT_EMISOR')
            nitEmisor.appendChild(document.createTextNode(str(0)))
            errores.appendChild(nitEmisor)
            nitReceptor = document.createElement('NIT_RECEPTOR')
            nitReceptor.appendChild(document.createTextNode(str(0)))
            errores.appendChild(nitReceptor)
            iva = document.createElement('IVA')
            iva.appendChild(document.createTextNode(str(0)))
            errores.appendChild(iva)
            total = document.createElement('TOTAL')
            total.appendChild(document.createTextNode(str(0)))
            errores.appendChild(total)
            referencia = document.createElement('REFERENCIA_DUPLICADA')
            referencia.appendChild(document.createTextNode(str(0)))
            errores.appendChild(referencia)

        for dg in listaDatosGenerales.lista_datosGen:
            if dg.fecha == fechaDTE:
                facturasCorrec = document.createElement('FACTURAS_CORRECTAS')
                facturasCorrec.appendChild(document.createTextNode(str(dg.cantFacturasCorrectas)))
                autorizacion.appendChild(facturasCorrec)
                canEmisores = document.createElement('CANTIDAD_EMISORES')
                canEmisores.appendChild(document.createTextNode(str(dg.cantEmisores)))
                autorizacion.appendChild(canEmisores)
                canRecepto = document.createElement('CANTIDAD_RECEPTORES')
                canRecepto.appendChild(document.createTextNode(str(dg.cantReceptores)))
                autorizacion.appendChild(canRecepto)

        listadoAutori = document.createElement('LISTADO_AUTORIZACIONES')
        autorizacion.appendChild(listadoAutori)
        cont = 0
        for a in listaAprobaciones.lista_aprobacion:
            if a.fecha == fechaDTE:
                cont = +1
                aprobacion = document.createElement('APROBACION')
                listadoAutori.appendChild(aprobacion)

                nitEmi = document.createElement('NIT_EMISOR')
                nitEmi.setAttribute("ref", a.referencia)
                nitEmi.appendChild(document.createTextNode(str(a.nitEmisor)))
                aprobacion.appendChild(nitEmi)

                codigo = document.createElement('CODIGO_APROBACION')
                codigo.appendChild(document.createTextNode(a.codigoAprobacion))
                aprobacion.appendChild(codigo)
        totalApro = document.createElement('TOTAL_APROBACIONES')
        totalApro.appendChild(document.createTextNode(str(cont)))
        listadoAutori.appendChild(totalApro)

    xml_text = root.toprettyxml(indent='\t', encoding='utf-8')
    xml_doc = xml_text.decode('utf-8')
    archivoXML = open("XML_Salida" + '.xml', 'wb')
    archivoXML.write(xml_text)
    archivoXML.close()
    print("**************DONE--Flask-GET-XML-********************************************")
    return xml_doc


@app.route('/segundoXML', methods=['GET'])
def CrearSegundoArchivo():
    global listaDTE
    fechas = []
    for d in listaDTE.lista_dte:
        fecha = d.fecha
        for d2 in listaDTE.lista_dte:
            fecha2 = d2.fecha
            if fecha2 != fecha:
                fechas.append(fecha2)
    document = minidom.Document()
    root = document.createElement('BASE_DATOS_NIT')
    for f in fechas:
        fechaDoc = document.createElement('FECHA')
        fechaDoc.appendChild(document.createTextNode(f))
        root.appendChild(fechaDoc)
        emisoresIva = []
        ivE = []
        ivR = []
        receptoresIva = []
        for dte in listaDTE.lista_dte:
            if dte.fecha == f:
                if emisoresIva:
                    c = 0
                    for emi in emisoresIva:
                        if emi != dte.nitEmisor:
                            emisoresIva.append(dte.nitEmisor)
                            ivE.append(dte.iva)
                        else:
                            ivE[c] = ivE[c] + dte.iva
                        c += 1
                else:
                    emisoresIva.append(dte.nitEmisor)
                    ivE.append(dte.iva)
                if receptoresIva:
                    c = 0
                    for rec in receptoresIva:
                        if rec != dte.nitReceptor:
                            receptoresIva.append(dte.nitReceptor)
                            ivR.append(dte.iva)
                        else:
                            ivR[c] = ivR[c] + dte.iva
                        c += 1
                else:
                    receptoresIva.append(dte.nitReceptor)
                    ivR.append(dte.iva)
        c2 = 0
        for e in emisoresIva:
            nitEmisor = document.createElement('NIT_EMISOR')
            nitEmisor.appendChild(document.createTextNode(e))
            fechaDoc.appendChild(nitEmisor)
            iva = document.createElement('IVA_EMISOR')
            iva.appendChild(document.createTextNode(str(ivE[c2])))
            fechaDoc.appendChild(iva)
            c2 += 1
        c3 = 0
        for rI in receptoresIva:
            nitReceptor = document.createElement('NIT_RECEPTOR')
            nitReceptor.appendChild(document.createTextNode(rI))
            fechaDoc.appendChild(nitReceptor)
            iva = document.createElement('IVA_RECEPTOR')
            iva.appendChild(document.createTextNode(str(ivR[c3])))
            fechaDoc.appendChild(iva)
            c3 += 1

    xml_text = root.toprettyxml(indent='\t', encoding='utf-8')
    xml_doc = xml_text.decode('utf-8')
    archivoXML = open("BaseDatosNIT" + '.xml', 'wb')
    archivoXML.write(xml_text)
    archivoXML.close()
    print("**************DONE--Flask-GET-XML2-********************************************")
    return xml_doc


if __name__ == '__main__':
    app.run(debug=True, port=5000)
