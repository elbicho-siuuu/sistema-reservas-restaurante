## Instalación y ejecución

### Requisitos

El proyecto requiere:

- Python 3.14.7.
- `uv` para administrar el entorno y las dependencias.

La versión de Python está indicada en `.python-version` y el proyecto también exige Python 3.14 o superior en `pyproject.toml`.

### Obtener el proyecto

Clona el repositorio o copia la carpeta completa del proyecto. Luego, abre una terminal dentro de la carpeta `sistema-reservas-restaurante`.

Si utilizas Git, el comando tiene esta forma:

```powershell
git clone <https://github.com/elbicho-siuuu/sistema-reservas-restaurante.git>
cd "sistema-reservas-restaurante"
```

### Instalar dependencias

Comprueba que Python sea la versión requerida:

```powershell
python --version
```

Sincroniza el entorno del proyecto e instala las dependencias de desarrollo:

```powershell
uv sync --dev
```

### Comandos de Verificación de Calidad
* **Verificación de Tipos:** `uv run pyrefly check`
* **Análisis Estático:** `uv run ruff check .`
* **Pruebas unitarias:** `uv run pytest tests/test_reservas.py tests/test_modelos.py`
* **Pruebas de integración:** `uv run pytest tests/test_api.py`
* **Pruebas no funcionales:** `uv run pytest tests/test_no_funcionales.py`
* **Pruebas E2E:** `uv run pytest tests/e2e/`

## 📋 Catálogo de Reglas de Negocio

1. **Regla 1 (Límite de Mesas):** Una reserva no puede incluir más de 3 mesas en total.
2. **Regla 2 (Capacidad de Aforo):** La cantidad de personas de la reserva no puede superar la capacidad total acumulada de las mesas seleccionadas.
3. **Regla 3 (Disponibilidad y Superposición):** Una misma mesa no puede estar asignada a dos reservas con horarios superpuestos.
4. **Regla 4 (Anticipación Mínima):** La reserva debe realizarse con al menos 60 minutos de anticipación respecto a la hora de inicio.
5. **Regla 5 (Anticipación Máxima):** La reserva no puede realizarse con más de 30 días de anticipación.
6. **Regla 6 (Unicidad de Mesas):** Una misma mesa física no puede seleccionarse más de una vez dentro de una misma reserva.

## 🤖 Uso de IA y agentes

La IA se utilizó como apoyo para analizar, implementar y revisar el proyecto. Las decisiones de aceptación, descarte y alcance fueron revisadas por el estudiante.

### Tareas apoyadas por IA o agentes

- **EP1:** propuesta de la estructura inicial, entidades, reglas de negocio, validaciones y pruebas unitarias.
- **Auditoría de EP1:** revisión de `reservas.py`, `modelos.py` y las pruebas para buscar casos no cubiertos, límites y comportamientos incorrectos.
- **EP2:** incorporación de la API FastAPI, modelos de entrada y salida, pruebas de integración, prueba E2E con Playwright y corrección de la infraestructura para iniciar Uvicorn automáticamente.
- **Evaluación final:** diseño de las pruebas de rendimiento, seguridad y privacidad, implementación técnica del derecho de supresión y preparación de la documentación y del pipeline de GitHub Actions.
- **Verificación:** ejecución de pytest, Ruff y Pyrefly, revisión de resultados y actualización de la documentación.

En la documentación de EP1 se registra además el apoyo de GeminiAI para identificar el código sin uso relacionado con `EstadoCliente` y la falta de pruebas específicas para algunas validaciones. ChatGPT y Codex/CodexAI se utilizaron para el análisis, la implementación y la revisión iterativa del proyecto.

### Revisión y decisiones del estudiante

El estudiante definió y revisó el alcance del sistema, las reglas de negocio y los criterios de aceptación. También auditó los cambios propuestos, ejecutó las pruebas, revisó los resultados y decidió qué propuestas incorporar o descartar.

Entre las decisiones técnicas tomadas directamente por el estudiante estuvieron:

- Mantener la lógica de negocio de EP1 en `reservas.py` al agregar la API de EP2.
- Mantener las reservas y el catálogo en memoria, sin base de datos ni autenticación completa.
- Exigir que las pruebas de integración utilizaran `TestClient` contra `app` y que la prueba E2E utilizara Playwright con HTTP real mediante Uvicorn.
- Agregar la Regla 6 después de revisar el problema de mesas repetidas.
- Cubrir en la evaluación final rendimiento, seguridad y privacidad, implementando únicamente la supresión de reservas con un token opaco.

### Caso concreto de propuesta incorrecta o insuficiente

Durante la auditoría, una propuesta inicial apoyada por IA trataba como aceptable seleccionar `[M1, M1]`. Al reproducirla, se comprobó que el sistema sumaba dos veces la capacidad de una misma mesa. El estudiante revisó que este comportamiento no estaba incluido en las cinco reglas iniciales y decidió convertirlo explícitamente en la **Regla 6: una misma mesa no puede seleccionarse más de una vez**. Luego se implementó la validación y se agregó su prueba.

También se consideró como posible hallazgo que una persona reservara una mesa con mucha capacidad. El estudiante descartó ese caso como incumplimiento de las reglas vigentes porque la regla existente solo establece que la cantidad de personas no puede superar la capacidad total; no existe una regla que exija una utilización mínima de la mesa. Por lo tanto, no se incorporó como regla ni como defecto del código.

### Evolución de EP1 a EP2 y experimentos finales

EP1 comenzó con las entidades, las reglas de reservas y las pruebas unitarias. Tras la auditoría se corrigió la duplicación de mesas, se eliminó código sin uso y se agregaron pruebas para validaciones que no estaban cubiertas.

En EP2 el proyecto se amplió con FastAPI, pruebas de integración mediante `TestClient` y una prueba E2E mediante Playwright. Para la evaluación final se agregaron pruebas no funcionales y su documentación, sin cambiar las reglas de negocio de EP1.

Finalmente, se realizaron tres experimentos temporales controlados: se introdujo y revirtió un defecto en una regla para comprobar las pruebas unitarias, otro en el código HTTP de la API para comprobar las pruebas de integración y otro en la lectura de reservas para comprobar el flujo E2E. El estudiante revisó que cada prueba fallara por el motivo esperado y confirmó que volviera a pasar después de revertir cada defecto.
