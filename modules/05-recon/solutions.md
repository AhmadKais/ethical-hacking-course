<div dir="rtl">

# ✅ פתרונות מלאים — מודול 5: איסוף מידע (Reconnaissance)

> נסה לבד ב-[`missions.md`](missions.md) קודם. חלק מהתרגילים הם חקירה חופשית — כאן ההנחיות והתשובות לדוגמה.

---

## משימה 1 — קריאת Scope
היכנס ל-[HackerOne](https://hackerone.com/directory/programs) או [Bugcrowd](https://bugcrowd.com/programs), פתח תוכנית ציבורית, וגלול לסעיף **Scope / Targets**.
- **In-Scope** לדוגמה: `*.example.com`, אפליקציית המובייל הרשמית.
- **Out-of-Scope** לדוגמה: `blog.example.com` (WordPress מנוהל), נכסים של צד ג', מתקפות DoS.

**מה עלול לקרות אם תתקוף Out-of-Scope?** אין הרשאה חוקית → זו עבירה פלילית / הפרת תנאי התוכנית, ללא תשלום ובאחריותך המשפטית.

---

## משימה 2 — זיהוי טכנולוגיות אתר
```text
1. builtwith.com → הזן דומיין → קרא Framework / Server / CMS / Analytics
2. התקן Wappalyzer בדפדפן ובקר באתר
```
**דוגמת פלט:** Web Server: `nginx`; Framework: `React`; CMS: `WordPress 6.1`; CDN: `Cloudflare`.

**מדוע גרסה ישנה חשובה?** לגרסאות ישנות יש לרוב **חולשות ידועות (CVE)** עם Exploits מוכנים — נקודת כניסה מהירה בשלב הניצול (מודול 7).

---

## משימה 3 — Google Dorking
```text
site:TARGET.com                      → כל הדפים המאונדקסים
site:TARGET.com filetype:pdf         → מסמכי PDF (לעיתים רגישים)
site:TARGET.com inurl:login          → עמודי התחברות
site:TARGET.com intitle:"index of"   → ספריות חשופות
```
תוצאה מעניינת = קובץ פנימי, עמוד ניהול, או ספריית קבצים פתוחה. ל-Dorks נוספים: [Google Hacking Database](https://www.exploit-db.com/google-hacking-database).

---

## משימה 4 — גילוי תת-דומיינים
```bash
sudo apt install sublist3r -y
sublist3r -d TARGET.com
# חלופה ידנית:
git clone https://github.com/aboul3la/Sublist3r.git
cd Sublist3r && pip install -r requirements.txt
python3 sublist3r.py -d TARGET.com
```
סמן תת-דומיינים כמו `dev.`, `staging.`, `test.`, `admin.`.

**מדוע `dev.` מעניין?** סביבות פיתוח/בדיקה לרוב **מאובטחות פחות** (סיסמאות ברירת מחדל, דיבוג פתוח, גרסאות ישנות) — יעד קל יותר.

---

## משימה 5 — OSINT על מיילים
```text
1. hunter.io → הזן דומיין → זהה את תבנית המייל, למשל {first}.{last}@company.com
2. email-checker.net → אמת מייל בודד
3. haveibeenpwned.com → בדוק אם הדומיין/מייל הופיע בדלף
```
**תבנית המייל** מאפשרת לנחש מיילים של עובדים נוספים (לצורך פישינג/Password Spraying — בתוך Scope בלבד).

> ⚠️ אין לשלוח מיילים או לנסות התחברות — זהו OSINT פסיבי בלבד.

---

## משימה 6 — Burp Suite: לכידת בקשה
```text
1. Burp → Temporary Project → Use Burp defaults → Start Burp
2. Firefox → Settings → Network Settings → Manual proxy → 127.0.0.1:8080
3. Burp → Proxy → Intercept → "Intercept is on"
4. גלוש ל- http://testphp.vulnweb.com
5. חזור ל-Burp — הבקשה נתפסה; קרא את שורת ה-GET ואת ה-Headers
```
תראה את מתודת ה-HTTP, הנתיב, ה-Host, ה-User-Agent, ועוגיות (Cookies). זהו הבסיס לתקיפות Web (מודול 9).

---

## 🔴 אתגר מסכם — מבנה "תיק מודיעין" לדוגמה

```markdown
# תיק מודיעין — TARGET.com

## 1. Scope
In:  *.target.com, app.target.com
Out: blog.target.com, third-party.com

## 2. Tech Stack (builtwith / Wappalyzer)
Server: nginx 1.18 | Framework: Laravel | CMS: — | CDN: Cloudflare

## 3. תת-דומיינים (Sublist3r)
www, mail, dev*, staging*, vpn   (* = פוטנציאל פגיע)

## 4. תבנית מייל (hunter.io)
{first}.{last}@target.com

## 5. Google Dorking
- site:target.com filetype:pdf → מדריך פנימי חשוף
- inurl:admin → פאנל ניהול

## 6. סיכום
משטח התקיפה הבולט: תת-הדומיין dev.target.com (סביבת פיתוח חשופה).
המלצה לשלב הבא: סריקת nmap ממוקדת ל-dev ול-vpn (מודול 6).
```

> עברת? יש לך תמונת מודיעין מלאה. המשך ל[מודול 6 — סריקה ומיפוי](../06-scanning-enumeration/), שם נסרוק **אקטיבית** את מה שמיפינו.

</div>
