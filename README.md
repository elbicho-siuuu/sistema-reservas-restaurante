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

### Comandos de Verificación de Calidad
* **Análisis Estático:** `uv run ruff check`
* **Verificación de Tipos:** `uv run pyrefly`
* **Suite de Pruebas:** `uv run pytest`

## 📋 Catálogo de Reglas de Negocio

1. **Regla 1 (Límite de Mesas):** Una reserva no puede incluir más de 3 mesas en total.
2. **Regla 2 (Capacidad de Aforo):** La cantidad de personas de la reserva no puede superar la capacidad total acumulada de las mesas seleccionadas.
3. **Regla 3 (Disponibilidad y Superposición):** Una misma mesa no puede estar asignada a dos reservas con horarios superpuestos.
4. **Regla 4 (Anticipación Mínima):** La reserva debe realizarse con al menos 60 minutos de anticipación respecto a la hora de inicio.
5. **Regla 5 (Anticipación Máxima):** La reserva no puede realizarse con más de 30 días de anticipación.
6. **Regla 6 (Unicidad de Mesas):** Una misma mesa física no puede seleccionarse más de una vez dentro de una misma reserva.

## 🤖 Uso de IA y Agentes (Enfoque Adversarial)

* **Herramientas:** ChatGPT y CodexAI.
* **Flujo Adversarial Aplicado:**
  * *Propuesta de IA:* ChatGPT diseñó la prueba inicial para la asignación de mesas aceptando la duplicación del mismo objeto mesa en la lista.
  * *Auditoría de IA:* CodexAI alertó que esto permitía inflar artificialmente la capacidad total de asientos simulando que una mesa de 4 se convertía en una de 8.
  * *Arbitraje Humano:* Identifiqué este fallo como un vacío crítico de lógica que rompía el negocio. Rechacé la propuesta automatizada, implementé la restricción de identificación única en `crear_reserva()` para dar origen a la **Regla 6** y escribí el test unitario manual correspondiente.
