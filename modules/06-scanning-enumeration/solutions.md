<div dir="rtl">

# ✅ פתרונות מלאים — מודול 6: סריקה ומיפוי

> נסה לבד ב-[`missions.md`](missions.md) קודם. (הפלט המדויק תלוי בגרסת Kioptrix שלך — הערכים כאן אופייניים ל-Kioptrix Level 1.)

---

## חלק א' — גילוי וסריקה בסיסית

**6.1**
```bash
nmap -sn 192.168.1.0/24     # התאם לתת-הרשת שלך
```
זהה את ה-IP שאינו Kali/Gateway — זהו Kioptrix.

**6.2**
```bash
nmap 192.168.1.10
```
פורטים אופייניים ב-Kioptrix 1: **22 (ssh), 80 (http), 111 (rpcbind), 139 (netbios), 443 (https)**.

**6.3**
```bash
nmap -sV -oN kioptrix_scan.txt 192.168.1.10
```
תוצאה אופיינית: `Apache httpd 1.3.20 ((Unix) mod_ssl/2.8.4 OpenSSL/0.9.6b)`, `OpenSSH 2.9p2`, `Samba`.

**6.4**
```bash
nmap -p- 192.168.1.10
```
לעיתים מתגלה פורט Samba גבוה נוסף שלא היה ב-1000 הנפוצים.

---

## חלק ב' — מנייה לפי שירות

**6.5**
```bash
whatweb http://192.168.1.10
nikto -h http://192.168.1.10
```
`nikto` יחשוף לרוב את גרסת mod_ssl הפגיעה ואת OpenSSL 0.9.6b (חולשה ידועה), וקבצים/הגדרות מיושנים.

**6.6**
```bash
gobuster dir -u http://192.168.1.10 -w /usr/share/wordlists/dirb/common.txt
```
תוצאות אופייניות: `/usage`, `/manual`, `/mrtg`, `/cgi-bin`.

**6.7**
```bash
enum4linux -a 192.168.1.10
```
חושף את גרסת ה-Samba (למשל **Samba 2.2.1a**) — גרסה זו פגיעה ל-Exploit ידוע (trans2open).

**6.8**
```bash
nmap -p 445 --script smb-vuln-ms17-010 192.168.1.10
```
ב-Kioptrix 1 (לינוקס ישן) לרוב **לא** פגיע ל-MS17-010 (זו חולשת Windows) — אך זהו תרגול חשוב לזהות מתי כן/לא. על מכונת Windows פגיעה, הסקריפט ידווח `VULNERABLE`.

---

## חלק ג' — חקר חולשות

**6.9**
```bash
searchsploit apache 1.3.20
searchsploit mod_ssl 2.8
```
ה-Exploit המפורסם: **OpenLuck / "OpenFuck" (mod_ssl 2.8.x)** — CVE-2002-0082. זהו וקטור הניצול הקלאסי של Kioptrix.

**6.10**
```bash
searchsploit samba 2.2
```
קיים Exploit ל-**Samba trans2open** (CVE-2003-0201) — וקטור חלופי להשגת גישה.

**6.11**
חפש `CVE-2002-0082` ב-nvd.nist.gov → ציון CVSS גבוה (Critical). זה מצדיק ניצול מיידי.

---

## 🔴 אתגר מסכם — דוח מנייה לדוגמה

```markdown
# דוח מנייה — Kioptrix Level 1
IP: 192.168.1.10 | OS: Linux (Kernel 2.4, Red Hat)

## פורטים
| פורט | שירות | גרסה | הערה |
|------|-------|------|------|
| 22   | ssh   | OpenSSH 2.9p2 | ישן |
| 80   | http  | Apache 1.3.20 + mod_ssl 2.8.4 | פגיע! |
| 139  | smb   | Samba 2.2.1a | פגיע (trans2open) |
| 443  | https | mod_ssl/OpenSSL 0.9.6b | CVE-2002-0082 |

## מנייה
- HTTP: gobuster מצא /usage,/manual; nikto חשף mod_ssl פגיע
- SMB: enum4linux → Samba 2.2.1a, שיתופים גלויים

## חולשות
- CVE-2002-0082 (mod_ssl "OpenFuck") — CVSS גבוה
- CVE-2003-0201 (Samba trans2open) — וקטור חלופי

## מסקנה — וקטור תקיפה
הווקטור המבטיח: ניצול mod_ssl (CVE-2002-0082) דרך פורט 443 → RCE כ-root.
חלופה: Samba trans2open. שני המסלולים מובילים לשליטה מלאה.
```

> עברת? יש לך וקטור תקיפה ברור. במודול 7 ננצל אותו בפועל. המשך ל[מודול 7](../07-exploitation/).

</div>
