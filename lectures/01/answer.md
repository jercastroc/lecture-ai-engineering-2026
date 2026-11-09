# Clase 1

## Práctica

- Respuesta del modelo a la pregunta de los tres niveles: dijo que no tenía información de AIE2026 y pidió más contexto sobre la institución y la materia.
- El glosario dice: Básico (repasar el contenido de la clase), Implementación (escribir código por cuenta propia) y Avanzado (investigar o experimentar), y basta con uno. El modelo dio una respuesta general porque no conoce el curso.
- Tokens (entrada / salida): 19 / 162.

## Tarea

Nivel: Avanzado.

En `app/ask.py` medí el tiempo de respuesta y mostré los tokens de entrada, salida, pensamiento y total. También agregué pruebas en `tests/test_ask.py` sin usar la API. Corrí dos preguntas con dos modelos: "LoRAとは何ですか？" y la de los tres niveles.

| Modelo | Pregunta | Tiempo | Tokens (entrada / salida / pensamiento / total) |
|---|---|---|---|
| flash-lite | LoRA | 2.81, 2.45 y 2.73 s | 7 / 587, 569, 604 / 0 / 594, 576, 611 |
| flash-lite | tres niveles | 3.33, 3.21 y 2.68 s | 21 / 781, 695, 514 / 0 / 802, 716, 535 |
| 3.8-flash | LoRA | 179.07 s (1 vez) | 7 / 788 / 787 / 1582 |
| 3.8-flash | tres niveles | 19.83 s (1 vez) | 21 / 742 / 1070 / 1833 |

Lo que vi:
- flash-lite fue rápido y estable, entre 2.5 y 3.3 s, y no usó tokens de pensamiento. Los tokens de salida variaron mucho entre ejecuciones de la misma pregunta (de 514 a 781), así que una sola medición engaña.
- 3.8-flash gastó entre 787 y 1070 tokens de pensamiento, así que el total fue 2 o 3 veces mayor aunque la salida visible fue parecida.
- Con 3.8-flash los tiempos fueron muy distintos (179 s y 19.83 s) y no sé por qué. La segunda llamada a LoRA no respondió en más de 3 minutos y la corté, por eso solo hay una ejecución por pregunta con ese modelo.
- Con la pregunta del curso, en las ejecuciones que miré el modelo no dijo que no sabía, sino que dio una descripción general de niveles distinta a la del glosario.

Sobre la cuota: el material indica 15 por minuto y 500 por día para flash-lite, y 5 por minuto y unas 10 a 20 por día para 3.8-flash. Con llamadas de 20 a 180 s no llegué al límite por minuto; lo que pesa es el diario, porque cada medición repetida gasta una de esas pocas solicitudes. No revisé la cuota real en AI Studio. Son números de una sola sesión, no prueban una diferencia general entre modelos.

Modelos usados: gemini-3.5-flash-lite y gemini-3.8-flash.
