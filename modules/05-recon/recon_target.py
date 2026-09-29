#!/usr/bin/env python3
# =====================================================================
#  אתר החברה לתרגול איסוף מידע  —  Recon Target  (מודול 5)
#  "אתר" קטן של חברה מדומה (ACME) עם דליפות מידע קלאסיות שתוקף מחפש:
#  הערות בקוד המקור, robots.txt שחושף נתיבים, כותרת Server חושפנית,
#  וקובץ גיבוי שנשכח חשוף. מצא 4 דגלים — כולם באיסוף מידע בלבד.
#
#  אין צורך בהתקנות — פייתון בלבד (ספריית http.server המובנית).
#  הרצה:   python3 recon_target.py      → http://127.0.0.1:8000
#  עצירה:  Ctrl+C
# =====================================================================
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST, PORT = "127.0.0.1", 8000

HOME = """<!doctype html>
<html dir="rtl"><head><title>ACME Corp — דף הבית</title></head>
<body style="font-family:sans-serif">
  <h1>ACME Corp</h1>
  <p>צרו קשר: info@acme-corp.local</p>
  <p>גיוס: careers@acme-corp.local · מנהל מערכת: admin@acme-corp.local</p>
  <!-- TODO(dev): remove before production!  flag{view_source_reveals_secrets} -->
  <!-- temp admin panel: /admin-panel/  (protected by robots) -->
</body></html>"""

ROBOTS = ("User-agent: *\n"
          "Disallow: /admin-panel/\n"
          "Disallow: /backup/\n"
          "# do not index our backups\n")

ADMIN = ("<h1>Admin Panel</h1><p>flag{robots_txt_leaks_hidden_paths}</p>"
         "<p>found a path hidden only in robots.txt — a classic mistake.</p>")

BACKUP = ("# config.bak — forgotten, exposed backup file\n"
          "DB_HOST=127.0.0.1\n"
          "DB_USER=acme_admin\n"
          "DB_PASS=Summer2024!\n"
          "SECRET=flag{exposed_backup_files_are_gold}\n")

BACKUP_INDEX = "<h1>Index of /backup/</h1><ul><li><a href='config.bak'>config.bak</a></li></ul>"

ROUTES = {
    "/": ("text/html; charset=utf-8", HOME),
    "/robots.txt": ("text/plain; charset=utf-8", ROBOTS),
    "/admin-panel/": ("text/html; charset=utf-8", ADMIN),
    "/admin-panel": ("text/html; charset=utf-8", ADMIN),
    "/backup/": ("text/html; charset=utf-8", BACKUP_INDEX),
    "/backup/config.bak": ("text/plain; charset=utf-8", BACKUP),
}


class Handler(BaseHTTPRequestHandler):
    server_version = "Apache/2.4.49"     # גרסה חושפנית עם חולשה ידועה
    sys_version = ""

    def _send(self, code, ctype, body):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("X-Powered-By", "PHP/5.6.40")
        self.send_header("X-Recon-Flag", "flag{http_headers_leak_tech_stack}")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ROUTES:
            ctype, body = ROUTES[self.path]
            self._send(200, ctype, body)
        else:
            self._send(404, "text/html; charset=utf-8", "<h1>404 Not Found</h1>")

    def do_HEAD(self):
        # curl -I שולח HEAD — נחזיר את אותן כותרות (כולל ה-Server החושפני)
        ctype = ROUTES.get(self.path, ("text/html; charset=utf-8", ""))[0]
        self.send_response(200 if self.path in ROUTES else 404)
        self.send_header("Content-Type", ctype)
        self.send_header("X-Powered-By", "PHP/5.6.40")
        self.send_header("X-Recon-Flag", "flag{http_headers_leak_tech_stack}")
        self.end_headers()

    def log_message(self, *a):
        pass   # שקט — אל תציף את הטרמינל


if __name__ == "__main__":
    print(f"[*] ACME site running on http://{HOST}:{PORT}")
    print(f"[*] recon:  curl -sI {HOST}:{PORT}  |  curl {HOST}:{PORT}/robots.txt")
    print("[*] 4 hidden flags. Ctrl+C to stop.")
    try:
        HTTPServer((HOST, PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n[*] stopped.")
