"""Configuración por entorno, para poder desplegar sin tocar el código.

Los valores por defecto son exactamente el comportamiento de siempre, así que
correrlo local sigue funcionando igual sin definir ninguna variable.

En Hugging Face Spaces el sistema de archivos es de solo lectura salvo /tmp, y
el dominio no es localhost, así que allá se definen las tres variables.
"""

import os

# Carpeta donde se escriben la base y los archivos subidos (avatares, robots).
# En local es la carpeta backEnd; en el Space, /tmp.
DATOS = os.environ.get("PYROBOTS_DATA", "..")

# Base de la URL de WebSocket que se le entrega al frontend.
WS_BASE = os.environ.get("PYROBOTS_WS", "ws://localhost:8000")

# Orígenes permitidos por CORS, separados por coma.
ORIGENES = [
    o.strip()
    for o in os.environ.get("PYROBOTS_ORIGINS", "http://localhost:3000").split(",")
    if o.strip()
]


def ruta(*partes: str) -> str:
    """Arma una ruta dentro de la carpeta de datos."""
    return os.path.join(DATOS, *partes)


def preparar_carpetas() -> None:
    """Crea la carpeta de datos y sus subcarpetas si no existen.

    Hace falta en el Space: /tmp arranca vacío en cada reinicio, así que si no
    se crean, falla tanto abrir la base como el primer alta de usuario.
    """
    os.makedirs(DATOS, exist_ok=True)
    for nombre in ("user_avatars", "robot_avatars", "robot_files"):
        os.makedirs(ruta(nombre), exist_ok=True)


# Se ejecuta al importar y no desde endpoints.py a propósito: la base se abre
# cuando se importa `models`, que pasa ANTES de que corra nada de endpoints. Si
# la carpeta no existe todavía, Pony falla con "unable to open database file".
preparar_carpetas()
