from datetime import UTC, datetime, timedelta

import pytest

from app.services.jwt_service import InvalidTokenError, create_jwt_token, verify_jwt_token


def test_verify_jwt_token_returns_payload() -> None:
    payload = {"sub": "user-1"}
    token = create_jwt_token(payload)

    assert verify_jwt_token(token) == payload


def test_verify_jwt_token_rejects_invalid_signature() -> None:
    token = create_jwt_token({"sub": "user-1"})
    invalid_token = f"{token[:-1]}x"

    with pytest.raises(InvalidTokenError, match="Invalid token signature"):
        verify_jwt_token(invalid_token)


def test_verify_jwt_token_rejects_expired_token() -> None:
    payload = {"sub": "user-1", "exp": (datetime.now(UTC) - timedelta(minutes=1)).timestamp()}
    token = create_jwt_token(payload)

    with pytest.raises(InvalidTokenError, match="Token has expired"):
        verify_jwt_token(token)
