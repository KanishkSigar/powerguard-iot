"""PowerGuard IoT — Theme Settings Validation Tests"""
import re, pytest

VALID_THEMES = {"light", "dark", "high_contrast", "cyberpunk"}

def validate_theme_config(theme: str, accent_color: str) -> dict:
    errors = []
    if theme not in VALID_THEMES: errors.append(f"Invalid theme: {theme}")
    if not re.match(r"^#[0-9a-fA-F]{6}$", accent_color): errors.append(f"Invalid hex color: {accent_color}")
    return {"is_valid": len(errors) == 0, "errors": errors}

def test_valid_theme():
    res = validate_theme_config("dark", "#00ffcc")
    assert res["is_valid"] is True

def test_invalid_theme():
    res = validate_theme_config("neon", "invalid-color")
    assert res["is_valid"] is False
    assert len(res["errors"]) == 2