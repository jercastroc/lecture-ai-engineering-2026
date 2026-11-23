# Clase 5

## Ejercicio

- Modelo: gemini-3.5-flash-lite (el `[model]` que salió al correr). Todo lo corrí en Codespaces.
- Pregunta: 第2回の説明では、LoRAは何を固定し何を学習しますか？ QLoRAは何を加えますか？ (la respuesta está en la clase 2, PDF p.52).
- Material: el texto completo mete los 9 documentos (227,971 caracteres); los otros tres buscan solo en las clases 1 a 3 (214 páginas). No es la misma cobertura.

### Resultados

| Método | Respuesta | Páginas citadas | Tiempo (s) | Tokens entrada / salida | Respuestas del modelo | Costo estimado (USD) |
|---|---|---|---|---|---|---|
| Texto completo | Correcta | Clase 2 p.51 y p.52 | 7.32 | 117,025 / 222 | 1 | 0.035662 |
| Búsqueda vectorial | Correcta | Clase 2 p.51-52 | 4.02 | 3,509 / 190 | 2 | 0.001528 |
| Tree | Correcta | Clase 2 p.52 | 4.65 | 9,214 / 339 | 5 | 0.003612 |
| Graph | Correcta | Clase 2 p.51 y p.52 | 2.96 | 5,776 / 206 | 2 | 0.002248 |

- Solo búsqueda (`app.retrieval "LoRA QLoRA 違い"`): devolvió p.52, 51, 60, 47 y 61 de la clase 2. La p.52 está primera y tiene la respuesta completa (pesos originales fijos, se entrenan solo las matrices pequeñas A y B, QLoRA además comprime los pesos a 4 bits).
- `--trace`: la búsqueda vectorial hizo una sola llamada, `search_materials('LoRA 固定 学習 QLoRA 追加')`. Tree fue raíz → clase 2 → el capítulo "選んだモデルを、いつ・どう直すか" → la página, por eso fueron 5 respuestas del modelo. Graph hizo una sola llamada, `search_graph`.
- Las cuatro respondieron bien esta pregunta, así que aquí no vi un caso de "faltó información". El texto completo también acertó, pero gastó unas 33 veces más tokens de entrada y fue el más caro y el más lento.
- Para este uso me quedaría con la búsqueda vectorial o Graph: misma respuesta, mucho más barato. Ojo que es una sola pregunta y una sola corrida por método.

## Tarea

Nivel: Implementación.

Qué hice: en `app/retrieval.py`, después de la búsqueda, agrego la página anterior y la siguiente de cada resultado (`add_neighbors`). Las vecinas salen del mismo índice, ordenadas por documento y página, no cruzan a otro documento y no se repiten si ya estaban. A cada vecina le pongo `neighbor_of` con la página de la que viene. Se controla con `AIE_RAG_NEIGHBORS` en `app/config.py` (1 por defecto, 0 = búsqueda normal), así pude comparar con el mismo código. Agregué pruebas en `tests/test_neighbors.py`.

Un problema que me encontré: al correr Graph saltó `KeyError: 'distance'`, porque Graph usa `search()` para sus puntos de entrada y las páginas vecinas no tienen distancia. Lo arreglé haciendo que Graph pida la búsqueda sin vecinas (`search(query, neighbors=0)`), ya que Graph de todas formas recorre las páginas contiguas por su cuenta, y le agregué una prueba.

Condiciones fijas: mismo modelo (gemini-3.5-flash-lite), mismo índice (clases 1 a 3), mismas preguntas, `RAG_TOP_K = 5`. Cambia solo `AIE_RAG_NEIGHBORS` (0 o 1).

Solo búsqueda con "LoRA QLoRA 違い": sin vecinas 5 páginas, con vecinas 11 (se sumaron p.53, 50, 59, 46, 48 y 62).

| Pregunta | Vecinas | Resultado | Páginas citadas | Tiempo (s) | Tokens entrada / salida | Costo (USD) |
|---|---|---|---|---|---|---|
| LoRA y QLoRA (1 página) | No | Correcta | Clase 2 p.51-52 | 4.02 | 3,509 / 190 | 0.001528 |
| LoRA y QLoRA (1 página) | Sí | Correcta | Clase 2 p.52 | 2.98 | 5,818 / 183 | 0.002203 |
| Compactación y memoria (varias páginas) | No | Error 503 en 9 intentos | - | - | - | - |
| Compactación y memoria (varias páginas) | Sí | Correcta | Clase 3 p.13, 39 y 40 | 2.36 | 5,013 / 272 | 0.002184 |
| Datos de nuestro RAG (no está) | No | Dice que no está en el material | Menciona clase 2 p.13 como relacionado | 9.13 | 3,598 / 214 | 0.001614 |
| Datos de nuestro RAG (no está) | Sí | Dice que no está en el material | Menciona clase 2 p.13 | 10.71 | 7,575 / 139 | 0.002620 |

Lo que vi:
- Con vecinas la entrada subió entre 1.4 y 2.1 veces en tokens, y el costo en la misma proporción. El tiempo casi no cambió.
- En la pregunta de una sola página no sumó nada: la p.52 ya alcanzaba sola. Las páginas extra (p.53, 50, 59...) son ruido para esa pregunta.
- En la pregunta de varias páginas, con vecinas la respuesta citó justo las tres páginas que pide el enunciado (p.13, 39 y 40) y respondió las dos partes: que la compactación resume el historial dentro de una sesión y que no todas las notas diarias pasan a la memoria larga. Sin vecinas no la pude comparar: dio 503 en 9 intentos seguidos (con 1 y 2 minutos de espera), mientras las otras corridas funcionaban. No sé si fue mala suerte o algo de esa combinación.
- En la pregunta que no está en el material, las dos versiones dijeron bien que no había datos. Las vecinas solo agregaron tokens.

Conclusión: sumar vecinas ayuda cuando la explicación sigue en la diapositiva de al lado y cuesta de más cuando una página basta. Me falta repetir las corridas (fue una por caso) y conseguir la de Q2 sin vecinas para comparar de verdad. Una idea sería sumar vecinas solo para el primer resultado, en vez de para los 5.
