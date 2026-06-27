# PROGRANATOR

## Descripción

PROGRANATOR es un juego de preguntas y respuestas donde el programa intenta adivinar en qué está pensando el usuario. Para lograrlo, hace preguntas de Sí o No y recorre un árbol de decisión binario según las respuestas. Si falla, aprende la respuesta correcta y guarda ese conocimiento para las siguientes partidas.

---

## Características

- Juego de preguntas Sí/No con árbol de decisión binario
- Aprende nuevas respuestas cuando no adivina
- Guarda el árbol actualizado automáticamente en un archivo JSON
- Permite cargar distintos árboles desde archivo
- Interfaz gráfica con Tkinter
- Incluye 5 árboles de ejemplo listos para usar (animales, frutas, videojuegos, países, lugares de Costa Rica)

---

## Requisitos

- Python 3.x
- Tkinter (viene incluido con Python en la mayoría de instalaciones)

---

## Estructura del proyecto

```
proyecto/
├── main.py
├── datos/
│   ├── arbol_actual.json
│   ├── animales.json
│   ├── frutas.json
│   ├── videojuegos.json
│   ├── paises.json
│   └── lugares_costa_rica.json
├── Clases/
│   ├── Nodo.py
│   ├── Arbol.py
│   └── AppGUI.py
└── README.md
```

---

## Ejecución

1. Clonar o descargar el repositorio
2. Abrir una terminal en la carpeta raíz del proyecto (donde está `main.py`)
3. Ejecutar el siguiente comando:

```bash
python main.py
```

> Asegurarse de ejecutar `main.py` desde la carpeta raíz, no desde dentro de `Clases/` ni de `datos/`.

---

## Funcionamiento

Al iniciar, el programa carga un árbol básico por defecto con dos respuestas: perro y computadora. Desde el menú se puede cargar un árbol distinto desde un archivo JSON.

Durante la partida, el programa hace preguntas de Sí o No y avanza por el árbol según cada respuesta. Cuando llega a una hoja, intenta adivinar lo que el usuario está pensando.

Si adivina correctamente, muestra un mensaje y permite jugar de nuevo. Si falla, le pide al usuario tres cosas:

1. La respuesta correcta
2. Una pregunta que diferencie esa respuesta de la que el programa dijo
3. Si para esa nueva respuesta la contestación a la pregunta es Sí o No

Con esa información, el árbol crece y guarda el aprendizaje automáticamente.

---

## Archivos JSON

El árbol de conocimiento se guarda en formato JSON. Cada nodo tiene tres campos: `contenido`, `si` y `no`. Los nodos hoja tienen `si` y `no` en `null`.

Cuando el programa aprende algo nuevo, guarda el árbol en el mismo archivo que se cargó al inicio. Si no se cargó ningún archivo, lo guarda en `datos/arbol_actual.json`.

Los archivos de la carpeta `datos/` se pueden cargar desde el botón "Cargar árbol" en el menú principal.

---

## Autores

- Gabriel Montero Garro