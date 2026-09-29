#!/usr/bin/env bash
# =====================================================================
#  מצוד הדגלים של Linux  —  Linux Filesystem CTF  (מודול 2)
#  בונה "שרת שנפרץ" קטן ומבודד בתיקייה ~/linux-ctf, עם 5 דגלים חבויים.
#  תמצא כל דגל באמצעות פקודה שלמדת במודול. כל הפעולות בתוך תיקייה אחת —
#  שום קובץ מערכת אמיתי לא נוגעים בו. בטוח לחלוטין.
#
#  הרצה:     bash linux_ctf.sh
#  איפוס:    bash linux_ctf.sh --reset
#  זירת המשחק:  cd ~/linux-ctf
# =====================================================================
set -euo pipefail
LAB="$HOME/linux-ctf"

if [ "${1:-}" = "--reset" ]; then
    rm -rf "$LAB"
    echo "[*] הזירה אופסה. הרץ שוב בלי --reset כדי לבנות מחדש."
    exit 0
fi

rm -rf "$LAB"
mkdir -p "$LAB"/{etc,var/log,home/webadmin,opt/backup,tmp}
cd "$LAB"

# ── דגל 1: קובץ מוסתר (מתגלה עם ls -la) ─────────────────────────────
echo "flag{hidden_files_start_with_dot}" > "$LAB/home/webadmin/.env_secret"

# ── דגל 2: קבור בתוך קובץ גדול (מתגלה עם grep) ──────────────────────
{
  for i in $(seq 1 200); do echo "log line $i: system running normally"; done
  echo "log line 201: DEBUG password reset token=flag{grep_found_the_needle}"
  for i in $(seq 202 400); do echo "log line $i: system running normally"; done
} > "$LAB/var/log/app.log"

# ── דגל 3: סיסמה בקובץ הגדרות (מתגלה עם grep -r) ────────────────────
cat > "$LAB/etc/config.ini" <<'EOF'
[database]
host = 127.0.0.1
port = 5432
db_password = flag{never_hardcode_secrets}
EOF

# ── דגל 4: "קובץ SUID" — הרשאות חשודות (מתגלה עם find -perm) ─────────
echo '#!/bin/sh'                                  > "$LAB/opt/backup/run_as_root.sh"
echo 'echo flag{suid_is_a_privesc_goldmine}'     >> "$LAB/opt/backup/run_as_root.sh"
chmod 4755 "$LAB/opt/backup/run_as_root.sh" 2>/dev/null || chmod 755 "$LAB/opt/backup/run_as_root.sh"

# ── דגל 5: מקודד ב-Base64 בתוך לוג (מתגלה עם grep | base64 -d) ──────
ENC=$(printf 'flag{base64_is_encoding_not_encryption}' | base64)
echo "auth token (b64): $ENC" > "$LAB/tmp/token.txt"

# רעש/הסחות
echo "nothing to see here" > "$LAB/home/webadmin/notes.txt"
echo "TODO: rotate keys"   > "$LAB/opt/backup/README"

cat <<EOF

============================================================
  🐧  מצוד הדגלים של Linux מוכן!
============================================================
  הזירה:  cd ~/linux-ctf
  יש כאן 5 דגלים חבויים בפורמט  flag{...}
  לכל דגל — פקודה אחת שלמדת במודול תחשוף אותו.

  התחל כך:   cd ~/linux-ctf  &&  ls -la
  איפוס:     bash linux_ctf.sh --reset
============================================================
EOF
