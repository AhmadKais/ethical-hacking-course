/* =====================================================================
 *  הדגמת גלישת חוצץ מקומית  —  Local Buffer Overflow Demo  (מודול 10)
 *  תוכנית פגיעה: מעתיקה קלט לחוצץ בן 16 בתים בלי לבדוק אורך (strcpy).
 *  ממש ליד החוצץ בזיכרון יושב המשתנה authenticated. אם תשלח יותר מ-16
 *  בתים — ה"גלישה" תדרוס את authenticated, ותקבל גישה בלי סיסמה!
 *
 *  קומפילציה (הגנות כבויות, כמו בתרגול קלאסי):
 *     gcc -fno-stack-protector -o bof_demo bof_demo.c
 *  הרצה תקינה:   ./bof_demo hello
 *  ניצול:        ./bof_demo AAAAAAAAAAAAAAAAAAAA     (20 תווים)
 * ===================================================================== */
#include <stdio.h>
#include <string.h>

struct data {
    char buffer[16];      /* החוצץ — 16 בתים */
    int  authenticated;   /* יושב מיד אחרי החוצץ בזיכרון */
};

int main(int argc, char **argv) {
    struct data d;
    d.authenticated = 0;                 /* ברירת מחדל: לא מאומת */

    if (argc < 2) {
        printf("usage: %s <input>\n", argv[0]);
        printf("(this program copies your input into a 16-byte buffer)\n");
        return 1;
    }

    /* ❌ החולשה: strcpy אינה בודקת את אורך הקלט */
    strcpy(d.buffer, argv[1]);

    printf("buffer = %s\n", d.buffer);
    printf("authenticated = %d\n", d.authenticated);

    if (d.authenticated != 0) {
        printf("\n[+] Access granted! flag{stack_buffer_overflow_overwrote_the_flag}\n");
    } else {
        printf("\n[-] Access denied. (need authenticated != 0)\n");
    }
    return 0;
}
