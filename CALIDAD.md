# Calidad del sistema de reservas de restaurante

## 1. Ficha de calidad ISO/IEC 25010

| Característica prioritaria | Justificación | Criterio verificable |
| --- | --- | --- |
| Adecuación funcional | El sistema debe aplicar correctamente las reglas de negocio de las reservas. | Las pruebas automatizadas deben comprobar el máximo de 3 mesas, la capacidad total, el solapamiento de horarios y los límites de anticipación de 60 minutos y 30 días. |
| Fiabilidad | El sistema debe rechazar reservas inválidas de manera predecible y aceptar los casos válidos, especialmente en los límites. | `pytest` debe ejecutar todas las pruebas sin fallos, incluyendo los casos límite de 3 mesas, 60 minutos y 30 días. |
| Mantenibilidad | La lógica de negocio debe estar separada de las entidades y ser fácil de modificar y probar. | Las reglas deben estar concentradas en `src/trabajo_eval_1/reservas.py`, las entidades en `modelos.py` y las pruebas en `tests/test_reservas.py`; además, `ruff` no debe reportar errores. |

## 2. Tabla de trazabilidad

| Necesidad | Criterio | Evidencia de verificación | Evidencia de validación |
| --- | --- | --- | --- |
| Limitar una reserva a un máximo de 3 mesas. | Una reserva con 1, 2 o 3 mesas se acepta; una con 4 mesas se rechaza. | `tests/test_reservas.py`: `test_acepta_reserva_con_hasta_tres_mesas` y `test_rechaza_una_reserva_con_mas_de_tres_mesas`. Resultado: pruebas aprobadas. |  |
| Evitar que la cantidad de personas supere la capacidad de las mesas. | La cantidad de personas debe ser menor o igual a la capacidad total. | `tests/test_reservas.py`: pruebas para capacidad igual y superior a la capacidad disponible. Resultado: pruebas aprobadas. |  |
| Impedir reservas solapadas para una misma mesa. | Los intervalos se solapan cuando `inicio_nueva < termino_existente` y `termino_nueva > inicio_existente`; comenzar exactamente al terminar es válido. | `tests/test_reservas.py`: pruebas de solapamiento y de inicio exactamente al término de la reserva anterior. Resultado: pruebas aprobadas. |  |
| Exigir al menos 60 minutos de anticipación. | Una reserva con 59 minutos se rechaza y una con exactamente 60 minutos se acepta. | `tests/test_reservas.py`: `test_rechaza_reserva_con_menos_de_60_minutos_de_anticipacion` y `test_acepta_reserva_con_exactamente_60_minutos_de_anticipacion`. Resultado: pruebas aprobadas. |  |
| Limitar la anticipación máxima a 30 días. | Una reserva con 29 días o exactamente 30 días se acepta; una con 30 días y una unidad de tiempo adicional se rechaza. | `tests/test_reservas.py`: pruebas de 29 días, exactamente 30 días y más de 30 días. Resultado: pruebas aprobadas. |  |
| Mantener la calidad técnica del código. | El código debe superar las comprobaciones automatizadas de estilo y análisis estático. | `ruff`: sin errores. `pyrefly`: 0 errores. `pytest`: 16 pruebas aprobadas. |  |

Las evidencias de validación se mantienen vacías porque todavía no se ha registrado una validación manual o una demostración con usuarios. Las pruebas automatizadas corresponden a evidencia de verificación.

## 3. Justificación de diagnósticos ignorados

Actualmente no existen diagnósticos de `ruff` o `pyrefly` ignorados.

- `ruff` finaliza sin errores y sin reglas desactivadas para el código revisado.
- `pyrefly` informa 0 errores.
- Pyrefly muestra una advertencia informativa indicando que no existe un archivo `pyrefly.toml` y que utiliza su configuración básica. Esta advertencia no fue ignorada como diagnóstico de código ni afecta el resultado del análisis.

## 4. Hallazgos de auditoría

### Hallazgo 1: Se podía repetir una misma mesa

Durante las primeras pruebas del sistema encontramos un problema que no habíamos considerado en las reglas iniciales.

El sistema permitía seleccionar la misma mesa más de una vez dentro de una reserva. Esto provocaba que la capacidad se sumara nuevamente, aunque físicamente solo existiera una mesa.

Por ejemplo, si `M1` tiene una capacidad de 4 personas y se seleccionaba `M1` dos veces, el sistema calculaba una capacidad de 8 personas.

A partir de este problema se propone la **Regla 6**, que establece que una misma mesa no puede ser seleccionada más de una vez en una reserva.

### Corrección

Se agregó una validación en `crear_reserva()` para impedir que una misma mesa pueda repetirse dentro de una reserva. La capacidad se calcula únicamente después de comprobar que los identificadores de las mesas sean únicos.
