# סקריפטינג: Bash ו-Python
## מודול 4 — Scripting for Hackers

- למה סקריפטינג? אוטומציה
- Bash — שפת ה-Terminal
- Python — שפת הכלים
- פרויקטים: Ping Sweep + Port Scanner

## למה סקריפטינג?

- האקר לא מקליד פקודה 254 פעם — כותב לולאה
- **Bash** — אוטומציה של פקודות מערכת
- **Python** — כלים, Exploits, לוגיקה
- לא צריך להיות מתכנת

## Bash — מבנה בסיסי

- `#!/bin/bash` — Shebang (חובה)
- `name="Kali"` — משתנה (ללא רווחים!)
- `echo "$name"` — שימוש
- הרצה: `chmod +x` ואז `./script.sh`

## Bash — קלט, תנאים, לולאות

- `read -p "IP: " ip` — קלט
- `$1 $2` — ארגומנטים
- `if [ "$port" -eq 80 ]; then ... fi`
- `for i in $(seq 1 254); do ... done`

## פרויקט Bash — Ping Sweep

- מוצא מכונות **חיות** בתת-רשת (Host Discovery)
- לולאה על 1–254 + `ping -c 1`
- `&` להרצה מקבילה · `wait` לסיום
- בסיס לשלב הסריקה

## Python — טיפוסים

- **String** `"nmap"` · **Integer** `443`
- **Float** `2.5` · **Boolean** `True`
- f-strings: `f"Scan {ip}:{port}"`
- `banner.split("/")` — פרסינג פלט

## Python — מבני נתונים

- **List** `[ ]` — מסודר, משתנה
- **Dictionary** `{80: "HTTP"}` — מיפוי
- **Tuple** `( )` — קבוע
- `services.get(port, "Unknown")`

## Python — תנאים, לולאות, פונקציות

- `if / elif / else`
- `for port in range(1, 1025)`
- `def scan_port(ip, port):`
- `import socket, sys`

## פרויקט Python — Port Scanner

- `socket(AF_INET, SOCK_STREAM)` — TCP
- `settimeout(0.5)` — לא להיתקע
- `connect_ex()` == 0 → פורט פתוח
- `try/except` ל-Ctrl+C ולשגיאות DNS

## Bash מול Python — מתי מה?

- **Bash** — one-liners, שרשור כלים, מערכת
- **Python** — כלים גדולים, רשת, לוגיקה
- Bash "מדביק" · Python "בונה"
- ⚠️ להריץ רק על `127.0.0.1`/המעבדה

## סיכום מודול 4

- Bash: Shebang, משתנים, תנאים, לולאות → Ping Sweep
- Python: טיפוסים, מבנים, פונקציות → Port Scanner
- שני כלים אמיתיים ביד
- **תרגילים** → `missions.md` · **פתרונות** → `solutions.md`
