#!/usr/bin/env python3
# =====================================================================
#  מטרת סריקה רב-שירותית  —  Multi-Service Scan Target  (מודול 6)
#  פותח כמה "שירותים" עם Banner-ים ריאליסטיים (גרסאות!), כדי לתרגל
#  סריקת פורטים, זיהוי גרסאות (banner grabbing) וחקר חולשות.
#  אין צורך בהתקנות — פייתון בלבד. משתמש בפורטים גבוהים (ללא root).
#
#  הרצה:   python3 scan_target.py
#  ואז:    nmap 127.0.0.1 -p 2121,2222,8080,10000    |    nc 127.0.0.1 2121
#  עצירה:  Ctrl+C
# =====================================================================
import socket
import threading

# פורט : (שם, Banner שמוחזר בעת חיבור)
SERVICES = {
    2121: ("FTP",  "220 (vsFTPd 2.3.4)\r\n"),                    # גרסה עם Backdoor מפורסם!
    2222: ("SSH",  "SSH-2.0-OpenSSH_2.9p2\r\n"),                 # גרסה ישנה מאוד
    8080: ("HTTP", "HTTP/1.1 200 OK\r\nServer: Apache/1.3.20\r\n"
                   "\r\n<html><h1>ACME internal</h1>"
                   "<!-- flag{banner_grabbing_reveals_versions} --></html>\r\n"),
    10000: ("Backup", "SECRET-SERVICE v0.1 — flag{enumerate_every_open_port}\r\n"),
}


def serve(port, name, banner):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", port))
    s.listen(5)
    while True:
        try:
            conn, _ = s.accept()
            conn.sendall(banner.encode())
            conn.close()
        except OSError:
            break


if __name__ == "__main__":
    for port, (name, banner) in SERVICES.items():
        threading.Thread(target=serve, args=(port, name, banner), daemon=True).start()
    ports = ",".join(str(p) for p in SERVICES)
    print("[*] שירותים פתוחים עכשיו:")
    for port, (name, _) in SERVICES.items():
        print(f"      {port}/tcp  ->  {name}")
    print(f"[*] סרוק:         nmap 127.0.0.1 -p {ports} -sV")
    print(f"[*] תפוס Banner:  nc 127.0.0.1 2121   (או כל פורט אחר)")
    print("[*] לעצירה: Ctrl+C")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print("\n[*] נעצר. כל הפורטים נסגרו.")
