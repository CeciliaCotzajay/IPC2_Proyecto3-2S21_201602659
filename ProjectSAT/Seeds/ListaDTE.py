class ListaDTE:
    def __init__(self):
        self.lista_dte = []

    def add(self, tarea):
        self.lista_dte.append(tarea)

    def buscarReferencia(self,referencia):
        if self.lista_dte:
            for dte in self.lista_dte:
                if dte.referencia == referencia:
                    return True
        return False

    def validarNit(self, nit):
        print("")
        return False
