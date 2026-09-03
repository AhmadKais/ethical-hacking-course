<div dir="rtl">

# 🎯 תרגילים — מודול 13: Active Directory

> ⚠️ **רק על מעבדת AD חוקית** — מומלץ **[TryHackMe](https://tryhackme.com)** (*Attacktive Directory*, *Attacking Kerberos*), או מעבדה מקומית (GOAD). לעולם לא על דומיין ארגוני ללא הרשאה בכתב. פתרונות ב-[**`solutions.md`**](solutions.md).

מקרא רמות: 🟢 קל · 🟡 בינוני · 🟠 מתקדם · 🔴 אתגר

---

## חלק א' — יסודות ו-Enumeration (🟢🟡)

**13.1** — הסבר במילים שלך: מהו Domain Controller, ולמה השתלטות עליו = שליטה בכל הארגון?

**13.2** — תאר בקצרה את זרימת אימות **Kerberos** (TGT → TGS → שירות).

**13.3** 🟡 — בצע **Enumeration** על DC: מצא את שם הדומיין, גרסת השרת, ורשימת משתמשים (crackmapexec / enum4linux-ng). רשום את הפקודות.

---

## חלק ב' — תקיפות Kerberos ו-LLMNR (🟠)

**13.4** 🟠 — הפעל **Responder** ולכוד NTLMv2 hash של משתמש (סימולציה: גש לשם שגוי ממכונת לקוח). פצח אותו עם hashcat (`-m 5600`).

**13.5** 🟠 — בצע **Kerberoasting**: בקש את ה-TGS של חשבונות השירות (`GetUserSPNs.py -request`), ופצח אותם (`-m 13100`).

**13.6** 🟠 — בצע **AS-REP Roasting**: מצא חשבונות ללא preauth (`GetNPUsers.py`) ופצח (`-m 18200`). מה מיוחד בתקיפה זו לעומת Kerberoasting?

---

## חלק ג' — תנועה רוחבית ו-BloodHound (🟠)

**13.7** 🟠 — עם NTLM hash של Local Admin, בצע **Pass-the-Hash** למכונה נוספת (crackmapexec / evil-winrm / psexec). הסבר למה לא צריך לפצח את הסיסמה.

**13.8** 🟠 — הרץ **BloodHound** (bloodhound-python), טען את הנתונים, והרץ את השאילתה *"Shortest Path to Domain Admins"*. תאר את הנתיב שמצאת.

**13.9** 🟠 — הרץ **secretsdump.py** על מכונה שנפרצה. אילו סוגי אישורים שלפת (SAM/LSA/cached)?

---

## 🔴 אתגר מסכם — "מ-Zero ל-Domain Admin"

בחדר AD מלא (TryHackMe *Attacktive Directory* או מעבדת GOAD):

1. התחל **ללא אישורים** (או עם משתמש הכי מוגבל).
2. השג אישורים ראשונים (LLMNR / AS-REP / brute).
3. הרחב עם **Kerberoasting** ו-**BloodHound** — מצא נתיב ל-Domain Admin.
4. בצע **תנועה רוחבית** (Pass-the-Hash) עד לחשבון בעל הרשאות גבוהות.
5. סיים ב-**DCSync** — שלוף את ה-hash של Administrator, והוכח **Domain Admin**.
6. **תעד** את כל השרשרת: כל שלב, הכלי, הפקודה, והתוצאה.

> 📤 שרשרת "Zero to Domain Admin" היא בדיוק בחינת ה-AD של PNPT/OSCP. תעד אותה במלואה — זהו נכס מרכזי לתיק העבודות.

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
