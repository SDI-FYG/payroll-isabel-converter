#!/usr/bin/env python3
"""Build the password-protected index.html for GitHub Pages.

Usage:
    python tools/build_protected.py <Payroll_Isabel_Converter.html> [-o index.html]

The script asks for the account and password (they are NOT stored anywhere).
The converter page is gzip-compressed and encrypted with AES-256-GCM; the key is
derived from "ACCOUNT\\nPASSWORD" with PBKDF2-SHA256 (600 000 iterations).
Requires: pip install cryptography
"""
import argparse, base64, getpass, gzip, json, os, re, sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ITER = 600_000
LOGOUT = ('<button class="btn sec sm" type="button" title="Log out" '
          'onclick="try{sessionStorage.removeItem(\'fg-payroll-key\')}catch(e){};location.reload()">Log out</button>')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source"); ap.add_argument("-o", "--out", default=str(Path(__file__).resolve().parent.parent / "index.html"))
    ap.add_argument("--user"); ap.add_argument("--password")
    a = ap.parse_args()
    user = (a.user or input("Account: ")).strip().upper()
    pw = a.password or getpass.getpass("Password: ")
    if not a.password and getpass.getpass("Repeat password: ") != pw:
        sys.exit("Passwords do not match.")
    html = Path(a.source).read_text(encoding="utf-8")
    # add a log-out button next to the masterdata buttons
    html = html.replace('<button class="btn sec sm" id="btnOpenMd2">', LOGOUT + '\n    <button class="btn sec sm" id="btnOpenMd2">', 1)
    html = html.replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive((user + "\n" + pw).encode())
    data = AESGCM(key).encrypt(iv, gzip.compress(html.encode("utf-8"), 9), None)
    payload = json.dumps({"v": 1, "iter": ITER, "gzip": True, "salt": base64.b64encode(salt).decode(),
                          "iv": base64.b64encode(iv).decode(), "data": base64.b64encode(data).decode()})
    tpl = (Path(__file__).resolve().parent / "login_template.html").read_text(encoding="utf-8")
    logo = re.search(r'src="data:image/png;base64,([^"]+)"', html).group(1)
    out = tpl.replace("__LOGO__", logo).replace("__PAYLOAD__", payload)
    Path(a.out).write_text(out, encoding="utf-8")
    print(f"Written {a.out} ({len(out)/1e6:.1f} MB) for account {user}")

if __name__ == "__main__":
    main()
