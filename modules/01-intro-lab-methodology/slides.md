# מבוא, מעבדה ומתודולוגיה
## מודול 1 — האקינג אתי מהיסוד

- מהו האקינג אתי + CIA Triad
- סוגי האקרים וסוגי בדיקות
- טרמינולוגיה ומתודולוגיית 5 השלבים
- הקמת מעבדה + Kali Linux

## מהו האקינג אתי?

- בדיקה **מורשית** למציאת חולשות לפני התוקף
- אותם כלים של התוקף — אך בהרשאה ולמטרת הגנה
- ההבדל: **הרשאה** + **כוונה**, לא הכלים
- ⚠️ ללא אישור בכתב = עבירה פלילית

## CIA Triad — שלושת עמודי התווך

- **Confidentiality** (סודיות) — רק מורשים רואים
- **Integrity** (שלמות) — המידע לא שונה
- **Availability** (זמינות) — המערכת זמינה
- כל ממצא מסווג לפי העיקרון שנפגע

## סוגי האקרים (Threat Actors)

- **White Hat** — אתי, בהרשאה (זה אנחנו)
- **Black Hat** — זדוני, ללא הרשאה
- **Grey Hat** — ללא הרשאה, ללא זדון
- **Script Kiddie · Hacktivist · APT · Insider**

## סוגי בדיקות חדירה

- **Black Box** — מידע מינימלי (תוקף חיצוני)
- **White Box** — גישה מלאה (קוד, פרטים)
- **Grey Box** — מידע חלקי (הנפוץ ביותר)
- Engagements: External · Internal · Web · Wireless · Social

## טרמינולוגיה — הנוסחה

- **Vulnerability** — הפגם (מנעול פגום)
- **Exploit** — ניצול הפגם (שיטת הפריצה)
- **Payload** — מה שרץ אחרי (הפעולה בפנים)
- `Vulnerability + Exploit + Payload = גישה`

## חמשת שלבי ההאקינג האתי

- **1. Reconnaissance** — איסוף מידע (פסיבי/אקטיבי)
- **2. Scanning & Enumeration** — פורטים ושירותים
- **3. Gaining Access** — ניצול חולשה
- **4. Maintaining Access** — שמירת גישה
- **5. Covering Tracks** — טשטוש עקבות

## היבטים משפטיים — לפני כל בדיקה

- **Scope** — מה מותר לתקוף
- **RoE** — כללי ההתקשרות
- **NDA** — הסכם סודיות
- **מכתב הרשאה** — הוכחת חוקיות

## הקמת המעבדה

- **Hypervisor** — VMware / VirtualBox (חינמי)
- **תוקף** — Kali Linux · **מטרות** — Metasploitable, Kioptrix
- רשת: **NAT / Host-Only** (לא Bridged!) 🔒
- **Snapshot** נקי מיד אחרי התקנה

## Kali Linux — סקירה

- הפצת Debian לבדיקות חדירה, 600+ כלים
- עדכון: `sudo apt update && sudo apt full-upgrade -y`
- **Terminal** = סביבת העבודה המרכזית
- wordlists ב-`/usr/share/wordlists` (rockyou)

## קטגוריות הכלים

- Information Gathering — nmap
- Vulnerability Analysis — nikto, Nessus
- Web — Burp Suite · Passwords — hydra
- Exploitation — Metasploit
- Sniffing — Wireshark · Post-Exp — mimikatz

## סיכום מודול 1

- האקינג אתי = בדיקה מורשית המגנה על ה-CIA
- מכירים סוגי האקרים, בדיקות וטרמינולוגיה
- 5 השלבים = הלב של הקורס
- מעבדה מבודדת + Kali מוכנים
- **תרגילים** → `missions.md` · **פתרונות** → `solutions.md`
