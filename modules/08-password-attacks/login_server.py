#!/usr/bin/env python3
# =====================================================================
#  שרת התחברות לתרגול Brute Force מקוון  —  Login Target  (מודול 8)
#  טופס התחברות פשוט. משתמש: admin, סיסמה: אחת מ-rockyou (ברירת מחדל:
#  "superman"). המשימה: לפצח את הסיסמה עם Hydra דרך טופס ה-web.
#  אין הגבלת נסיונות — לכן Brute Force מקוון עובד.
#
#  אין צורך בהתקנות — פייתון בלבד. מאזין על 127.0.0.1 בלבד.
#  הרצה:   python3 login_server.py       → http://127.0.0.1:8081
#  עצירה:  Ctrl+C
# =====================================================================
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

HOST, PORT = "127.0.0.1", 8081
VALID_USER = "admin"
VALID_PASS = "superman"     # <-- שנה לסיסמה אחרת מ-rockyou כדי לשנות קושי
FLAG = "flag{online_brute_force_cracked_the_login}"

FORM = """<!doctype html><html dir="rtl"><head><meta charset="utf-8">
<title>ACME Login</title></head><body style="font-family:sans-serif">
<h1>🔐 ACME — כניסת מנהל</h1>
<form method="POST" action="/login">
  משתמש: <input name="user" value="admin"><br><br>
  סיסמה: <input name="pass" type="password"><br><br>
  <button>התחבר</button>
</form>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "ACME-Login/1.0"

    def _send(self, body, code=200):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(FORM)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        params = parse_qs(self.rfile.read(length).decode("utf-8", "replace"))
        user = params.get("user", [""])[0]
        pw = params.get("pass", [""])[0]
        if user == VALID_USER and pw == VALID_PASS:
            # "Welcome" = סימן ההצלחה ש-Hydra יחפש בהיעדרו
            self._send(f"<h1>Welcome, {user}!</h1><p>{FLAG}</p>")
        else:
            self._send("<h1>Invalid credentials</h1>", 200)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"[*] ACME Login running on http://{HOST}:{PORT}")
    print(f"[*] (מדריך) user={VALID_USER} pass={VALID_PASS} — התלמידים יפצחו עם Hydra")
    print("[*] failure marker for hydra:  'Invalid credentials'")
    print("[*] Ctrl+C to stop.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n[*] stopped.")
