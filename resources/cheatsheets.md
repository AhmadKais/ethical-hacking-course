<div dir="rtl">

# 📋 דף פקודות מרוכז (Cheat Sheet)

אוסף הפקודות הנפוצות בקורס. יתעדכן ככל שיתווספו מודולים.

</div>

---

## Linux Basics
```bash
whoami                  # המשתמש הנוכחי
pwd                     # התיקייה הנוכחית
ls -la                  # קבצים כולל מוסתרים
ip a                    # כתובות רשת
uname -a                # פרטי מערכת + Kernel
sudo apt update && sudo apt full-upgrade -y   # עדכון המערכת
find / -perm -4000 2>/dev/null   # קבצי SUID (הסלמת הרשאות)
```

## Networking
```bash
ping -c 4 <ip>          # בדיקת קישוריות (ICMP)
traceroute <host>       # מסלול החבילה
ipcalc <ip>/<cidr>      # חישוב Subnet
cat /etc/resolv.conf    # שרת DNS
```

## Reconnaissance (מודול 4)
```bash
sublist3r -d <domain>              # גילוי תת-דומיינים
whatweb <url>                      # זיהוי טכנולוגיות אתר
# אופרטורי Google: site:  filetype:  inurl:  intitle:  intext:
```

## Scanning — Nmap (מודול 5)
```bash
nmap <ip>                          # סריקה בסיסית
nmap -sV <ip>                      # גילוי גרסאות שירותים
nmap -sC -sV <ip>                  # סקריפטים ברירת מחדל + גרסאות
nmap -p- <ip>                      # כל 65535 הפורטים
nmap -A <ip>                       # אגרסיבי (OS, גרסאות, סקריפטים)
nmap 192.168.1.0/24                # סריקת תת-רשת שלמה
```
> יורחב במלואו במודול 5.

## Exploitation — Metasploit (מודול 6)
```bash
msfconsole                         # הפעלת Metasploit
search <service>                   # חיפוש Exploit
use <module>                       # בחירת מודול
show options                       # הצגת פרמטרים
set RHOSTS <ip> ; run              # הגדרה והרצה
msfvenom -p <payload> LHOST=<ip> LPORT=<port> -f <format>   # יצירת Payload
```
> יורחב במלואו במודול 6.

## Password Attacks
```bash
hydra -l <user> -P <wordlist> <ip> ssh    # Brute Force ל-SSH
john --wordlist=<list> <hashfile>         # פיצוח Hashes
hashcat -m <mode> <hashfile> <wordlist>   # פיצוח מואץ
```

---

*הרץ כל פקודה רק על מכונות המעבדה שלך או יעדים מורשים.*

[⬅️ חזרה למפת הקורס](../README.md)
