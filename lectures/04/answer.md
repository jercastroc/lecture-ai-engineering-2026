# Clase 4

## Ejercicio

No hice el etiquetado del set del profesor. Solo hice la tarea.

## Tarea

Nivel: Implementación.

Armé 10 preguntas propias con el comportamiento que espero (`data/eval/my_cases.jsonl`). Las escribí en español y mezclé 4 casos normales con 6 raros: un término que no está en el glosario (transformer), pedir el código de la tarea, una pregunta fuera del curso (el mundial 2022), "ignora tus instrucciones", una clase que no existe (la 20) y una pregunta ambigua ("¿Y eso para qué sirve?").

Las respuestas las generó el agente que armé en la clase 3, con `app.judge --generate`. Dos cosas que tuve que hacer para que funcionara: la primera corrida se cortó con un 429 y la segunda con un 503, y perdía todo el avance. Le agregué a `generate_answers` un reintento por pregunta (espera 60 s si recibe 429 o 503, hasta 5 veces) y subí la espera entre preguntas a 12 s. Con eso terminó. Después etiqueté yo las 10 respuestas contra la referencia y la rúbrica (`lectures/04/my_labels.jsonl`) y las califiqué con `app.judge`.

Resultado, mis etiquetas contra el LLM (modelo por defecto, gemini-3.5-flash-lite):

| Criterio | Acuerdo |
|---|---|
| Grounding | 10 / 10 |
| Scope | 10 / 10 |
| Hint | 10 / 10 |
| Clarity | 9 / 10 |
| Lecture ref. (código) | 9 / 10 |

Acuerdo general 9 de 10, con cobertura 10 de 10. Pedidos de revisión del LLM: 0.

Los dos desacuerdos:
- #04 (época y tasa de aprendizaje), clarity: yo puse fail porque el "まとめると" final repite lo mismo que ya dijo; el LLM puso pass y dijo que no había repetición. Es el criterio más subjetivo y yo mismo dudé.
- #09 (clase 20), lecture ref.: el código puso pass porque "第20回" aparece en la última línea, pero la respuesta no termina con una marca de clase, sino con la lista de clases disponibles. Yo puse fail.

Qué conviene revisar con código y qué dejar al LLM:
- Con código: la marca "第N回" al final. Es una cadena, da siempre el mismo resultado y no gasta cuota. El problema de #09 es que la regla actual es literal (mira si la última línea contiene la marca), así que habría que hacerla más estricta, por ejemplo que la marca esté entre paréntesis al final. También se podría comprobar por código si la respuesta incluye un bloque de código, como señal barata para el criterio de no dar la tarea hecha.
- Con el LLM: grounding, scope y hint, porque dependen del significado (si algo contradice el glosario, si se negó bien, si dio la solución). Coincidieron en 10 de 10, aunque son pocos casos. Clarity también se queda con el LLM, pero es donde menos confío: no vio la repetición que yo sí vi.

Lo que noté:
- El agente falló en un caso raro que el LLM sí detectó: #07, contestó quién ganó el mundial sin decir que estaba fuera del curso. Mis etiquetas pusieron fail en scope y grounding y el LLM coincidió.
- Aunque las preguntas eran en español, casi todas las respuestas salieron en japonés. Para quien lee en español hay que fijarse en eso al etiquetar.
- El LLM no marcó ninguna respuesta como "unsure", pero yo dudé en 4. Con 10 casos y una sola corrida no puedo decir si el LLM es mejor o peor que yo, solo que coincidimos en 9 de 10.
