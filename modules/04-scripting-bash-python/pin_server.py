#!/usr/bin/env python3
# =====================================================================
#  שרת ה-PIN הפגיע  —  Vulnerable PIN Service  (מודול 4)
#  שירות רשת קטן שמוגן ב-PIN בן 4 ספרות. חולשה: אין הגבלת נסיונות!
#  המשימה שלך: לכתוב סקריפט שמנחש את ה-PIN (Brute Force) ומקבל דגל.
#
#  טרמינל 1 (המטרה):   python3 pin_server.py
#  טרמינל 2 (התקיפה):  python3 brute_force.py
#  עצירה:              Ctrl+C
# =====================================================================
import socket
import random

HOST, PORT = "127.0.0.1", 9999
# PIN "אקראי" בן 4 ספרות — אבל בלי הגבלת נסיונות, אפשר לנסות את כולם
PIN = f"{random.randint(0, 9999):04d}"
FLAG = "flag{brute_force_beats_weak_pins}"


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[*] שרת ה-PIN מאזין על {HOST}:{PORT}")
    print(f"[*] (למדריך בלבד — ה-PIN הפעם הוא {PIN})")
    print("[*] שלח 4 ספרות; תשובה: OK <flag>  או  NO")
    print("[*] לעצירה: Ctrl+C")
    try:
        while True:
            conn, _ = s.accept()
            data = conn.recv(16).decode(errors="ignore").strip()
            if data == PIN:
                conn.sendall(f"OK {FLAG}\n".encode())
            else:
                conn.sendall(b"NO\n")
            conn.close()
    except KeyboardInterrupt:
        print("\n[*] נעצר.")
    finally:
        s.close()


if __name__ == "__main__":
    main()
