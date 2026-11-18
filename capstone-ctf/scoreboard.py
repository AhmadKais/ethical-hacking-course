#!/usr/bin/env python3
"""
ACME Corp engagement — flag scoreboard.

Submit the six flags you recovered (in any order). Tracks progress and tells
you which stage each one proves. No internet, no cheating help — it only
checks what you paste.

    python3 scoreboard.py                 # interactive
    python3 scoreboard.py flag{...} ...   # or pass flags as arguments
"""
import sys

STAGES = [
    ("1. Recon — source/headers disclosure",        "flag{recon_source_disclosure}"),
    ("2. Web — SQL injection auth bypass",           "flag{sqli_auth_bypass}"),
    ("3. Web — command injection RCE (user flag)",   "flag{command_injection_rce}"),
    ("4. Pivot — internal jumpbox access",           "flag{pivot_internal_access}"),
    ("5. PrivEsc — writable cron -> root",           "flag{privesc_writable_cron}"),
    ("6. Domain Admin — NTLM crack",                 "flag{domain_admin_ntlm_crack}"),
]


def grade(submitted):
    found = {flag for flag in submitted}
    got = 0
    print("\n" + "=" * 58)
    print("  ACME CORP — ENGAGEMENT SCOREBOARD")
    print("=" * 58)
    for name, flag in STAGES:
        ok = flag in found
        got += ok
        print(f"  [{'✓' if ok else ' '}] {name}")
    print("-" * 58)
    print(f"  {got}/6 objectives  —  {'🏆 FULL COMPROMISE! Now write the report.' if got == 6 else 'keep going.'}")
    print("=" * 58)
    if got == 6:
        print("  Next: findings-template.md  ->  turn 6 flags into a client report")
        print("  (Module 16). That report is your portfolio centerpiece.\n")
    return got


def main():
    args = [a.strip() for a in sys.argv[1:] if a.strip()]
    if args:
        grade(args)
        return
    print("Paste flags one per line (blank line to grade):")
    subs = []
    try:
        while True:
            line = input("flag> ").strip()
            if not line:
                break
            subs.append(line)
    except (EOFError, KeyboardInterrupt):
        pass
    grade(subs)


if __name__ == "__main__":
    main()
