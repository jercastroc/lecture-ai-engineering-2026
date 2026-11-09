# Clase 2 - Respuestas

## Ejercicio

- Modelo y configuración (del `config` de result.json): Qwen/Qwen3.5-0.8B (revision 2fc06364), LoRA sin cuantización, 20 épocas, lr 2e-4, lora_r 16, lora_alpha 32, warmup 6, seed 42, generación greedy. Colab con T4. Versiones: transformers 5.18.0, peft 0.21.1, trl 1.14.2, torch 2.14.1+cu130 (la de Colab, no la 2.11 de las diapositivas).
- Entrené yo mismo (`executed_training_myself`): sí. Corrí el cuaderno completo de arriba abajo.
- Antes de entrenar: format_rate = 0.095 (2 de 21) / content_rate = 0.0
- Después de entrenar: format_rate = 1.0 / content_rate = 0.857 (18 de 21)
- Entrenamiento: 40 pasos, 227 s. Parámetros entrenables 6 389 760 de 758 782 784 (0.84%). Loss en los pasos 10, 20, 30 y 40: 1.5625, 0.0838, 0.0184, 0.0138.
- Preguntas que empeoraron: ninguna.
- Fallos que quedaron (3), los tres son preguntas sin base en el FAQ que el modelo contestó con needs_review en false, copiando el texto de otro ítem del FAQ:
  - "¿Cuándo salen las notas?" respondió con la fecha de entrega.
  - "¿Hay límite de caracteres?" respondió con el formato PDF.
  - "¿Hay que reservar para las horas de atención?" respondió con el horario de atención.
  Es el tipo "afirmó sin base". No vi fallos del tipo "evadió con base" ni de formato roto.
- Preguntas de conocimiento (sección 6), antes -> después:
  - Fecha de la tarea final: format_error -> asserted (repitió la fecha de entrega del FAQ, que es otra cosa).
  - Nombre del profesor: format_error -> needs_review.
  - Tema de la próxima clase: format_error -> needs_review.
  - Control, fecha de entrega (sí está en el FAQ): format_error -> asserted, correcto.
- Qué cambió y qué no: el formato pasó de casi nunca a siempre correcto, y el contenido de 0 a 18 de 21. Lo que no se resolvió es saber si el FAQ respalda la pregunta: en 3 preguntas sin respaldo (y en la de la tarea final) respondió con seguridad usando otro ítem. Con solo 14 ejemplos de entrenamiento, 4 de ellos sin base, no puedo decir si más datos lo arreglarían; solo puedo decir lo que pasó aquí.

## Tarea

- Nivel elegido: Básico.
- Qué cambié: solo `num_train_epochs`, de 20 a 10 (20 pasos en vez de 40). Todo lo demás igual. Reinicié la sesión de Colab y volví a correr desde el principio.
- Resultados (misma evaluación de 21 preguntas):

| | 20 épocas | 10 épocas |
|---|---|---|
| format_rate después | 1.0 | 1.0 |
| content_rate después | 0.857 | 0.857 |
| Loss final | 0.0138 (paso 40) | 0.1001 (paso 20) |
| Tiempo de entrenamiento | 227 s | 114 s |
| Preguntas que empeoraron | 0 | 0 |
| Fallos que quedan | 3 | 3 |

  Antes de entrenar el resultado fue el mismo en las dos corridas (format 0.095, content 0.0).
- Lo que vi: las dos tasas fueron idénticas aunque la loss final es unas 7 veces mayor con 10 épocas. Una loss más baja no significó mejor resultado en esta evaluación. Con la mitad de épocas el entrenamiento duró la mitad y llegó igual.
- Lo que cambió fue el tipo de fallo. Con 10 épocas las tres preguntas fallidas fueron otras:
  - "¿Se puede entregar en otro formato además de PDF?" (sí tiene base en el FAQ): dijo que no estaba en el FAQ, o sea se escapó con needs_review en true.
  - "¿Hay límite de caracteres?" y "¿Cómo se citan las referencias?" (sin base): puso needs_review en true, que es lo correcto, pero la respuesta repitió el ítem de la ubicación de entrega ("...la sección de Tareas" / "...la sección de Referencias", esta última inventada) y no incluyó la palabra "confirmar", por eso cuenta como error de contenido.
  Así que con 20 épocas el error era afirmar sin base y con 10 épocas apareció escaparse y una respuesta con texto inventado aunque la marca era correcta. Una sola corrida por configuración, y el entrenamiento en GPU no es exactamente reproducible, así que no sé si esto es efecto de las épocas o de la variación entre corridas.
- Preguntas de conocimiento con 10 épocas: las mismas clases que con 20. Una respuesta salió con un error de redacción ("必ずに確認が必要です").
- Cuándo sirve y cuándo no el fine-tuning (según lo que vi, no una regla general): sirvió para fijar un formato de salida que el prompt solo no lograba en un modelo de 0.8B (de 2 a 21 de 21), con pocos minutos de GPU. No sirvió para que el modelo juzgue cuándo no hay información: siguió usando datos de otros ítems con seguridad. Para eso una búsqueda sobre el FAQ, o una verificación aparte, parece más adecuada que entrenar más.
