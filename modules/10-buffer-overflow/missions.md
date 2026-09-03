<div dir="rtl">

# 🎯 תרגילים — מודול 10: גלישת חוצץ (Buffer Overflow)

> ⚠️ **רק על סביבת תרגול חוקית** — `vulnserver` במעבדה שלך, או חדר **"Buffer Overflow Prep"** ב-[TryHackMe](https://tryhackme.com/room/bufferoverflowprep). לעולם לא על תוכנה/שרת אמיתי. פתרונות ב-[**`solutions.md`**](solutions.md).

מקרא רמות: 🟢 קל · 🟡 בינוני · 🟠 מתקדם · 🔴 אתגר

---

## חלק א' — הבנת המבנה (🟢)

**10.1** — הסבר במילים שלך מה תפקידם של **EIP** ו-**ESP**. מדוע EIP הוא המטרה של תוקף BOF?

**10.2** — צייר (או תאר) את מבנה ה-Stack **לפני** ו**אחרי** גלישת חוצץ. סמן היכן נדרס ה-EIP.

**10.3** — הקם את `vulnserver` על מכונת Windows והתחבר אליו מ-Kali עם `nc`. הרץ `HELP` ורשום 3 פקודות זמינות.

---

## חלק ב' — Fuzzing ו-Offset (🟡)

**10.4** 🟡 — כתוב סקריפט Python ל-**Fuzzing** של הפקודה `TRUN` שמעלה את הקלט ב-100 בתים בכל סבב. באיזה גודל התוכנה קרסה?

**10.5** 🟡 — צור **דפוס ייחודי** עם `msf-pattern_create`, שלח אותו, וקרא את הערך שנדרס ב-EIP. השתמש ב-`msf-pattern_offset` כדי למצוא את ה-**Offset** המדויק.

**10.6** 🟡 — אמת את ה-Offset: שלח `A`×offset + `B`×4. מה מציג EIP ב-Immunity? מדוע `42424242`?

---

## חלק ג' — Bad Chars ו-JMP ESP (🟠)

**10.7** 🟠 — שלח את כל 255 הבתים אחרי ה-EIP והשתמש ב-`mona` (`bytearray` + `compare`) כדי לזהות אילו **Bad Characters** קיימים ב-vulnserver.

**10.8** 🟠 — הרץ `!mona modules` ובחר מודול מתאים ל-`JMP ESP`. אילו קריטריונים בדקת (ASLR/Rebase/SafeSEH)?

**10.9** 🟠 — מצא את כתובת ה-`JMP ESP` עם `!mona find -s "\xff\xe4"`. כתוב אותה בפורמט **Little-Endian** כפי שתופיע בקוד.

---

## 🔴 אתגר מסכם — "Exploit מלא מקצה לקצה"

בנה **Exploit עובד** ל-`vulnserver` (פקודת `TRUN`) שמעניק לך **Reverse Shell**:

1. **בצע את כל 7 השלבים** בסדר: Fuzz → Offset → EIP → Bad Chars → JMP ESP → Shellcode.
2. צור Shellcode של `windows/shell_reverse_tcp` עם `msfvenom`, תוך **החרגת הבתים הרעים** שמצאת.
3. הרכב את ה-Payload: `A×offset` + `JMP ESP` + `NOP sled` + `Shellcode`.
4. הקם מאזין (`nc -lvnp 4444`), הרץ את ה-Exploit, וקבל **Shell**. הרץ `whoami` להוכחה.
5. **תעד** את התהליך: כל שלב, הערכים שמצאת (offset, bad chars, כתובת JMP ESP), וצילום ה-Shell.

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
