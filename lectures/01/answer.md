# Respuesta de la clase 1

## Práctica

- Respuesta del modelo a la pregunta específica del curso sobre los tres niveles (resumen): dijo que no tenía información de AIE2026 y pidió más contexto sobre la institución y la materia.
- Diferencias con la definición correcta del glosario: el glosario define los niveles como «Básico (repasar el contenido de la clase)», «Implementación (escribir código por cuenta propia)» y «Avanzado (investigar o experimentar)». Basta con completar uno. El modelo dio una respuesta general y no conocía la definición específica del curso.
- Tokens mostrados (entrada / salida): 19 / 162.

## Tarea

- Nivel elegido: Avanzado.
- Qué hice: en `app/ask.py` mido el tiempo de respuesta con `time.perf_counter()` (también cuando la llamada falla) y muestro los tokens de entrada, salida, pensamiento (`thoughts_token_count`) y total. Agregué pruebas en `tests/test_ask.py` que no usan la API. Corrí dos preguntas con dos modelos en Codespaces, usando mi clave como secreto del Codespaces. Preguntas: "LoRAとは何ですか？" y la pregunta del curso sobre los tres niveles. Para `gemini-3.5-flash-lite` hice 3 ejecuciones por pregunta; para `gemini-3.8-flash` pude hacer solo 1 por pregunta (explico abajo).
- Resultados:

| Modelo | Pregunta | Tiempo | Tokens entrada / salida / pensamiento / total |
|---|---|---|---|
| flash-lite | LoRA | 2.81 s, 2.45 s, 2.73 s (mediana 2.73 s) | 7 / 587, 569, 604 / 0 / 594, 576, 611 |
| flash-lite | tres niveles | 3.33 s, 3.21 s, 2.68 s (mediana 3.21 s) | 21 / 781, 695, 514 / 0 / 802, 716, 535 |
| 3.8-flash | LoRA | 179.07 s (1 ejecución) | 7 / 788 / 787 / 1582 |
| 3.8-flash | tres niveles | 19.83 s (1 ejecución) | 21 / 742 / 1070 / 1833 |

- Lo que vi:
  - `gemini-3.5-flash-lite` fue rápido y estable, entre 2.5 y 3.3 s, y no usó tokens de pensamiento. El número de tokens de salida varió bastante entre ejecuciones de la misma pregunta (514 a 781), así que una sola medición engaña.
  - `gemini-3.8-flash` gastó entre 787 y 1070 tokens de pensamiento, por lo que el total fue 2 o 3 veces mayor que en flash-lite aunque la salida visible tuvo un tamaño parecido. Los tokens de salida solos no muestran el gasto real.
  - Con 3.8-flash los tiempos fueron muy distintos entre preguntas: 179 s y 19.83 s. No sé la causa. La segunda llamada a LoRA no había respondido después de más de 3 minutos y la corté con Ctrl+C. Por eso no hay segunda ejecución con ese modelo, ni tercera ni cuarta. No lo repetí.
  - Con la pregunta del curso, en las ejecuciones que miré el modelo no dijo que no sabía, sino que contestó con una descripción general de niveles, distinta de la del glosario.
- Observaciones y límites: el material indica 15 solicitudes por minuto y 500 al día para flash-lite, y 5 por minuto y unos 10 a 20 al día para 3.8-flash. Con una llamada de 20 a 180 s no llegué al límite por minuto de 3.8-flash; el límite que importa en la práctica es el diario, porque cada medición repetida gasta una de esas pocas solicitudes. No comprobé la cuota real en AI Studio. Los números son de una sola sesión, así que no demuestran una diferencia general entre modelos.
- Modelos usados: `gemini-3.5-flash-lite` y `gemini-3.8-flash`.
