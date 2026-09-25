"""Reglas de negocio para la creacion de reservas."""

from collections.abc import Sequence
from datetime import datetime, timedelta

from .modelos import Cliente, Mesa, Reserva

MAXIMO_MESAS = 3
ANTICIPACION_MINIMA = timedelta(minutes=60)
ANTICIPACION_MAXIMA = timedelta(days=30)


def validar_anticipacion(inicio: datetime, ahora: datetime) -> None:
    """Valida los limites minimo y maximo de anticipacion."""
    anticipacion = inicio - ahora

    if anticipacion < ANTICIPACION_MINIMA:
        raise ValueError(
            "La reserva debe realizarse con al menos 60 minutos de anticipacion."
        )

    if anticipacion > ANTICIPACION_MAXIMA:
        raise ValueError(
            "La reserva no puede realizarse con mas de 30 dias de anticipacion."
        )


def _hay_solapamiento(reserva_nueva: Reserva, reserva_existente: Reserva) -> bool:
    """Indica si dos reservas comparten mesa y sus horarios se solapan."""
    comparten_mesa = any(
        mesa_nueva.identificador == mesa_existente.identificador
        for mesa_nueva in reserva_nueva.mesas
        for mesa_existente in reserva_existente.mesas
    )
    horarios_se_solapan = (
        reserva_nueva.inicio < reserva_existente.termino
        and reserva_nueva.termino > reserva_existente.inicio
    )
    return comparten_mesa and horarios_se_solapan


def crear_reserva(
    identificador: str,
    cliente: Cliente,
    mesas: list[Mesa],
    cantidad_personas: int,
    inicio: datetime,
    termino: datetime,
    reservas_existentes: Sequence[Reserva],
    ahora: datetime,
) -> Reserva:
    """Valida las reglas de negocio y crea una reserva valida."""
    if not mesas:
        raise ValueError("La reserva debe incluir al menos una mesa.")

    identificadores_mesas = [mesa.identificador for mesa in mesas]
    if len(identificadores_mesas) != len(set(identificadores_mesas)):
        raise ValueError(
            "La reserva no puede incluir la misma mesa m\u00E1s de una vez."
        )

    if cantidad_personas <= 0:
        raise ValueError("La cantidad de personas debe ser mayor que cero.")

    if termino <= inicio:
        raise ValueError("La hora de termino debe ser posterior a la hora de inicio.")

    if len(mesas) > MAXIMO_MESAS:
        raise ValueError(
            "Una reserva no puede incluir mas de 3 mesas (m\u00E1s de 3 mesas no permitido)."
        )

    capacidad_total = sum(mesa.capacidad for mesa in mesas)
    if cantidad_personas > capacidad_total:
        raise ValueError(
            "La cantidad de personas no puede superar la capacidad total de las mesas."
        )

    reserva = Reserva(
        identificador,
        cliente,
        mesas,
        inicio,
        termino,
        cantidad_personas,
    )

    if any(_hay_solapamiento(reserva, existente) for existente in reservas_existentes):
        raise ValueError(
            "Una de las mesas ya esta reservada en ese horario (ya est\u00E1 reservada)."
        )

    validar_anticipacion(inicio, ahora)
    return reserva
