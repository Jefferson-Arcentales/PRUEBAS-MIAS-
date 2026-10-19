import tkinter as tk

from interfaz_docente import VentanaAnadirDocente, VentanaListaDocentes


class MenuPrincipal(tk.Frame):
    """Menú que aparece después de iniciar sesión."""

    def __init__(self, master, gestor, gestion, alCerrarSesion):
        super().__init__(master, padx=30, pady=30)
        self.__gestion = gestion
        self.__alCerrarSesion = alCerrarSesion

        tk.Label(self, text=f"Bienvenido/a, {gestor.nombreGestor}").pack(pady=(0, 15))
        tk.Button(self, text="Añadir docente", width=25,
                  command=self.__abrirAnadir).pack(pady=4)
        tk.Button(self, text="Ver docentes", width=25,
                  command=self.__abrirLista).pack(pady=4)
        tk.Button(self, text="Cerrar sesión", width=25,
                  command=self.__alCerrarSesion).pack(pady=(15, 0))

    def __abrirAnadir(self):
        VentanaAnadirDocente(self, self.__gestion)

    def __abrirLista(self):
        VentanaListaDocentes(self, self.__gestion)
