#!/usr/bin/env python3
# =====================================================================
#  הדגמת Port Forwarding / Pivot  —  Local Port Forwarder  (מודול 12)
#  מנתב פורט מקומי אל יעד אחר — בדיוק מה ש-`ssh -L` עושה, אבל בפייתון
#  טהור (בלי צורך ב-SSH server). כך "רואים" איך תעבורה עוברת דרך גשר.
#
#  שימוש:   python3 pivot_demo.py <פורט-מקומי> <יעד-host> <יעד-port>
#  דוגמה:   python3 pivot_demo.py 8888 127.0.0.1 8000
#           → עכשיו localhost:8888 מנתב אל 127.0.0.1:8000 ("הרשת הפנימית")
#  עצירה:   Ctrl+C
# =====================================================================
import socket
import sys
import threading


def pipe(src, dst):
    """מעביר בתים מצד אחד לשני עד סגירה."""
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass


def handle(client, thost, tport):
    try:
        target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target.connect((thost, tport))
    except OSError as e:
        print(f"[!] לא ניתן להתחבר ל-{thost}:{tport} ({e})")
        client.close()
        return
    # שני כיוונים במקביל = מנהרה דו-כיוונית
    threading.Thread(target=pipe, args=(client, target), daemon=True).start()
    threading.Thread(target=pipe, args=(target, client), daemon=True).start()


def main():
    if len(sys.argv) != 4:
        print("usage: python3 pivot_demo.py <local_port> <target_host> <target_port>")
        sys.exit(1)
    lport = int(sys.argv[1])
    thost, tport = sys.argv[2], int(sys.argv[3])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", lport))
    s.listen(50)
    print(f"[*] מנהרה פעילה:  127.0.0.1:{lport}  ──►  {thost}:{tport}")
    print(f"[*] פנה אל 127.0.0.1:{lport} כאילו הוא {thost}:{tport} ('הרשת הפנימית')")
    print("[*] Ctrl+C לעצירה.")
    try:
        while True:
            client, _ = s.accept()
            handle(client, thost, tport)
    except KeyboardInterrupt:
        print("\n[*] נעצר.")
    finally:
        s.close()


if __name__ == "__main__":
    main()
