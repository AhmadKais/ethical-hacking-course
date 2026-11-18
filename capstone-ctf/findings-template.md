<div dir="rtl">

# 📝 דוח בדיקת חדירה — ACME Corp (תבנית למילוי)

> מלא את התבנית אחרי שסיימת את התרגיל. זה התוצר שמעסיק רוצה לראות. סדר ממצאים מהחמור לקל. ראה מודול 16 להסבר על מבנה דוח ו-CVSS.

**לקוח:** ACME Corp · **בודק:** _________ · **תאריך:** _________ · **סוג:** Grey Box External→Internal

---

## 1. תקציר מנהלים (Executive Summary)
> 3–5 שורות בשפה עסקית (לא טכנית): מה נמצא, מה הסיכון, מה ההמלצה העיקרית. דוגמה: "הצלחנו להשתלט על סביבת ACME מקצה-לקצה, מגישה חיצונית ועד שליטה מלאה על הדומיין (Domain Admin), בניצול שרשרת של 6 חולשות..."

______________________________________________

## 2. היקף ומתודולוגיה
- **Scope:** 127.0.0.1:8080, :8081, :9090
- **מתודולוגיה:** Recon → Scanning → Exploitation → Post-Exploitation → Reporting (PTES).

## 3. סיכום הממצאים

| # | ממצא | חומרה | CVSS |
|:-:|------|:-----:|:----:|
| F-01 | Command Injection (RCE) בכלי ה-ping | 🔴 Critical | 9.8 |
| F-02 | SQL Injection — עקיפת אימות | 🔴 Critical | 9.1 |
| F-03 | NTLM חלש → Domain Admin | 🔴 Critical | 8.8 |
| F-04 | Writable cron → Privilege Escalation | 🟠 High | 7.8 |
| F-05 | סיסמאות חלשות / MD5 לא מומלח | 🟠 High | 7.5 |
| F-06 | חשיפת מידע ב-recon + Apache 2.4.49 מיושן | 🟡 Medium | 5.3 |

## 4. ממצאים מפורטים
> לכל ממצא: **תיאור · השפעה · הוכחת היתכנות (PoC — הפקודה המדויקת) · המלצת תיקון**.

### F-01 — Command Injection (RCE) · Critical · CVSS 9.8
- **תיאור:** הפרמטר `host` ב-`/tools/ping` מועבר ישירות ל-shell.
- **השפעה:** הרצת קוד שרירותי בשרת.
- **PoC:** `curl "127.0.0.1:8081/tools/ping?host=x;id"`
- **תיקון:** אל תעביר קלט ל-shell; השתמש ב-`subprocess` עם רשימת ארגומנטים ו-whitelist לכתובת IP.

### F-02 — SQL Injection · Critical · CVSS 9.1
- **תיאור / השפעה / PoC / תיקון:** ______ (תיקון: Prepared Statements / Parameterized Queries).

### F-03 — Domain Admin via NTLM · Critical
- ______ (תיקון: מדיניות סיסמאות חזקה, ניטור Kerberoasting, gMSA).

### F-04 — Writable Cron Privilege Escalation · High
- ______ (תיקון: הרשאות קבצים, אין קבצי cron שניתנים לכתיבה ע"י משתמשים).

### F-05 — Weak Passwords / Unsalted MD5 · High
- ______ (תיקון: bcrypt/argon2 עם salt, אכיפת מורכבות).

### F-06 — Information Disclosure / Outdated Apache · Medium
- ______ (תיקון: הסרת הערות וכותרות גרסה, עדכון Apache).

## 5. המלצות — סיכום מתועדף
1. תקן את ה-RCE וה-SQLi מיידית (Critical).
2. אכוף מדיניות סיסמאות + החלף MD5 ב-bcrypt.
3. תקן הרשאות קבצים (cron) ועדכן רכיבים מיושנים.

## 6. נספח — ציר זמן התקיפה
`Recon(8080) → SQLi(8081) → RCE → crack MD5 → pivot(9090) → writable cron → root → crack NTLM → Domain Admin`

---
*דוח זה נכתב למטרות תרגול בלבד, על סביבת מעבדה מבודדת.*

[⬅️ חזרה לכתב המינוי](README.md)

</div>
