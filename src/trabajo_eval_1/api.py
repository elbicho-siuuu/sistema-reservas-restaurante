"""API HTTP para el sistema de reservas de restaurante."""

import secrets
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .modelos import Cliente, Mesa, Reserva, UbicacionMesa
from .reservas import crear_reserva

app = FastAPI(title="Sistema de Reservas de Restaurante")

CATALOGO_MESAS: list[Mesa] = [
    Mesa("M1", 4, UbicacionMesa.INTERIOR),
    Mesa("M2", 4, UbicacionMesa.INTERIOR),
    Mesa("M3", 2, UbicacionMesa.SEMI_EXTERIOR),
]
RESERVAS: list[Reserva] = []
TOKENS_GESTION: dict[str, str] = {}


class MesaResponse(BaseModel):
    identificador: str
    capacidad: int
    ubicacion: UbicacionMesa


class ReservaCreateRequest(BaseModel):
    identificador: str
    cliente_id: str
    cliente_nombre: str
    mesa_ids: list[str]
    cantidad_personas: int
    inicio: datetime
    termino: datetime


class ReservaResponse(BaseModel):
    identificador: str
    cliente_id: str
    cliente_nombre: str
    mesas: list[MesaResponse]
    cantidad_personas: int
    inicio: datetime
    termino: datetime


class ReservaCreadaResponse(ReservaResponse):
    token_gestion: str


def _mesa_response(mesa: Mesa) -> MesaResponse:
    return MesaResponse(
        identificador=mesa.identificador,
        capacidad=mesa.capacidad,
        ubicacion=mesa.ubicacion,
    )


def _reserva_response(reserva: Reserva) -> ReservaResponse:
    return ReservaResponse(
        identificador=reserva.identificador,
        cliente_id=reserva.cliente.identificador,
        cliente_nombre=reserva.cliente.nombre,
        mesas=[_mesa_response(mesa) for mesa in reserva.mesas],
        cantidad_personas=reserva.cantidad_personas,
        inicio=reserva.inicio,
        termino=reserva.termino,
    )


@app.get("/mesas", response_model=list[MesaResponse])
def listar_mesas() -> list[MesaResponse]:
    """Devuelve el catálogo de mesas del restaurante."""
    return [_mesa_response(mesa) for mesa in CATALOGO_MESAS]


@app.post("/reservas", response_model=ReservaCreadaResponse, status_code=201)
def crear_reserva_api(datos: ReservaCreateRequest) -> ReservaCreadaResponse:
    """Crea una reserva utilizando las reglas del dominio."""
    mesas_por_id = {mesa.identificador: mesa for mesa in CATALOGO_MESAS}
    mesas: list[Mesa] = []

    for mesa_id in datos.mesa_ids:
        mesa = mesas_por_id.get(mesa_id)
        if mesa is None:
            raise HTTPException(
                status_code=404,
                detail=f"No existe la mesa '{mesa_id}'.",
            )
        mesas.append(mesa)

    cliente = Cliente(datos.cliente_id, datos.cliente_nombre)

    try:
        reserva = crear_reserva(
            datos.identificador,
            cliente,
            mesas,
            datos.cantidad_personas,
            datos.inicio,
            datos.termino,
            RESERVAS,
            datetime.now(UTC),
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    RESERVAS.append(reserva)
    token_gestion = secrets.token_urlsafe(32)
    TOKENS_GESTION[reserva.identificador] = token_gestion
    return ReservaCreadaResponse(
        **_reserva_response(reserva).model_dump(),
        token_gestion=token_gestion,
    )


@app.get("/reservas", response_model=list[ReservaResponse])
def listar_reservas() -> list[ReservaResponse]:
    """Devuelve las reservas creadas durante la ejecución de la aplicación."""
    return [_reserva_response(reserva) for reserva in RESERVAS]


@app.delete("/reservas/{identificador}", status_code=204)
def eliminar_reserva(identificador: str, token_gestion: str) -> None:
    """Elimina una reserva cuando se presenta su token de gestión."""
    reserva = next(
        (reserva for reserva in RESERVAS if reserva.identificador == identificador),
        None,
    )
    if reserva is None:
        raise HTTPException(status_code=404, detail="La reserva no existe.")

    token_esperado = TOKENS_GESTION.get(identificador, "")
    if not secrets.compare_digest(token_esperado, token_gestion):
        raise HTTPException(status_code=403, detail="Token de gestión inválido.")

    RESERVAS.remove(reserva)
    TOKENS_GESTION.pop(identificador, None)

