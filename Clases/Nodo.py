class Nodo:

    def __init__(self, contenido, si=None, no=None):

        self.contenido = contenido
        self.si = si
        self.no = no

    def es_hoja(self):

        return self.si is None and self.no is None

    def a_diccionario(self):

        return {
            "contenido": self.contenido,
            "si": self.si.a_diccionario() if self.si is not None else None,
            "no": self.no.a_diccionario() if self.no is not None else None
        }

    @staticmethod
    def desde_diccionario(diccionario):
 
        if diccionario is None:
            return None

        if "contenido" not in diccionario:
            raise ValueError("Diccionario de nodo invalido: falta 'contenido'")

        hijo_si = Nodo.desde_diccionario(diccionario.get("si"))
        hijo_no = Nodo.desde_diccionario(diccionario.get("no"))

        return Nodo(diccionario["contenido"], hijo_si, hijo_no)
