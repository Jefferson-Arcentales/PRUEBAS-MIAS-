import tkinter as tk
from tkinter import messagebox

from almacenamiento import ArchivoJSON
from gestor_academico import GestorAcademico


class Login:
    """Lógica del inicio de sesión (sin interfaz gráfica)."""

    def __init__(self, rutaGestores):
        # Composición: el login maneja su propio archivo de gestores.
        self.__archivo = ArchivoJSON(rutaGestores)
        self.__gestorActual = None

    @property
    def gestorActual(self):
        return self.__gestorActual

    def cargarGestores(self):
        gestores = []
        for registro in self.__archivo.leer():
            gestores.append(GestorAcademico.desdeDiccionario(registro))
        return gestores

    #Método: registrarGestor
    # Lo usa crear_gestor.py: las cuentas las crean ustedes, no se auto-registran.

    def registrarGestor(self, correo, nombreGestor, contrasena):
        nuevo = GestorAcademico(correo, nombreGestor)
        nuevo.establecerContrasena(contrasena)
        registros = self.__archivo.leer()
        for registro in registros:
            if registro["correo"] == nuevo.correo:
                raise ValueError("Ya existe un gestor con ese correo.")
        registros.append(nuevo.anadirDiccionario())
        self.__archivo.guardar(registros)
        return nuevo

    #Método: iniciarSesion

    def iniciarSesion(self, correo, contrasena):
        # Se usa el mismo mensaje de error para no revelar qué dato falló.
        mensaje = "Correo o contraseña incorrectos."
        try:
            correo = GestorAcademico.validarCorreo(correo)
        except ValueError:
            raise ValueError(mensaje)
        for gestor in self.cargarGestores():
            if gestor.correo == correo:
                if gestor.verificarContrasena(contrasena):
                    self.__gestorActual = gestor
                    return gestor
                break
        raise ValueError(mensaje)

    #Método: cerrarSesion

    def cerrarSesion(self):
        self.__gestorActual = None


class VentanaLogin(tk.Frame):
    """Pantalla de inicio de sesión con Tkinter."""

    def __init__(self, master, login, alIngresar):
        super().__init__(master, padx=30, pady=30)
        self.__login = login
        # Función que se ejecuta cuando el ingreso es correcto.
        self.__alIngresar = alIngresar

        tk.Label(self, text="Chronomind - Inicio de sesión").grid(
            row=0, column=0, columnspan=2, pady=(0, 15))

        tk.Label(self, text="Correo institucional:").grid(row=1, column=0, sticky="e")
        self.__entradaCorreo = tk.Entry(self, width=32)
        self.__entradaCorreo.grid(row=1, column=1, pady=4)

        tk.Label(self, text="Contraseña:").grid(row=2, column=0, sticky="e")
        self.__entradaClave = tk.Entry(self, width=32, show="*")
        self.__entradaClave.grid(row=2, column=1, pady=4)

        tk.Button(self, text="Ingresar", command=self.__intentarIngreso).grid(
            row=3, column=0, columnspan=2, pady=(15, 0))

        # Enter también ingresa.
        self.__entradaCorreo.bind("<Return>", lambda evento: self.__intentarIngreso())
        self.__entradaClave.bind("<Return>", lambda evento: self.__intentarIngreso())
        self.__entradaCorreo.focus()

    def __intentarIngreso(self):
        try:
            gestor = self.__login.iniciarSesion(
                self.__entradaCorreo.get(), self.__entradaClave.get()
            )
        except ValueError as error:
            messagebox.showerror("No se pudo ingresar", str(error))
            self.__entradaClave.delete(0, tk.END)
            return
        self.__alIngresar(gestor)
