# Clase 3 - Respuestas

## Ejercicio

- Diferencia entre la clase 1 (LLM solo) y el agente: en la clase 1 el modelo contestó con una descripción general, sin conocer el curso. El agente llamó una vez a `search_glossary` con el argumento `'3レベル'` y respondió a partir del glosario; la respuesta empieza con "1. 基礎: 講義内容の確認", que coincide con la definición de `homework-levels`.
- Llamadas a herramientas con `--trace` (pregunta "LoRAとQLoRAの違いは？"): `search_glossary({'query': 'LoRA'})` y `search_glossary({'query': 'QLoRA'})`, es decir una búsqueda por término, como pide la descripción de la herramienta ("un solo término").
- Llamadas al LLM por pregunta (`requests`): 2 en las tres preguntas de prueba (la de los tres niveles, la de LoRA y QLoRA, y la del quiz). Una llamada para decidir qué herramientas usar y otra para redactar la respuesta con lo que devolvieron.
- Herramienta que agregué: `make_quiz(lecture: int)` en `app/tools.py`, registrada en `app/agent.py`. Docstring: elige un término de la clase indicada y devuelve una pregunta y su respuesta; se usa cuando piden una pregunta de repaso o un quiz; el modelo debe hacer la pregunta tal cual y dar la respuesta solo después de que el usuario conteste. Si la clase no tiene términos devuelve un mensaje en lugar de fallar (la prueba automática la llama con `lecture=0`).
- Resultado de `--trace "第2回の内容から確認問題を1問出して"`: `[tool call] make_quiz({'lecture': 2})`, que devolvió la pregunta "「学習率」の意味は？" con su respuesta. Modelo usado: `gemini-3.5-flash-lite`.

## Tarea

- Nivel elegido: Implementación.
- Qué hice: agregué `save_learning_log(topic, notes)` en `app/tools.py`, que guarda un archivo `.md` con fecha y hora en `learning_log/`. En `app/agent.py` lo registré con `requires_approval=True` y puse `output_type=[str, DeferredToolRequests]` en el agente. Escribí `run_with_approval`: ejecuta la pregunta y, mientras el resultado sea `DeferredToolRequests`, muestra cada llamada pendiente, pregunta `[y/N]` y vuelve a ejecutar con `DeferredToolResults` y `message_history=result.all_messages()`. Agregué `learning_log/` al `.gitignore`. Pruebas en `tests/test_learning_tools.py` (con el modelo falso y sin API): el quiz, la clase sin términos, que el archivo se escribe, que se pide aprobación y guarda al responder "y", y que no guarda al responder "n".
- Resultados (corrida real en Codespaces con `gemini-3.5-flash-lite`):
  - Pedí "学習メモとして、今日はLoRAを学んだと記録して" y respondí `y`: apareció `[確認] save_learning_log({'topic': ..., 'notes': ...})`, y después se guardó `20261109-050657.md` con el mensaje "se guardó".
  - Pedí lo mismo sobre RAG y respondí `n`: apareció la confirmación, el resultado de la herramienta fue "The tool call was denied" y no se creó ningún archivo nuevo (la carpeta seguía con un solo archivo).
- Observaciones: tras la negativa el modelo no insistió; contestó que si quería guardar, se lo dijera. En el caso de RAG, antes de pedir guardar el modelo también buscó "RAG" en el glosario, no solo llamó a la herramienta de guardado. La confirmación ocurre antes de ejecutar la función, así que no queda un archivo a medias si se rechaza. Una duda: `learning_log/` queda ignorado por git, entonces los registros no se suben con el PR; si se quisieran versionar habría que quitar esa línea del `.gitignore`.
