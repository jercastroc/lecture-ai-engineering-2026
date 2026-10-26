"""Configuración compartida por todo el curso.

La clave de API y el nombre del modelo se leen de variables de entorno, no del código.
"""

import os

# Modelo predeterminado. Puedes cambiarlo con la variable de entorno AIE_MODEL.
#   Ejemplo: export AIE_MODEL=gemini-3.5-flash-lite
DEFAULT_MODEL = "gemini-3.5-flash-lite"
MODEL = os.getenv("AIE_MODEL", DEFAULT_MODEL)


def api_error_message(status: int, detail: str = "") -> str:
    """Convierte un estado HTTP en un mensaje para el usuario (compartido por ask.py y agent.py)."""
    if status == 429:
        return "Se alcanzó el límite de solicitudes. Espera aproximadamente un minuto y vuelve a intentarlo."
    if status == 503:
        return "El modelo está ocupado (503). Espera un poco y vuelve a intentarlo."
    if status in (400, 401, 403, 404):
        return f"Hay un problema con la clave de API o el nombre del modelo ({status}): {detail}"
    return f"Error de API ({status}): {detail}"


def get_api_key() -> str:
    """Devuelve GEMINI_API_KEY; si no está definida, muestra instrucciones y termina."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise SystemExit(
            "No se encontró la variable de entorno GEMINI_API_KEY.\n"
            "1. En GitHub, ve a Settings → Codespaces → Secrets y registra GEMINI_API_KEY.\n"
            "   Selecciona tu fork como repositorio autorizado.\n"
            "2. Si la registraste después de iniciar Codespaces, reinicia Codespaces.\n"
            "   (Codespaces, abajo a la izquierda → Stop Current Codespace → vuelve a abrirlo)"
        )
    return key
