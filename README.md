<div dir="rtl">

# 🛡️ האקינג אתי מהיסוד

**Ethical Hacking from Zero** — קורס מלא בעברית לבדיקות חדירה (Penetration Testing), ממתחילים ועד רמה מקצועית.

מבוסס על מתודולוגיית *Practical Ethical Hacking* של TCM Security, בתוספת מודולים משלימים (Web / OWASP, אלחוט, הסלמת הרשאות, כתיבת דוח) לכיסוי מלא של המקצוע.

---

## 📚 מפת הקורס

הקורס **תואם למסלולי ההסמכה המובילים בעולם** (eJPT · PNPT · OSCP). ראה [טבלת ההתאמה המלאה בסילבוס](SYLLABUS.md#-התאמה-לתקנים-עולמיים).

**חלק א' — יסודות**
| # | מודול | חומר | משימות | מצגת |
|---|-------|:----:|:------:|:----:|
| 1 | [מבוא, המעבדה ומתודולוגיה](modules/01-intro-lab-methodology/) | ✅ | ✅ | ✅ |
| 2 | 🆕 [יסודות Linux](modules/02-linux-fundamentals/) | ✅ | ✅ | ✅ |
| 3 | [יסודות רשתות](modules/03-networking/) | ✅ | ✅ | ✅ |
| 4 | [סקריפטינג: Bash ו-Python](modules/04-scripting-bash-python/) | ✅ | ✅ | ✅ |

**חלק ב' — שרשרת התקיפה**
| # | מודול | חומר | משימות | מצגת |
|---|-------|:----:|:------:|:----:|
| 5 | [איסוף מידע (Reconnaissance)](modules/05-recon/) | ✅ | ✅ | ✅ |
| 6 | [סריקה, מיפוי והערכת חולשות](modules/06-scanning-enumeration/) | ✅ | ✅ | ✅ |
| 7 | [ניצול והשגת גישה (Exploitation)](modules/07-exploitation/) | ✅ | ✅ | ✅ |
| 8 | 🆕 [מתקפות סיסמאות (Password Attacks)](modules/08-password-attacks/) | ✅ | ✅ | ✅ |
| 9 | 🆕 [אבטחת Web — OWASP Top 10](modules/09-web-owasp/) | ✅ | ✅ | ✅ |
| 10 | [Buffer Overflow](modules/10-buffer-overflow/) | 🚧 | 🚧 | 🚧 |

**חלק ג' — לאחר הפריצה ותקיפה פנימית**
| # | מודול | חומר | משימות | מצגת |
|---|-------|:----:|:------:|:----:|
| 11 | 🆕 [פוסט-אקספלויטציה והסלמת הרשאות](modules/11-post-exploitation-privesc/) | 🚧 | 🚧 | 🚧 |
| 12 | 🆕 [Pivoting ותנועה רוחבית](modules/12-pivoting-tunneling/) | 🚧 | 🚧 | 🚧 |
| 13 | [Active Directory](modules/13-active-directory/) | 🚧 | 🚧 | 🚧 |

**חלק ד' — התמחויות ומקצועיות**
| # | מודול | חומר | משימות | מצגת |
|---|-------|:----:|:------:|:----:|
| 14 | 🆕 [תקיפות אלחוטיות (Wireless)](modules/14-wireless/) | 🚧 | 🚧 | 🚧 |
| 15 | 🆕 [הנדסה חברתית ופישינג](modules/15-social-engineering/) | 🚧 | 🚧 | 🚧 |
| 16 | [כתיבת דוח ותיעוד (Reporting)](modules/16-reporting/) | 🚧 | 🚧 | 🚧 |

✅ הושלם · 🚧 בבנייה · 🆕 נוסף להתאמה לתקן העולמי

📄 [**הסילבוס המלא**](SYLLABUS.md) · 🧰 [**מדריך הקמת המעבדה**](resources/lab-setup.md) · 🖥️ [**מדריך מאויר צעד-אחר-צעד**](resources/lab-setup-illustrated.md) · 🏫 [**בקשת התקנה ל-IT (מכללה)**](resources/it-setup-request.md) · 📋 [**דף פקודות מרוכז (Cheat Sheet)**](resources/cheatsheets.md)

🎓 **תרגול והערכה:** 🌍 [דוגמאות מהעולם האמיתי](exam/real-world-examples.md) · 📝 [בנק שאלות תרגול](exam/question-bank.md) · 🏆 [מבחן מעשי (PNPT/OSCP-style)](exam/practical-exam.md)

---

## 🚀 איך להשתמש בקורס

1. **קרא את המודול** — כל מודול הוא תיקייה עם `README.md` (חומר צעד-אחר-צעד).
2. **בצע את המשימות** — קובץ `missions.md` בכל מודול, עם תרגילים מדורגים ואתגר מסכם.
3. **חזור עם המצגת** — קובץ `slides.md` לסיכום מהיר.
4. **תרגל על מכונה חוקית** — [TryHackMe](https://tryhackme.com), [HackTheBox](https://www.hackthebox.com), [VulnHub](https://www.vulnhub.com).

### מבנה כל מודול
```
modules/NN-topic/
├── README.md      # חומר הלימוד (צעד-אחר-צעד, עם דוגמאות)   → material.pdf
├── missions.md    # תרגילים מדורגים (קל→קשה) + אתגר מסכם
├── solutions.md   # פתרונות מלאים צעד-אחר-צעד             → exercises.pdf (missions+solutions)
├── practice.md    # שאלות תרגול (עם תשובות) + תרחיש אמיתי  → practice.pdf
├── slides.md      # מצגת (Markdown, נפתחת ישירות ב-GitHub)
├── slides.pdf     # 🖥️ המצגת כ-PDF — נפתחת ב-GitHub עמוד-אחר-עמוד (להצגה)
└── slides.pptx    # 📊 המצגת ל-PowerPoint (לעריכה והצגה)

# כל קובצי ה-PDF וה-PPTX נמצאים כעת בתוך תיקיית המודול עצמה — הכול במקום אחד.
```

---

## 🧰 דרישות מקדימות

- **חומרה:** 16GB RAM מומלץ (8GB מינימום), ~100GB דיסק פנוי, וירטואליזציה מופעלת ב-BIOS.
- **תוכנה:** [VMware Workstation Player](https://www.vmware.com) או [VirtualBox](https://www.virtualbox.org) (חינמי).
- **ידע קודם:** אין. הקורס מתחיל מאפס.

---

## ⚠️ אזהרה משפטית — קרא לפני שתתחיל

כל הטכניקות בקורס מיועדות **אך ורק** לשימוש בסביבה מבוקרת ומורשית: המעבדה הפרטית שלך, מכונות תרגול ייעודיות, או יעד שקיבלת ממנו **אישור בכתב**.

**תקיפת מערכת ללא רשות היא עבירה פלילית** לפי חוק המחשבים, התשנ"ה-1995. הידע כאן נועד ל**הגנה** ולבדיקות מורשות בלבד. השימוש באחריות הלומד בלבד.

---

## 📈 מסלול המשך והסמכות

מתחילים → **eJPT** · מתקדמים → **PNPT** / **OSCP**

---

*הקורס נבנה כחומר לימוד בעברית. תרומות, תיקונים והצעות — יתקבלו בברכה דרך Issues ו-Pull Requests.*

</div>
