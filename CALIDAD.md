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
| Limitar una reserva a un máximo de 3 mesas. | Una reserva con 1, 2 o 3 mesas se acepta; una con 4 mesas se rechaza. | Prueba unitaria: `test_acepta_una_reserva_con_hasta_tres_mesas` y `test_rechaza_una_reserva_con_mas_de_tres_mesas` en `tests/test_reservas.py`. Resultado: pruebas aprobadas. |  |
| Evitar que la cantidad de personas supere la capacidad de las mesas. | La cantidad de personas debe ser menor o igual a la capacidad total. | Pruebas unitarias: `test_rechaza_cantidad_de_personas_superior_a_capacidad_total` y `test_acepta_cantidad_de_personas_igual_a_capacidad_total` en `tests/test_reservas.py`. Resultado: pruebas aprobadas. |  |
| Impedir reservas solapadas para una misma mesa. | Los intervalos se solapan cuando `inicio_nueva < termino_existente` y `termino_nueva > inicio_existente`; comenzar exactamente al terminar es válido. | Pruebas unitarias: `test_rechaza_solapamiento_en_la_misma_mesa` y `test_acepta_reserva_que_comienza_al_terminar_la_anterior` en `tests/test_reservas.py`. Resultado: pruebas aprobadas. |  |
| Exigir al menos 60 minutos de anticipación. | Una reserva con 59 minutos se rechaza y una con exactamente 60 minutos se acepta. | Pruebas unitarias: `test_rechaza_reserva_con_menos_de_60_minutos_de_anticipacion` y `test_acepta_reserva_con_exactamente_60_minutos_de_anticipacion` en `tests/test_reservas.py`. Resultado: pruebas aprobadas. |  |
| Limitar la anticipación máxima a 30 días. | Una reserva con 29 días o exactamente 30 días se acepta; una con 30 días y una unidad de tiempo adicional se rechaza. | Pruebas unitarias: `test_acepta_reserva_con_menos_de_30_dias_de_anticipacion`, `test_acepta_reserva_con_exactamente_30_dias_de_anticipacion` y `test_rechaza_reserva_con_mas_de_30_dias_de_anticipacion` en `tests/test_reservas.py`. Resultado: pruebas aprobadas. |  |
| Mantener la calidad técnica del código. | El código debe superar las comprobaciones automatizadas de estilo y análisis estático. | `ruff`: sin errores. `pyrefly`: 0 errores. Pruebas unitarias: 18 pruebas en `tests/test_reservas.py`. Pruebas de integración: 4 pruebas en `tests/test_api.py` y 4 pruebas en `tests/test_modelos.py`. Pruebas no funcionales: 10 pruebas en `tests/test_no_funcionales.py`, sobre rendimiento, seguridad y privacidad/protección de datos, documentadas en `NO-FUNCIONALES.md`. Prueba E2E: 1 prueba en `tests/e2e/test_reservas_e2e.py`. Total: 37 pruebas. |  |

Las evidencias de validación se mantienen vacías porque todavía no se ha registrado una validación manual o una demostración con usuarios. Las pruebas automatizadas corresponden a evidencia de verificación.

## 3. Justificación de diagnósticos ignorados

Actualmente no existen diagnósticos de `ruff` o `pyrefly` ignorados.

- `ruff` finaliza sin errores y sin reglas desactivadas para el código revisado.
- `pyrefly` informa 0 errores.
- Pyrefly muestra una advertencia informativa indicando que no existe un archivo `pyrefly.toml` y que utiliza su configuración básica. Esta advertencia no fue ignorada como diagnóstico de código.

## 4. Hallazgos de auditoría

### Hallazgo 1: Se podía repetir una misma mesa

Durante las primeras pruebas del sistema encontramos un problema que no habíamos considerado en las reglas iniciales.

El sistema permitía seleccionar la misma mesa más de una vez dentro de una reserva. Esto provocaba que la capacidad se sumara nuevamente, aunque físicamente solo existiera una mesa.

Por ejemplo, si `M1` tiene una capacidad de 4 personas y se seleccionaba `M1` dos veces, el sistema calculaba una capacidad de 8 personas.

A partir de este problema se creó la **Regla 6**, que establece que una misma mesa no puede ser seleccionada más de una vez en una reserva.

#### Corrección

La validación se realiza en `crear_reserva()` en `src/trabajo_eval_1/reservas.py` antes de calcular la capacidad de las mesas.

Se obtienen los identificadores de las mesas seleccionadas:

```python
identificadores_mesas = [mesa.identificador for mesa in mesas]
if len(identificadores_mesas) != len(set(identificadores_mesas)):
    raise ValueError("La reserva no puede incluir la misma mesa más de una vez.")
```

Si un identificador aparece más de una vez, se lanza un `ValueError`. Esto también permite detectar objetos diferentes que representan la misma mesa física.

La prueba unitaria `test_rechaza_la_misma_mesa_repetida_en_una_reserva()` en `tests/test_reservas.py` verifica que el sistema rechaza correctamente las mesas repetidas.

**Estado: Corregido y probado.**

---

### Hallazgo 2: Código sin uso

Durante una revisión del proyecto realizada con apoyo de **GeminiAI**, se encontró que el enumerador `EstadoCliente` y la propiedad `estado` de la clase `Cliente` no estaban siendo utilizados por ninguna de las reglas ni por la lógica de reservas.

Esto no afectaba el funcionamiento actual del sistema ni las 6 reglas de negocio, pero mantenía código que no cumplía ninguna función.

#### Corrección

Se eliminaron `EstadoCliente` y la propiedad `estado` de `Cliente`. La clase `Cliente` en `src/trabajo_eval_1/modelos.py` ahora contiene únicamente:

```python
@dataclass
class Cliente:
    identificador: str
    nombre: str
```

La prueba `test_cliente_contiene_sus_datos_basicos()` en `tests/test_modelos.py` verifica que la clase `Cliente` mantiene correctamente sus datos básicos tras la eliminación del código sin uso.

**Estado: Corregido y eliminado del código actual.**

---

### Hallazgo 3: Faltaban pruebas para algunas validaciones

Durante una revisión de las pruebas del sistema, realizada con apoyo de **GeminiAI**, se encontró que algunas validaciones que ya existen en `reservas.py` no tenían pruebas unitarias específicas.

Las validaciones corresponden a impedir una cantidad de personas menor o igual a 0 y a impedir que la hora de término de una reserva sea anterior o igual a la hora de inicio.

Esto no significaba que las validaciones estuvieran funcionando mal, sino que no existían pruebas que comprobaran que el sistema rechazara correctamente estos casos.

#### Corrección

Se agregaron pruebas unitarias utilizando `pytest.raises(ValueError)` en `tests/test_reservas.py` para comprobar que:

* `test_rechaza_cantidad_de_personas_cero()`: Una cantidad de personas igual a 0 sea rechazada.
* `test_rechaza_cantidad_de_personas_negativa()`: Una cantidad de personas negativa sea rechazada.
* `test_rechaza_termino_igual_al_inicio()`: Una hora de término igual a la hora de inicio sea rechazada.
* `test_rechaza_termino_anterior_al_inicio()`: Una hora de término anterior a la hora de inicio sea rechazada.

De esta forma, las validaciones quedan comprobadas mediante pruebas automatizadas y se reduce el riesgo de que dejen de funcionar por cambios futuros en el código.

**Estado: Corregido con pruebas implementadas.**

---

## 5. Búsqueda de hallazgos de validación

Durante la auditoría del estado actual del proyecto se realizó una investigación exhaustiva para identificar casos donde las pruebas automatizadas existentes pasaran pero el sistema incumpliera una regla de negocio (hallazgo de validación).

Se revisaron:
- La lógica de validación en `src/trabajo_eval_1/reservas.py`
- Las pruebas unitarias en `tests/test_reservas.py` (18 pruebas)
- Las pruebas de integración en `tests/test_api.py` (4 pruebas)
- Las pruebas de modelos en `tests/test_modelos.py` (4 pruebas)
- Las pruebas no funcionales en `tests/test_no_funcionales.py` (10 pruebas)
- La prueba E2E en `tests/e2e/test_reservas_e2e.py` (1 prueba)

En total, el proyecto cuenta con 37 pruebas automatizadas. Las pruebas no funcionales cubren rendimiento, seguridad y privacidad/protección de datos y están documentadas en `NO-FUNCIONALES.md`.

**Conclusión: No se logró identificar ni reproducir un caso real donde las pruebas automatizadas pasen pero el sistema incumpla una regla de negocio.**

Las validaciones implementadas son coherentes con las reglas de negocio y las pruebas cubren adecuadamente los casos límite. No existe un hallazgo de validación que reportar en este ciclo de auditoría.
