"""Crea una cuenta de gestor académico. Uso:

    python crear_gestor.py correo@live.uleam.edu.ec "Nombre Apellido" contraseña
"""

import sys
from pathlib import Path

from login import Login

CARPETA_DATOS = Path(__file__).resolve().parent.parent / "datos"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    login = Login(CARPETA_DATOS / "gestores_academicos.json")
    try:
        gestor = login.registrarGestor(sys.argv[1], sys.argv[2], sys.argv[3])
    except ValueError as error:
        print(f"Error: {error}")
        sys.exit(1)
    print(f"Gestor creado: {gestor.nombreGestor} ({gestor.correo})")
