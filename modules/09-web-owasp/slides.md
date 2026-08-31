# אבטחת אפליקציות Web
## מודול 9 — OWASP Top 10

- כיצד עובדות חולשות Web
- OWASP Top 10
- SQLi · XSS · Command Injection
- Access Control · File Upload · הגנה

## איך עובדת אפליקציית Web?

- דפדפן → בקשת HTTP → שרת → DB → תשובה
- **השורש:** אמון בקלט משתמש
- קלט לא מסונן = הזרקת קוד/פקודות
- הכלי המרכזי: **Burp Suite**

## OWASP Top 10

- **A01 Broken Access Control** (הנפוץ)
- **A03 Injection** — SQLi, Command, XSS
- A05 Misconfiguration · A07 Auth
- A06 Vulnerable Components · **A10 SSRF**

## סביבת התרגול

- **DVWA** — PHP פגיע, רמות קושי
- **OWASP Juice Shop** — 100+ אתגרים
- `docker run -d -p 3000:3000 bkimminich/juice-shop`
- PortSwigger Web Security Academy (חינמי)

## SQL Injection

- קלט נכנס לשאילתת SQL
- `' OR '1'='1' -- ` → עוקף התחברות
- Union-based (פלט ישיר) מול Blind
- **sqlmap** — `-u URL --dbs / --dump`

## Cross-Site Scripting (XSS)

- הזרקת JavaScript לדפדפן קורבן
- **Reflected · Stored · DOM**
- `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>`
- גניבת Cookie → חטיפת Session

## Command Injection

- קלט נכנס לפקודת מערכת
- `127.0.0.1; whoami`
- מפרידים: `;` `|` `&&` `` ` ``
- = **RCE** — מהחמורות ביותר

## Broken Access Control / IDOR

- A01 — הנפוץ ביותר
- **IDOR:** `account?id=1001` → `?id=1002`
- Forced Browsing ל-`/admin`
- שינוי `role=user` → `role=admin`

## File Upload ו-Inclusion

- **Upload:** Web Shell `<?php system($_GET['cmd']);?>` → RCE
- עקיפה: `shell.php.jpg`, Content-Type
- **LFI:** `?file=../../etc/passwd`
- **RFI:** קובץ מרוחק → RCE

## כלים

- **Burp Suite** — Proxy, Repeater, Intruder
- **sqlmap** — אוטומציית SQLi
- **ffuf / gobuster** — נתיבים
- **nikto** — חולשות נפוצות

## הגנה

- **Prepared Statements** → מונע SQLi
- **Output Encoding** → מונע XSS
- **בקרת גישה בשרת** (לא רק ב-UI)
- CSP · HTTPS · CSRF Tokens · MFA

## סיכום מודול 9

- חולשות Web = אמון בקלט
- Injection (SQLi/XSS/Command), IDOR, Upload
- Burp + sqlmap = הכלים
- המיומנות הכי מבוקשת בשוק
- **תרגול** → `practice.md` · **פתרונות** → `solutions.md`
