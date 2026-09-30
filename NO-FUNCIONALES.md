# Pruebas no funcionales

Este documento cubre exactamente las categorías solicitadas para la evaluación final: rendimiento, seguridad y privacidad/protección de datos.

Las pruebas se ejecutan sobre la API FastAPI y mantienen las reglas de negocio de la Evaluación 1. El almacenamiento continúa siendo en memoria y no se incorpora una base de datos.

## 1. Rendimiento

### Objetivo

Medir la operación crítica `POST /reservas` en un entorno local de desarrollo.

### Criterio declarado antes de medir

- 100 solicitudes válidas consecutivas.
- Cero errores.
- Percentil 95 (`p95`) menor o igual a 500 ms.

El umbral se utiliza como criterio académico explícito para una API local en memoria. No representa una garantía de rendimiento para producción.

### Prueba realizada

`test_rendimiento_post_reservas_cumple_umbral` crea 100 reservas válidas con la mesa `M1` y horarios consecutivos sin solapamiento. La medición muestra mínimo, promedio, máximo y p95.

### Ejecución

```powershell
uv run pytest tests/test_no_funcionales.py -k rendimiento -s
```

### Resultado

La prueba ejecutó 100 solicitudes válidas sin errores (0 errores).

Resultados obtenidos:

* Tiempo mínimo: 6.459 ms
* Tiempo promedio: 7.770 ms
* Tiempo máximo: 15.944 ms
* Percentil 95 (`p95`): 10.651 ms

Criterio: `p95 ≤ 500 ms` y cero errores.

Resultado: **Cumple**.


### Limitaciones

Estos valores corresponden a una medición local con almacenamiento en memoria y no representan una garantía de rendimiento en producción. La prueba no evalúa carga distribuida, persistencia ni comportamiento de producción.

## 2. Seguridad

### Objetivo

Comprobar que la API no acepta ciegamente entradas del cliente y que sus errores no exponen información interna innecesaria.

### Criterios declarados antes de medir

- Una mesa inexistente debe devolver HTTP 404.
- Un dato de negocio inválido debe devolver HTTP 400.
- Una solicitud rechazada no debe modificar `RESERVAS`.
- Los errores no deben incluir traceback, rutas locales ni nombres internos de módulos.
- El catálogo de mesas no debe incluir datos de clientes.

### Pruebas realizadas

- `test_seguridad_mesa_inexistente_no_modifica_reservas`.
- `test_seguridad_dato_de_negocio_invalido_no_modifica_reservas`.
- `test_seguridad_error_no_expone_informacion_interna`.
- `test_seguridad_catalogo_no_expone_datos_de_clientes`.

### Ejecución

```powershell
uv run pytest tests/test_no_funcionales.py -k seguridad
```

### Limitaciones

Estas pruebas no implementan autenticación, autorización, roles, rate limiting ni protección de transporte. Solo comprueban los controles definidos en este alcance.

## 3. Privacidad y protección de datos

### Objetivo

Demostrar técnicamente un único derecho sobre los datos personales que maneja el sistema: el derecho de supresión de una reserva.

El sistema maneja actualmente `cliente_id` y `cliente_nombre` con la finalidad de asociar una reserva a su cliente. La implementación de este derecho no constituye una certificación de cumplimiento legal integral de la Ley 21.719.

### Criterios declarados antes de medir

- Un token correcto debe permitir la supresión y producir HTTP 204.
- Un token incorrecto debe producir HTTP 403 y conservar la reserva.
- Una reserva inexistente debe producir HTTP 404.
- El token no debe ser un dato personal ni aparecer en `GET /reservas`.
- Eliminar una reserva no debe afectar otras reservas.

### Implementación evaluada

La API genera un token opaco e impredecible al crear la reserva y lo entrega únicamente en la respuesta de creación. El endpoint `GET /reservas` no lo incluye.

La supresión se solicita mediante:

```text
DELETE /reservas/{identificador}?token_gestion=...
```

### Pruebas realizadas

- `test_privacidad_token_de_gestion_no_se_expone_en_listado`.
- `test_privacidad_token_correcto_suprime_la_reserva`.
- `test_privacidad_token_incorrecto_no_suprime_la_reserva`.
- `test_privacidad_reserva_inexistente_devuelve_404`.
- `test_privacidad_suprimir_una_reserva_no_afecta_otras`.

### Ejecución

```powershell
uv run pytest tests/test_no_funcionales.py -k privacidad
```

### Limitaciones

No se implementan otros derechos, autenticación completa, base de datos, política de retención, consentimiento, anonimización ni certificación jurídica de cumplimiento de la Ley 21.719.
