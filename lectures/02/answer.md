# Clase 2

## Ejercicio

- Modelo y configuración: Qwen3.5-0.8B con LoRA sin cuantizar, 20 épocas, lr 2e-4, r 16, seed 42. Lo corrí en Colab con la T4.
- Entrené yo mismo: sí.
- Antes de entrenar: format_rate 0.095 y content_rate 0.0.
- Después de entrenar: format_rate 1.0 y content_rate 0.857 (18 de 21).
- El entrenamiento fueron 40 pasos y tardó 227 s. La loss bajó de 1.56 a 0.0138. Se entrenan 6.4 millones de parámetros de 758 millones (0.84%).
- Preguntas que empeoraron: ninguna.
- Fallos que quedaron (3): son preguntas que no están en el FAQ (cuándo salen las notas, si hay límite de caracteres, si hay que reservar para las horas de atención). El modelo contestó con needs_review en false copiando el texto de otro ítem del FAQ. Es el caso de afirmar sin base.
- Preguntas de conocimiento: la fecha de la tarea final salió "asserted" (repitió la fecha de entrega). El nombre del profesor y el tema de la próxima clase salieron "needs_review". La de control (fecha de entrega) salió "asserted", y ahí está bien porque sí está en el FAQ.
- Lo que cambió con el entrenamiento fue el formato. Lo que no cambió es que el modelo sepa cuándo el FAQ no tiene la respuesta.

## Tarea

Nivel: Básico.

Cambié solo `num_train_epochs`, de 20 a 10 (20 pasos). Reinicié la sesión y corrí todo otra vez desde arriba.

| | 20 épocas | 10 épocas |
|---|---|---|
| format_rate | 1.0 | 1.0 |
| content_rate | 0.857 | 0.857 |
| loss final | 0.0138 | 0.1001 |
| tiempo | 227 s | 114 s |
| empeoraron | 0 | 0 |
| fallos | 3 | 3 |

Las dos tasas salieron iguales aunque la loss final con 10 épocas es mucho mayor. Una loss más baja no se tradujo en mejor resultado aquí.

Los fallos sí fueron distintos. Con 10 épocas falló "¿Se puede entregar en otro formato además de PDF?", que sí tiene respuesta en el FAQ, y el modelo dijo que no estaba. En otras dos preguntas sin respuesta en el FAQ (límite de caracteres y referencias) puso needs_review en true, que es correcto, pero la respuesta repitió el texto de la entrega y no incluía "confirmar", así que cuenta como error de contenido.

Solo hice una corrida de cada una y el entrenamiento en GPU no se repite exactamente, así que no puedo decir si esa diferencia viene de las épocas o del azar.

Sobre cuándo sirve el fine-tuning: en este caso sirvió para fijar el formato, que el prompt solo no lograba con un modelo tan chico. No sirvió para que el modelo juzgue cuándo no hay información, porque siguió usando datos de otros ítems con seguridad. Para eso me parece mejor buscar en el FAQ que seguir entrenando.
