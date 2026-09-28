import os
import socket
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from playwright.sync_api import APIRequestContext, Error, Playwright


@pytest.fixture
def api(playwright: Playwright):
    root = Path(__file__).parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src")

    with socket.socket() as port_socket:
        port_socket.bind(("127.0.0.1", 0))
        port = port_socket.getsockname()[1]

    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "trabajo_eval_1.api:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    client = None
    try:
        client = playwright.request.new_context(
            base_url=f"http://127.0.0.1:{port}"
        )
        last_connection_error = None

        for _ in range(100):
            if server.poll() is not None:
                output = server.communicate(timeout=1)[0]
                pytest.fail(
                    "Uvicorn termino antes de estar disponible "
                    f"(codigo {server.returncode}).\nSalida:\n{output}"
                )

            try:
                response = client.get("/mesas", timeout=1000)
                if response.ok:
                    break
            except Error as error:
                last_connection_error = str(error)
            time.sleep(0.1)
        else:
            if server.poll() is not None:
                output = server.communicate(timeout=1)[0]
                pytest.fail(
                    "Uvicorn termino antes de estar disponible "
                    f"(codigo {server.returncode}).\nSalida:\n{output}"
                )

            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()
            output = server.communicate(timeout=1)[0]
            pytest.fail(
                "La API no respondio a tiempo.\n"
                f"Ultimo error de conexion: {last_connection_error}\n"
                f"Salida de Uvicorn:\n{output}"
            )

        yield client
    finally:
        if client is not None:
            client.dispose()
        if server.poll() is None:
            server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()


def test_flujo_completo_reserva(api: APIRequestContext) -> None:
    mesas_response = api.get("/mesas")
    assert mesas_response.ok

    mesas = mesas_response.json()
    assert len(mesas) > 0

    mesa_id = mesas[0]["identificador"]

    inicio = datetime.now(UTC) + timedelta(hours=2)
    termino = inicio + timedelta(hours=2)

    reserva_payload = {
        "identificador": "E2E-R1",
        "cliente_id": "E2E-C1",
        "cliente_nombre": "Cliente E2E",
        "mesa_ids": [mesa_id],
        "cantidad_personas": 2,
        "inicio": inicio.isoformat(),
        "termino": termino.isoformat(),
    }

    response = api.post("/reservas", data=reserva_payload)
    assert response.status == 201
    reserva = response.json()
    assert reserva["identificador"] == "E2E-R1"

    reservas_response = api.get("/reservas")
    assert reservas_response.ok

    reservas = reservas_response.json()
    assert any(r["identificador"] == "E2E-R1" for r in reservas)

