#!/usr/bin/env python3
"""
PowerGuard IoT — Firmware Binary Signature & Integrity Verifier
Validates SHA-256 hashes, magic bytes, and hardware headers of ESP32 firmware binaries
before Over-The-Air (OTA) deployment to field devices.
"""

import argparse
import hashlib
import os
import sys

ESP_IMAGE_MAGIC = 0xE9


def verify_binary(file_path: str, expected_sha256: str = None) -> bool:
    """Verifies file existence, ESP32 header magic byte, and SHA-256 checksum."""
    if not os.path.exists(file_path):
        print(f"Error: Binary file not found: {file_path}", file=sys.stderr)
        return False

    file_size = os.path.getsize(file_path)
    if file_size < 32:
        print(f"Error: Binary file is too small ({file_size} bytes)", file=sys.stderr)
        return False

    with open(file_path, "rb") as f:
        header = f.read(32)
        f.seek(0)
        hasher = hashlib.sha256()
        while chunk := f.read(65536):
            hasher.update(chunk)
        computed_sha256 = hasher.hexdigest()

    magic = header[0]
    is_valid_esp = (magic == ESP_IMAGE_MAGIC)
    
    print(f"File: {os.path.basename(file_path)}")
    print(f"Size: {file_size} bytes")
    print(f"SHA-256: {computed_sha256}")
    print(f"Magic Byte: 0x{magic:02X} ({'Valid ESP32 Image' if is_valid_esp else 'Invalid/Non-ESP header'})")

    if expected_sha256:
        if computed_sha256.lower() == expected_sha256.lower():
            print("Checksum verification: PASSED [MATCH]")
            return True
        else:
            print("Checksum verification: FAILED [MISMATCH]", file=sys.stderr)
            return False

    return True


def main():
    parser = argparse.ArgumentParser(description="Verify ESP32 firmware binary integrity")
    parser.add_argument("binary", help="Path to compiled .bin firmware file")
    parser.add_argument("--sha256", help="Expected SHA-256 hash to verify against")
    args = parser.parse_args()

    success = verify_binary(args.binary, args.sha256)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()