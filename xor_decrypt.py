# XOR decrypt script for HackTheBox Jet Secret Message
# Use in combination with the found password
# !/usr/bin/python

import sys

def xor_decrypt(data: bytes, key: str) -> bytes:
    key_bytes = key.encode()
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <key>")
        sys.exit(1)

    key = sys.argv[1]

    with open("encrypted.txt", "rb") as f:
        encrypted_data = f.read()

    decrypted = xor_decrypt(encrypted_data, key)

    try:
        print(decrypted.decode("utf-8"))
    except UnicodeDecodeError:
        print("[!] Decrypted data is not valid UTF-8. Printing raw bytes:\n")
        print(decrypted)