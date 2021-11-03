from Seeds.Error import Error


class ListaErrores:
    def __init__(self):
        self.lista_errores = []

    def add(self, tarea):
        self.lista_errores.append(tarea)

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
