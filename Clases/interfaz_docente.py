import tkinter as tk
from tkinter import messagebox, ttk


class VentanaAnadirDocente(tk.Toplevel):
    """Carrera -> semestre -> asignatura -> datos del docente."""

    def __init__(self, master, gestion):
        super().__init__(master)
        self.title("Añadir docente")
        self.resizable(False, False)
        self.__gestion = gestion
        self.__carreras = []
        self.__niveles = []
        self.__asignaturas = []

        marco = tk.Frame(self, padx=20, pady=20)
        marco.pack()

        # --- Selección en cascada ---
        tk.Label(marco, text="Carrera:").grid(row=0, column=0, sticky="e", pady=3)
        self.__comboCarrera = ttk.Combobox(marco, state="readonly", width=40)
        self.__comboCarrera.grid(row=0, column=1, pady=3)
        self.__comboCarrera.bind("<<ComboboxSelected>>", self.__alElegirCarrera)

        tk.Label(marco, text="Semestre:").grid(row=1, column=0, sticky="e", pady=3)
        self.__comboNivel = ttk.Combobox(marco, state="disabled", width=40)
        self.__comboNivel.grid(row=1, column=1, pady=3)
        self.__comboNivel.bind("<<ComboboxSelected>>", self.__alElegirNivel)

        tk.Label(marco, text="Asignatura:").grid(row=2, column=0, sticky="e", pady=3)
        self.__comboAsignatura = ttk.Combobox(marco, state="disabled", width=40)
        self.__comboAsignatura.grid(row=2, column=1, pady=3)

        # --- Datos del docente ---
        tk.Label(marco, text="Cédula:").grid(row=3, column=0, sticky="e", pady=(15, 3))
        self.__entradaCedula = tk.Entry(marco, width=43)
        self.__entradaCedula.grid(row=3, column=1, pady=(15, 3))

        tk.Label(marco, text="Nombres:").grid(row=4, column=0, sticky="e", pady=3)
        self.__entradaNombre = tk.Entry(marco, width=43)
        self.__entradaNombre.grid(row=4, column=1, pady=3)

        tk.Label(marco, text="Apellidos:").grid(row=5, column=0, sticky="e", pady=3)
        self.__entradaApellido = tk.Entry(marco, width=43)
        self.__entradaApellido.grid(row=5, column=1, pady=3)

        tk.Label(marco, text="Título graduado:").grid(row=6, column=0, sticky="e", pady=3)
        self.__entradaTitulo = tk.Entry(marco, width=43)
        self.__entradaTitulo.grid(row=6, column=1, pady=3)

        botones = tk.Frame(marco)
        botones.grid(row=7, column=0, columnspan=2, pady=(15, 0))
        tk.Button(botones, text="Guardar", command=self.__guardar).pack(side="left", padx=5)
        tk.Button(botones, text="Cerrar", command=self.destroy).pack(side="left", padx=5)

        self.__cargarCarreras()

    def __cargarCarreras(self):
        self.__carreras = self.__gestion.listarCarreras()
        nombres = []
        for carrera in self.__carreras:
            nombres.append(carrera.nombre)
        self.__comboCarrera["values"] = nombres

    def __alElegirCarrera(self, evento=None):
        carrera = self.__carreraElegida()
        self.__comboNivel.set("")
        self.__comboAsignatura.set("")
        self.__comboAsignatura["values"] = []
        self.__comboAsignatura.config(state="disabled")

        self.__niveles = self.__gestion.listarNiveles(carrera)
        if not self.__niveles:
            self.__comboNivel["values"] = []
            self.__comboNivel.config(state="disabled")
            messagebox.showinfo(
                "Sin malla", "Esta carrera todavía no tiene semestres registrados "
                "en su malla curricular.", parent=self)
            return
        textos = []
        for nivel in self.__niveles:
            textos.append(f"Semestre {nivel}")
        self.__comboNivel["values"] = textos
        self.__comboNivel.config(state="readonly")

    def __alElegirNivel(self, evento=None):
        carrera = self.__carreraElegida()
        nivel = self.__nivelElegido()
        self.__asignaturas = self.__gestion.listarAsignaturas(carrera, nivel)
        textos = []
        for asignatura in self.__asignaturas:
            textos.append(f"{asignatura.idAsignatura} - {asignatura.nombreAsignatura}")
        self.__comboAsignatura.set("")
        self.__comboAsignatura["values"] = textos
        self.__comboAsignatura.config(state="readonly")

    def __carreraElegida(self):
        indice = self.__comboCarrera.current()
        if indice < 0:
            return None
        return self.__carreras[indice]

    def __nivelElegido(self):
        indice = self.__comboNivel.current()
        if indice < 0:
            return None
        return self.__niveles[indice]

    def __asignaturaElegida(self):
        indice = self.__comboAsignatura.current()
        if indice < 0:
            return None
        return self.__asignaturas[indice]

    def __guardar(self):
        try:
            docente = self.__gestion.registrarDocente(
                self.__carreraElegida(),
                self.__asignaturaElegida(),
                self.__entradaCedula.get(),
                self.__entradaNombre.get(),
                self.__entradaApellido.get(),
                self.__entradaTitulo.get()
            )
        except ValueError as error:
            messagebox.showerror("Datos incorrectos", str(error), parent=self)
            return
        messagebox.showinfo(
            "Docente guardado",
            f"{docente.nombreCompleto} quedó registrado con la asignatura elegida.",
            parent=self)
        self.__limpiarDatos()

    def __limpiarDatos(self):
        # La carrera/semestre se conservan por si se añaden más docentes.
        self.__comboAsignatura.set("")
        for entrada in (self.__entradaCedula, self.__entradaNombre,
                        self.__entradaApellido, self.__entradaTitulo):
            entrada.delete(0, tk.END)


class VentanaListaDocentes(tk.Toplevel):
    """Muestra los docentes guardados y las materias que dan."""

    def __init__(self, master, gestion):
        super().__init__(master)
        self.title("Docentes registrados")
        self.__gestion = gestion

        marco = tk.Frame(self, padx=15, pady=15)
        marco.pack(fill="both", expand=True)

        self.__texto = tk.Text(marco, width=70, height=22)
        barra = tk.Scrollbar(marco, command=self.__texto.yview)
        self.__texto.config(yscrollcommand=barra.set)
        self.__texto.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self.actualizar()

    def actualizar(self):
        self.__texto.config(state="normal")
        self.__texto.delete("1.0", tk.END)
        self.__texto.insert(tk.END, self.__gestion.resumenDocentes())
        self.__texto.config(state="disabled")
