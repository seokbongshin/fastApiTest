import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.calculator_service import add, divide, multiply, subtract
from app.services.jwt_service import create_jwt_token


client = TestClient(app)


def auth_headers() -> dict[str, str]:
    token = create_jwt_token({"sub": "test-user"})
    return {"Authorization": f"Bearer {token}"}


def test_calculator_service() -> None:
    assert add(10, 2) == 12
    assert subtract(10, 2) == 8
    assert multiply(10, 2) == 20
    assert divide(10, 2) == 5


def test_divide_by_zero_raises_error() -> None:
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_calculate_api() -> None:
    response = client.get(
        "/api/v1/calculate",
        params={"left": 10, "right": 2},
        headers=auth_headers(),
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "data": {
            "left": 10.0,
            "right": 2.0,
            "add": 12.0,
            "subtract": 8.0,
            "multiply": 20.0,
            "divide": 5.0,
        },
        "message": None,
    }


def test_calculate_api_rejects_divide_by_zero() -> None:
    response = client.get(
        "/api/v1/calculate",
        params={"left": 10, "right": 0},
        headers=auth_headers(),
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot divide by zero"}


def test_calculate_api_requires_token() -> None:
    response = client.get("/api/v1/calculate", params={"left": 10, "right": 2})

    assert response.status_code == 401
    assert response.json() == {"detail": "Authorization token is required"}


def test_calculate_api_rejects_invalid_token() -> None:
    response = client.get(
        "/api/v1/calculate",
        params={"left": 10, "right": 2},
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token format"}
