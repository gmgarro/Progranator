import json
import os

from Clases.Nodo import Nodo


class ArchivoArbolInvalido(Exception):
    pass


class Arbol:

    def __init__(self):
        self.raiz = self.crear_arbol_default()
        self.nodo_actual = self.raiz
        self.ruta_archivo = None

    def crear_arbol_default(self):
        hoja_si = Nodo("perro")
        hoja_no = Nodo("computadora")
        return Nodo("¿Es un animal?", si=hoja_si, no=hoja_no)

    def reiniciar_partida(self):
        self.nodo_actual = self.raiz

    def es_pregunta_actual(self):
        return not self.nodo_actual.es_hoja()

    def obtener_contenido_actual(self):
        return self.nodo_actual.contenido

    def responder(self, respuesta):
        if self.nodo_actual.es_hoja():
            raise ValueError("No se puede responder: el nodo actual es una hoja")

        self.nodo_actual = self.nodo_actual.si if respuesta else self.nodo_actual.no

    def aprender(self, respuesta_correcta, nueva_pregunta, respuesta_para_si):
        respuesta_incorrecta = self.nodo_actual.contenido

        nodo_correcto = Nodo(respuesta_correcta)
        nodo_incorrecto = Nodo(respuesta_incorrecta)

        self.nodo_actual.contenido = nueva_pregunta

        if respuesta_para_si:
            self.nodo_actual.si = nodo_correcto
            self.nodo_actual.no = nodo_incorrecto
        else:
            self.nodo_actual.si = nodo_incorrecto
            self.nodo_actual.no = nodo_correcto

    def guardar_json(self, ruta):
        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(self.raiz.a_diccionario(), archivo, ensure_ascii=False, indent=2)
            self.ruta_archivo = ruta
            
            if self.ruta_archivo is None:
                self.ruta_archivo = ruta
        except OSError as error:
            raise ArchivoArbolInvalido(f"No se pudo guardar el archivo: {error}")

    def cargar_json(self, ruta):
        if not os.path.isfile(ruta):
            raise ArchivoArbolInvalido(f"El archivo '{ruta}' no existe")

        if os.path.getsize(ruta) == 0:
            raise ArchivoArbolInvalido("El archivo esta vacio")

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                diccionario = json.load(archivo)
        except (OSError, json.JSONDecodeError) as error:
            raise ArchivoArbolInvalido(f"El archivo esta dañado o mal formado: {error}")

        try:
            nueva_raiz = Nodo.desde_diccionario(diccionario)
        except (ValueError, AttributeError, TypeError) as error:
            raise ArchivoArbolInvalido(f"El contenido no representa un arbol valido: {error}")

        if nueva_raiz is None:
            raise ArchivoArbolInvalido("El archivo no contiene un arbol valido")

        self.raiz = nueva_raiz
        self.ruta_archivo = ruta
        self.reiniciar_partida()