from werkzeug.security import check_password_hash

# ANSI escape codes for color
GREEN = "\033[92m"
RESET = "\033[0m"

hash_val = ""  # insert your hash here
wordlist = "/usr/share/wordlists/rockyou.txt"

print(f"[+] Loaded hash")
print(f"[+] Starting brute-force using: {wordlist}\n")

count = 0

with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        pw = line.strip()
        if not pw:
            continue

        count += 1
        if count % 50000 == 0:
            print(f"[>] Tested {count:,} passwords so far...")

        if check_password_hash(hash_val, pw):
            print(f"\n{GREEN}[✓] Cracked! Password is: {pw}{RESET}")
            break
    else:
        print("\n[-] No match found in provided wordlist.")