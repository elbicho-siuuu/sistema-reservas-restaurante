"""Prueba E2E del flujo principal de reservas usando Playwright."""

from datetime import UTC, datetime, timedelta
import os
from pathlib import Path
import subprocess
import sys
import time

import pytest
from playwright.sync_api import APIRequestContext, Playwright


BASE_URL = "http://127.0.0.1:8765"


@pytest.fixture
def api(playwright: Playwright):
    """Levanta FastAPI y devuelve un cliente HTTP externo de Playwright."""
    root = Path(__file__).parents[2]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root / "src")

    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "trabajo_eval_1.api:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8765",
        ],
        cwd=root,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    client = playwright.request.new_context(base_url=BASE_URL)
    try:
        for _ in range(50):
            if server.poll() is not None:
                pytest.fail("FastAPI no pudo iniciar.")
            response = client.get("/mesas")
            if response.ok:
                break
            time.sleep(0.1)
        else:
            pytest.fail("FastAPI no respondió a tiempo.")

        yield client
    finally:
        client.dispose()
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()


def test_flujo_completo_de_reserva(api: APIRequestContext) -> None:
    """Consulta mesas, crea una reserva y la encuentra en el listado."""
    mesas_response = api.get("/mesas")

    assert mesas_response.ok
    mesas = mesas_response.json()
    assert mesas
    mesa_id = mesas[0]["identificador"]

    inicio = datetime.now(UTC) + timedelta(hours=2)
    termino = inicio + timedelta(hours=2)
    reserva_id = "E2E-R1"
    datos_reserva = {
        "identificador": reserva_id,
        "cliente_id": "E2E-C1",
        "cliente_nombre": "Cliente E2E",
        "mesa_ids": [mesa_id],
        "cantidad_personas": 2,
        "inicio": inicio.isoformat(),
        "termino": termino.isoformat(),
    }

    crear_response = api.post("/reservas", data=datos_reserva)

    assert crear_response.status == 201
    assert crear_response.json()["identificador"] == reserva_id

    reservas_response = api.get("/reservas")

    assert reservas_response.ok
    reservas = reservas_response.json()
    assert any(reserva["identificador"] == reserva_id for reserva in reservas)
