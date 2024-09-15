"""Security."""

from datetime import datetime, timedelta, timezone
from typing import Any

from jwt import decode as jwt_decode, encode as jwt_encode


class JWT:
    """JWT utility class for encoding and decoding JSON Web Tokens."""

    def __init__(self, secret_key: str, jwt_algorithm: str):
        """Initialize the JWT class with a secret key, algorithm, and expiration time.

        Args:
            secret_key (str): The secret key to sign the JWT.
            jwt_algorithm (str): The algorithm to use for signing the JWT.
        """
        self._secret_key = secret_key
        self._jwt_algorithm = jwt_algorithm

    def encode(self, data: Any, expires_in: int | None = None, kwargs: dict[str, Any] | None = None) -> str:
        """Encode data into a JWT.

        Args:
            data (Any): The data to encode into the JWT.
            expires_in (int | None, optional): The expiration time in minutes. Defaults to None.

        Returns:
            str: The encoded JWT.
        """
        payload: dict[str, Any] = {"sub": str(data)} | (kwargs or {})
        if expires_in is not None:
            payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        return jwt_encode(payload, self._secret_key, algorithm=self._jwt_algorithm)

    def decode(self, token: str) -> dict[str, Any]:
        """Decode a JWT.

        Args:
            token (str): The JWT to decode.

        Returns:
            dict[str, Any]: The decoded data.
        """
        return jwt_decode(token, key=self._secret_key, algorithms=[self._jwt_algorithm])
