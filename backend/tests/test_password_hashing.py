"""PowerGuard IoT — Password Hashing Unit Tests"""
import hashlib, hmac, os, pytest

def hash_password(password: str, salt: bytes = None) -> str:
    salt = salt or os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000)
    return f"{salt.hex()}:{dk.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    salt_hex, hash_hex = stored_hash.split(":")
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000)
    return hmac.compare_digest(dk.hex(), hash_hex)

def test_password_hashing_and_verification():
    h = hash_password("Secret123!")
    assert verify_password("Secret123!", h) is True
    assert verify_password("WrongPassword", h) is False

def test_password_unique_salts():
    h1 = hash_password("SamePass")
    h2 = hash_password("SamePass")
    assert h1 != h2