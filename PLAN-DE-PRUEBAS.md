# Plan de Pruebas - Evaluación 2

## 1. Objetivo
El objetivo de este plan de pruebas es verificar que el Sistema de Reservas de Restaurante funciona correctamente y cumple las reglas de negocio definidas para la creación de reservas.

Las pruebas buscan detectar errores tanto en la lógica de las reservas como en la API FastAPI que permite utilizar el sistema. Para esto, se aplican pruebas unitarias, de integración y E2E, con el fin de comprobar el sistema desde sus componentes individuales hasta un flujo completo de uso.


## 2. Alcance

El alcance de este plan de pruebas comprende las funcionalidades implementadas en la Evaluación 2 del Sistema de Reservas de Restaurante.

Se incluye:

La lógica de negocio relacionada con la creación de reservas y sus reglas de validación.
La API FastAPI, incluyendo las operaciones para consultar mesas, crear reservas y consultar las reservas existentes.
Las pruebas unitarias de las reglas de negocio mediante pytest.
Las pruebas de integración de los endpoints de la API mediante TestClient.
Las pruebas E2E mediante Playwright, verificando un flujo completo de uso de la API.

Quedan fuera del alcance las funcionalidades que no forman parte de la implementación actual, como base de datos, autenticación, cancelación de reservas y una interfaz gráfica.


## 3. Estrategia de pruebas

Como referencia para organizar el proceso de pruebas se utiliza ISO/IEC/IEEE 29119, especialmente para ordenar el alcance, los niveles de prueba, los criterios y la trazabilidad. Esto no implica una certificación formal del proyecto.

Se utilizarán tres niveles de pruebas para verificar el funcionamiento del sistema desde distintos puntos de vista: pruebas unitarias, pruebas de integración y pruebas E2E.

### 3.1 Pruebas unitarias

Las pruebas unitarias verifican de forma aislada la lógica de negocio relacionada con la creación de reservas. Se utiliza pytest para comprobar las reglas de validación definidas en `crear_reserva()`, incluyendo cantidad de mesas, capacidad, horarios, anticipación y disponibilidad.

### 3.2 Pruebas de integración

Las pruebas de integración verifican que los componentes de la API FastAPI funcionan correctamente en conjunto. Se utiliza `TestClient` para realizar solicitudes a los endpoints de FastAPI y comprobar sus respuestas.

### 3.3 Pruebas E2E

Las pruebas E2E verifican un flujo completo de uso de la API mediante Playwright. El flujo consulta las mesas disponibles, crea una reserva y posteriormente consulta las reservas para comprobar que la reserva creada está disponible.


## 4. Riesgos de prueba

Durante la ejecución de las pruebas se consideran los siguientes riesgos que podrían afectar la confiabilidad de los resultados:

| Riesgo                             | Posible efecto                                                                                                     | Medida de control                                                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Dependencia de fecha y hora actual | Una pequeña diferencia de tiempo puede afectar las pruebas de los límites de anticipación de 60 minutos y 30 días. | Las pruebas utilizan fechas calculadas explícitamente para comprobar los valores límite.                                   |
| Estado compartido entre pruebas    | Una reserva creada por una prueba podría afectar el resultado de otra.                                             | Se limpia la lista `RESERVAS` antes de cada prueba de integración.                                                         |
| Fallo al iniciar Uvicorn           | Las pruebas E2E podrían fallar sin que exista un error en la lógica de la aplicación.                              | El fixture de Playwright inicia Uvicorn automáticamente y verifica que la API esté disponible antes de ejecutar la prueba. |
| Puerto ocupado                     | Otro proceso podría impedir que Uvicorn utilice un puerto determinado.                                             | La prueba E2E obtiene automáticamente un puerto disponible antes de iniciar el servidor.                                   |

Estos controles buscan reducir la posibilidad de falsos resultados y hacer que las pruebas sean reproducibles y estables.



## 5. Criterios de entrada y salida

### 5.1 Criterios de entrada

Antes de ejecutar las pruebas se debe contar con:

* El código fuente de la aplicación disponible.
* Las dependencias necesarias para ejecutar pytest, FastAPI, TestClient y Playwright.
* Las pruebas unitarias, de integración y E2E implementadas.
* La API FastAPI configurada para poder ser ejecutada durante las pruebas.

### 5.2 Criterios de salida

La etapa de pruebas se considerará completada cuando:

* Las pruebas unitarias se ejecuten correctamente.
* Las pruebas de integración de la API se ejecuten correctamente.
* La prueba E2E se ejecute correctamente mediante Playwright.
* Los errores encontrados durante las pruebas hayan sido corregidos o queden documentados.
* Los resultados obtenidos sean coherentes con los casos de prueba diseñados.


## 6. Entorno y herramientas

Las pruebas se ejecutan en un entorno de desarrollo con Windows y Python 3.14.

Para la ejecución y gestión del proyecto se utilizan las siguientes herramientas:

* **uv:** gestión del entorno y las dependencias del proyecto.
* **pytest:** ejecución de las pruebas automatizadas.
* **FastAPI:** framework utilizado para la API que será sometida a las pruebas de integración y E2E.
* **TestClient:** realización de solicitudes a los endpoints de FastAPI y comprobación de sus respuestas durante las pruebas de integración.
* **Playwright:** ejecución de las pruebas E2E mediante solicitudes HTTP reales a la API.
* **Uvicorn:** servidor utilizado para ejecutar la aplicación FastAPI durante las pruebas E2E.

Las pruebas se ejecutan sobre el código del proyecto y utilizan los mismos componentes implementados para la aplicación, evitando reemplazar la API por simulaciones durante las pruebas de integración y E2E.


## 7. Trazabilidad

La trazabilidad permite relacionar los requisitos y reglas de negocio con los casos de prueba diseñados y las pruebas automatizadas implementadas.

En este proyecto se establece la siguiente relación:

### 7.1 Reglas de negocio y pruebas unitarias

Las reglas de negocio definidas para la creación de reservas se relacionan con los casos de prueba identificados en `DISENO-DE-CASOS.md`.

Cada caso diseñado indica la prueba automatizada que permite verificar su comportamiento. De esta forma, las pruebas unitarias de `test_reservas.py` permiten comprobar las reglas de creación de reservas de forma individual.

### 7.2 API y pruebas de integración

Los casos definidos para la API se relacionan con las pruebas de `test_api.py`.

Estas pruebas verifican que los endpoints de FastAPI respondan correctamente y que sus resultados sean coherentes con el comportamiento esperado.

### 7.3 Flujo completo y prueba E2E

El caso `E2E-C01` se relaciona con la prueba `test_flujo_completo_reserva` ubicada en `tests/e2e/test_reservas_e2e.py`.

Esta prueba verifica un flujo completo mediante Playwright: consultar las mesas, crear una reserva y consultar posteriormente las reservas para comprobar que la reserva creada está disponible.

De esta manera, cada nivel de prueba mantiene una relación con los casos diseñados y permite verificar el sistema desde la lógica de negocio hasta el flujo completo de uso.


## 8. Resultados esperados

Se espera que las pruebas automatizadas permitan verificar que el Sistema de Reservas de Restaurante cumple las reglas de negocio definidas y que la API FastAPI funciona correctamente.

Se espera obtener los siguientes resultados:

* Las pruebas unitarias deben validar correctamente las reglas de creación de reservas y rechazar los datos que no cumplan las condiciones establecidas.
* Las pruebas de integración deben comprobar que los endpoints de la API responden correctamente ante solicitudes válidas y que entregan errores adecuados ante solicitudes inválidas. En particular, una solicitud con la mesa inexistente `M99` debe responder con HTTP 404 y no modificar `RESERVAS`.
* La prueba E2E debe completar correctamente el flujo de consultar mesas, crear una reserva y consultar las reservas existentes.
* Las pruebas deben ejecutarse de forma estable y entregar resultados reproducibles.
* No deben existir fallos sin resolver que impidan considerar funcionales las características incluidas en el alcance de este plan.

Los resultados obtenidos durante la ejecución final de las pruebas serán utilizados para verificar el cumplimiento de estos criterios.
