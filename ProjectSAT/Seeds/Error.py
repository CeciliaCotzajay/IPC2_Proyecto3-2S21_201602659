class Error:

    def __init__(self, fecha=None, cantNitEmisor=None, cantNitReceptor=None, cantIva=None, cantTotal=None,
                 CantReferencia=None):
        self.fecha = fecha
        self.cantNitEmisor = cantNitEmisor
        self.cantNitReceptor = cantNitReceptor
        self.cantIva = cantIva
        self.cantTotal = cantTotal
        self.CantReferencia = CantReferencia
