import json
from pathlib import Path


class ArchivoJSON:
    """Lee y guarda una lista de registros en un archivo JSON."""

    def __init__(self, ruta):
        self.__ruta = Path(ruta)

    @property
    def ruta(self):
        return self.__ruta

    def leer(self):
        # Si el archivo todavía no existe, se trabaja con una lista vacía.
        if not self.__ruta.exists():
            return []
        with self.__ruta.open(encoding="utf-8") as archivo:
            registros = json.load(archivo)
        if type(registros) != list:
            raise ValueError(f"El archivo {self.__ruta.name} debe contener una lista.")
        return registros

    def guardar(self, registros):
        self.__ruta.parent.mkdir(parents=True, exist_ok=True)
        # Se escribe primero en un temporal para no dañar el archivo original.
        temporal = self.__ruta.with_name(self.__ruta.name + ".tmp")
        try:
            with temporal.open("w", encoding="utf-8") as archivo:
                json.dump(registros, archivo, ensure_ascii=False, indent=4)
                archivo.write("\n")
            temporal.replace(self.__ruta)
        finally:
            if temporal.exists():
                temporal.unlink()
