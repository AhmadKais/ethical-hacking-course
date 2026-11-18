#!/usr/bin/env python3
"""
ACME Corp — Capstone Engagement Range (self-contained, localhost-only).

Boots a small SIMULATED corporate network as several HTTP services on 127.0.0.1,
chaining the whole kill-chain the course teaches:

    Recon (:8080) -> Web/SQLi + RCE (:8081) -> Password cracking (offline)
      -> Pivot to internal jumpbox (:9090) -> Writable-cron privesc
      -> Domain Admin via NTLM crack -> Report

Everything runs in ONE process, no VM, stdlib only. Each stage leaks the KEY
you need for the next stage, exactly like a real engagement.

    python3 acme_range.py          # start the range
    (Ctrl+C to stop)

Then attack it with the course tools (curl, sqlmap-style payloads, john/hashcat...).
Collect six flag{...} values and submit them:  python3 scoreboard.py

⚠️  Legal: every service listens on 127.0.0.1 (your own machine) only. For
    training. Never point these techniques at a system you do not own.
"""
import http.server
import socketserver
import subprocess
import threading
import pathlib
import hashlib
import html
import struct
import os
import sys

HOST = "127.0.0.1"
LOOT = pathlib.Path("/tmp/acme_range")

# ----- credentials / secrets used across the chain -----------------------
JUMP_PASSWORD = "superman"       # cracked from employee MD5 hashes -> pivot token
DA_PASSWORD   = "Password123"    # cracked from NTLM hash          -> domain admin

FLAGS = {
    "recon":    "flag{recon_source_disclosure}",
    "sqli":     "flag{sqli_auth_bypass}",
    "rce":      "flag{command_injection_rce}",
    "pivot":    "flag{pivot_internal_access}",
    "privesc":  "flag{privesc_writable_cron}",
    "domain":   "flag{domain_admin_ntlm_crack}",
}


# ----- pure-python MD4 (OpenSSL disables it) for NTLM hashes --------------
def md4(data: bytes) -> bytes:
    def lrot(x, n): return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
    a, b, c, d = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476
    msg = bytearray(data)
    ln = (8 * len(data)) & 0xFFFFFFFFFFFFFFFF
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0)
    msg += struct.pack("<Q", ln)
    for off in range(0, len(msg), 64):
        X = list(struct.unpack("<16I", msg[off:off + 64]))
        aa, bb, cc, dd = a, b, c, d
        for i in (0, 4, 8, 12):
            a = lrot((a + ((b & c) | (~b & d)) + X[i]) & 0xFFFFFFFF, 3)
            d = lrot((d + ((a & b) | (~a & c)) + X[i + 1]) & 0xFFFFFFFF, 7)
            c = lrot((c + ((d & a) | (~d & b)) + X[i + 2]) & 0xFFFFFFFF, 11)
            b = lrot((b + ((c & d) | (~c & a)) + X[i + 3]) & 0xFFFFFFFF, 19)
        for i in (0, 1, 2, 3):
            a = lrot((a + ((b & c) | (b & d) | (c & d)) + X[i] + 0x5A827999) & 0xFFFFFFFF, 3)
            d = lrot((d + ((a & b) | (a & c) | (b & c)) + X[i + 4] + 0x5A827999) & 0xFFFFFFFF, 5)
            c = lrot((c + ((d & a) | (d & b) | (a & b)) + X[i + 8] + 0x5A827999) & 0xFFFFFFFF, 9)
            b = lrot((b + ((c & d) | (c & a) | (d & a)) + X[i + 12] + 0x5A827999) & 0xFFFFFFFF, 13)
        for i in (0, 2, 1, 3):
            a = lrot((a + (b ^ c ^ d) + X[i] + 0x6ED9EBA1) & 0xFFFFFFFF, 3)
            d = lrot((d + (a ^ b ^ c) + X[i + 8] + 0x6ED9EBA1) & 0xFFFFFFFF, 9)
            c = lrot((c + (d ^ a ^ b) + X[i + 4] + 0x6ED9EBA1) & 0xFFFFFFFF, 11)
            b = lrot((b + (c ^ d ^ a) + X[i + 12] + 0x6ED9EBA1) & 0xFFFFFFFF, 15)
        a = (a + aa) & 0xFFFFFFFF
        b = (b + bb) & 0xFFFFFFFF
        c = (c + cc) & 0xFFFFFFFF
        d = (d + dd) & 0xFFFFFFFF
    return struct.pack("<4I", a, b, c, d)


def ntlm(password: str) -> str:
    return md4(password.encode("utf-16-le")).hex()


# ----- loot files planted "on disk" for the RCE stage --------------------
def plant_loot():
    LOOT.mkdir(parents=True, exist_ok=True)
    (LOOT / "user_flag.txt").write_text(FLAGS["rce"] + "\n")
    (LOOT / "root.txt").write_text(FLAGS["privesc"] + "\n")


# employee password MD5 hashes (one of them is the jumpbox password)
EMPLOYEE_HASHES = "\n".join(
    f"{u}:{hashlib.md5(p.encode()).hexdigest()}"
    for u, p in [("j.smith", "autumn2019"), ("a.jones", "liverpool"),
                 ("svc_backup", JUMP_PASSWORD), ("m.brown", "trustno1")]
)

# domain NTLM dump (secretsdump format) — one cracks to DA_PASSWORD
NTLM_DUMP = "\n".join([
    f"ACME\\Administrator:500:aad3b435b51404eeaad3b435b51404ee:{ntlm(DA_PASSWORD)}:::",
    "ACME\\guest:501:aad3b435b51404eeaad3b435b51404ee:" + ntlm("Qwerty!2024xZ") + ":::",
    "ACME\\krbtgt:502:aad3b435b51404eeaad3b435b51404ee:" + ntlm("S3cr3t__uncrackable__9z") + ":::",
])


def page(title, body):
    return (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>{html.escape(title)}</title></head><body>{body}</body></html>").encode()


# ===================== STAGE 1 — public website :8080 ====================
class ReconHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send(self, body, code=200, ctype="text/html"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Server", "Apache/2.4.49 (Unix)")  # juicy version for recon
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            body = (
                "<h1>ACME Corp</h1><p>Leading provider of widgets since 1998.</p>"
                "<p>Careers &middot; Products &middot; Contact</p>"
                f"<!-- DEV NOTE: staging login portal lives on port 8081. "
                f"Creds were rotated but the app is still vulnerable. "
                f"Recon reward: {FLAGS['recon']} -->"
            )
            self._send(page("ACME Corp", body))
        elif self.path == "/robots.txt":
            self._send("User-agent: *\nDisallow: /backup/\n", ctype="text/plain")
        elif self.path.startswith("/backup/"):
            self._send(
                "-- partial DB export --\n"
                "-- employees table dumped to /admin/hashes.txt on the staging app (8081)\n"
                "-- staging login is at http://127.0.0.1:8081/\n",
                ctype="text/plain")
        else:
            self._send(page("404", "<h1>404 Not Found</h1>"), code=404)


# ============ STAGE 2+3 — staging app :8081 (SQLi + RCE) =================
class WebAppHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send(self, body, code=200, ctype="text/html"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        if self.path == "/":
            self._send(page("Staging Login",
                "<h1>ACME Staging — Login</h1>"
                "<form method='POST' action='/login'>"
                "User: <input name='user'><br>Pass: <input name='pass' type='password'><br>"
                "<button>Sign in</button></form>"))
        elif self.path == "/admin/hashes.txt":
            self._send(EMPLOYEE_HASHES + "\n", ctype="text/plain")
        elif self.path.startswith("/tools/ping"):
            # STAGE 3: command injection via shell=True
            from urllib.parse import urlparse, parse_qs
            host = parse_qs(urlparse(self.path).query).get("host", [""])[0]
            if not host:
                self._send(page("ping", "<h1>Ping Tool</h1>usage: /tools/ping?host=127.0.0.1"))
                return
            try:
                out = subprocess.run("ping -c 1 -w 1 " + host, shell=True,
                                     capture_output=True, text=True, timeout=6)
                res = out.stdout + out.stderr
            except Exception as e:
                res = str(e)
            self._send(page("ping", "<pre>" + html.escape(res) + "</pre>"))
        else:
            self._send(page("404", "<h1>404</h1>"), code=404)

    def do_POST(self):
        if self.path == "/login":
            n = int(self.headers.get("Content-Length", 0))
            from urllib.parse import parse_qs
            form = parse_qs(self.rfile.read(n).decode())
            user = form.get("user", [""])[0]
            pw = form.get("pass", [""])[0]
            # STAGE 2: classic SQLi — string-concatenated query over a fake table
            query = f"SELECT * FROM users WHERE user='{user}' AND pass='{pw}'"
            bypassed = ("'" in user or "'" in pw) and ("--" in query or " OR " in query.upper())
            legit = (user == "admin" and pw == "SuperSecretStaging!")
            if bypassed or legit:
                self._send(page("Dashboard",
                    "<h1>Welcome, admin</h1>"
                    f"<p>Auth bypass successful: {FLAGS['sqli']}</p>"
                    "<ul>"
                    "<li>Employee hash export: <a href='/admin/hashes.txt'>/admin/hashes.txt</a></li>"
                    "<li>Network diagnostics: <a href='/tools/ping?host=127.0.0.1'>/tools/ping</a> "
                    "(passes host straight to the shell...)</li>"
                    "<li>Internal jumpbox: http://127.0.0.1:9090/ "
                    "(authenticate with a cracked employee password)</li>"
                    "</ul>"))
            else:
                self._send(page("Login", "<h1>Invalid credentials</h1>"
                                "<a href='/'>back</a>"), code=401)
        else:
            self._send(page("404", "404"), code=404)


# ============ STAGE 4+5+6 — internal jumpbox :9090 ======================
class JumpboxHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _send(self, body, code=200, ctype="text/html"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def _authed(self):
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(self.path).query)
        token = q.get("token", [""])[0] or self.headers.get("X-Pivot-Token", "")
        return token == JUMP_PASSWORD

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.path)
        if not self._authed():
            self._send(page("401", "<h1>401 Unauthorized</h1>"
                "<p>Internal host. Authenticate: add <code>?token=&lt;password&gt;</code> "
                "or header <code>X-Pivot-Token</code> with a cracked employee password.</p>"),
                code=401)
            return
        if parsed.path == "/":
            self._send(page("Jumpbox",
                "<h1>ACME Internal Jumpbox</h1>"
                f"<p>Pivot successful: {FLAGS['pivot']}</p>"
                "<ul>"
                "<li>Domain secrets dump: <a href='/secrets/ntlm.txt?token=%s'>/secrets/ntlm.txt</a></li>"
                "<li>Root backup job (writable!): <code>/cron/backup</code> — "
                "POST a command, root runs it.</li>"
                "<li>Domain controller: <code>/dc?da=&lt;cracked_admin_password&gt;</code></li>"
                "</ul>" % JUMP_PASSWORD))
        elif parsed.path == "/secrets/ntlm.txt":
            self._send(NTLM_DUMP + "\n", ctype="text/plain")
        elif parsed.path == "/cron/backup":
            self._send(page("cron",
                "<pre># /etc/cron.d/backup  (runs as root every 5 min)\n"
                "# NOTE: this script is world-writable (oops).\n"
                "*/5 * * * * root /opt/acme/backup.sh\n\n"
                "POST new contents to this endpoint to overwrite backup.sh; "
                "root will execute it.</pre>"))
        elif parsed.path == "/dc":
            # STAGE 6: domain admin via cracked NTLM
            da = parse_qs(parsed.query).get("da", [""])[0]
            if da == DA_PASSWORD:
                self._send(page("DC",
                    "<h1>Domain Controller — ACME.local</h1>"
                    f"<p>Authenticated as Domain Admin. {FLAGS['domain']}</p>"))
            else:
                self._send(page("DC", "<h1>Access denied</h1>"
                    "<p>Crack the Administrator NTLM hash (hashcat -m 1000) and pass it as "
                    "<code>?da=</code>.</p>"), code=403)
        else:
            self._send(page("404", "404"), code=404)

    def do_POST(self):
        if not self._authed():
            self._send(page("401", "401"), code=401)
            return
        from urllib.parse import urlparse
        if urlparse(self.path).path == "/cron/backup":
            n = int(self.headers.get("Content-Length", 0))
            payload = self.rfile.read(n).decode(errors="replace").strip()
            if payload:
                # STAGE 5: writable cron -> root executes attacker's command
                root_flag = (LOOT / "root.txt").read_text().strip()
                self._send(page("cron",
                    "<pre>[+] backup.sh overwritten\n"
                    "[+] root cron executed your payload:\n"
                    f"    {html.escape(payload)}\n"
                    f"[+] id=uid=0(root) gid=0(root)\n"
                    f"[+] /root/root.txt -> {root_flag}</pre>"))
            else:
                self._send(page("cron", "empty payload"), code=400)
        else:
            self._send(page("404", "404"), code=404)


def serve(port, handler):
    httpd = socketserver.ThreadingTCPServer((HOST, port), handler)
    httpd.daemon_threads = True
    httpd.serve_forever()


def main():
    plant_loot()
    servers = [(8080, ReconHandler), (8081, WebAppHandler), (9090, JumpboxHandler)]
    for port, h in servers:
        t = threading.Thread(target=serve, args=(port, h), daemon=True)
        t.start()
    print("=" * 62)
    print("  ACME Corp engagement range is LIVE (localhost only)")
    print("=" * 62)
    print("  [*] External website ....... http://127.0.0.1:8080/")
    print("  [*] Staging web app ........ http://127.0.0.1:8081/")
    print("  [*] Internal jumpbox ....... http://127.0.0.1:9090/  (needs pivot)")
    print()
    print("  Scope: these three hosts only. Find SIX flags, then report.")
    print("  Start with recon on :8080.  Stuck? see README.md hint ladder.")
    print("  Submit flags:  python3 scoreboard.py")
    print("  Ctrl+C to stop.")
    print("=" * 62)
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print("\n[*] Range stopped. Loot left in /tmp/acme_range (harmless).")
        sys.exit(0)


if __name__ == "__main__":
    main()
