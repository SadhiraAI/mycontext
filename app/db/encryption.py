"""Encryption/decryption for user API keys using Fernet."""

import base64

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.config import get_settings


def _get_fernet() -> Fernet:
    """Get Fernet instance from app secret."""
    settings = get_settings()
    key = settings.encryption_key
    if key:
        try:
            return Fernet(key.encode() if isinstance(key, str) else key)
        except Exception:
            pass
    # Derive key from secret_key if encryption_key not set
    secret = settings.secret_key.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"mycontext-api-keys",
        iterations=100000,
    )
    derived = base64.urlsafe_b64encode(kdf.derive(secret))
    return Fernet(derived)


def encrypt_api_key(plain_key: str) -> str:
    """Encrypt an API key for storage."""
    return _get_fernet().encrypt(plain_key.encode()).decode()


def decrypt_api_key(encrypted_key: str) -> str | None:
    """Decrypt an API key. Returns None on failure."""
    try:
        return _get_fernet().decrypt(encrypted_key.encode()).decode()
    except (InvalidToken, Exception):
        return None
