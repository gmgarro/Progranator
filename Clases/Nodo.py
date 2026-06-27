class Nodo:
    
    def __init__(self, contenido, si=None, no=None):
        # Cada nodo guarda su texto y sus dos posibles hijos
        self.contenido = contenido
        self.si = si
        self.no = no

    def es_hoja(self):
        # Si no tiene hijos, es una respuesta final
        return self.si is None and self.no is None

    def a_diccionario(self):
        # Convierte el nodo (y sus hijos) a un diccionario para guardarlo en JSON
        return {
            "contenido": self.contenido,
            "si": self.si.a_diccionario() if self.si is not None else None,
            "no": self.no.a_diccionario() if self.no is not None else None
        }

    @staticmethod
    def desde_diccionario(diccionario):
        # Reconstruye un nodo desde un diccionario leído del JSON
        if diccionario is None:
            return None

        if "contenido" not in diccionario:
            raise ValueError("Diccionario de nodo invalido: falta 'contenido'")

        # Primero reconstruye los hijos de forma recursiva
        hijo_si = Nodo.desde_diccionario(diccionario.get("si"))
        hijo_no = Nodo.desde_diccionario(diccionario.get("no"))

        return Nodo(diccionario["contenido"], hijo_si, hijo_no)