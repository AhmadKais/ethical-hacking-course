# תקיפות אלחוטיות (Wireless)
## מודול 14 — האקינג אתי מהיסוד

- אבטחת Wi-Fi: WEP → WPA3
- לכידת Handshake ופיצוח WPA2
- Deauthentication ו-Evil Twin
- הגנה על רשת אלחוטית

## ⚠️ דרישת חומרה

- צריך מתאם USB עם **Monitor Mode + Injection**
- הכרטיס המובנה לרוב לא מספיק
- אין חומרה? למד תיאוריה + תרגל פיצוח `.cap`
- רק על רשת שבבעלותך!

## יסודות אלחוט

- **SSID** — שם הרשת · **BSSID** — MAC של ה-AP
- **Client** — מכשיר מחובר
- תעבורה **משודרת באוויר** — כולם שומעים
- לכן הצפנה קריטית

## פרוטוקולי אבטחה

- **WEP** — שבור לחלוטין (דקות)
- **WPA** — חלש (TKIP)
- **WPA2** — הנפוץ; פגיע לסיסמה חלשה
- **WPA3** — חזק (SAE)

## Monitor Mode

- מאזין לכל התעבורה באוויר
- `airmon-ng check kill`
- `airmon-ng start wlan0` → wlan0mon
- דורש מתאם/דרייבר תואם

## סריקה — airodump-ng

- `airodump-ng wlan0mon` — כל הרשתות
- מזהים: BSSID, CH, ENC, ESSID
- מתמקדים: `--bssid -c -w capture`
- STATION = לקוחות מחוברים

## Deauth ולכידת Handshake

- Handshake נלכד רק בהתחברות לקוח
- `aireplay-ng --deauth 5 -a AP -c client`
- הלקוח מתחבר מחדש → לוכדים ✅
- "WPA handshake" מופיע ב-airodump

## פיצוח WPA2

- מפצחים את ה-Handshake **offline**
- `aircrack-ng capture.cap -w rockyou.txt`
- או hashcat -m 22000 (מהיר יותר)
- סיסמה חזקה = פיצוח נכשל = בטוח

## Evil Twin ו-WPS

- **Evil Twin** — AP מזויף, דף התחברות גונב סיסמה
- עוקף WPA2 — מרמה את המשתמש!
- **WPS** — PIN בן 8 ספרות → reaver brute-force
- airgeddon/wifiphisher מאוטמים

## הגנה

- **סיסמה חזקה 15+ תווים** — ההגנה #1
- WPA3 · כבה WPS
- הפרד רשת אורחים (VLAN)
- WPA2-Enterprise (802.1X)

## סיכום מודול 14

- WEP שבור · WPA2 בטוח עם סיסמה חזקה
- לוכדים Handshake (Deauth) ומפצחים offline
- Evil Twin/WPS = מתקדם, עוקף הצפנה
- הגנה: סיסמה חזקה, WPA3, VLAN
- **תרגול** → `practice.md` · **פתרונות** → `solutions.md`
