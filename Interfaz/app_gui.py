import os
from tkinter import *
from tkinter import filedialog, messagebox

from Clases.Arbol import Arbol, ArchivoArbolInvalido

CARPETA_DATOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datos")
ARCHIVO_DEFAULT = os.path.join(CARPETA_DATOS, "arbol_actual.json")


class AppGUI:

    def __init__(self, root):
        self.root = root
        self.arbol = Arbol()

        os.makedirs(CARPETA_DATOS, exist_ok=True)

        self.canvas = Canvas(
            root,
            width=1200,
            height=600,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack()

        # Botón persistente — se crea una vez y se muestra/oculta según pantalla
        self.btn_menu = Button(
            self.root,
            text="Volver al menú",
            command=self.mostrar_pantalla_inicial,
            font=("Arial", 11, "bold"),
            bg="#630000",
            fg="white",
            activebackground="#3A0000",
            activeforeground="white",
            bd=0,
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2"
        )

        def entrar_menu(e):
            self.btn_menu.config(bg="#3A0000")

        def salir_menu(e):
            self.btn_menu.config(bg="#630000")

        self.btn_menu.bind("<Enter>", entrar_menu)
        self.btn_menu.bind("<Leave>", salir_menu)

        self.mostrar_pantalla_inicial()

    # ── IMPORTANTE PARA MAIN ──
    def destruir(self):
        self.canvas.destroy()

    def limpiar(self):
        self.canvas.delete("all")
        for widget in self.root.pack_slaves():
            if widget is not self.canvas:
                widget.destroy()

    def ajustar(self, ancho, alto):
        self.root.geometry(f"{ancho}x{alto}")
        self.canvas.config(width=ancho, height=alto)

    def crear_boton(self, texto, accion, ancho=20):
        btn = Button(
            self.root,
            text=texto,
            command=accion,
            font=("Arial", 14, "bold"),
            bg="#111111",
            fg="white",
            activebackground="#630000",
            activeforeground="white",
            bd=0,
            relief="flat",
            width=ancho,
            height=2,
            cursor="hand2"
        )

        def entrar(e):
            btn.config(bg="#630000")

        def salir(e):
            btn.config(bg="#111111")

        btn.bind("<Enter>", entrar)
        btn.bind("<Leave>", salir)
        return btn

    def crear_entrada(self, ancho=40):
        entrada = Entry(
            self.root,
            font=("Arial", 12),
            bg="#1D1D1D",
            fg="white",
            insertbackground="white",
            relief="flat",
            width=ancho
        )
        return entrada

    # ── RF-01: PANTALLA INICIAL ──
    def mostrar_pantalla_inicial(self):
        self.ajustar(1200, 600)
        self.limpiar()
        # En el menú el botón no se muestra
        self.btn_menu.place_forget()
        centro_x = 600

        self.canvas.create_rectangle(
            275, 55, 925, 470,
            fill="#111111",
            outline="#630000",
            width=3
        )
        self.canvas.create_text(
            centro_x, 130,
            text="PROGRANATOR",
            fill="#C47602",
            font=("Impact", 36)
        )

        btn_jugar = self.crear_boton("Jugar", self.iniciar_partida)
        btn_cargar = self.crear_boton("Cargar arbol", self.cargar_archivo)
        btn_salir = self.crear_boton("Salir", self.root.destroy)

        self.canvas.create_window(centro_x, 230, window=btn_jugar)
        self.canvas.create_window(centro_x, 300, window=btn_cargar)
        self.canvas.create_window(centro_x, 370, window=btn_salir)

    # ── RF-02: CARGAR ARBOL ──
    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de arbol",
            initialdir=CARPETA_DATOS,
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )

        if not ruta:
            return

        try:
            self.arbol.cargar_json(ruta)
            messagebox.showinfo("Arbol cargado", "El arbol se cargo correctamente.")
        except ArchivoArbolInvalido as error:
            messagebox.showerror(
                "Error al cargar",
                f"No se pudo cargar el archivo:\n{error}\n\nSe continuara con el arbol actual."
            )

    # ── RF-04 a RF-06: PREGUNTAS ──
    def iniciar_partida(self):
        self.arbol.reiniciar_partida()
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        self.ajustar(1200, 600)
        self.limpiar()
        # Mostrar botón menú durante el juego
        self.btn_menu.place(x=16, y=12)

        if not self.arbol.es_pregunta_actual():
            self.mostrar_resultado_adivinanza()
            return

        centro_x = 600

        self.canvas.create_rectangle(
            200, 150, 1000, 400,
            fill="#111111",
            outline="#630000",
            width=3
        )
        self.canvas.create_text(
            centro_x, 260,
            text=self.arbol.obtener_contenido_actual(),
            fill="white",
            font=("Arial", 20, "bold"),
            width=700
        )

        btn_si = self.crear_boton("Si", self.responder_si, ancho=12)
        btn_no = self.crear_boton("No", self.responder_no, ancho=12)

        self.canvas.create_window(centro_x - 100, 460, window=btn_si)
        self.canvas.create_window(centro_x + 100, 460, window=btn_no)

    def responder_si(self):
        self.arbol.responder(True)
        self.mostrar_pregunta()

    def responder_no(self):
        self.arbol.responder(False)
        self.mostrar_pregunta()

    # ── RF-06, RF-07, RF-08: ADIVINANZA ──
    def mostrar_resultado_adivinanza(self):
        self.ajustar(1200, 600)
        self.limpiar()
        # Mantener botón menú visible
        self.btn_menu.place(x=16, y=12)
        centro_x = 600
        respuesta = self.arbol.obtener_contenido_actual()

        self.canvas.create_rectangle(
            200, 150, 1000, 400,
            fill="#111111",
            outline="#630000",
            width=3
        )
        self.canvas.create_text(
            centro_x, 260,
            text=f"¿Estabas pensando en: {respuesta}?",
            fill="white",
            font=("Arial", 20, "bold"),
            width=700
        )

        btn_si = self.crear_boton("Si", self.confirmar_acierto, ancho=12)
        btn_no = self.crear_boton("No", self.mostrar_formulario_aprendizaje, ancho=12)

        self.canvas.create_window(centro_x - 100, 460, window=btn_si)
        self.canvas.create_window(centro_x + 100, 460, window=btn_no)

    def confirmar_acierto(self):
        self.ajustar(1200, 600)
        self.limpiar()
        # Ya hay "Volver al inicio" en esta pantalla, no hace falta el botón persistente
        self.btn_menu.place_forget()
        centro_x = 600

        self.canvas.create_rectangle(
            275, 150, 925, 400,
            fill="#111111",
            outline="#630000",
            width=3
        )
        self.canvas.create_text(
            centro_x, 220,
            text="¡ADIVINE CORRECTAMENTE!",
            fill="#DA0000",
            font=("Impact", 28)
        )

        btn_otra_vez = self.crear_boton("Jugar otra vez", self.iniciar_partida)
        btn_inicio = self.crear_boton("Volver al inicio", self.mostrar_pantalla_inicial)

        self.canvas.create_window(centro_x, 300, window=btn_otra_vez)
        self.canvas.create_window(centro_x, 360, window=btn_inicio)

    # ── RF-08, RF-09, RF-14: APRENDIZAJE ──
    def mostrar_formulario_aprendizaje(self):
        self.ajustar(1200, 600)
        self.limpiar()
        # Mantener botón menú visible
        self.btn_menu.place(x=16, y=12)
        centro_x = 600

        self.canvas.create_rectangle(
            175, 60, 1025, 540,
            fill="#111111",
            outline="#630000",
            width=3
        )
        self.canvas.create_text(
            centro_x, 110,
            text="NO LOGRE ADIVINAR",
            fill="#DA0000",
            font=("Impact", 26)
        )

        self.canvas.create_text(
            centro_x, 170,
            text="¿En que estabas pensando?",
            fill="white",
            font=("Arial", 13)
        )
        entrada_respuesta = self.crear_entrada()
        self.canvas.create_window(centro_x, 200, window=entrada_respuesta)

        self.canvas.create_text(
            centro_x, 250,
            text=f"Escribe una pregunta de si o no que diferencie tu respuesta\nde '{self.arbol.obtener_contenido_actual()}':",
            fill="white",
            font=("Arial", 13),
            width=700
        )
        entrada_pregunta = self.crear_entrada()
        self.canvas.create_window(centro_x, 300, window=entrada_pregunta)

        self.canvas.create_text(
            centro_x, 350,
            text="La respuesta correcta a tu pregunta es:",
            fill="white",
            font=("Arial", 13)
        )

        valor_respuesta_si = BooleanVar(value=True)
        radio_si = Radiobutton(
            self.root, text="Si", variable=valor_respuesta_si, value=True,
            font=("Arial", 12), bg="#111111", fg="white",
            selectcolor="#630000", activebackground="#111111"
        )
        radio_no = Radiobutton(
            self.root, text="No", variable=valor_respuesta_si, value=False,
            font=("Arial", 12), bg="#111111", fg="white",
            selectcolor="#630000", activebackground="#111111"
        )
        self.canvas.create_window(centro_x - 50, 385, window=radio_si)
        self.canvas.create_window(centro_x + 50, 385, window=radio_no)

        btn_guardar = self.crear_boton(
            "Guardar aprendizaje",
            lambda: self.procesar_aprendizaje(
                entrada_respuesta.get(),
                entrada_pregunta.get(),
                valor_respuesta_si.get()
            )
        )
        self.canvas.create_window(centro_x, 460, window=btn_guardar)

    def procesar_aprendizaje(self, respuesta_correcta, nueva_pregunta, respuesta_para_si):
        respuesta_correcta = respuesta_correcta.strip()
        nueva_pregunta = nueva_pregunta.strip()

        if not respuesta_correcta or not nueva_pregunta:
            messagebox.showerror(
                "Datos incompletos",
                "Debes completar la respuesta correcta y la nueva pregunta."
            )
            return

        self.arbol.aprender(respuesta_correcta, nueva_pregunta, respuesta_para_si)

        ruta_destino = self.arbol.ruta_archivo or ARCHIVO_DEFAULT
        try:
            self.arbol.guardar_json(ruta_destino)
        except ArchivoArbolInvalido as error:
            messagebox.showerror(
                "Error al guardar",
                f"El aprendizaje se aplico, pero no se pudo guardar el archivo:\n{error}"
            )

        messagebox.showinfo("¡Gracias!", "Respuesta guardada.")
        self.iniciar_partida()