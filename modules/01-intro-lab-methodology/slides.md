# מבוא, מעבדה ו-Kali Linux
## מודול 1 — האקינג אתי מהיסוד

- מהו האקינג אתי (Ethical Hacking)?
- חמשת שלבי התקיפה (Five Stages)
- הקמת מעבדה וירטואלית (Lab)
- היכרות עם Kali Linux

## מהו האקינג אתי?

- בדיקה **מורשית** של מערכת למציאת חולשות (Vulnerabilities)
- אותם כלים של התוקף — אך בהרשאה ולמטרת הגנה
- ההבדל: **הרשאה** + **כוונה**, לא הכלים
- ⚠️ ללא אישור בכתב = עבירה פלילית

## חמשת שלבי ההאקינג האתי

- **1. איסוף מידע (Reconnaissance)** — פסיבי ואקטיבי
- **2. סריקה ומיפוי (Scanning & Enumeration)** — פורטים ושירותים
- **3. השגת גישה (Exploitation)** — ניצול חולשה
- **4. שמירת גישה (Maintaining Access)**
- **5. טשטוש עקבות (Covering Tracks)**

## הקמת המעבדה (Lab)

- **Hypervisor** — VMware Player / VirtualBox (חינמי)
- **מכונת תוקף** — Kali Linux
- **מכונות מטרה** — Kioptrix, Metasploitable, TryHackMe
- 🔒 רשת מבודדת: Host-Only / NAT

## התקנת Kali ב-VMware

- הורדת גרסת ה-VM מ-**kali.org**
- התקנת VMware Workstation Player
- Open ← קובץ ה-`.vmx`
- הגדרות: 2GB RAM לפחות, 2 ליבות
- התחברות: `kali` / `kali`

## Kali Linux — סקירה

- הפצת לינוקס (Debian) לבדיקות חדירה
- 300+ כלי אבטחה מותקנים מראש
- **Terminal** = סביבת העבודה המרכזית
- כלים מסודרים לפי שלבי התקיפה

## קטגוריות הכלים

- Information Gathering — nmap, Maltego
- Vulnerability Analysis — Nessus
- Web Application — Burp Suite
- Password Attacks — Hydra, John
- Exploitation — Metasploit
- Sniffing & Spoofing — Wireshark

## מיומנויות נדרשות

- **Linux** — שורת פקודה
- **רשתות (Networking)** — OSI, TCP/UDP (מודול 3)
- **סקריפטינג** — Bash, Python (מודול 4)
- הקורס מלמד הכל בהדרגה

## סיכום מודול 1

- האקינג אתי = בדיקה מורשית לפני התוקף
- חמשת השלבים הם הלב של הקורס
- מעבדה מבודדת = תרגול בטוח
- Kali = ארגז הכלים המרכזי
- **תרגול:** הקם את המעבדה ופתח TryHackMe
