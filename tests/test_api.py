from datetime import UTC, datetime, timedelta

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


def datos_reserva(mesa_ids: list[str] | None = None) -> ReservaCreateRequest:
    inicio = datetime.now(UTC) + timedelta(hours=2)
    termino = inicio + timedelta(hours=2)
    return ReservaCreateRequest(
        identificador="R1",
        cliente_id="C1",
        cliente_nombre="Ana Pérez",
        mesa_ids=mesa_ids or ["M1"],
        cantidad_personas=2,
        inicio=inicio,
        termino=termino,
    )


def payload_reserva(datos: ReservaCreateRequest) -> dict[str, object]:
    return datos.model_dump(mode="json")


def test_get_mesas_devuelve_el_catalogo() -> None:
    client = TestClient(app)
    respuesta = client.get("/mesas")

    assert respuesta.status_code == 200
    assert {mesa["identificador"] for mesa in respuesta.json()} == {
        "M1",
        "M2",
        "M3",
    }


def test_post_reservas_crea_una_reserva_valida() -> None:
    client = TestClient(app)
    respuesta = client.post(
        "/reservas",
        json=payload_reserva(datos_reserva(["M1", "M2"])),
    )
    reserva = respuesta.json()

    assert respuesta.status_code == 201
    assert reserva["identificador"] == "R1"
    assert reserva["cantidad_personas"] == 2


def test_post_reservas_rechaza_mesa_inexistente_sin_modificar_reservas() -> None:
    client = TestClient(app)
    client.post("/reservas", json=payload_reserva(datos_reserva()))
    reservas_antes = list(RESERVAS)

    respuesta = client.post(
        "/reservas",
        json=payload_reserva(datos_reserva(["M99"])),
    )

    assert respuesta.status_code == 404
    assert RESERVAS == reservas_antes


def test_get_reservas_devuelve_las_reservas_creadas() -> None:
    client = TestClient(app)
    client.post("/reservas", json=payload_reserva(datos_reserva()))

    respuesta = client.get("/reservas")
    reservas = respuesta.json()

    assert respuesta.status_code == 200
    assert len(reservas) == 1
    assert reservas[0]["identificador"] == "R1"
