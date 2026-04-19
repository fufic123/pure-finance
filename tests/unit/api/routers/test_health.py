from fastapi.testclient import TestClient

from src.api.main import create_app


class TestHealthz:
    def test_returns_ok_status(self) -> None:
        client = TestClient(create_app())

        response = client.get("/healthz")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
