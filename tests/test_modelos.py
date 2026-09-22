from datetime import UTC, datetime

from trabajo_eval_1.modelos import (
    Cliente,
    Mesa,
    Piso,
    Reserva,
    Restaurante,
    UbicacionMesa,
)


def test_mesa_contiene_sus_datos_basicos() -> None:
    mesa = Mesa("M1", 4, UbicacionMesa.INTERIOR)

    assert mesa.identificador == "M1"
    assert mesa.capacidad == 4
    assert mesa.ubicacion is UbicacionMesa.INTERIOR


def test_cliente_contiene_sus_datos_basicos() -> None:
    cliente = Cliente("C1", "Ana Pérez")

    assert cliente.identificador == "C1"
    assert cliente.nombre == "Ana Pérez"


def test_restaurante_contiene_pisos_y_el_piso_contiene_mesas() -> None:
    mesa = Mesa("M1", 4, UbicacionMesa.SEMI_EXTERIOR)
    piso = Piso("P1", [mesa])
    restaurante = Restaurante("Mi Restaurante", [piso])

    assert restaurante.pisos == [piso]
    assert piso.mesas == [mesa]


def test_reserva_contiene_cliente_mesas_y_horario() -> None:
    cliente = Cliente("C1", "Ana Pérez")
    mesa = Mesa("M1", 4, UbicacionMesa.EXTERIOR)
    inicio = datetime(2026, 10, 1, 20, 0, tzinfo=UTC)
    termino = datetime(2026, 10, 1, 22, 0, tzinfo=UTC)

    reserva = Reserva("R1", cliente, [mesa], inicio, termino)

    assert reserva.cliente is cliente
    assert reserva.mesas == [mesa]
    assert reserva.inicio == inicio
    assert reserva.termino == termino
