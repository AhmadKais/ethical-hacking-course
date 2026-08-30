# יסודות Linux
## מודול 2 — Linux Fundamentals

- השֶׁל, ה-Terminal ומערכת הקבצים
- ניווט, קבצים ועריכה
- הרשאות, משתמשים ו-sudo
- חבילות, שירותים, רשת וצינורות

## השֶׁל ושורת הפקודה

- **Bash** מפרש את הפקודות; `#`=root, `$`=משתמש
- **Tab** — השלמה אוטומטית
- **↑/↓** — פקודות קודמות · `history`
- **`man <cmd>`** — המדריך המלא

## מערכת הקבצים — עץ אחד מ-`/`

- `/etc` — הגדרות (`/etc/passwd`, `/etc/shadow`)
- `/home` · `/root` — תיקיות בית
- `/var` — לוגים ואתרים (`/var/www`)
- `/tmp` — זמני · `/usr/share/wordlists`

## ניווט

- `pwd` — איפה אני
- `ls -la` — קבצים כולל מוסתרים
- `cd /etc` (מוחלט) · `cd ..` (הורה) · `cd ~` (בית)
- `.` נוכחי · `..` הורה · `~` בית

## קבצים ותיקיות

- `touch` / `mkdir -p` — יצירה
- `cp -r` / `mv` — העתקה/העברה
- `rm -rf` — מחיקה (⚠️ ללא סל מיחזור!)
- `cat` / `less` / `head` / `tail -f`

## עריכה והפניית פלט

- **nano** — פשוט (Ctrl+O שמירה, Ctrl+X יציאה)
- **vim** — `i` עריכה, `:wq` שמירה, `:q!` יציאה
- `>` דורס · `>>` מוסיף בסוף
- `command > out.txt 2>&1`

## הרשאות

- `-rwxr-xr--` : בעלים / קבוצה / כולם
- r=4 · w=2 · x=1 → `chmod 755`
- `chown user:group file`
- 🔍 קובצי **SUID** → הסלמת הרשאות

## sudo והרשאות-על

- **root** = UID 0, יכול הכל
- `sudo <cmd>` — פקודה אחת כ-root
- **`sudo -l`** — מה מותר לי? (בדיקה ראשונה אחרי פריצה)
- `sudo su` — מעטפת root מלאה

## חבילות ושירותים

- `apt update && apt full-upgrade -y`
- `apt install <tool>` · `git clone` + `pip install -r`
- `systemctl start/stop/status/enable <svc>`
- שרת מהיר: `python3 -m http.server 8000`

## פקודות רשת ותהליכים

- `ip a` · `ip route` · `ping -c 4`
- `ss -tuln` — פורטים מאזינים
- `curl` / `wget` / `ssh`
- `ps aux` · `top` · `kill -9 <PID>`

## חיפוש וצינורות (Pipes)

- `find / -perm -4000 2>/dev/null` — SUID
- `grep -r "password" /var/www`
- `|` — פלט אחד → קלט לבא
- `cat passwd | grep root | wc -l`

## סיכום מודול 2

- שולטים בשֶׁל, בקבצים ובעריכה
- הרשאות ו-sudo = מפתח להסלמה
- apt/systemctl/רשת — תשתית העבודה
- find+grep+pipes = כלי הסיור
- **תרגילים** → `missions.md` · **פתרונות** → `solutions.md`
