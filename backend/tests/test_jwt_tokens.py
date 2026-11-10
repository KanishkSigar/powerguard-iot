"""PowerGuard IoT — JWT Token Utilities Tests"""
import base64, json, hmac, hashlib, time, pytest

def create_mock_jwt(payload: dict, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    sig = hmac.new(secret.encode(), f"{h_b64}.{p_b64}".encode(), hashlib.sha256).digest()
    s_b64 = base64.urlsafe_b64encode(sig).decode().rstrip("=")
    return f"{h_b64}.{p_b64}.{s_b64}"

def verify_mock_jwt(token: str, secret: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3: raise ValueError("Invalid token")
    h_b64, p_b64, s_b64 = parts
    expected = base64.urlsafe_b64encode(hmac.new(secret.encode(), f"{h_b64}.{p_b64}".encode(), hashlib.sha256).digest()).decode().rstrip("=")
    if not hmac.compare_digest(expected, s_b64): raise ValueError("Signature mismatch")
    padding = "=" * (-len(p_b64) % 4)
    payload = json.loads(base64.urlsafe_b64decode(p_b64 + padding).decode())
    if payload.get("exp", 0) < time.time(): raise ValueError("Token expired")
    return payload

def test_jwt_valid_signature():
    secret = "supersecretkey"
    token = create_mock_jwt({"sub": "admin", "exp": time.time() + 3600}, secret)
    payload = verify_mock_jwt(token, secret)
    assert payload["sub"] == "admin"

def test_jwt_tampered_signature():
    secret = "supersecretkey"
    token = create_mock_jwt({"sub": "admin", "exp": time.time() + 3600}, secret)
    tampered = token[:-4] + "AAAA"
    with pytest.raises(ValueError, match="Signature mismatch"):
        verify_mock_jwt(tampered, secret)