# Clase 3

## Ejercicio

- Diferencia con la clase 1: en la clase 1 el modelo contestó algo general sin conocer el curso. El agente buscó una vez `3レベル` en el glosario y respondió con eso; la respuesta empieza con "1. 基礎: 講義内容の確認", que coincide con `homework-levels`.
- Con `--trace` en "LoRAとQLoRAの違いは？" llamó a `search_glossary` con `LoRA` y después con `QLoRA`, un término por búsqueda.
- Llamadas al LLM por pregunta (`requests`): 2 en las tres que probé. Una para decidir qué herramienta usar y otra para redactar la respuesta.
- Herramienta que agregué: `make_quiz(lecture)`. En el docstring puse que se usa cuando piden una pregunta de repaso, que el modelo haga la pregunta tal cual y dé la respuesta solo después de que el usuario conteste. Si la clase no tiene términos, devuelve un mensaje en vez de fallar.
- Con `--trace "第2回の内容から確認問題を1問出して"` salió `make_quiz({'lecture': 2})` y la pregunta "「学習率」の意味は？". Usé gemini-3.5-flash-lite.

## Tarea

Nivel: Implementación.

Hice `save_learning_log(topic, notes)`, que guarda un `.md` con fecha y hora en `learning_log/`. Lo registré con `requires_approval=True`, puse `output_type=[str, DeferredToolRequests]` y escribí `run_with_approval`, que pregunta `[y/N]` por cada llamada pendiente y vuelve a ejecutar con `DeferredToolResults` y el historial. Agregué `learning_log/` al `.gitignore` y pruebas en `tests/test_learning_tools.py` sin usar la API.

Resultados con la API real:
- Pedí que guardara una nota sobre LoRA y respondí `y`: apareció la confirmación y se guardó `20261109-050657.md`.
- Pedí lo mismo sobre RAG y respondí `n`: el resultado fue "The tool call was denied" y no se creó ningún archivo nuevo.

Después de la negativa el modelo no insistió, dijo que si quería guardar se lo avisara. En el caso de RAG, antes de pedir guardar también buscó "RAG" en el glosario.

Una duda: como `learning_log/` está en el `.gitignore`, las notas no se suben con el PR. Si se quisieran versionar habría que quitar esa línea.
