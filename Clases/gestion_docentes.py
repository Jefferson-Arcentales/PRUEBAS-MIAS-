from almacenamiento import ArchivoJSON
from carrera import Carrera
from docente import Docente


class GestionDocentes:
    """Conecta las carreras (con sus mallas) con los docentes guardados."""

    def __init__(self, carpetaDatos):
        self.__archivoCarreras = ArchivoJSON(carpetaDatos / "carreras.json")
        self.__archivoDocentes = ArchivoJSON(carpetaDatos / "docentes.json")
        self.__carreras = []
        self.__docentes = []
        self.cargar()

    #Método: cargar

    def cargar(self):
        self.__carreras = []
        for registro in self.__archivoCarreras.leer():
            self.__carreras.append(Carrera.desdeDiccionario(registro))
        # Los docentes se cargan después porque necesitan las carreras.
        self.__docentes = []
        for registro in self.__archivoDocentes.leer():
            self.__docentes.append(Docente.desdeDiccionario(registro, self.__carreras))

    # Consultas usadas por la interfaz (carrera -> nivel -> asignatura)

    def listarCarreras(self):
        return list(self.__carreras)

    def listarNiveles(self, carrera):
        return carrera.mostrarMallaCurricular().niveles

    def listarAsignaturas(self, carrera, nivel):
        return carrera.mostrarMallaCurricular().consultarAsignaturasNivel(nivel)

    def listarDocentes(self):
        return list(self.__docentes)

    def buscarDocente(self, cedula):
        for docente in self.__docentes:
            if docente.idDocente == cedula.strip():
                return docente
        return None

    #Método: registrarDocente

    def registrarDocente(self, carrera, asignatura, cedula, nombre, apellido, titulo):
        if carrera is None or asignatura is None:
            raise ValueError("Seleccione la carrera, el semestre y la asignatura.")

        docente = self.buscarDocente(cedula)
        if docente is None:
            nuevo = True
            docente = Docente(cedula, nombre, apellido, titulo)
        else:
            # Misma cédula: es la misma persona, solo se le suma otra asignatura.
            nuevo = False
            if (docente.nombreDocente.lower() != nombre.strip().lower()
                    or docente.apellidoDocente.lower() != apellido.strip().lower()):
                raise ValueError(
                    "Esa cédula ya pertenece a " + docente.nombreCompleto + "."
                )

        docente.vincularAsignatura(carrera, asignatura)
        if nuevo:
            self.__docentes.append(docente)
        self.guardar()
        return docente

    def guardar(self):
        registros = []
        for docente in self.__docentes:
            registros.append(docente.anadirDiccionario())
        self.__archivoDocentes.guardar(registros)

    #Método: resumenDocentes
    # Texto sencillo con cada docente y las materias que imparte.

    def resumenDocentes(self):
        if not self.__docentes:
            return "No hay docentes guardados."
        lineas = []
        for docente in self.__docentes:
            lineas.append(f"{docente.nombreCompleto} - C.I. {docente.idDocente}")
            lineas.append(f"   Título: {docente.tituloGraduado}")
            if not docente.asignaturasImparte:
                lineas.append("   Sin asignaturas vinculadas")
            for registro in docente.asignaturasImparte:
                lineas.append(
                    f"   - {registro['asignatura'].nombreAsignatura}"
                    f" ({registro['carrera'].nombre})"
                )
            lineas.append("")
        return "\n".join(lineas)
