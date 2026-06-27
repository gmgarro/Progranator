import tkinter as tk

from Interfaz.app_gui import AppGUI


def main():
    ventana = tk.Tk()
    AppGUI(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()