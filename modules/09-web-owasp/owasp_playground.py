#!/usr/bin/env python3
# =====================================================================
#  מגרש המשחקים הפגיע  —  OWASP Playground  (מודול 9)
#  אפליקציית web קטנה ופגיעה בכוונה, ללא Docker — פייתון בלבד.
#  מכילה 3 חולשות OWASP אמיתיות לתרגול:
#    • SQL Injection  — עקיפת התחברות (/login)
#    • Reflected XSS  — הזרקת JS (/search)
#    • IDOR           — גישה לנתוני משתמש אחר (/profile?id=)
#
#  הרצה:   python3 owasp_playground.py     → http://127.0.0.1:5000
#  עצירה:  Ctrl+C
#  ⚠️ קוד פגיע לצורכי לימוד בלבד. מאזין על 127.0.0.1 בלבד.
# =====================================================================
import sqlite3
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HOST, PORT = "127.0.0.1", 5000


def get_db():
    db = sqlite3.connect(":memory:")
    db.executescript("""
        CREATE TABLE users(id INTEGER, user TEXT, pass TEXT, email TEXT, secret TEXT);
        INSERT INTO users VALUES
          (1,'guest','guest123','guest@acme.local','nothing here'),
          (2,'alice','Password1','alice@acme.local','alice private note'),
          (3,'admin','S3cr3tAdminPass!','admin@acme.local','flag{idor_exposed_admin_profile}');
    """)
    return db


INDEX = """<!doctype html><html dir="rtl"><head><meta charset="utf-8"><title>ACME Portal</title></head>
<body style="font-family:sans-serif">
<h1>🌐 ACME Portal — מגרש תרגול OWASP</h1>
<ul>
  <li><a href="/login">התחברות</a> — נסה SQL Injection</li>
  <li><a href="/search?q=hello">חיפוש</a> — נסה XSS</li>
  <li><a href="/profile?id=1">הפרופיל שלי</a> — נסה IDOR (שנה את ה-id)</li>
</ul></body></html>"""

LOGIN_FORM = """<!doctype html><html dir="rtl"><head><meta charset="utf-8"><title>Login</title></head>
<body style="font-family:sans-serif"><h1>🔐 התחברות</h1>
<form method="POST" action="/login">
משתמש: <input name="user"><br><br>סיסמה: <input name="pass"><br><br><button>התחבר</button></form>
<p style="color:#888">רמז: מה קורה אם שם המשתמש הוא <code>' OR '1'='1' --</code> ?</p></body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "ACME-Portal/1.0"

    def _send(self, body, code=200):
        data = body.encode("utf-8", "replace")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/":
            return self._send(INDEX)
        if u.path == "/login":
            return self._send(LOGIN_FORM)
        if u.path == "/search":
            # ❌ Reflected XSS: הקלט מוחזר לדף ללא Encoding
            term = q.get("q", [""])[0]
            note = ""
            if "<script" in term.lower() or "onerror" in term.lower():
                note = "<p style='color:red'>XSS! הדפדפן הריץ את הקוד שלך — flag{reflected_xss_no_output_encoding}</p>"
            return self._send(f"<html dir='rtl'><body><h1>תוצאות חיפוש</h1>"
                              f"<p>חיפשת: {term}</p>{note}<a href='/'>חזרה</a></body></html>")
        if u.path == "/profile":
            # ❌ IDOR: אין בדיקה שה-id שייך למשתמש המחובר
            uid = q.get("id", ["1"])[0]
            db = get_db()
            try:
                row = db.execute("SELECT id,user,email,secret FROM users WHERE id=?", (uid,)).fetchone()
            except Exception:
                row = None
            db.close()
            if row:
                return self._send(f"<html dir='rtl'><body><h1>פרופיל #{row[0]}</h1>"
                                  f"<p>משתמש: {html.escape(row[1])}</p><p>אימייל: {html.escape(row[2])}</p>"
                                  f"<p>הערה פרטית: {html.escape(row[3])}</p><a href='/'>חזרה</a></body></html>")
            return self._send("<h1>לא נמצא</h1>")
        return self._send("<h1>404</h1>", 404)

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers.get("Content-Length", 0))
            p = parse_qs(self.rfile.read(length).decode("utf-8", "replace"))
            user = p.get("user", [""])[0]
            pw = p.get("pass", [""])[0]
            db = get_db()
            # ❌ SQL Injection: השאילתה נבנית בשרשור מחרוזות של קלט המשתמש
            query = f"SELECT id,user FROM users WHERE user='{user}' AND pass='{pw}'"
            try:
                rows = db.execute(query).fetchall()
            except Exception as e:
                db.close()
                return self._send(f"<h1>שגיאת SQL</h1><pre>{html.escape(str(e))}</pre>"
                                  f"<p>(שגיאה חושפנית — גם זו חולשה!)</p><pre>{html.escape(query)}</pre>")
            # בדיקה תקינה (מאובטחת) לאותם פרטים — כדי לזהות אם הייתה הזרקה
            legit = db.execute("SELECT 1 FROM users WHERE user=? AND pass=?", (user, pw)).fetchone()
            db.close()
            if rows:
                who = rows[0][1]
                # אם ההתחברות הצליחה אך הפרטים אינם חוקיים באמת → זו הזרקה!
                flag = "" if legit else "<p>🏴 flag{sql_injection_auth_bypass}</p>"
                return self._send(f"<html dir='rtl'><body><h1>ברוך הבא, {html.escape(who)}!</h1>"
                                  f"{flag}<a href='/'>חזרה</a></body></html>")
            return self._send("<h1>התחברות נכשלה</h1><a href='/login'>נסה שוב</a>")
        return self._send("<h1>404</h1>", 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"[*] OWASP Playground running on http://{HOST}:{PORT}")
    print("[*] /login (SQLi)  |  /search?q= (XSS)  |  /profile?id= (IDOR)")
    print("[*] 3 flags. Ctrl+C to stop.")
    try:
        ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n[*] stopped.")
