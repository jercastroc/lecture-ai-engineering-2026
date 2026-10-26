# Clase 1: práctica y tarea. Preparar el entorno y preguntar a un LLM

## Objetivos

- Abrir tu fork en Codespaces y llamar a la API de Gemini.
- Hacer pequeños cambios en el código con GitHub Copilot.
- Entregar el trabajo mediante un PR desde una rama de trabajo. Se seguirá este mismo flujo en las próximas clases.

## Requisitos

- Una cuenta personal de GitHub. Según la configuración de la organización, una cuenta administrada por una empresa podría no tener acceso a Codespaces o Copilot.
- Una cuenta personal de Google. Según la configuración del administrador, una cuenta de Google Workspace de empresa podría no tener acceso a AI Studio.

## Práctica (45 minutos)

### 1. Crea un fork del repositorio del curso

Usa **Fork**, en la parte superior derecha del repositorio del curso, para crear un fork en tu cuenta. A partir de ahora, trabaja siempre en tu fork.

### 2. Crea una clave de Gemini API

Crea y copia una clave en [Google AI Studio](https://aistudio.google.com/apikey).

> La clave de API es secreta. No la incluyas en el código, el chat ni los commits. Si se filtra, elimínala en AI Studio y crea otra.

### 3. Registra la clave como secreto de Codespaces

En GitHub, ve a **Settings → Codespaces → Secrets → New secret** y registra estos datos:

- Name: `GEMINI_API_KEY`
- Value: la clave del paso 2
- Repository access: selecciona **tu fork**

> Registra el secreto antes de iniciar Codespaces. Si lo registras después, tendrás que reiniciar Codespaces.

### 4. Inicia Codespaces

En tu fork, selecciona **Code → Codespaces → Create codespace on main**. La primera preparación del entorno puede tardar unos minutos. En la terminal, ejecuta lo siguiente y confirma que pasen las pruebas:

```bash
uv run pytest -q
```

### 5. Haz preguntas a un LLM sin herramientas

```bash
uv run python -m app.ask "¿Qué es LoRA?"
uv run python -m app.ask "¿Cuáles son los tres niveles de las tareas del curso AIE2026?"
```

La primera pregunta trata un tema general y debería obtener una respuesta aproximadamente correcta. La segunda trata una definición específica del curso. Como el LLM no conoce el curso, puede decir que no lo sabe o responder con una explicación general que parezca convincente. La definición correcta está en `data/glossary.json`, bajo `homework-levels`. Compara ambas respuestas.

Si tienes tiempo, prueba también otras preguntas específicas del curso. Observa que las respuestas pueden variar entre ejecuciones y que el modelo puede responder con seguridad incluso cuando no sabe algo.

```bash
uv run python -m app.ask "¿Qué significa la etiqueta lecNN-start que se usa en el curso AIE2026?"
uv run python -m app.ask "¿Qué se aprende en la clase 2 de AIE2026?"
```

### 6. Muestra el número de tokens con Copilot

Modifica `app/ask.py` para mostrar los tokens de entrada y salida. Puedes usar el autocompletado o el chat de Copilot, pero lee y entiende el código sugerido antes de adoptarlo.

### 7. Crea una rama y abre un PR

```bash
git switch -c lec01
# Escribe lectures/01/answer.md
git add -A
git commit -m "Práctica de la clase 1"
git push -u origin lec01
```

En tu fork de GitHub, crea un PR desde `lec01` hacia `main`. **Comprueba que el repositorio base sea tu fork**; no abras el PR hacia el repositorio del curso.

### 8. Detén Codespaces

En la esquina inferior izquierda, selecciona **Codespaces → Stop Current Codespace**. Si lo dejas ejecutándose, seguirá consumiendo tu cuota gratuita.

## Tarea (basta con completar un nivel)

| Nivel | Contenido |
|---|---|
| Básico | Ejecuta la misma pregunta tres veces, cambiando el modelo con la variable de entorno `AIE_MODEL` o cambiando la temperatura. Resume las diferencias en `answer.md`. |
| Implementación | Modifica `app/ask.py` para poder seguir preguntando y conservar el historial de la conversación. |
| Avanzado | Mide el tiempo de respuesta y los tokens, y compara varios modelos y preguntas. Analiza también la relación con los límites de la cuota gratuita. |

### Cambiar el modelo

El límite gratuito depende del modelo. Según la información de la clase:

| Modelo | Límite gratuito indicado | Uso recomendado |
|---|---|---|
| `gemini-3.5-flash-lite` | 15 solicitudes por minuto y 500 al día | Límite alto; adecuado para repetir pruebas y hacer comparaciones. |
| `gemini-3.8-flash` | 5 por minuto y aproximadamente 10–20 al día; puede responder con error 503 | Modelo más potente; úsalo para pocas preguntas. |

Ejemplos:

```bash
AIE_MODEL=gemini-3.5-flash-lite uv run python -m app.ask "¿Qué es LoRA?"
AIE_MODEL=gemini-3.8-flash uv run python -m app.ask "¿Qué es LoRA?"
```

No uses `gemini-3.5-flash` (sin `-lite`): está obsoleto desde el 8 de octubre de 2026 y se redirige a `gemini-3.6-flash`. Los límites cambian según el modelo y pueden variar; consulta la cuota actual en AI Studio antes de probar.

### Cambiar la temperatura

Consulta el argumento `config` de `generate_content`. Google declaró obsoleta la temperatura el 21 de julio de 2026, así que puede ignorarse o producir un error. Si lo pruebas, anota el resultado tal como ocurra.
