#!/usr/bin/env python3
"""
BONUS target — "MegaShop" web app (module 09 extra practice).

A SECOND vulnerable web app, covering OWASP bugs the main owasp_playground.py
does NOT: Local File Inclusion / path traversal, JWT 'none'-algorithm auth
bypass, and API IDOR. Three more flags, stdlib only, localhost only.

    python3 web_lab2.py        # starts on http://127.0.0.1:8090/
    (Ctrl+C to stop)

⚠️  Training only, binds 127.0.0.1. Never use these techniques off this lab.
"""
import http.server
import socketserver
import pathlib
import base64
import json
import html
from urllib.parse import urlparse, parse_qs

HOST, PORT = "127.0.0.1", 8090
LOOT = pathlib.Path("/tmp/weblab2")

FLAG_LFI  = "flag{lfi_path_traversal_reads_secrets}"
FLAG_JWT  = "flag{jwt_none_algorithm_bypass}"
FLAG_IDOR = "flag{api_idor_other_users_data}"

# fake "database" of orders — order 9001 belongs to admin and holds the flag
ORDERS = {
    "1001": {"user": "you",   "item": "USB cable",      "total": "$7"},
    "1002": {"user": "you",   "item": "Mouse",          "total": "$19"},
    "9001": {"user": "admin", "item": "[CONFIDENTIAL]",  "total": FLAG_IDOR},
}


def b64url_decode(s):
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s.encode())


def b64url_encode(b):
    return base64.urlsafe_b64encode(b).decode().rstrip("=")


def plant():
    LOOT.mkdir(parents=True, exist_ok=True)
    (LOOT / "secret.conf").write_text(
        "# internal config — do not expose\nADMIN_NOTE=" + FLAG_LFI + "\n")
    # a normal 'home' page template that the app includes by name
    (LOOT / "home.html").write_text("<h2>Welcome to MegaShop</h2><p>Deals of the day!</p>")
    (LOOT / "about.html").write_text("<h2>About MegaShop</h2><p>Since 2011.</p>")


def page(title, body):
    return (f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}"
            f"</title></head><body>{body}</body></html>").encode()


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send(self, body, code=200, ctype="text/html"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        q = parse_qs(parsed.query)

        if parsed.path == "/":
            self._send(page("MegaShop",
                "<h1>MegaShop</h1>"
                "<ul>"
                "<li>Pages: <code>/view?page=home</code> (includes files by name...)</li>"
                "<li>Login (get a JWT): <code>/login</code></li>"
                "<li>Your profile: <code>/api/profile</code> (send the JWT in Authorization)</li>"
                "<li>Your orders: <code>/api/orders?id=1001</code></li>"
                "</ul>"))

        # ---- VULN 1: Local File Inclusion / path traversal -------------
        elif parsed.path == "/view":
            name = q.get("page", ["home"])[0]
            target = LOOT / name            # no sanitisation -> ../ escapes
            try:
                data = (LOOT / name).read_bytes() if ".." not in name \
                    else pathlib.Path(str(LOOT / name)).resolve(strict=False).read_bytes()
                self._send(data, ctype="text/plain")
            except Exception as e:
                self._send(page("view", f"<pre>cannot read {html.escape(name)}: "
                                        f"{html.escape(str(e))}</pre>"), code=404)

        # ---- issue a normal user JWT -----------------------------------
        elif parsed.path == "/login":
            header = b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
            payload = b64url_encode(json.dumps({"user": "you", "role": "user"}).encode())
            token = f"{header}.{payload}.c2lnbmF0dXJl"   # fake sig
            self._send(page("login",
                "<h1>Logged in as 'you'</h1>"
                f"<p>Your JWT:</p><code>{token}</code>"
                "<p>Use it: <code>Authorization: Bearer &lt;jwt&gt;</code> on /api/profile. "
                "Admins see a flag. (Is the signature actually verified?)</p>"))

        # ---- VULN 2: JWT 'none' algorithm bypass -----------------------
        elif parsed.path == "/api/profile":
            auth = self.headers.get("Authorization", "")
            tok = auth[7:] if auth.startswith("Bearer ") else ""
            try:
                h_b64, p_b64, _sig = tok.split(".")
                hdr = json.loads(b64url_decode(h_b64))
                pl = json.loads(b64url_decode(p_b64))
                # INSECURE: trust alg from the token; 'none' => skip verification
                if hdr.get("alg", "").lower() == "none" or True:
                    role = pl.get("role", "user")
                    if role == "admin":
                        self._send(page("profile",
                            f"<h1>Admin profile</h1><p>{FLAG_JWT}</p>"))
                    else:
                        self._send(page("profile",
                            f"<h1>Profile: {html.escape(pl.get('user','?'))} "
                            f"(role={html.escape(role)})</h1>"
                            "<p>Only admins get the flag. Forge the token...</p>"))
                    return
            except Exception:
                pass
            self._send(page("profile", "<h1>Missing/invalid token</h1>"
                            "Get one at /login"), code=401)

        # ---- VULN 3: API IDOR ------------------------------------------
        elif parsed.path == "/api/orders":
            oid = q.get("id", [""])[0]
            if oid in ORDERS:                # no ownership check!
                self._send(json.dumps(ORDERS[oid]).encode(), ctype="application/json")
            else:
                self._send(b'{"error":"not found"}', code=404, ctype="application/json")
        else:
            self._send(page("404", "404"), code=404)


def main():
    plant()
    httpd = socketserver.ThreadingTCPServer((HOST, PORT), Handler)
    httpd.daemon_threads = True
    print(f"[*] MegaShop bonus target: http://{HOST}:{PORT}/  (Ctrl+C to stop)")
    print("    3 flags: LFI, JWT none-alg, API IDOR.  Hints in missions; solutions in solutions.md")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] stopped.")


if __name__ == "__main__":
    main()
