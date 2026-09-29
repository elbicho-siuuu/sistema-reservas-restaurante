# Diseño de casos de prueba - Evaluación 2

## 1. Objetivo y alcance

Este documento relaciona las reglas de negocio actuales con sus particiones de equivalencia, valores límite, casos diseñados y pruebas automatizadas existentes.

El alcance incluye:

- La creación de reservas mediante `crear_reserva()`.
- La API FastAPI de `api.py`.
- El flujo HTTP probado mediante Playwright.

No se incluyen base de datos, autenticación, cancelación de reservas ni una interfaz gráfica, porque no existen en el proyecto actual.

## 2. Casos derivados de las reglas de negocio

### Regla 1: al menos una mesa y máximo 3 mesas

| Partición | Valores representativos | Resultado esperado | Caso y prueba |
|---|---|---|---|
| Válida: entre 1 y 3 mesas | 1, 2 y 3 mesas | Aceptar | `R1-C01`: `test_acepta_una_reserva_con_mesas_diferentes`; `R1-C02`: `test_acepta_una_reserva_con_hasta_tres_mesas`; el caso de 1 mesa aparece en `test_post_reservas_crea_una_reserva_valida`. |
| Inválida: sin mesas | 0 mesas | Rechazar | `R1-C03`: no existe una prueba automatizada específica. |
| Inválida: más de 3 mesas | 4 o más mesas | Rechazar | `R1-C04`: `test_rechaza_una_reserva_con_mas_de_tres_mesas`. |

Límites comprobados: 3 mesas es válido y 4 mesas es inválido. El caso de 0 mesas está definido por el código, pero no está cubierto por una prueba actual.

### Regla 2: capacidad de las mesas

| Partición | Valores representativos | Resultado esperado | Caso y prueba |
|---|---|---|---|
| Válida: personas menores que la capacidad | 2 personas en mesas con capacidad total 8 | Aceptar | `R2-C01`: `test_acepta_una_reserva_con_mesas_diferentes`. |
| Válida: personas iguales a la capacidad | 6 personas en mesas de capacidad 4 + 2 | Aceptar | `R2-C02`: `test_acepta_cantidad_de_personas_igual_a_capacidad_total`. |
| Inválida: personas superiores a la capacidad | 7 personas en mesas de capacidad 4 + 2 | Rechazar | `R2-C03`: `test_rechaza_cantidad_de_personas_superior_a_capacidad_total`. |
| Inválida: cero personas | 0 personas | Rechazar | `R2-C04`: `test_rechaza_cantidad_de_personas_cero`. |
| Inválida: cantidad negativa | -1 personas | Rechazar | `R2-C05`: `test_rechaza_cantidad_de_personas_negativa`. |

Límites comprobados: capacidad exacta y capacidad exacta más una persona. Las capacidades cero o negativas de una mesa no tienen un caso diseñado porque el proyecto no define una regla específica para validar la capacidad de la mesa.

### Regla 3: no solapamiento de reservas

| Partición | Situación | Resultado esperado | Caso y prueba |
|---|---|---|---|
| Inválida: misma mesa y horarios superpuestos | Reserva existente 20:00-22:00; nueva 21:00-23:00 | Rechazar | `R3-C01`: `test_rechaza_solapamiento_en_la_misma_mesa`. |
| Válida: misma mesa, sin solapamiento por límite | Reserva existente termina a las 22:00; nueva comienza a las 22:00 | Aceptar | `R3-C02`: `test_acepta_reserva_que_comienza_al_terminar_la_anterior`. |
| Válida: mesas diferentes con horarios superpuestos | Una reserva usa M1 y la otra M2 | Aceptar | `R3-C03`: no existe una prueba específica en `test_reservas.py`; el caso no está diseñado actualmente. |

La condición aplicada por el código es:

```text
inicio_nueva < termino_existente
y
termino_nueva > inicio_existente
```

No existe una prueba específica para el caso inverso, donde la nueva reserva termina exactamente cuando comienza la existente.

### Regla 4: anticipación mínima de 60 minutos

| Partición | Valor | Resultado esperado | Caso y prueba |
|---|---|---|---|
| Inválida: menor que 60 minutos | 59 minutos | Rechazar | `R4-C01`: `test_rechaza_reserva_con_menos_de_60_minutos_de_anticipacion`. |
| Válida en el límite | Exactamente 60 minutos | Aceptar | `R4-C02`: `test_acepta_reserva_con_exactamente_60_minutos_de_anticipacion`. |
| Válida: mayor que 60 minutos | 61 minutos | Aceptar | `R4-C03`: `test_acepta_reserva_con_mas_de_60_minutos_de_anticipacion`. |

El valor de 60 minutos es inclusivo.

### Regla 5: anticipación máxima de 30 días

| Partición | Valor | Resultado esperado | Caso y prueba |
|---|---|---|---|
| Válida: menor que 30 días | 29 días | Aceptar | `R5-C01`: `test_acepta_reserva_con_menos_de_30_dias_de_anticipacion`. |
| Válida en el límite | Exactamente 30 días | Aceptar | `R5-C02`: `test_acepta_reserva_con_exactamente_30_dias_de_anticipacion`. |
| Inválida: mayor que 30 días | 30 días y 1 microsegundo | Rechazar | `R5-C03`: `test_rechaza_reserva_con_mas_de_30_dias_de_anticipacion`. |

La implementación compara la anticipación del inicio de la reserva. No existe un caso diseñado para un inicio dentro de los 30 días cuyo término quede después de ese límite.

### Regla 6: mesas únicas

| Partición | Situación | Resultado esperado | Caso y prueba |
|---|---|---|---|
| Válida: identificadores diferentes | `[M1, M2]` | Aceptar | `R6-C01`: `test_acepta_una_reserva_con_mesas_diferentes`. |
| Inválida: identificador repetido | `[M1, M1]` | Rechazar | `R6-C02`: `test_rechaza_la_misma_mesa_repetida_en_una_reserva`. |

La validación se realiza antes del cálculo de capacidad y compara los identificadores físicos de las mesas.

## 3. Validaciones técnicas adicionales

Estas validaciones no son reglas de disponibilidad, pero forman parte de la creación de una reserva válida.

| Caso | Resultado esperado | Prueba |
|---|---|---|
| `termino == inicio` | Rechazar | `test_rechaza_termino_igual_al_inicio`. |
| `termino < inicio` | Rechazar | `test_rechaza_termino_anterior_al_inicio`. |
| `termino > inicio` | Aceptar en los casos válidos | Cubierto indirectamente por las pruebas de creación válida. |

## 4. Tabla de decisión para crear una reserva

La reserva solo se crea cuando todas las condiciones necesarias son verdaderas.

| Condición                               | T1: caso válido | T2: falla una condición |

| Tiene al menos una mesa                              | Sí | No |
| Tiene como máximo 3 mesas                            | Sí | No |
| Las mesas son únicas                                 | Sí | No |
| Personas mayores que cero                            | Sí | No |
| Capacidad suficiente                                 | Sí | No |
| Término posterior al inicio                          | Sí | No |
| Anticipación entre 60 minutos y 30 días              | Sí | No |
| No existe solapamiento                               | Sí | No |
| Resultado                               | Crear `Reserva` | Lanzar `ValueError`     |

Las pruebas actuales comprueban principalmente cada condición de forma aislada. No existe una prueba automatizada para cada combinación posible de condiciones inválidas; esas combinaciones se consideran descartadas por su costo combinatorio y porque la función debe rechazar la reserva cuando falla cualquiera de las condiciones.

## 5. Trazabilidad de la API

| Caso | Operación | Resultado esperado | Prueba |
|---|---|---|---|
| `API-C01` | Consultar `GET /mesas` | Devolver el catálogo M1, M2 y M3 | `test_get_mesas_devuelve_el_catalogo`. |
| `API-C02` | Crear una reserva válida mediante el handler de `POST /reservas` | Devolver una reserva con identificador y cantidad de personas | `test_post_reservas_crea_una_reserva_valida`. |
| `API-C03` | Consultar reservas mediante el handler de `GET /reservas` | Devolver la reserva creada en memoria | `test_get_reservas_devuelve_las_reservas_creadas`. |

Las pruebas de `test_api.py` llaman directamente a los handlers; no realizan peticiones HTTP mediante `TestClient`.

## 6. Trazabilidad E2E

| Caso | Flujo | Resultado esperado | Prueba |
|---|---|---|---|
| `E2E-C01` | Consultar mesas, crear una reserva por HTTP y consultar las reservas | La reserva creada aparece en la respuesta de `GET /reservas` | `tests/e2e/test_reservas_e2e.py::test_flujo_completo_reserva`. |

El fixture E2E inicia Uvicorn, espera a que la API responda y utiliza Playwright `APIRequestContext` para realizar las peticiones HTTP reales.

## 7. Casos sin diseño específico

Las pruebas de `tests/test_modelos.py` verifican que las dataclasses conserven sus datos básicos. No representan un Diseño de Uso ni una regla de negocio, por lo que no se les asigna un caso de este documento.

Tampoco existe actualmente una prueba E2E separada para cada regla de negocio. El E2E existente cubre únicamente el flujo válido completo; las reglas se cubren en las pruebas unitarias de `test_reservas.py`.
