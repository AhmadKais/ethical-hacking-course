# Pivoting ותנועה רוחבית
## מודול 12 — האקינג אתי מהיסוד

- מעבר לרשת הפנימית שמאחורי הפריצה
- SSH Tunneling ו-Port Forwarding
- proxychains ו-SOCKS
- Chisel, Ligolo ו-Metasploit

## למה Pivoting?

- המכונה שפרצת = כמעט אף פעם לא היעד
- שרתים רגישים ב-**רשת פנימית** לא-נגישה
- המכונה שנפרצה "רואה" רשתות שאתה לא
- מנתבים דרכה פנימה

## המושגים

- **Lateral Movement** — בין מכונות באותה רשת
- **Pivoting** — מכונה כנקודת מעבר לרשת אחרת
- **Tunneling** — עטיפת תעבורה (SSH) לחציית גבול
- מזהים רשת: `ip a`, `ip route`, `arp -a`

## התרחיש: Dual-Homed Host

- `eth0` — DMZ (כאן אתה)
- `eth1` — רשת פנימית (לא נגיש!)
- Kali → Pivot → מכונה פנימית
- מנתבים דרך ה-Pivot

## SSH Tunneling — 3 סוגים

- **-L** Local — מביא שירות פנימי אליך
- **-R** Remote — פורט על ה-Pivot אליך
- **-D** Dynamic — SOCKS proxy מלא
- `-D` = הסכין השוויצרי

## proxychains

- מריץ **כל כלי** דרך הפרוקסי
- `socks5 127.0.0.1 9050` בקונפיג
- `proxychains nmap -sT -Pn <target>`
- ⚠️ חובה `-sT` (לא SYN) ו-`-Pn`

## Pivoting עם Metasploit

- יש Meterpreter? קל ומובנה
- `run autoroute -s 10.10.10.0/24`
- מודולי MSF "רואים" את הרשת
- `socks_proxy` לכלים חיצוניים

## Chisel ו-Ligolo

- **Chisel** — מנהור מעל HTTP, בינארי יחיד
- `chisel server --reverse` + `client R:socks`
- **Ligolo-ng** — מודרני, ממשק tun, ללא proxychains
- מצוינים כשאין SSH / למעבדות AD

## סריקה דרך ה-Pivot

- `proxychains nmap -sT -Pn 10.10.10.0/24`
- `proxychains crackmapexec smb ...`
- `proxychains xfreerdp /v:...`
- חוזרים על מחזור: recon→exploit→privesc

## Double Pivot

- רשת שלישית שגם ה-Pivot לא רואה
- משרשרים מנהרות: Kali→P1→P2→עמוק
- נפוץ ברשתות ארגוניות רב-שכבתיות
- המפתח לחדירת AD (מודול 13)

## סיכום השיטות

- SSH -L/-R/-D · Metasploit autoroute
- Chisel (מעל HTTP) · Ligolo (tun)
- proxychains = הדבק שמחבר הכול
- Segmentation = ההגנה שעוצרת

## סיכום מודול 12

- Pivoting = גשר לרשת פנימית לא-נגישה
- SSH -D + proxychains = הבסיס
- Chisel/Metasploit/Ligolo = חלופות
- Double Pivot = חדירה עמוקה
- **תרגול** → `practice.md` · **פתרונות** → `solutions.md`
