<div dir="rtl">

# ✅ פתרונות מלאים — מודול 1

> נסה לפתור לבד ב-[`missions.md`](missions.md) לפני שתקרא כאן. הפתרונות מפורטים צעד-אחר-צעד.

---

## חלק א' — שאלות ידע

**פתרון 1.1 — CIA Triad**
- **Confidentiality (סודיות):** רק מורשים רואים מידע. *פגיעה:* דלף מסד נתונים של סיסמאות.
- **Integrity (שלמות):** המידע אינו משתנה ללא הרשאה. *פגיעה:* שינוי סכום בהעברה בנקאית.
- **Availability (זמינות):** המערכת זמינה. *פגיעה:* מתקפת DoS שמפילה את השרת.

**פתרון 1.2 — White vs Grey Hat**
White Hat פועל **בהרשאה מלאה** ובחוזה. Grey Hat פועל **ללא הרשאה** אך לרוב ללא כוונת זדון (למשל מוצא חולשה במערכת של אחר ומדווח עליה) — אך עצם הפעולה ללא רשות היא **בלתי חוקית**.

**פתרון 1.3 — Vulnerability / Exploit / Payload**
- **Vulnerability** = הפגם. *דלת עם מנעול פגום.*
- **Exploit** = ניצול הפגם. *שיטת פריצת המנעול.*
- **Payload** = מה שקורה אחרי. *מה שאתה עושה בפנים — גונב/מצלם.*
נוסחה: `Vulnerability + Exploit + Payload = גישה`.

**פתרון 1.4 — חמשת השלבים (בסדר)**
1. Reconnaissance (איסוף מידע)
2. Scanning & Enumeration (סריקה ומיפוי)
3. Gaining Access (השגת גישה)
4. Maintaining Access (שמירת גישה)
5. Covering Tracks (טשטוש עקבות)

**פתרון 1.5 — שיוך פעולות לשלבים**
- (א) LinkedIn → **Reconnaissance** (פסיבי)
- (ב) `nmap` → **Scanning & Enumeration**
- (ג) מחיקת לוגים → **Covering Tracks**
- (ד) הוספת משתמש לחזרה → **Maintaining Access**
- (ה) Exploit ב-Metasploit → **Gaining Access**

---

## חלק ב' — הקמת הסביבה

**פתרון 2.1 — התקנה**
עקוב אחר סעיף 1.7 ב-[README](README.md#17-הקמת-המעבדה-lab-setup). לאחר `Play Virtual Machine`, התחבר עם `kali`/`kali`. פתח Terminal מסרגל הכלים או בקיצור `Ctrl+Alt+T`.

**פתרון 2.2 — עדכון**
```bash
sudo apt update && sudo apt full-upgrade -y
```
`update` מרענן את רשימת החבילות; `full-upgrade` מתקין את הגרסאות החדשות. הזן את הסיסמה `kali` כשתתבקש.

**פתרון 2.3 — זיהוי IP**
```bash
ip a
```
חפש את השורה `inet` תחת המתאם (למשל `eth0`), למשל:
```
inet 192.168.152.130/24
```
- `192.168.x.x` → שייך לטווח הפרטי **192.168.0.0/16**.
- (אם קיבלת `10.x.x.x` → טווח **10.0.0.0/8**; אם `172.16–31.x.x` → **172.16.0.0/12**.)

**פתרון 2.4 — Snapshot**
`VM → Snapshot → Take Snapshot`, שם: `Kali-clean-install`.
**למה חשוב:** אם תקיפה/עדכון ישברו את המערכת, אפשר לחזור למצב תקין בשנייה במקום להתקין מחדש.

---

## חלק ג' — היכרות עם Kali

**פתרון 3.1 — כלים לפי קטגוריה**
דוגמאות תקינות: Information Gathering → `nmap`; Password Attacks → `hydra` / `john`; Exploitation Tools → `metasploit`. (כל כלי מהקטגוריה נכון.)

**פתרון 3.2 — rockyou.txt**
```bash
ls -lh /usr/share/wordlists/
# אם דחוס:
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
wc -l /usr/share/wordlists/rockyou.txt
```
התוצאה: **14,344,392** סיסמאות (בגרסה הסטנדרטית). זהו ה-wordlist המפורסם ביותר לתקיפת סיסמאות.

**פתרון 3.3 — קטגוריה → שלב**
- Information Gathering → שלב 1–2 (Recon / Scanning)
- Exploitation Tools → שלב 3 (Gaining Access)
- Post Exploitation → שלב 4 (Maintaining Access) ולאחר-פריצה

---

## חלק ד' — חשיבה מתודולוגית

**פתרון 4.1 — תרחיש Acme**
- (א) **Black Box** — קיבלת מידע מינימלי בלבד (רק דומיין).
- (ב) פרופיל: **תוקף חיצוני ללא פרטי גישה**.
- (ג) פעולה ראשונה: **איסוף מידע פסיבי** (WHOIS, תת-דומיינים, OSINT) — שלב 1, Reconnaissance. לא קופצים ישר לסריקה.

**פתרון 4.2 — סוגי Engagement**
- בדיקת עובדים בפישינג → **Social Engineering**.
- בדיקת שרת web חיצוני → **External Network / Web Application**.

**פתרון 4.3 — שרת מחוץ ל-Scope**
**אסור** לתקוף אותו — הוא מחוץ ל-Scope, ותקיפתו אינה מורשית (ועלולה להיות עבירה פלילית / הפרת חוזה). **מותר ומומלץ** לתעד את הממצא ולדווח ללקוח שהנכס קיים ונראה פגיע, ולהמליץ להוסיפו ל-Scope בבדיקה נפרדת.

---

## 🔴 אתגר מסכם — קווים מנחים לפתרון

מסמך מלא ייכלול:
1. **מעבדה:** צילומי מסך של Kali + `ip a` (IP פרטי מסומן) + `uname -a` + Snapshot.
2. **טבלת מתודולוגיה:** למשל —

| שלב | מטרה | כלי | דוגמה |
|-----|------|-----|-------|
| Recon | איסוף מידע | hunter.io | מציאת מיילים |
| Scanning | מיפוי שירותים | nmap | `nmap -sV target` |
| Gaining Access | ניצול | Metasploit | הפעלת exploit |
| Maintaining | שמירת גישה | ssh-key | הוספת מפתח |
| Covering Tracks | ניקוי | — | מחיקת לוגים |

3. **תוכנית Black Box ל-acme.com:** שורה לכל שלב (Recon פסיבי → סריקת nmap → ניצול חולשה → שתילת גישה → ניקוי + דוח).
4. **אתיקה:** המעבדה מבודדת (NAT/Host-Only) כדי לא לפגוע ברשת אמיתית; מסמכים נדרשים: Scope, RoE, NDA, מכתב הרשאה.

> אם כיסית את כל אלה — עברת את המודול בהצלחה. המשך ל[מודול 2](../02-linux-fundamentals/).

</div>
