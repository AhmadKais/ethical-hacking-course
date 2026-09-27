#!/usr/bin/env python3
# =====================================================================
#  שרת הדגמה לשיעור רשתות  —  Networking Demo Server
#  הרץ אותי, ואז "ראה" את הפורט נפתח וסרוק אותי עם nmap / ss / curl.
#
#  התקנה (פעם אחת):   pip install flask   (או: sudo apt install python3-flask)
#  הרצה:              python3 demo_server.py
#  עצירה:             Ctrl+C
# =====================================================================
from flask import Flask, request

app = Flask(__name__)

PORT = 5000  # <-- שנה כאן כדי לפתוח פורט אחר, ואז סרוק שוב


@app.route("/")
def home():
    return """
    <html dir="rtl"><body style="font-family:sans-serif;text-align:center;margin-top:60px">
      <h1>🚀 שרת הרשת של הכיתה עובד!</h1>
      <p>הפורט הזה <b>פתוח</b> עכשיו. נסה לסרוק אותי:</p>
      <pre style="text-align:left;display:inline-block;background:#111;color:#0f0;padding:16px">
ss -tulpn | grep %d
nmap 127.0.0.1 -p %d
curl http://127.0.0.1:%d/whoami
      </pre>
      <p>עצור את השרת (Ctrl+C) ותראה שהפורט נסגר.</p>
    </body></html>
    """ % (PORT, PORT, PORT)


@app.route("/whoami")
def whoami():
    # מראה לכל מי שמתחבר את כתובת ה-IP שלו — נהדר לתרגיל "סרוק את השכן"
    return f"👋 שלום! ה-IP שממנו התחברת הוא: {request.remote_addr}\n"


@app.route("/secret")
def secret():
    return "🏴 flag{you_found_the_open_port}\n"


if __name__ == "__main__":
    print(f"[*] מפעיל שרת על פורט {PORT} ...")
    print(f"[*] בדוק בטרמינל אחר:  ss -tulpn | grep {PORT}")
    print(f"[*] או סרוק:           nmap 127.0.0.1 -p {PORT}")
    print(f"[*] גלוש:              http://127.0.0.1:{PORT}")
    print("[*] לעצירה: Ctrl+C")
    # host="0.0.0.0" = הקשב לכל הרשת, כדי שחברים בכיתה יוכלו לסרוק אותך
    app.run(host="0.0.0.0", port=PORT)
