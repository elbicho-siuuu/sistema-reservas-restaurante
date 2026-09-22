## Instalación y ejecución

### Requisitos

El proyecto requiere:

- Python 3.14.7.
- `uv` para administrar el entorno y las dependencias.

La versión de Python está indicada en `.python-version` y el proyecto también exige Python 3.14 o superior en `pyproject.toml`.

### Obtener el proyecto

Clona el repositorio o copia la carpeta completa del proyecto. Luego, abre una terminal dentro de la carpeta `Trabajo Eval 1`.

Si utilizas Git, el comando tiene esta forma:

```powershell
git clone <URL_DEL_REPOSITORIO>
cd "Trabajo Eval 1"
```

### Instalar dependencias

Comprueba que Python sea la versión requerida:

```powershell
python --version
```

Sincroniza el entorno del proyecto e instala las dependencias de desarrollo:

```powershell
uv sync
```

Esto instala las herramientas definidas en el grupo de desarrollo: `pytest`, `ruff` y `pyrefly`.

### Ejecutar el proyecto

El script configurado en `pyproject.toml` se ejecuta con:

```powershell
uv run trabajo-eval-1
```

### Ejecutar las pruebas

```powershell
uv run pytest
```

### Revisar la calidad del código

Ejecuta `ruff` sobre el código fuente y las pruebas:

```powershell
uv run ruff check src tests
```

Ejecuta `pyrefly` para realizar el análisis estático:

```powershell
uv run pyrefly check
```

## Uso de IA o agentes

**Herramientas:** ChatGPT, CodexAI

**Uso:**

* **ChatGPT:** Apoyo para definir el alcance y las reglas de negocio del sistema.

* **ChatGPT:** Apoyo para diseñar la estructura inicial del sistema y sus entidades.

* **ChatGPT:** Apoyo para revisar las pruebas y analizar la cobertura de las reglas de negocio.

* **CodexAI:** Generación de la estructura inicial del proyecto, modelos y pruebas básicas.

* **CodexAI:** Implementación de las reglas de negocio y generación de pruebas específicas.

* **CodexAI:** Verificación mediante `pytest`, `ruff` y `pyrefly`.

**Trabajo realizado por el estudiante:**

* Elección del sistema de reservas de restaurante como proyecto.

* Elección, revisión y modificación de las reglas de negocio propuestas.

* Incorporación de una regla que limita las reservas a un máximo de 30 días de anticipación.

* Decisión sobre la estructura del restaurante, incluyendo pisos y tipos de ubicación de las mesas.

* Revisión de las propuestas y código generado por las herramientas de IA.

* Revisión de las pruebas generadas y de los casos cubiertos por ellas.

* Verificación de los resultados obtenidos mediante las herramientas de calidad.

**Revisiones/correcciones realizadas:**

* Se revisó la estructura generada por CodexAI y se comprobó que las entidades correspondieran al diseño planteado.

* Se identificó que las primeras pruebas generadas comprobaban principalmente que las entidades almacenaran correctamente sus datos, pero no verificaban todavía las reglas de negocio.

* Se mantuvieron las pruebas básicas como base y posteriormente se incorporaron pruebas específicas para las reglas de negocio.

* Se revisó la cobertura de las pruebas y se identificaron escenarios de las reglas de negocio que todavía requieren una revisión adicional.

* Se verificó que `pytest` ejecutara correctamente las pruebas y que `ruff` y `pyrefly` no presentaran errores.

**Error o limitación detectada:**

* Los primeros tests generados por CodexAI no comprobaban las reglas de negocio del sistema, por lo que no eran suficientes para cumplir con el requisito de tener al menos una prueba por cada regla. Se decidió mantenerlos como pruebas básicas y agregar posteriormente pruebas específicas para las reglas de negocio.
