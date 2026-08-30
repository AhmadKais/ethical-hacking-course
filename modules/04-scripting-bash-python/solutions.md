<div dir="rtl">

# ✅ פתרונות מלאים — מודול 4: סקריפטינג

> נסה לבד ב-[`missions.md`](missions.md) קודם.

---

## חלק א' — Bash

**4.1**
```bash
#!/bin/bash
echo "Hello Hacker"
```
```bash
chmod +x hello.sh
./hello.sh
```

**4.2**
```bash
#!/bin/bash
read -p "Enter name: " name
echo "Welcome, $name"
```

**4.3**
```bash
#!/bin/bash
if [ "$1" -eq 80 ]; then
    echo "HTTP"
elif [ "$1" -eq 443 ]; then
    echo "HTTPS"
else
    echo "Unknown"
fi
```
הרצה: `./script.sh 443` → `HTTPS`.

**4.4**
```bash
#!/bin/bash
for i in $(seq 1 5); do
    echo "Pinging 10.0.0.$i"
done
```

---

## חלק ב' — Python בסיסי

**4.5**
```python
target = "10.0.0.5"
print(f"[*] Target is {target}")
```

**4.6**
```python
banner = "Apache/2.4.49 (Debian)"
version = banner.split("/")[1].split(" ")[0]
print(version)   # 2.4.49
```
הסבר: `split("/")` → `['Apache', '2.4.49 (Debian)']`; לוקחים אינדקס 1, ואז `split(" ")[0]` לוקח את החלק לפני הרווח.

**4.7**
```python
services = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS"}
for port, name in services.items():
    print(f"Port {port} -> {name}")
```

---

## חלק ג' — לוגיקה ולולאות

**4.8**
```python
def check_port(port):
    services = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS"}
    return services.get(port, "Unknown")
```
`dict.get(key, default)` מחזיר את הערך אם קיים, אחרת את ברירת המחדל.

**4.9**
```python
for port in range(20, 26):
    print(f"Port {port}: {check_port(port)}")
```

---

## חלק ד' — הכלים האמיתיים

**4.10** — הרצה:
```bash
chmod +x ping_sweep.sh
./ping_sweep.sh 192.168.1
```
מספר המכונות החיות תלוי במעבדה שלך — לפחות Kali וה-Gateway אמורים לענות.

**4.11**
```bash
# טרמינל 1:
python3 -m http.server 8000
# טרמינל 2:
python3 scanner.py     # הזן 127.0.0.1
```
תראה `[+] Port 8000 is OPEN` (ואולי פורטים נוספים שרצים).

**4.12** —
- `connect_ex` מחזיר **0** כשהפורט פתוח (החיבור הצליח).
- `settimeout(0.5)` מגביל את ההמתנה לחיבור — מונע היתקעות על פורט מסונן ומאיץ את הסריקה.
- `try/except KeyboardInterrupt` מאפשר לעצור בנקישת Ctrl+C בצורה נקייה במקום קריסה מכוערת.

---

## 🔴 אתגר מסכם — פתרון מלא

```python
#!/usr/bin/env python3
import socket, sys, time

services = {21:"FTP",22:"SSH",80:"HTTP",443:"HTTPS",3389:"RDP",8000:"HTTP-alt"}

target = input("[*] Enter target: ")
start_port = int(input("[*] Start port: "))
end_port   = int(input("[*] End port: "))

print(f"[*] Scanning {target} ports {start_port}-{end_port}")
open_count = 0
start_time = time.time()

try:
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((target, port)) == 0:
            name = services.get(port, "")
            print(f"[+] Port {port} is OPEN ({name})" if name else f"[+] Port {port} is OPEN")
            open_count += 1
        s.close()
except KeyboardInterrupt:
    print("\n[!] Stopped by user"); sys.exit()

elapsed = round(time.time() - start_time, 1)
print(f"[*] Scan complete. Found {open_count} open ports in {elapsed}s")
```

**בונוס Bash — שרשור Ping Sweep + Scanner:**
```bash
#!/bin/bash
# מוצא מכונות חיות, ואז מריץ את סורק הפייתון על כל אחת
network=$1
for ip in $(seq 1 254); do
    if ping -c 1 -W 1 "$network.$ip" > /dev/null 2>&1; then
        echo "[+] $network.$ip is UP — scanning..."
        echo "$network.$ip" | python3 scanner.py
    fi
done
```

> עברת? מצוין — יש לך עכשיו בסיס סקריפטינג אמיתי. המשך ל[מודול 5](../05-recon/).

</div>
