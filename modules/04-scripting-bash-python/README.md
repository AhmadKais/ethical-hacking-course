<div dir="rtl">

> 📘 **הכול בגלילה אחת:** [**כל החומר של המודול בקובץ אחד**](כל-החומר.md) — חומר לימוד, תרגילים, תרגול ופתרונות, ברצף.

# מודול 4 — סקריפטינג: Bash ו-Python (Scripting for Hackers)

> **מטרות המודול:** לרכוש את יכולת האוטומציה הנדרשת בבדיקות חדירה — כתיבת סקריפטים ב-**Bash** (שפת ה-Terminal) וב-**Python** (שפת הכלים). נגיע לשני כלים אמיתיים: **Ping Sweep** ב-Bash ו-**Port Scanner** ב-Python.
>
> **קבצים:** `README.md` · [`missions.md`](missions.md) · [`solutions.md`](solutions.md) · [`practice.md`](practice.md) · [`slides.md`](slides.md).
>
> **מבוסס על שיעורי המקור** #10 (Bash Scripting) ו-#11–#29 (Python → Port Scanner).

> **למה סקריפטינג?** האקר טוב לא מקליד את אותה פקודה 254 פעמים — הוא כותב לולאה. **Bash** מעולה לאוטומציה מהירה של פקודות מערכת; **Python** היא השפה שבה כתובים רוב כלי האבטחה וה-Exploits. אין צורך להיות מתכנת — מספיק לקרוא, לשנות ולכתוב סקריפטים פשוטים.

---

## תוכן העניינים
**חלק א' — Bash**
1. [מהו סקריפט Bash](#41-מהו-סקריפט-bash)
2. [משתנים וקלט](#42-משתנים-וקלט-משתמש)
3. [תנאים](#43-תנאים-ב-bash)
4. [לולאות](#44-לולאות-ב-bash)
5. [פרויקט: Ping Sweep](#45-פרויקט-bash--ping-sweep)

**חלק ב' — Python**
6. [יסודות וטיפוסים](#46-python--יסודות-וטיפוסים)
7. [מבני נתונים](#47-מבני-נתונים)
8. [תנאים ולולאות](#48-תנאים-ולולאות)
9. [פונקציות ומודולים](#49-פונקציות-ומודולים)
10. [פרויקט: Port Scanner](#410-פרויקט-python--port-scanner)

---

# חלק א' — Bash Scripting

## 4.1 מהו סקריפט Bash?

**סקריפט Bash** הוא קובץ טקסט עם רצף פקודות Terminal, שרץ בזו אחר זו. כך הופכים סדרת פקודות ידניות לכלי אוטומטי.

```bash
#!/bin/bash
# השורה הראשונה — "Shebang" — אומרת למערכת להריץ עם bash
echo "Hello, Hacker!"
```

**הרצה:**
```bash
chmod +x script.sh   # הפיכה לניתן-הרצה (זוכרים ממודול 2?)
./script.sh          # הרצה
```

> 💡 ה-`#!/bin/bash` הוא **Shebang** — חובה בתחילת כל סקריפט. שורות שמתחילות ב-`#` (מלבד ה-Shebang) הן הערות.

---

## 4.2 משתנים וקלט משתמש

```bash
#!/bin/bash
name="Kali"                 # הצבה — ללא רווחים סביב ה-=
echo "Target is $name"      # שימוש — עם $

read -p "Enter an IP: " ip  # קלט מהמשתמש
echo "You entered $ip"
```

- **ללא רווחים** סביב ה-`=` (זו טעות נפוצה: `name = "x"` שגוי).
- `$name` — קורא את הערך. `${name}` — צורה בטוחה יותר בתוך מחרוזת.
- **ארגומנטים משורת הפקודה:** `$1`, `$2` = הארגומנט הראשון/שני; `$#` = מספרם.

```bash
#!/bin/bash
echo "First argument: $1"   # ./script.sh 10.0.0.5 → 10.0.0.5
```

---

## 4.3 תנאים ב-Bash

```bash
#!/bin/bash
read -p "Enter port: " port
if [ "$port" -eq 80 ]; then
    echo "HTTP"
elif [ "$port" -eq 443 ]; then
    echo "HTTPS"
else
    echo "Unknown"
fi
```

אופרטורים נפוצים (בתוך `[ ]`):
| מספרי | מחרוזות | קבצים |
|-------|---------|-------|
| `-eq` שווה | `=` שווה | `-f` קובץ קיים |
| `-ne` שונה | `!=` שונה | `-d` תיקייה קיימת |
| `-gt` גדול | `-z` ריק | `-x` ניתן-הרצה |
| `-lt` קטן | | |

---

## 4.4 לולאות ב-Bash

```bash
# לולאת for על רשימה
for host in 10.0.0.1 10.0.0.2 10.0.0.3; do
    echo "Pinging $host"
done

# לולאה על טווח
for i in $(seq 1 10); do
    echo "Number $i"
done

# לולאת while
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))     # חשבון ב-Bash
done
```

---

## 4.5 פרויקט Bash — Ping Sweep

כלי אמיתי: סורק תת-רשת ומזהה אילו מכונות **חיות** (Host Discovery) — בדיוק מה שעושים בתחילת שלב הסריקה.

```bash
#!/bin/bash
# ping_sweep.sh — מוצא מכונות חיות בתת-רשת /24
# שימוש: ./ping_sweep.sh 192.168.1

if [ -z "$1" ]; then
    echo "Usage: $0 <network>   e.g. $0 192.168.1"
    exit 1
fi

network=$1
echo "[*] Scanning $network.0/24 ..."

for ip in $(seq 1 254); do
    # -c 1 = חבילה אחת, -W 1 = timeout שנייה
    ping -c 1 -W 1 "$network.$ip" > /dev/null 2>&1 && \
        echo "[+] $network.$ip is UP" &
done
wait
echo "[*] Sweep complete."
```

**איך זה עובד:**
1. בודק שהתקבל ארגומנט רשת (`$1`), אחרת מדפיס שימוש ויוצא.
2. לולאה על 1–254 (כל המארחים ב-`/24`).
3. `ping -c 1` לכל כתובת; אם הצליח (`&&`) — מדפיס שהמכונה חיה.
4. ה-`&` מריץ במקביל (מהיר יותר); `wait` ממתין לסיום כולם.

> ⚠️ הרץ רק על תת-הרשת של המעבדה שלך.

---

# חלק ב' — Python

## 4.6 Python — יסודות וטיפוסים

```python
target = "192.168.1.10"   # String (מחרוזת)
port = 80                  # Integer (מספר שלם)
timeout = 1.5              # Float (עשרוני)
is_open = True             # Boolean
```

- **String** — טקסט במרכאות · **Integer** — מספר שלם · **Float** — עשרוני · **Boolean** — `True`/`False`.

### מחרוזות — פעולות שימושיות לניתוח פלט
```python
banner = "Apache/2.4.49"
print(banner.upper())          # APACHE/2.4.49
print(banner.split("/"))       # ['Apache', '2.4.49']
print("2.4.49" in banner)      # True
```
**f-strings** — שילוב משתנים בטקסט:
```python
ip, port = "10.0.0.5", 22
print(f"Scanning {ip} on port {port}")   # Scanning 10.0.0.5 on port 22
```

---

## 4.7 מבני נתונים

```python
ports = [21, 22, 80, 443]              # List — מסודר, ניתן לשינוי
ports.append(8080)                      # הוספה
print(ports[0], len(ports))             # 21  5

services = {80: "HTTP", 443: "HTTPS"}   # Dictionary — מפתח:ערך
print(services[80])                     # HTTP

address = ("10.0.0.1", 80)              # Tuple — קבוע
```

| מבנה | תחביר | ניתן לשינוי? | שימוש |
|------|-------|-------------|-------|
| List | `[ ]` | כן | רשימת פורטים/יעדים |
| Dictionary | `{k: v}` | כן | מיפוי פורט←שירות |
| Tuple | `( )` | לא | זוג IP+port קבוע |

---

## 4.8 תנאים ולולאות

```python
port = 22
if port == 22:
    print("SSH")
elif port == 80:
    print("HTTP")
else:
    print("Unknown")

# לולאה על טווח
for port in range(1, 101):       # 1 עד 100
    print(port)

# לולאה על רשימה
for p in [21, 22, 80]:
    print(f"Checking {p}")
```
אופרטורים: `==` `!=` `<` `>` `and` `or` `not`.

---

## 4.9 פונקציות ומודולים

```python
def scan_port(ip, port):          # הגדרת פונקציה
    print(f"Scanning {ip}:{port}")
    return True

scan_port("10.0.0.1", 80)         # קריאה

import socket   # תקשורת רשת — לב הסורק
import sys       # ארגומנטים ומערכת
```
- **socket** — יצירת חיבורי רשת. **sys** — אינטראקציה עם המערכת. התקנת ספריות: `pip install <שם>`.

---

## 4.10 פרויקט Python — Port Scanner

הכלי המרכזי של המודול — מיישם את **TCP** ואת **לחיצת היד** ממודול 3:

```python
#!/usr/bin/env python3
import socket
import sys

target = input("[*] Enter target IP: ")   # קלט מהמשתמש
print(f"[*] Scanning {target}")

try:
    for port in range(1, 1025):            # פורטים 1–1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP over IPv4
        s.settimeout(0.5)                  # אל תחכה יותר מחצי שנייה
        result = s.connect_ex((target, port))  # מחזיר 0 אם פתוח
        if result == 0:
            print(f"[+] Port {port} is OPEN")
        s.close()
except KeyboardInterrupt:
    print("\n[!] Stopped by user")
    sys.exit()
except socket.gaierror:
    print("[!] Hostname could not be resolved")
    sys.exit()
```

**שורה אחר שורה:**
1. `socket.socket(AF_INET, SOCK_STREAM)` — יוצר חיבור TCP מעל IPv4.
2. `settimeout(0.5)` — מונע היתקעות על פורט חסום.
3. `connect_ex((target, port))` — מנסה את לחיצת היד; מחזיר `0` אם הפורט **פתוח**.
4. הלולאה עוברת על 1–1024; `try/except` מטפל ב-Ctrl+C ובשגיאות DNS.

> ⚠️ הרץ **אך ורק** על `127.0.0.1` או מכונות המעבדה שלך.

---

## Bash מול Python — מתי מה?

| | **Bash** | **Python** |
|---|---|---|
| חוזק | אוטומציה של פקודות מערכת | לוגיקה מורכבת, רשת, פרסינג |
| מהירות כתיבה | מהיר לדברים קצרים | טוב לכלים גדולים |
| דוגמה | Ping Sweep, שרשור כלים | Port Scanner, Exploits |
| נפוץ ב | סקריפטי שרת, one-liners | כלי אבטחה, Metasploit modules |

> 💡 בפועל משלבים: Bash "מדביק" כלים קיימים במהירות, Python בונה כלים חדשים.

---

## סיכום המודול

- **Bash:** Shebang, משתנים, `read`, תנאים (`[ ]`), לולאות (`for`/`while`) — ובנינו **Ping Sweep**.
- **Python:** טיפוסים, מבני נתונים (List/Dict/Tuple), תנאים, לולאות, פונקציות, מודולים (`socket`) — ובנינו **Port Scanner**.
- **Bash** לאוטומציית מערכת מהירה; **Python** לכלים ולוגיקה.

### מה הלאה?
➡️ [**תרגילים — `missions.md`**](missions.md) · [**פתרונות — `solutions.md`**](solutions.md) · [**תרגול ותרחישים — `practice.md`**](practice.md)
➡️ [**מודול 5 — איסוף מידע**](../05-recon/)

[⬅️ חזרה למפת הקורס](../../README.md)

</div>
