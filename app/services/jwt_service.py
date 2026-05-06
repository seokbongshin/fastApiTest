import base64
import binascii
import hashlib
import hmac
import json
from datetime import UTC, datetime
from typing import Any

from app.core.config import JWT_ALGORITHM, JWT_SECRET_KEY


class InvalidTokenError(ValueError):
    pass


def create_jwt_token(payload: dict[str, Any]) -> str:
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    encoded_header = _base64url_encode_json(header)
    encoded_payload = _base64url_encode_json(payload)
    signature = _sign(f"{encoded_header}.{encoded_payload}")

    return f"{encoded_header}.{encoded_payload}.{signature}"


def verify_jwt_token(token: str) -> dict[str, Any]:
    encoded_header, encoded_payload, signature = _split_token(token)
    header = _base64url_decode_json(encoded_header)

    if header.get("alg") != JWT_ALGORITHM:
        raise InvalidTokenError("Invalid token algorithm")

    expected_signature = _sign(f"{encoded_header}.{encoded_payload}")
    if not hmac.compare_digest(signature, expected_signature):
        raise InvalidTokenError("Invalid token signature")

    payload = _base64url_decode_json(encoded_payload)
    _validate_expiration(payload)

    return payload


def _split_token(token: str) -> tuple[str, str, str]:
    parts = token.split(".")
    if len(parts) != 3:
        raise InvalidTokenError("Invalid token format")

    return parts[0], parts[1], parts[2]


def _sign(message: str) -> str:
    digest = hmac.new(
        _get_signing_key(),
        message.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return _base64url_encode_bytes(digest)


def _get_signing_key() -> bytes:
    try:
        return base64.b64decode(JWT_SECRET_KEY)
    except binascii.Error:
        return JWT_SECRET_KEY.encode("utf-8")


def _validate_expiration(payload: dict[str, Any]) -> None:
    expires_at = payload.get("exp")
    if expires_at is None:
        return

    if not isinstance(expires_at, int | float):
        raise InvalidTokenError("Invalid token expiration")

    now = datetime.now(UTC).timestamp()
    if expires_at < now:
        raise InvalidTokenError("Token has expired")


def _base64url_encode_json(value: dict[str, Any]) -> str:
    json_value = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return _base64url_encode_bytes(json_value.encode("utf-8"))


def _base64url_encode_bytes(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _base64url_decode_json(value: str) -> dict[str, Any]:
    try:
        decoded = base64.urlsafe_b64decode(_add_base64_padding(value)).decode("utf-8")
        data = json.loads(decoded)
    except (ValueError, json.JSONDecodeError) as exc:
        raise InvalidTokenError("Invalid token content") from exc

    if not isinstance(data, dict):
        raise InvalidTokenError("Invalid token content")

    return data


def _add_base64_padding(value: str) -> str:
    return value + "=" * (-len(value) % 4)
