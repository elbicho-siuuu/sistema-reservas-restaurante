"""Entidades del sistema de reservas de restaurante."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class UbicacionMesa(Enum):
    INTERIOR = "INTERIOR"
    SEMI_EXTERIOR = "SEMI_EXTERIOR"
    EXTERIOR = "EXTERIOR"


@dataclass
class Mesa:
    identificador: str
    capacidad: int
    ubicacion: UbicacionMesa


@dataclass
class Cliente:
    identificador: str
    nombre: str


@dataclass
class Piso:
    identificador: str
    mesas: list[Mesa] = field(default_factory=list)


@dataclass
class Restaurante:
    nombre: str
    pisos: list[Piso] = field(default_factory=list)


@dataclass
class Reserva:
    identificador: str
    cliente: Cliente
    mesas: list[Mesa]
    inicio: datetime
    termino: datetime
    cantidad_personas: int = 0
