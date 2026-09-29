from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException

from trabajo_eval_1.api import (
    RESERVAS,
    ReservaCreateRequest,
    crear_reserva_api,
    listar_mesas,
    listar_reservas,
)


def setup_function() -> None:
    RESERVAS.clear()


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


def test_get_mesas_devuelve_el_catalogo() -> None:
    mesas = listar_mesas()

    assert {mesa.identificador for mesa in mesas} == {"M1", "M2", "M3"}


def test_post_reservas_crea_una_reserva_valida() -> None:
    reserva = crear_reserva_api(datos_reserva(["M1", "M2"]))

    assert reserva.identificador == "R1"
    assert reserva.cantidad_personas == 2


def test_post_reservas_rechaza_mesa_inexistente_sin_modificar_reservas() -> None:
    crear_reserva_api(datos_reserva())
    reservas_antes = list(RESERVAS)

    with pytest.raises(HTTPException) as error:
        crear_reserva_api(datos_reserva(["M99"]))

    assert error.value.status_code == 404
    assert RESERVAS == reservas_antes


def test_get_reservas_devuelve_las_reservas_creadas() -> None:
    crear_reserva_api(datos_reserva())

    reservas = listar_reservas()

    assert len(reservas) == 1
    assert reservas[0].identificador == "R1"
