from datetime import UTC, datetime, timedelta
from math import ceil
from time import perf_counter

from fastapi.testclient import TestClient

from trabajo_eval_1.api import (
    RESERVAS,
    TOKENS_GESTION,
    ReservaCreateRequest,
    app,
)


def setup_function() -> None:
    RESERVAS.clear()
    TOKENS_GESTION.clear()


def datos_reserva(
    identificador: str = "R1",
    mesa_ids: list[str] | None = None,
    cantidad_personas: int = 2,
    inicio: datetime | None = None,
) -> ReservaCreateRequest:
    inicio = inicio or datetime.now(UTC) + timedelta(hours=2)
    return ReservaCreateRequest(
        identificador=identificador,
        cliente_id="C1",
        cliente_nombre="Persona Prueba",
        mesa_ids=mesa_ids or ["M1"],
        cantidad_personas=cantidad_personas,
        inicio=inicio,
        termino=inicio + timedelta(hours=1),
    )


def payload_reserva(datos: ReservaCreateRequest) -> dict[str, object]:
    return datos.model_dump(mode="json")


def test_rendimiento_post_reservas_cumple_umbral() -> None:
    client = TestClient(app)
    duraciones: list[float] = []
    ahora = datetime.now(UTC) + timedelta(hours=2)

    for indice in range(100):
        datos = datos_reserva(
            identificador=f"PERF-{indice}",
            inicio=ahora + timedelta(hours=2 * indice),
        )
        inicio_medicion = perf_counter()
        respuesta = client.post("/reservas", json=payload_reserva(datos))
        duraciones.append(perf_counter() - inicio_medicion)
        assert respuesta.status_code == 201

    ordenadas = sorted(duraciones)
    p95 = ordenadas[ceil(len(ordenadas) * 0.95) - 1]
    minimo = min(duraciones)
    promedio = sum(duraciones) / len(duraciones)
    maximo = max(duraciones)
    print(
        "Rendimiento POST /reservas: "
        f"mínimo={minimo:.6f}s, promedio={promedio:.6f}s, "
        f"máximo={maximo:.6f}s, p95={p95:.6f}s"
    )

    assert len(RESERVAS) == 100
    assert p95 <= 0.5


def test_seguridad_mesa_inexistente_no_modifica_reservas() -> None:
    client = TestClient(app)
    reservas_antes = list(RESERVAS)

    respuesta = client.post(
        "/reservas",
        json=payload_reserva(datos_reserva(mesa_ids=["M99"])),
    )

    assert respuesta.status_code == 404
    assert RESERVAS == reservas_antes


def test_seguridad_dato_de_negocio_invalido_no_modifica_reservas() -> None:
    client = TestClient(app)
    reservas_antes = list(RESERVAS)

    respuesta = client.post(
        "/reservas",
        json=payload_reserva(datos_reserva(cantidad_personas=0)),
    )

    assert respuesta.status_code == 400
    assert RESERVAS == reservas_antes


def test_seguridad_error_no_expone_informacion_interna() -> None:
    client = TestClient(app)
    respuesta = client.post(
        "/reservas",
        json=payload_reserva(datos_reserva(mesa_ids=["M99"])),
    )

    detalle = respuesta.text.lower()
    assert "traceback" not in detalle
    assert "c:" not in detalle
    assert "src/" not in detalle
    assert "trabajo_eval_1" not in detalle


def test_seguridad_catalogo_no_expone_datos_de_clientes() -> None:
    client = TestClient(app)
    respuesta = client.get("/mesas")
    catalogo = respuesta.json()

    assert respuesta.status_code == 200
    assert all("cliente_id" not in mesa for mesa in catalogo)
    assert all("cliente_nombre" not in mesa for mesa in catalogo)


def test_privacidad_token_de_gestion_no_se_expone_en_listado() -> None:
    client = TestClient(app)
    respuesta_creacion = client.post(
        "/reservas",
        json=payload_reserva(datos_reserva(identificador="PRIV-1")),
    )
    respuesta = respuesta_creacion.json()
    listado = client.get("/reservas")

    assert respuesta_creacion.status_code == 201
    assert respuesta["token_gestion"] not in {"C1", "Persona Prueba"}
    assert len(respuesta["token_gestion"]) >= 32
    assert all("token_gestion" not in reserva for reserva in listado.json())


def test_privacidad_token_correcto_suprime_la_reserva() -> None:
    client = TestClient(app)
    creacion = client.post(
        "/reservas",
        json=payload_reserva(datos_reserva(identificador="PRIV-1")),
    )
    token = creacion.json()["token_gestion"]

    resultado = client.delete("/reservas/PRIV-1", params={"token_gestion": token})

    assert resultado.status_code == 204
    assert client.get("/reservas").json() == []


def test_privacidad_token_incorrecto_no_suprime_la_reserva() -> None:
    client = TestClient(app)
    creacion = client.post(
        "/reservas",
        json=payload_reserva(datos_reserva(identificador="PRIV-1")),
    )
    token = creacion.json()["token_gestion"]

    respuesta = client.delete(
        "/reservas/PRIV-1",
        params={"token_gestion": f"{token}-incorrecto"},
    )

    assert respuesta.status_code == 403
    assert len(RESERVAS) == 1


def test_privacidad_reserva_inexistente_devuelve_404() -> None:
    client = TestClient(app)
    respuesta = client.delete(
        "/reservas/NO-EXISTE",
        params={"token_gestion": "token-inexistente"},
    )

    assert respuesta.status_code == 404


def test_privacidad_suprimir_una_reserva_no_afecta_otras() -> None:
    client = TestClient(app)
    primera = client.post(
        "/reservas",
        json=payload_reserva(datos_reserva(identificador="PRIV-1")),
    )
    client.post(
        "/reservas",
        json=payload_reserva(
            datos_reserva(identificador="PRIV-2", mesa_ids=["M2"])
        ),
    )

    client.delete(
        "/reservas/PRIV-1",
        params={"token_gestion": primera.json()["token_gestion"]},
    )

    reservas = client.get("/reservas").json()
    assert [reserva["identificador"] for reserva in reservas] == ["PRIV-2"]
