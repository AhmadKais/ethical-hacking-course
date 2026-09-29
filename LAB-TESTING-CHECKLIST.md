<div dir="rtl">

# 🧪 צ'ק-ליסט בדיקת המעבדות על Kali

> **למרצה:** רשימת ההדגמות שמשתמשות ב**כלים של Kali** (nmap, John, Hydra, hashcat, aircrack-ng, gobuster, searchsploit). מומלץ להריץ אותן פעם אחת על ה-Kali שלך **לפני** השיעור, כדי לוודא שהכול עובד בסביבה שלך. שאר ההדגמות (M1, M2, M7, M9, M10, M11, M12, M15) הן פייתון/bash/gcc טהורים ונבדקו במלואן.
>
> 💡 טיפ: פתח **טאב טרמינל חדש** לכל שרת במקום `&` אם אינך רגיל בניהול משימות (`kill %1`).
> אם כלי חסר ב-Kali מינימלי: `sudo apt install hydra gobuster hcxtools -y`.

---

## ☑️ M3 · רשתות — nmap רואה את שרת ה-Flask
```bash
cd modules/03-networking
sudo apt install python3-flask -y
python3 demo_server.py &
nmap 127.0.0.1 -p 5000            # צפוי: 5000/tcp open
curl http://127.0.0.1:5000/whoami # צפוי: כתובת ה-IP שלך
kill %1
cd ../..
```

## ☑️ M6 · סריקה — nmap / nc / gobuster / searchsploit
```bash
cd modules/06-scanning-enumeration
python3 scan_target.py &
nmap 127.0.0.1 -p 2121,2222,8080,10000 -sV   # צפוי: 4 פורטים פתוחים + banners
nc 127.0.0.1 2121                             # צפוי: 220 (vsFTPd 2.3.4)  — Ctrl+C ליציאה
kill %1
python3 ../05-recon/recon_target.py &
gobuster dir -u http://127.0.0.1:8000 -w /usr/share/wordlists/dirb/common.txt   # צפוי: /admin-panel, /backup
kill %1
searchsploit vsftpd 2.3.4                     # צפוי: "Backdoor Command Execution"
cd ../..
```

## ☑️ M8 · סיסמאות — John (offline) + Hydra (online)
```bash
cd modules/08-password-attacks
sudo gunzip /usr/share/wordlists/rockyou.txt.gz 2>/dev/null
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
john --show --format=raw-md5 hashes.txt        # צפוי: password, iloveyou, sunshine, princess, superman
john --wordlist=/usr/share/wordlists/rockyou.txt shadow_demo.txt
john --show shadow_demo.txt                    # צפוי: victim:letmein
python3 login_server.py &
printf 'password\n123456\niloveyou\nsuperman\nprincess\n' > pws.txt
hydra -l admin -P pws.txt 127.0.0.1 -s 8081 http-post-form "/login:user=^USER^&pass=^PASS^:Invalid credentials"
# צפוי:  login: admin   password: superman
kill %1
cd ../..
```

## ☑️ M13 · Active Directory — פיצוח NTLM
```bash
cd modules/13-active-directory
john --format=nt ntlm_hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
john --format=nt ntlm_hashes.txt --show        # צפוי: iloveyou, sunshine, princess
# חלופה עם hashcat:
cut -d: -f4 ntlm_hashes.txt > nt_only.txt
hashcat -m 1000 nt_only.txt /usr/share/wordlists/rockyou.txt --show
cd ../..
```

## ☑️ M14 · אלחוט — פיצוח Handshake אמיתי
```bash
cd modules/14-wireless
wget https://github.com/aircrack-ng/aircrack-ng/raw/master/test/wpa.cap
aircrack-ng wpa.cap -w wifi_wordlist.txt       # צפוי:  KEY FOUND! [ biscotte ]
cd ../..
```

---

## ✅ נבדקו במלואן (פייתון/bash/gcc — אין צורך בכלים חיצוניים)
M1 (`first_hack.py`) · M2 (`linux_ctf.sh`) · M4 (`pin_server.py`+`brute_force.py`) · M5 (`recon_target.py`) · M7 (`vuln_webapp.py` — Command Injection/RCE) · M9 (`owasp_playground.py` — SQLi/XSS/IDOR) · M10 (`bof_demo.c`) · M11 (`privesc_lab.sh`) · M12 (`pivot_demo.py`) · M15 (`phishing_demo.py`).

> 🔒 כל היעדים מאזינים על `127.0.0.1` בלבד ומיועדים לתרגול חוקי. תקיפת מערכת ללא רשות = עבירה פלילית.

</div>
