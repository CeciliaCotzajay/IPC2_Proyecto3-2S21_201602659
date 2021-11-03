class ListaDTE:
    def __init__(self):
        self.lista_dte = []

    def add(self, tarea):
        self.lista_dte.append(tarea)

    def buscarReferencia(self, referencia):
        if self.lista_dte:
            for dte in self.lista_dte:
                if dte.referencia == referencia:
                    return True
        return False

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
        paso4 = 11-paso3
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
