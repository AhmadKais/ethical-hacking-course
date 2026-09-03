<div dir="rtl">

# 🎯 תרגילים — מודול 10: גלישת חוצץ (Buffer Overflow)

> ⚠️ **רק על סביבת תרגול חוקית** — `vulnserver` במעבדה שלך, או חדר **"Buffer Overflow Prep"** ב-[TryHackMe](https://tryhackme.com/room/bufferoverflowprep). לעולם לא על תוכנה/שרת אמיתי. פתרונות ב-[**`solutions.md`**](solutions.md).

> ### 🚦 לפני שמתחילים — קרא אותי!
> - **מה צריך לרוץ:** מכונת **Windows** עם `vulnserver.exe` + **Immunity Debugger** + `mona.py`, ומכונת **Kali** באותה רשת. **אין Windows?** השתמש בחדר **"Buffer Overflow Prep"** ב-TryHackMe — הכול מוכן שם בענן (מומלץ!).
> - **איך עובדים:** קרא קודם את ה-[`README.md`](README.md) — הוא מסביר כל שלב. התרגילים הקלים (🟢) **ישירים** (מה להקליד ומה לחפש); הקשים יש בהם **💡 רמז** ו-**✅ קריטריון**.
> - **נתקעת?** BOF הוא נושא מדויק — טעות קטנה מפילה הכול. נסה, קרא שוב את הסעיף, ואז הצץ ב-[`solutions.md`](solutions.md) שיש בו **סקריפט מלא וכל הפקודות**.
> - **טיפ:** רשום את הערכים שאתה מוצא (offset, bad chars, כתובת JMP ESP) — תזדקק להם בשלב הבא.

מקרא רמות: 🟢 קל · 🟡 בינוני · 🟠 מתקדם · 🔴 אתגר

---

## חלק א' — הבנת המבנה (🟢)

**10.1** — הסבר במילים שלך מה תפקידם של **EIP** ו-**ESP**. מדוע EIP הוא המטרה של תוקף BOF?
  💡 רמז: README §10.1 (טבלת הרגיסטרים).
  ✅ הצלחה: הסברת ש-EIP מצביע להוראה הבאה, ולכן שליטה בו = שליטה בביצוע.

**10.2** — צייר (או תאר) את מבנה ה-Stack **לפני** ו**אחרי** גלישת חוצץ. סמן היכן נדרס ה-EIP.
  💡 רמז: README §10.2 (הדיאגרמה).
  ✅ הצלחה: הדיאגרמה שלך מראה את החוצץ מתמלא ואת ה-EIP נדרס.

**10.3** 🟢 — הקם את `vulnserver` והתחבר אליו מ-Kali כדי לראות את הפקודות.
```bash
# ב-Windows: הפעל vulnserver.exe (מאזין על 9999)
# ב-Kali:
nc 192.168.56.50 9999      # החלף ב-IP של Windows
HELP
```
  👀 **חפש:** רשימת פקודות שהשרת מדפיס (TRUN, STATS, GMON...). רשום 3 מהן.
  ✅ הצלחה: התחברת וראית את פקודות ה-vulnserver.

---

## חלק ב' — Fuzzing ו-Offset (🟡)

**10.4** 🟡 — כתוב סקריפט Python ל-**Fuzzing** של הפקודה `TRUN` שמעלה את הקלט ב-100 בתים בכל סבב. באיזה גודל התוכנה קרסה?
  💡 רמז: README §10.5 (יש שם שלד סקריפט מלא). הרץ אותו וצפה ב-Immunity מתי vulnserver "מת".
  ✅ הצלחה: יש לך מספר משוער של בתים שבו התוכנה קרסה (~2000).

**10.5** 🟡 — צור **דפוס ייחודי**, שלח אותו, וקרא את הערך שנדרס ב-EIP. מצא את ה-**Offset** המדויק.
```bash
msf-pattern_create -l 3000          # הדבק במקום ה-A בסקריפט, שלח שוב
# קרא את הערך ב-EIP ב-Immunity (למשל 386F4337), ואז:
msf-pattern_offset -l 3000 -q 386F4337
```
  👀 **חפש:** שורת `Exact match at offset NNNN` — זה ה-Offset (למשל 2003).
  ✅ הצלחה: יש לך מספר Offset מדויק.

**10.6** 🟡 — אמת את ה-Offset: שלח `A`×offset + `B`×4. מה מציג EIP ב-Immunity? מדוע `42424242`?
  💡 רמז: README §10.7. בנה `buffer = b"A"*2003 + b"B"*4`.
  ✅ הצלחה: EIP מציג בדיוק `42424242` — הוכחת שליטה מלאה.

---

## חלק ג' — Bad Chars ו-JMP ESP (🟠)

**10.7** 🟠 — שלח את כל 255 הבתים אחרי ה-EIP והשתמש ב-`mona` (`bytearray` + `compare`) כדי לזהות **Bad Characters**.
  💡 רמז: README §10.8. `!mona bytearray -b "\x00"` ואז `!mona compare -f <bytearray.bin> -a <ESP>`.
  ✅ הצלחה: יש לך רשימת הבתים הרעים (ב-vulnserver לרוב רק `\x00`).

**10.8** 🟠 — הרץ `!mona modules` ובחר מודול מתאים ל-`JMP ESP`. אילו קריטריונים בדקת?
  💡 רמז: README §10.9. חפש מודול עם **הכול False** (Rebase/SafeSEH/ASLR/NXCompat) — ב-vulnserver זה `essfunc.dll`.
  ✅ הצלחה: בחרת מודול ללא הגנות ויודע להסביר למה.

**10.9** 🟠 — מצא את כתובת ה-`JMP ESP` וכתוב אותה ב-**Little-Endian** כפי שתופיע בקוד.
```text
!mona find -s "\xff\xe4" -m essfunc.dll
```
  👀 **חפש:** כתובת כמו `625011AF`. בקוד היא נכתבת הפוך: `\xaf\x11\x50\x62`.
  ✅ הצלחה: יש לך את כתובת ה-JMP ESP בפורמט Little-Endian.

---

## 🔴 אתגר מסכם — "Exploit מלא מקצה לקצה"

בנה **Exploit עובד** ל-`vulnserver` (פקודת `TRUN`) שמעניק לך **Reverse Shell**:

1. **בצע את כל 7 השלבים** בסדר: Fuzz → Offset → EIP → Bad Chars → JMP ESP → Shellcode.
2. צור Shellcode של `windows/shell_reverse_tcp` עם `msfvenom`, תוך **החרגת הבתים הרעים** שמצאת.
3. הרכב את ה-Payload: `A×offset` + `JMP ESP` + `NOP sled` + `Shellcode`.
4. הקם מאזין (`nc -lvnp 4444`), הרץ את ה-Exploit, וקבל **Shell**. הרץ `whoami` להוכחה.
5. **תעד** את התהליך: כל שלב, הערכים שמצאת (offset, bad chars, כתובת JMP ESP), וצילום ה-Shell.

  💡 רמז: כל השלבים מפורטים ב-README §10.10, ויש **סקריפט Exploit מלא** ב-[`solutions.md`](solutions.md).
  ✅ הצלחה: קיבלת Shell על ה-Windows והרצת `whoami`.

> 📤 זהו בדיוק תרגיל ה-Buffer Overflow של OSCP. אם השלמת אותו לבד — אתה מוכן לחלק ה-BOF בבחינה.

---

## ✅ רשימת בקרה — לפני מעבר למודול 11
- [ ] אני מבין את תפקיד EIP/ESP ומבנה ה-Stack ב-Overflow
- [ ] אני מבצע Fuzzing ומוצא את טווח הקריסה
- [ ] אני מוצא Offset מדויק עם pattern_create/offset
- [ ] אני משיג שליטה מלאה ב-EIP (42424242)
- [ ] אני מזהה Bad Characters עם mona
- [ ] אני מוצא כתובת JMP ESP וכותב אותה ב-Little-Endian
- [ ] אני מייצר Shellcode עם msfvenom ומקבל Shell

*פתרונות מלאים: [`solutions.md`](solutions.md)*

</div>
