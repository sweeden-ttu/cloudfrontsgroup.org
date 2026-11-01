#!/usr/bin/env python3
"""
Encode email parts for the click-to-reveal buttons (see site.js `revealEmail`).

    python3 scripts/encode_email.py scottweeden cloudfrontsgroup.org
    python3 scripts/encode_email.py --decode <user_enc> <domain_enc>

Scheme: every character's code point is shifted by +3, then the string is reversed.
Neither the address nor its halves appear anywhere in the HTML, and there is no
mailto: link until the visitor clicks. Paste the two outputs into _data/people.yml
as `email_user_enc` and `email_domain_enc`.
"""
import sys

SHIFT = 3


def encode(s):
    return "".join(chr(ord(c) + SHIFT) for c in s)[::-1]


def decode(s):
    return "".join(chr(ord(c) - SHIFT) for c in s[::-1])


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or len([a for a in args if not a.startswith("--")]) != 2:
        sys.exit(__doc__)
    fn = decode if "--decode" in args else encode
    user, domain = [a for a in args if not a.startswith("--")]
    for part in (user, domain):
        out = fn(part)
        assert '"' not in out and "<" not in out and "&" not in out, "unsafe attribute character"
        print(out)
