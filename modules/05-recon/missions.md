<div dir="rtl">

# 🎯 משימות מעשיות — מודול 5: איסוף מידע (Reconnaissance)

> ⚠️ **קרא לפני שתתחיל:** בצע איסוף מידע **רק** על יעד חוקי — תוכנית Bug Bounty פתוחה (עם Scope מוגדר), מכונת תרגול, או דומיין שבבעלותך. איסוף פסיבי על דומיין ציבורי מותר; **אל** תבצע פעולות אקטיביות (סריקה, ניסיונות התחברות) ללא הרשאה. ראה [חומר הלימוד](README.md).

מקרא רמות: 🟢 בסיסי · 🟡 בינוני · 🔴 אתגר

**יעד לדוגמה במשימות:** נשתמש בדומיין ציבורי לתרגול פסיבי בלבד. אם אתה בתוכנית Bug Bounty — השתמש ביעד שבתוך ה-Scope.

---

## משימה 1 — קריאת Scope 🟢

**מטרה:** להרגיל לקרוא גבולות הרשאה לפני כל פעולה.

**צעדים:**
1. היכנס ל-[HackerOne Directory](https://hackerone.com/directory/programs) או [Bugcrowd](https://bugcrowd.com/programs).
2. בחר תוכנית ציבורית אחת ופתח את עמוד ה-**Scope**.
3. רשום: 2 נכסים **In-Scope** ו-2 נכסים **Out-of-Scope**.

**✅ קריטריון הצלחה:** הבחנת נכון בין נכסים מותרים לאסורים.

**❓ שאלה:** מה עלול לקרות אם תתקוף נכס Out-of-Scope?

---

## משימה 2 — זיהוי טכנולוגיות אתר 🟢

**מטרה:** למפות את ה-Tech Stack של יעד (פסיבי).

**צעדים:**
1. פתח את [builtwith.com](https://builtwith.com) והזן דומיין יעד.
2. התקן את התוסף [Wappalyzer](https://www.wappalyzer.com) בדפדפן ובקר באתר היעד.
3. רשום: שרת ה-Web, שפת התכנות/Framework, ו-CMS (אם קיים).

**✅ קריטריון הצלחה:** זיהית לפחות 3 טכנולוגיות ואת גרסת שרת ה-Web (אם נחשפת).

**❓ שאלה:** מדוע גרסת שרת ישנה היא ממצא חשוב?

---

## משימה 3 — Google Dorking 🟡

**מטרה:** לתרגל אופרטורי חיפוש ממוקדים.

הרץ בגוגל את השאילתות הבאות (החלף `TARGET.com` ביעד):
```
site:TARGET.com
site:TARGET.com filetype:pdf
site:TARGET.com inurl:login
site:TARGET.com intitle:"index of"
```

**✅ קריטריון הצלחה:** לפחות שאילתה אחת החזירה תוצאה מעניינת (קובץ, עמוד ניהול, ספריה חשופה).

**מיני-אתגר:** גלוש ל-[Google Hacking Database](https://www.exploit-db.com/google-hacking-database) ומצא Dork אחד שלא הכרת.

---

## משימה 4 — גילוי תת-דומיינים 🟡

**מטרה:** להרחיב את משטח התקיפה עם Sublist3r.

**צעדים (ב-Kali):**
```bash
sudo apt install sublist3r -y
sublist3r -d TARGET.com
```
אם ההתקנה נכשלת — התקן ידנית:
```bash
git clone https://github.com/aboul3la/Sublist3r.git
cd Sublist3r
pip install -r requirements.txt
python3 sublist3r.py -d TARGET.com
```

**✅ קריטריון הצלחה:** קיבלת רשימת תת-דומיינים. סמן את אלה שנראים כמו סביבות פיתוח/בדיקה (`dev`, `staging`, `test`).

**❓ שאלה:** מדוע תת-דומיין בשם `dev.` מעניין יותר לתוקף?

---

## משימה 5 — OSINT על מיילים 🟡

**מטרה:** לזהות את תבנית המייל של ארגון.

**צעדים:**
1. פתח את [hunter.io](https://hunter.io) והזן דומיין של ארגון.
2. זהה את **תבנית המייל** (למשל `{first}.{last}@company.com`).
3. בדוק מייל אחד לתקינות ב-[email-checker.net](https://email-checker.net) או דומה.
4. בדוק דומיין/מייל ב-[HaveIBeenPwned](https://haveibeenpwned.com).

**✅ קריטריון הצלחה:** זיהית את תבנית המייל של הארגון.

> ⚠️ אין לשלוח מיילים, לנסות התחברות או לבצע פעולה כלשהי עם המידע — זהו תרגול OSINT פסיבי בלבד.

---

## משימה 6 — Burp Suite: לכידת בקשה ראשונה 🟡

**מטרה:** להקים את Burp כ-Proxy ולראות תעבורה.

**צעדים:**
1. פתח **Burp Suite** ב-Kali → `Temporary Project → Use Burp defaults → Start Burp`.
2. הגדר את Firefox: `Settings → Network Settings → Manual proxy`, HTTP Proxy `127.0.0.1` פורט `8080`.
3. ב-Burp, לשונית `Proxy → Intercept` → `Intercept is on`.
4. גלוש לאתר תרגול (למשל `http://testphp.vulnweb.com`) וצפה בבקשה שנתפסה.

**✅ קריטריון הצלחה:** תפסת בקשת HTTP אחת ואתה רואה את ה-Headers שלה ב-Burp.

---

## 🔴 אתגר מסכם — "תיק מודיעין על יעד"

בחר יעד **חוקי** אחד (מכונת תרגול או תוכנית Bug Bounty בתוך Scope), והפק דוח Recon פסיבי קצר הכולל:

1. **Scope** — הנכסים שבתוך ובחוץ.
2. **Tech Stack** — שרת, שפה, Framework, CMS (מ-builtwith/Wappalyzer).
3. **תת-דומיינים** — רשימה מ-Sublist3r, עם סימון הפגיעים-לכאורה.
4. **תבנית מייל** — אם רלוונטי (hunter.io).
5. **ממצאי Google Dorking** — 2 תוצאות מעניינות.
6. **סיכום** — פסקה: "משטח התקיפה הבולט של היעד הוא ______, וההמלצה לשלב הסריקה הבא היא ______".

זהו הבסיס למודול 6 — שם נתחיל לסרוק **אקטיבית** את מה שמיפינו.

---

## ✅ רשימת בקרה — לפני מעבר למודול 6

- [ ] אני יודע לקרוא ולכבד Scope
- [ ] אני יודע לזהות את ה-Tech Stack של יעד
- [ ] אני שולט ב-3 אופרטורים של Google Dorking לפחות
- [ ] הרצתי Sublist3r וקיבלתי תת-דומיינים
- [ ] זיהיתי תבנית מייל עם hunter.io
- [ ] הקמתי את Burp Suite ותפסתי בקשה

</div>
