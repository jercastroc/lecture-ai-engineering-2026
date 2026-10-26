"""Clase 1: script para hacer una pregunta a un LLM sin herramientas.

Uso:
    uv run python -m app.ask "¿Qué es LoRA?"
    uv run python -m app.ask  # Sin pregunta, usa una pregunta específica del curso.

Es una llamada sencilla, sin herramientas ni historial de conversación.
Comprueba que, ante una pregunta específica del curso, el modelo puede decir que no sabe o
dar una respuesta general convincente, pero distinta de la realidad del curso.
En la clase 3 se mejorará con un agente que pueda consultar el glosario.
"""

import argparse
from time import perf_counter

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# Pregunta específica del curso. La respuesta está en homework-levels de data/glossary.json.
DEFAULT_QUESTION = "¿Cuáles son los tres niveles de las tareas del curso AIE2026?"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())
    started_at = perf_counter()
    try:
        response = client.models.generate_content(model=MODEL, contents=question)
    finally:
        elapsed = perf_counter() - started_at
        print(f"[tiempo de respuesta] {elapsed:.3f}s")
    usage = response.usage_metadata
    if usage is None:
        print("[tokens] metadatos de uso no disponibles")
    else:
        print(
            f"[tokens] entrada={usage.prompt_token_count}, "
            f"salida={usage.candidates_token_count}"
        )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="Hacer una pregunta a un LLM sin herramientas")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[modelo] {MODEL}")
    print(f"[Pregunta] {args.question}\n")
    try:
        print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
