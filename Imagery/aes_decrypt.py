#!/usr/bin/env python3
import pyAesCrypt
import traceback

GREEN = "\033[92m"
RESET = "\033[0m"

buffer_size = 64 * 1024

encrypted_file = "" # INSERT FILENAME HERE
output_file = "decrypted.zip"
wordlist = "/usr/share/wordlists/rockyou.txt" # CHANGE IF NEEDED

def try_password(pwd):
    try:
        pyAesCrypt.decryptFile(encrypted_file, output_file, pwd.strip(), buffer_size)
        return True
    except Exception:
        return False

with open(wordlist, "r", encoding="latin-1") as wl:
    for password in wl:
        password = password.strip()
        try:
            if try_password(password):
                print(f"{GREEN}[+] Password found: {password}{RESET}")
                print("[✓] Decryption finished, check out output file.")
                break
        except KeyboardInterrupt:
            print("\n[!] Interrupted.")
            break
        except Exception:
            # silent fail for noisy errors
            pass
    else:
        print("[-] Password not found.")