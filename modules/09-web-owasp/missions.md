<div dir="rtl">

# 🎯 תרגילים — מודול 9: אבטחת Web (OWASP Top 10)

> ⚠️ **רק על סביבות תרגול חוקיות** — DVWA, OWASP Juice Shop, או [PortSwigger Academy](https://portswigger.net/web-security). לעולם לא על אתר אמיתי ללא רשות. פתרונות ב-[**`solutions.md`**](solutions.md).

> ### 🚦 לפני שמתחילים — קרא אותי!
> - **מה צריך לרוץ:** מכונת **Kali** ו-**Burp Suite** (מגיע עם Kali). בחלק א' נתקין **Docker** ונקים **שני** יעדי תרגול: **DVWA** (PHP קלאסי — לתרגילי Injection / Upload / LFI) ו-**OWASP Juice Shop** (אפליקציה מודרנית — ל-XSS / IDOR ולאתגר המסכם). כל תרגיל מציין 🎯 על איזה יעד לבצע אותו.
> - **☁️ אין Docker, או מעדיף דפדפן בלבד?** [**PortSwigger Web Security Academy**](https://portswigger.net/web-security) — חינמי, מבוסס-דפדפן, עם מעבדה מודרכת לכל חולשה (SQLi, XSS, Access Control ועוד). חלופה מצוינת לכל המודול, ללא התקנות.
> - **איך עובדים על תרגיל:** קרא קודם את ה-[`README.md`](README.md). בתרגילים הקלים (🟢) **נאמר לך בדיוק מה להקליד ומה לחפש**. בתרגילים הקשים יותר יש **💡 רמז** ו-**✅ קריטריון הצלחה**.
> - **נתקעת?** נסה ~10 דקות, קרא שוב את הסעיף ב-README, ואז הצץ ב-[`solutions.md`](solutions.md) — יש שם **פתרון מלא צעד-אחר-צעד**.
> - **טיפ:** צלם מסך של כל חולשה שמצאת — זה יהיה ה-PoC בדוח (מודול 16).

מקרא רמות: 🟢 קל · 🟡 בינוני · 🟠 מתקדם · 🔴 אתגר

---

## חלק א' — הקמה והיכרות (🟢)

> בחלק זה נהיה **ישירים** — עקוב אחר הפקודות בדיוק.

**9.1** 🟢 — התקן Docker והקם את **שני** יעדי התרגול.
```bash
# 1. התקנת Docker (אינו מותקן מראש ב-Kali) והפעלתו:
sudo apt update && sudo apt install docker.io -y
sudo systemctl start docker

# 2. יעד ראשי — DVWA (PHP קלאסי; ל-Injection / Upload / LFI):
sudo docker run -d -p 80:80 vulnerables/web-dvwa
#   גלוש ל- http://localhost  → התחבר עם admin / password
#   → לחץ "Create / Reset Database"  → ואז לשונית "DVWA Security" → הגדר ל-Low

# 3. יעד שני — OWASP Juice Shop (מודרני; ל-XSS / IDOR ולאתגר המסכם):
sudo docker run -d -p 3000:3000 bkimminich/juice-shop
#   גלוש ל- http://localhost:3000
```
  👀 **חפש:** `http://localhost` מציג את DVWA (אחרי כניסה), ו-`http://localhost:3000` את חנות ה-Juice Shop.
  ✅ הצלחה: שני היעדים רצים; DVWA מוגדר ל-**Security = Low**.
  > 💡 ללא Docker? דלג על ההקמה והשתמש ב-[PortSwigger Academy](https://portswigger.net/web-security) (ראה ההערה למעלה).

**9.2** 🟢 — הגדר את **Burp Suite** ללכוד תעבורה, ותפוס בקשת התחברות.
```text
1. פתח Burp → Temporary Project → Use Burp defaults → Start Burp.
2. Proxy → Intercept → ודא "Intercept is on".
3. הגדר Firefox לעבוד דרך Proxy 127.0.0.1:8080 (או השתמש בדפדפן המובנה של Burp).
4. בחנות, נסה להתחבר (Login) עם אימייל וסיסמה כלשהם.
```
  👀 **חפש:** ב-Burp תיתפס בקשת `POST` שכוללת את השדות `email` ו-`password`.
  ✅ הצלחה: אתה רואה את בקשת ההתחברות עם הפרמטרים שלה ב-Burp.

**9.3** 🟢 — שלח את הבקשה ל-**Repeater**, שנה ערך, ושלח שוב.
```text
לחיצה ימנית על הבקשה → Send to Repeater → עבור ללשונית Repeater → שנה ערך → לחץ Send.
```
  👀 **חפש:** בצד ימין (Response) — איך תגובת השרת משתנה כשאתה משנה את הבקשה.
  ✅ הצלחה: הבנת איך לערוך ולשלוח בקשה ידנית — הבסיס לכל תקיפת Web.

---

## חלק ב' — Injection (🟡🟠)

**9.4** 🟡 — **SQL Injection:** בטופס התחברות פגיע, עקוף את ההתחברות עם `' OR '1'='1' -- `. הסבר מדוע זה עובד.
  🎯 **יעד:** טופס ההתחברות ב-**Juice Shop** (`localhost:3000`), או עמוד ה-SQL Injection ב-**DVWA**.
  💡 רמז: README §9.4. הזן בשדה המשתמש/אימייל: `' OR '1'='1' -- ` וסיסמה כלשהי.
  ✅ הצלחה: התחברת ללא סיסמה נכונה, ואתה יכול להסביר את התפקיד של `'1'='1'` ושל `--`.

**9.5** 🟠 — **SQLi עם sqlmap:** מצא פרמטר פגיע (למשל `?id=1`), והרץ sqlmap כדי לשלוף את בסיסי הנתונים ואז את טבלת המשתמשים.
  🎯 **יעד:** **DVWA** — עמוד "SQL Injection" (ה-URL כולל `?id=`). (ב-Burp שמור בקשה עם ה-Cookie ותן ל-sqlmap `-r request.txt`.)
  💡 רמז: README §9.4. `sqlmap -u "http://localhost/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="..." --batch --dbs` ואז `-D dvwa --tables` ו-`-T users --dump`.
  ✅ הצלחה: sqlmap הדפיס רשימת בסיסי נתונים, ובהמשך שאב תוכן של טבלה.

**9.6** 🟡 — **XSS:** בשדה קלט פגיע, הזרק `<script>alert('XSS')</script>`. האם זה Reflected או Stored? כיצד קבעת?
  🎯 **יעד:** **DVWA** — עמודי "XSS (Reflected)" ו-"XSS (Stored)", או שדה החיפוש ב-**Juice Shop**.
  💡 רמז: README §9.5. אם ה-alert קופץ רק בתגובה המיידית → Reflected; אם נשמר וקופץ בכל טעינה → Stored.
  ✅ הצלחה: ה-alert קפץ, וקבעת נכון את סוג ה-XSS עם נימוק.

**9.7** 🟠 — **Command Injection:** בדף שמבצע `ping`, הזרק `127.0.0.1; whoami`. מה קיבלת, ומדוע זו חולשה חמורה?
  🎯 **יעד:** **DVWA** — עמוד "Command Injection" (Juice Shop הוא Node ואין בו עמוד כזה).
  💡 רמז: README §9.6. מפרידי פקודות: `;` `|` `&&`.
  ✅ הצלחה: ראית פלט של `whoami` (למשל `www-data`) והבנת שזו הרצת פקודות (RCE).

---

## חלק ג' — Access Control ו-Upload (🟠 מתקדם)

**9.8** 🟠 — **IDOR:** מצא URL עם מזהה (למשל `?id=1`), שנה את המספר, ובדוק אם אתה ניגש לנתונים של משתמש אחר.
  🎯 **יעד:** **Juice Shop** (סל הקניות / הזמנות — נסה `api/BasketItems`), או כל עמוד עם מזהה משאב.
  💡 רמז: README §9.7. שנה `?id=1` ל-`?id=2` וכו', או בדוק בקשות API ב-Burp.
  ✅ הצלחה: ראית נתונים שאינם שלך ע"י שינוי מזהה בלבד.

**9.9** 🟠 — **File Upload:** נסה להעלות Web Shell פשוט (`<?php system($_GET['cmd']); ?>`). אם יש סינון — נסה עקיפה (`shell.php.jpg` / שינוי Content-Type ב-Burp). הרץ `whoami` דרכו.
  🎯 **יעד:** **DVWA** — עמוד "File Upload" (חייב יעד **PHP**; ב-Node/Juice Shop ה-shell לא ירוץ).
  💡 רמז: README §9.8. אחרי העלאה: `http://localhost/hackable/uploads/shell.php?cmd=whoami`.
  ✅ הצלחה: הרצת פקודה דרך הקובץ שהעלית (RCE).

**9.10** 🟠 — **LFI:** בפרמטר שכולל שם קובץ, נסה `../../../../etc/passwd`. מה קיבלת?
  🎯 **יעד:** **DVWA** — עמוד "File Inclusion" (הפרמטר `?page=`).
  💡 רמז: README §9.8. חפש פרמטר כמו `?file=` או `?page=`.
  ✅ הצלחה: ראית את תוכן `/etc/passwd` (רשימת המשתמשים) בדף.

---

## 🔴 אתגר מסכם — "בדיקת Web מלאה על Juice Shop"

בצע בדיקת אבטחת web מובנית על **OWASP Juice Shop** ומצא לפחות **4 חולשות** מקטגוריות שונות:

1. **מיפוי:** מפה את האפליקציה (דפים, פרמטרים, נקודות קלט) עם Burp.
2. **מצא ונצל** לפחות אחת מכל: **Injection** (SQLi/XSS), **Broken Access Control** (IDOR/גישת admin), ועוד שתיים לבחירתך.
3. **תעד כל ממצא** בפורמט דוח: כותרת, חומרה (CVSS), תיאור, **PoC** (צעדים + צילום מסך), והמלצת תיקון.
4. **סיכום:** דרג את הממצאים לפי חומרה — מה הכי קריטי, ולמה?

  💡 רמז: השתמש בכל מה שתרגלת ב-9.4–9.10. מבנה דוח מלא: מודול 16.
  ✅ הצלחה: מסמך עם 4+ ממצאים מתועדים, כל אחד עם PoC והמלצת תיקון, מדורג לפי חומרה.

> 📤 זהו דוח בדיקת Web אמיתי — בדיוק מה שמגישים ללקוח / בתוכנית Bug Bounty. שמור אותו לתיק העבודות שלך.

---

## ✅ רשימת בקרה — לפני מעבר למודול 10
- [ ] אני מבין כיצד עובדת אפליקציית Web ומשתמש ב-Burp (Proxy/Repeater)
- [ ] אני מבצע SQL Injection ידני ואוטומטי (sqlmap)
- [ ] אני מזהה ומנצל XSS (Reflected/Stored)
- [ ] אני מבצע Command Injection ומבין שזה RCE
- [ ] אני מוצא IDOR ובעיות Broken Access Control
- [ ] אני מנצל File Upload / LFI
- [ ] אני יודע להמליץ הגנות (Prepared Statements, Encoding, בקרת גישה)

*פתרונות מלאים: [`solutions.md`](solutions.md)*

</div>
