from datetime import UTC, datetime, timedelta

import pytest

from trabajo_eval_1.modelos import (
    Cliente,
    Mesa,
    Reserva,
    UbicacionMesa,
)
from trabajo_eval_1.reservas import crear_reserva

AHORA = datetime(2026, 9, 17, 18, 0, tzinfo=UTC)


def cliente() -> Cliente:
    return Cliente("C1", "Ana Pérez")


def mesa(identificador: str, capacidad: int = 4) -> Mesa:
    return Mesa(identificador, capacidad, UbicacionMesa.INTERIOR)


def crear_reserva_base(
    mesas: list[Mesa] | None = None,
    inicio: datetime | None = None,
    termino: datetime | None = None,
    cantidad_personas: int = 2,
    reservas_existentes: list[Reserva] | None = None,
) -> Reserva:
    inicio = inicio or AHORA + timedelta(hours=2)
    termino = termino or inicio + timedelta(hours=2)
    return crear_reserva(
        "R1",
        cliente(),
        mesas or [mesa("M1")],
        cantidad_personas,
        inicio,
        termino,
        reservas_existentes or [],
        AHORA,
    )


def test_rechaza_una_reserva_con_mas_de_tres_mesas() -> None:
    with pytest.raises(ValueError, match="más de 3 mesas"):
        crear_reserva_base([mesa("M1"), mesa("M2"), mesa("M3"), mesa("M4")])


def test_acepta_una_reserva_con_hasta_tres_mesas() -> None:
    reserva = crear_reserva_base(
        [mesa("M1"), mesa("M2"), mesa("M3")], cantidad_personas=12
    )

    assert len(reserva.mesas) == 3


def test_acepta_una_reserva_con_mesas_diferentes() -> None:
    reserva = crear_reserva_base(
        [mesa("M1", 4), mesa("M2", 4)], cantidad_personas=8
    )

    assert [mesa.identificador for mesa in reserva.mesas] == ["M1", "M2"]


def test_rechaza_la_misma_mesa_repetida_en_una_reserva() -> None:
    m1 = mesa("M1", 4)

    with pytest.raises(ValueError, match="misma mesa"):
        crear_reserva_base([m1, m1], cantidad_personas=8)


def test_rechaza_cantidad_de_personas_superior_a_capacidad_total() -> None:
    with pytest.raises(ValueError, match="capacidad total"):
        crear_reserva_base([mesa("M1", 4), mesa("M2", 2)], cantidad_personas=7)


def test_rechaza_cantidad_de_personas_cero() -> None:
    with pytest.raises(ValueError):
        crear_reserva_base(cantidad_personas=0)


def test_rechaza_cantidad_de_personas_negativa() -> None:
    with pytest.raises(ValueError):
        crear_reserva_base(cantidad_personas=-1)


def test_rechaza_termino_igual_al_inicio() -> None:
    inicio = AHORA + timedelta(hours=2)

    with pytest.raises(ValueError):
        crear_reserva_base(inicio=inicio, termino=inicio)


def test_rechaza_termino_anterior_al_inicio() -> None:
    inicio = AHORA + timedelta(hours=2)
    termino = inicio - timedelta(minutes=1)

    with pytest.raises(ValueError):
        crear_reserva_base(inicio=inicio, termino=termino)


def test_acepta_cantidad_de_personas_igual_a_capacidad_total() -> None:
    reserva = crear_reserva_base(
        [mesa("M1", 4), mesa("M2", 2)], cantidad_personas=6
    )

    assert reserva.cantidad_personas == 6


def test_rechaza_solapamiento_en_la_misma_mesa() -> None:
    existente = crear_reserva_base(
        inicio=AHORA + timedelta(hours=2),
        termino=AHORA + timedelta(hours=4),
    )

    with pytest.raises(ValueError, match="ya está reservada"):
        crear_reserva_base(
            inicio=AHORA + timedelta(hours=3),
            termino=AHORA + timedelta(hours=5),
            reservas_existentes=[existente],
        )


def test_acepta_reserva_que_comienza_al_terminar_la_anterior() -> None:
    existente = crear_reserva_base(
        inicio=AHORA + timedelta(hours=2),
        termino=AHORA + timedelta(hours=4),
    )

    reserva = crear_reserva_base(
        inicio=AHORA + timedelta(hours=4),
        termino=AHORA + timedelta(hours=5),
        reservas_existentes=[existente],
    )

    assert reserva.inicio == existente.termino


def test_rechaza_reserva_con_menos_de_60_minutos_de_anticipacion() -> None:
    with pytest.raises(ValueError, match="60 minutos"):
        crear_reserva_base(inicio=AHORA + timedelta(minutes=59))


def test_acepta_reserva_con_exactamente_60_minutos_de_anticipacion() -> None:
    reserva = crear_reserva_base(inicio=AHORA + timedelta(minutes=60))

    assert reserva.inicio == AHORA + timedelta(minutes=60)


def test_acepta_reserva_con_mas_de_60_minutos_de_anticipacion() -> None:
    reserva = crear_reserva_base(inicio=AHORA + timedelta(minutes=61))

    assert reserva.inicio == AHORA + timedelta(minutes=61)


def test_acepta_reserva_con_menos_de_30_dias_de_anticipacion() -> None:
    reserva = crear_reserva_base(inicio=AHORA + timedelta(days=29))

    assert reserva.inicio == AHORA + timedelta(days=29)


def test_acepta_reserva_con_exactamente_30_dias_de_anticipacion() -> None:
    reserva = crear_reserva_base(inicio=AHORA + timedelta(days=30))

    assert reserva.inicio == AHORA + timedelta(days=30)


def test_rechaza_reserva_con_mas_de_30_dias_de_anticipacion() -> None:
    with pytest.raises(ValueError, match="30 dias"):
        crear_reserva_base(
            inicio=AHORA + timedelta(days=30, microseconds=1),
        )
