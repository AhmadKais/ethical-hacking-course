<div dir="rtl">

# 🧰 מדריך הקמת המעבדה

מדריך מרוכז להקמת סביבת התרגול לכל הקורס. בצע פעם אחת בתחילת הדרך.

> 🖥️ **גרסה מאוירת צעד-אחר-צעד עם צילומי מסך** (מומלץ לתלמידים על Ubuntu/VirtualBox): [**lab-setup-illustrated.md**](lab-setup-illustrated.md) — כולל פתרון תקלות נפוצות.

---

## דרישות חומרה

| רכיב | מינימום | מומלץ |
|------|---------|-------|
| RAM | 8GB | 16GB+ (חובה למודול AD) |
| דיסק פנוי | 60GB | 100GB+ |
| מעבד | תמיכה בווירטואליזציה (VT-x/AMD-V) מופעלת ב-BIOS | |

---

## 💻 מערכת ההפעלה של המארח (Host OS) — Windows / macOS / Ubuntu

**מערכת ההפעלה שלך לא משנה.** Kali תמיד רצה כ**אורחת (Guest)** בתוך וירטואליזציה, כך שאפשר לארח אותה על **Windows, macOS או Linux (כולל Ubuntu)** באותה צורה בדיוק. כל המעבדה — Kali (התוקף) + מכונות המטרה — רצה כ-VMs על המארח היחיד.

> ✅ **מרצים על Ubuntu:** התקינו **VirtualBox** (חינמי, משתלב מצוין ב-Ubuntu), הריצו את ה-VM של Kali, והציגו לתלמידים בשיתוף מסך — הסביבה זהה ל-1:1 לחומר הקורס.
> ```bash
> sudo apt update && sudo apt install virtualbox -y
> ```
> ⚠️ **אל תוסיפו את מאגרי ה-APT של Kali ל-Ubuntu** — זה עלול לשבור את המערכת. הריצו את Kali כ-VM, לא כמאגר על Ubuntu.

---

## 1. תוכנת וירטואליזציה (Hypervisor)

בחר אחת (שתיהן חינמיות לשימוש אישי):
- **[VirtualBox](https://www.virtualbox.org/)** (**מומלץ בקורס** — חינמי, חוצה-פלטפורמות, מתאים במיוחד למארח Ubuntu/Linux)
- **VMware Workstation Pro** (חלופה — חינמי לשימוש אישי מ-2024)

---

## 2. מכונת התוקף — Kali Linux

1. הורד את דמות ה-VM המוכנה מ-[kali.org/get-kali](https://www.kali.org/get-kali/#kali-virtual-machines) (בחר VMware או VirtualBox).
2. חלץ וטען ב-Hypervisor.
3. הגדרות: 2–4GB RAM, 2 ליבות.
4. התחברות ברירת מחדל: `kali` / `kali`.
5. עדכן מיד:
```bash
sudo apt update && sudo apt full-upgrade -y
```

---

## 3. מכונות המטרה (Targets)

לפי המודול:

| מכונה | שימוש | מקור |
|-------|-------|------|
| **Metasploitable 2** | סריקה, ניצול (מודולים 5–6) | [SourceForge](https://sourceforge.net/projects/metasploitable/) |
| **Kioptrix** | תרגול ניצול מלא | [VulnHub](https://www.vulnhub.com/series/kioptrix,8/) |
| **DVWA / OWASP Juice Shop** | Web / OWASP (מודול 10) | Docker / [OWASP](https://owasp.org/www-project-juice-shop/) |
| **Windows Server + Win10** | מעבדת Active Directory (מודול 8) | [Microsoft Eval Center](https://www.microsoft.com/en-us/evalcenter) |

### הרצת Juice Shop מהיר עם Docker
```bash
sudo apt install docker.io -y
sudo docker run -d -p 3000:3000 bkimminich/juice-shop
# גלוש ל- http://localhost:3000
```

---

## 4. רשת מבודדת — חובה! 🔒

הגדר את מתאם הרשת של **כל** מכונות המעבדה ל-**Host-Only** או **NAT Network**, כך שכל המכונות רואות זו את זו אך מנותקות מהרשת הביתית ומהאינטרנט הישיר.

**בדיקה:** מ-Kali, הרץ `ip a` וודא שאתה בטווח פרטי. נסה `ping` למכונת מטרה במעבדה.

> ⚠️ לעולם אל תריץ כלי תקיפה על מתאם Bridged המחובר לרשת אמיתית.

---

## 5. מכונות תרגול ענן (חלופה/תוספת)

אם אין מספיק משאבים למעבדה מקומית, השתמש בפלטפורמות ענן חוקיות:
- **[TryHackMe](https://tryhackme.com)** — מומלץ למתחילים, מסלולים מודרכים.
- **[HackTheBox](https://www.hackthebox.com)** — מכונות מאתגרות.
- **[VulnHub](https://www.vulnhub.com)** — דמויות VM להורדה.

[⬅️ חזרה למפת הקורס](../README.md)

</div>
