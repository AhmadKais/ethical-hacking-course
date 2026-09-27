#!/usr/bin/env python3
# =====================================================================
#  שרת רב-פורטים להדגמה  —  Multi-Port Demo Server
#  פותח כמה פורטים בבת אחת, כדי שסריקת nmap תיראה כמו מטרה אמיתית.
#  אין צורך בהתקנות — פייתון בלבד.
#
#  הרצה:   python3 multiport_server.py
#  ואז:    nmap 127.0.0.1 -p-        (או:  nmap <ה-IP-שלך> מהמכונה של השכן)
#  עצירה:  Ctrl+C
# =====================================================================
import socket
import threading

# פורט : שם-שירות מדומה (ה-Banner שיוחזר)
PORTS = {
    2121: "FTP",
    2323: "Telnet",
    8080: "HTTP",
    9000: "Custom-App",
    13337: "Secret-Service",
}


def serve(port, name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen(5)
    while True:
        try:
            conn, addr = s.accept()
            conn.sendall(f"220 Welcome to fake {name} service on port {port}\r\n".encode())
            conn.close()
        except OSError:
            break


if __name__ == "__main__":
    for port, name in PORTS.items():
        threading.Thread(target=serve, args=(port, name), daemon=True).start()
    print("[*] הפורטים הפתוחים עכשיו:", ", ".join(str(p) for p in PORTS))
    print("[*] סרוק אותם:  nmap 127.0.0.1 -p", ",".join(str(p) for p in PORTS))
    print("[*] או ראה בעצמך:  ss -tulpn")
    print("[*] לעצירה: Ctrl+C")
    try:
        threading.Event().wait()   # רוץ עד Ctrl+C
    except KeyboardInterrupt:
        print("\n[*] נעצר. כל הפורטים נסגרו.")
