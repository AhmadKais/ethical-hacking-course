<div dir="rtl">

# ✅ פתרונות מלאים — מודול 2: יסודות Linux

> נסה לפתור לבד ב-[`missions.md`](missions.md) קודם.

---

## חלק א' — ניווט ומערכת הקבצים

**2.1**
```bash
pwd            # מציג היכן אתה (למשל /home/kali)
cd /etc
ls
```

**2.2** — שתי דרכים לחזור הביתה:
```bash
cd ~     # דרך 1: הקיצור לבית
cd /home/kali   # דרך 2: נתיב מוחלט
# (גם cd בלי ארגומנטים מחזיר הביתה)
```

**2.3**
```bash
ls -lah ~     # l=פירוט, a=מוסתרים, h=גדלים קריאים
```

**2.4**
- `/etc/passwd` → תחת `/etc` (הגדרות מערכת ומשתמשים)
- `/usr/share/wordlists` → תחת `/usr` (נתונים משותפים)
- `/var/log` → תחת `/var` (לוגים)
- `/root` → תיקיית הבית של root

---

## חלק ב' — קבצים ותיקיות

**2.5**
```bash
mkdir lab
touch lab/notes.txt
```

**2.6**
```bash
echo "recon started" > lab/notes.txt     # > דורס/יוצר
echo "scanning next" >> lab/notes.txt     # >> מוסיף בסוף
cat lab/notes.txt
# פלט:
# recon started
# scanning next
```
> ⚠️ שים לב: `>` היה דורס את השורה הראשונה; `>>` שומר עליה.

**2.7**
```bash
cp lab/notes.txt /tmp/
mv /tmp/notes.txt /tmp/backup.txt
```

**2.8**
```bash
mkdir -p project/recon/results   # -p יוצר את כל השרשרת
```

---

## חלק ג' — הרשאות, משתמשים ו-sudo

**2.9**
```bash
id
# למשל: uid=1000(kali) gid=1000(kali) groups=1000(kali),27(sudo)...
```

**2.10**
```bash
touch run.sh
chmod +x run.sh
ls -l run.sh
# -rwxr-xr-x ... run.sh   ← ה-x מופיע
```

**2.11** — פענוח `-rwxr-x---`:
- בעלים: `rwx` = קריאה+כתיבה+הרצה
- קבוצה: `r-x` = קריאה+הרצה
- כולם: `---` = כלום
- ערך Octal: **750** (7=rwx, 5=r-x, 0=---)

**2.12**
```bash
sudo -l
```
מציג אילו פקודות מותר לך להריץ כ-root. **למה חשוב לתוקף:** אם המשתמש רשאי להריץ פקודה מסוימת כ-root (במיוחד עם `NOPASSWD`), לרוב אפשר לנצל זאת כדי להסלים ל-root — זהו אחד הבדיקות הראשונות אחרי השגת גישה.

---

## חלק ד' — חבילות, שירותים ורשת

**2.13**
```bash
sudo apt update
sudo apt install tree -y
```

**2.14**
```bash
python3 -m http.server 8000
# בטרמינל שני:
curl http://127.0.0.1:8000
# מקבלים HTML של רשימת הקבצים → השרת עונה
```

**2.15**
```bash
ip a                 # מציאת ה-IP (שורת inet תחת eth0)
ip route             # ה-Gateway (default via X.X.X.X)
ping -c 4 <gateway>  # בדיקת קישוריות
```

**2.16**
```bash
ss -tuln
# t=TCP, u=UDP, l=מאזינים, n=מספרים במקום שמות
```

---

## חלק ה' — חיפוש וצינורות

**2.17**
```bash
find / -perm -4000 2>/dev/null
# -perm -4000 = ביט SUID; 2>/dev/null מסתיר שגיאות "Permission denied"
```

**2.18**
```bash
cat /etc/passwd | wc -l
# או ישירות:
wc -l /etc/passwd
# כל שורה = משתמש אחד
```

**2.19**
```bash
grep "bash" /etc/passwd
# מציג משתמשים שה-shell שלהם /bin/bash (חשבונות אינטראקטיביים)
```

---

## 🔴 אתגר מסכם — פתרון לדוגמה

רצף ה-Local Enumeration:
```bash
# 1. זהות והרשאות
whoami; id; sudo -l

# 2. רשת
ip a; ip route; cat /etc/resolv.conf

# 3. פורטים מאזינים
ss -tuln

# 4. וקטור הסלמה — קובצי SUID
find / -perm -4000 2>/dev/null

# 5. משתמשים עם shell
grep "bash" /etc/passwd
```

**דוגמת מסקנה:** "המשתמש שלי חבר בקבוצת `sudo`, ו-`sudo -l` הראה הרשאה להריץ `/usr/bin/find` כ-root ללא סיסמה. זהו מסלול ההסלמה המבטיח ביותר — ניתן לנצל את `find` עם `-exec` כדי להריץ פקודות כ-root (GTFOBins). לחלופין, נבדוק את קובצי ה-SUID החריגים שנמצאו."

> כיסית את כל הצעדים? מצוין — המשך ל[מודול 3](../03-networking/).

</div>
