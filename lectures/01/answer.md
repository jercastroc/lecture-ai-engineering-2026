# Respuesta de la clase 1

## Práctica

- Respuesta del modelo a la pregunta específica del curso sobre los tres niveles (resumen): dijo que no tenía información de AIE2026 y pidió más contexto sobre la institución y la materia.
- Diferencias con la definición correcta del glosario: el glosario define los niveles como «Básico (repasar el contenido de la clase)», «Implementación (escribir código por cuenta propia)» y «Avanzado (investigar o experimentar)». Basta con completar uno. El modelo dio una respuesta general y no conocía la definición específica del curso.
- Tokens mostrados (entrada / salida): 19 / 162.

## Tarea

- Nivel elegido: Avanzado.
- Qué hice: añadí la medición del tiempo de respuesta a `app/ask.py` y ejecuté dos preguntas con `gemini-3.5-flash-lite` y `gemini-3.8-flash` para comparar tiempos y tokens.
- Resultados:

  | Pregunta | Modelo | Resultado |
  |---|---|---|
  | ¿Qué es LoRA? | gemini-3.5-flash-lite | 2,754 s; entrada 7 / salida 593 tokens |
  | ¿Cuáles son los tres niveles de la tarea? | gemini-3.5-flash-lite | 1,396 s; entrada 19 / salida 162 tokens |
  | ¿Qué es LoRA? | gemini-3.8-flash | La nueva ejecución sigue en curso; registrar el resultado cuando termine. |
  | ¿Cuáles son los tres niveles de la tarea? | gemini-3.8-flash | Pendiente de ejecutar tras completar la solicitud anterior. |

  `gemini-3.5-flash-lite` respondió a ambas preguntas. En esta ejecución, LoRA produjo una respuesta más larga y tardó más que la pregunta específica del curso. Cada combinación se ejecutó una sola vez, por lo que no demuestra una diferencia general de rendimiento.
- Observaciones y preguntas: los límites gratuitos indicados en el material son 15 solicitudes por minuto y 500 al día para `gemini-3.5-flash-lite`, y 5 por minuto y aproximadamente 10–20 al día para `gemini-3.8-flash`. Los límites reales pueden cambiar; deben comprobarse en AI Studio. Anotaré también los fallos tal como ocurran.
- Modelos usados: `gemini-3.5-flash-lite` y `gemini-3.8-flash`.
