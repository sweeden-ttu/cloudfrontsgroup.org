#!/usr/bin/env python3
"""
Parse Bell County OCR text files to extract foreclosure entities:
- Mortgage Servicer
- Substitute Trustee (law firm / trustee company)
- Noteholder / Mortgagee
- Original Trustee
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "bell_foreclosure_ocr"
RESULTS_JSON = DATA_DIR / "results.json"
OUT_JSON = DATA_DIR / "results_enhanced.json"

# Known mortgage servicers
SERVICER_PATTERNS = [
    r"PENNYMAC\s+LOAN\s+SERVICES?\s*,?\s*LLC",
    r"LAKEVIEW\s+LOAN\s+SERVICING\s*,?\s*LLC",
    r"LOANCARE\s*,?\s*LLC",
    r"CARRINGTON\s+MORTGAGE\s+SERVICES?\s*,?\s*LLC",
    r"FREEDOM\s+MORTGAGE\s+CORP(?:ORATION)?",
    r"SERVICEMAC",
    r"M\s*&\s*T\s+BANK",
    r"NEWREZ\s*,?\s*LLC",
    r"SHELLPOINT\s+MORTGAGE\s+SERVICING",
    r"SPECIALIZED\s+LOAN\s+SERVICING",
    r"NATIONSTAR\s+MORTGAGE",
    r"MR\.?\s*COOPER",
    r"PHH\s+MORTGAGE",
    r"ONITY\s+MORTGAGE",
    r"MIDFIRST\s+BANK",
    r"FLAGSTAR\s+BANK",
    r"CALIBER\s+HOME\s+LOANS",
    r"BOKF",
    r"SELECT\s+PORTFOLIO\s+SERVICING",
    r"BAYVIEW\s+LOAN\s+SERVICING",
    r"FIRST\s+UNITED\s+BANK\s+AND\s+TRUST",
]

# Known substitute trustee law firms / trustee companies
TRUSTEE_PATTERNS = [
    r"BARRETT\s+DAFFIN\s+FRAPPIER\s+TURNER\s*&\s*ENGEL\s*,?\s*LLP",
    r"DE\s+CUBAS\s*&\s*LEWIS\s*,?\s*P\.?\s*C\.",
    r"MARINOSCI\s+LAW\s+GROUP\s*,?\s*P\.?\s*C\.",
    r"MCCARTHY\s*&\s*HOLTHUS\s*,?\s*LLP",
    r"CODILIS\s*&\s*MOODY\s*,?\s*P\.?\s*C\.",
    r"AUCTION\.COM\s*,?\s*LLC",
    r"RESOLVE\s+TRUSTEE\s+SERVICES\s*,?\s*LLC",
    r"XOME\s+INC\.",
    r"AGENCY\s+SALES\s+AND\s+POSTING\s+LLC",
    r"PRESTIGE\s+POSTING\s+AND\s+PUBLISHING\s*,?\s*LLC",
    r"TEJAS\s+CORPORATE\s+SERVICES\s+LLC",
    r"NFPDS-TX\s+LLC",
    r"NESTOR\s+SOLUTIONS\s*,?\s*LLC",
    r"VYLLA\s+SOLUTIONS\s*,?\s*LLC",
    r"SHAPIRO\s+VAN\s+TURNBL",
    r"ZWICKER\s*&\s*ASSOCIATES",
    r"BKFS\s*,?\s*LLC",
    r"MACKIE\s+WOLF\s+ZIEN\s+&",
]

# Known noteholders / mortgagees
NOTEHOLDER_PATTERNS = [
    r"PENNYMAC\s+LOAN\s+SERVICES?\s*,?\s*LLC",
    r"LAKEVIEW\s+LOAN\s+SERVICING\s*,?\s*LLC",
    r"CARRINGTON\s+MORTGAGE\s+SERVICES?\s*,?\s*LLC",
    r"FREEDOM\s+MORTGAGE\s+CORP(?:ORATION)?",
    r"FIRST\s+UNITED\s+BANK\s+AND\s+TRUST",
    r"MORTGAGE\s+ELECTRONIC\s+REGISTRATION\s+SYSTEMS?\s*,?\s*INC",
]


def canonical_entity(val: str) -> str:
    """Convert any variant to a canonical display form."""
    v = re.sub(r"\s+", " ", val).strip()
    v = v.rstrip(".,;:")
    # Title-case known names
    replacements = [
        ("PENNYMAC LOAN SERVICES, LLC", "PennyMac Loan Services, LLC"),
        ("LAKEVIEW LOAN SERVICING, LLC", "Lakeview Loan Servicing, LLC"),
        ("LAKEVIEW LOAN SERVICING LLC", "Lakeview Loan Servicing, LLC"),
        ("LOANCARE, LLC", "LoanCare, LLC"),
        ("CARRINGTON MORTGAGE SERVICES, LLC", "Carrington Mortgage Services, LLC"),
        ("FREEDOM MORTGAGE CORPORATION", "Freedom Mortgage Corporation"),
        ("BARRETT DAFFIN FRAPPIER TURNER & ENGEL, LLP", "Barrett Daffin Frappier Turner & Engel, LLP"),
        ("DE CUBAS & LEWIS, P.C.", "De Cubas & Lewis, P.C."),
        ("MARINOSCI LAW GROUP, PC.", "Marinosci Law Group, P.C."),
        ("MARINOSCI LAW GROUP, P.C.", "Marinosci Law Group, P.C."),
        ("MCCARTHY & HOLTHUS, LLP", "McCarthy & Holthus, LLP"),
        ("CODILIS & MOODY, P.C.", "Codilis & Moody, P.C."),
        ("AUCTION.COM, LLC", "Auction.com, LLC"),
        ("AUCTION.COM LLC", "Auction.com, LLC"),
        ("AUCTION.COM LLC", "Auction.com, LLC"),
        ("AGENCY SALES AND POSTING LLC", "Agency Sales and Posting LLC"),
        ("RESOLVE TRUSTEE SERVICES, LLC", "Resolve Trustee Services, LLC"),
        ("XOME INC.", "Xome Inc."),
        ("XOME INC", "Xome Inc."),
        ("VYLLA SOLUTIONS, LLC", "Vylla Solutions, LLC"),
        ("NESTOR SOLUTIONS, LLC", "Nestor Solutions, LLC"),
        ("NFPDS-TX LLC", "NFPDS-TX LLC"),
        ("PRESTIGE POSTING AND PUBLISHING, LLC", "Prestige Posting and Publishing, LLC"),
        ("TEJAS CORPORATE SERVICES LLC", "Tejas Corporate Services LLC"),
        ("FIRST UNITED BANK AND TRUST", "First United Bank and Trust"),
        ("MORTGAGE ELECTRONIC REGISTRATION SYSTEMS, INC", "Mortgage Electronic Registration Systems, Inc. (MERS)"),
        ("SERVICEMAC", "ServiceMac"),
        ("SHELLPOINT MORTGAGE SERVICING", "Shellpoint Mortgage Servicing"),
        ("NEWREZ LLC", "NewRez LLC"),
        ("NEWREZ, LLC", "NewRez LLC"),
        ("NATIONSTAR MORTGAGE", "Nationstar Mortgage"),
        ("ONITY MORTGAGE", "Onity Mortgage"),
        ("PHH MORTGAGE", "PHH Mortgage"),
        ("M & T BANK", "M&T Bank"),
        ("M&T BANK", "M&T Bank"),
        ("MIDFIRST BANK", "MidFirst Bank"),
        ("CALIBER HOME LOANS", "Caliber Home Loans"),
        ("P.C.", "P.C."),
    ]
    vu = v.upper()
    for old, new in replacements:
        if vu == old:
            return new
    # Fix common abbr capitalization
    v = re.sub(r'\bP\.?\s*C\.?\b', 'P.C.', v, flags=re.I)
    v = re.sub(r'\bLLP\b', 'LLP', v, flags=re.I)
    v = re.sub(r'\bLLC\b', 'LLC', v, flags=re.I)
    v = re.sub(r'\bINC\b', 'Inc.', v, flags=re.I)
    v = re.sub(r'\bPC\b', 'P.C.', v, flags=re.I)
    # Fallback: title case each word
    return " ".join(w[0].upper() + w[1:].lower() if len(w) > 1 else w.upper() for w in v.split())


def dedup_entities(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        canon = canonical_entity(item)
        key = canon.upper()
        if key not in seen:
            seen.add(key)
            result.append(canon)
    return result


def extract_entities(text: str) -> dict:
    entities = {
        "servicers": [],
        "trustees": [],
        "noteholders": [],
        "original_trustees": [],
        "substitute_trustee_individuals": [],
    }

    # Extract mortgage servicers
    for pat in SERVICER_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            val = m.group(0).strip()
            # Normalize
            val = re.sub(r"\s+", " ", val)
            if val not in entities["servicers"]:
                entities["servicers"].append(val)

    # Extract substitute trustees (law firms)
    for pat in TRUSTEE_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            val = m.group(0).strip()
            val = re.sub(r"\s+", " ", val)
            if val not in entities["trustees"]:
                entities["trustees"].append(val)

    # Extract noteholders
    for pat in NOTEHOLDER_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            val = m.group(0).strip()
            val = re.sub(r"\s+", " ", val)
            if val not in entities["noteholders"]:
                entities["noteholders"].append(val)

    # Extract original trustee (often after "Original Trustee:" or "as Trustee")
    orig_pat = re.compile(r"Original\s+Trustee:\s*([A-Z][A-Z\s.]+?)(?:\s*Recorded|\s*Substitute|\s*\n|\s*$)", re.IGNORECASE)
    for m in orig_pat.finditer(text):
        val = m.group(1).strip()
        if val and len(val) > 3 and val not in entities["original_trustees"]:
            entities["original_trustees"].append(val)

    # Extract individual substitute trustees named (people)
    indiv_pat = re.compile(
        r"(?:Michelle\s+Jones|Angela\s+Zavala|Sharlet\s+Watts|Richard\s+Zavala|"
        r"Violet\s+Nunez|Kristopher\s+Holub|Ramiro\s+Cuevas|Aarti\s+Patel|"
        r"Jami\s+Grady|Thalia\s+Toler|Joshua\s+Sanders|Aleena\s+Litton|"
        r"Jacqualine\s+Hughes|Travis\s+Kaddatz|Dustin\s+George|Sammy\s+Hooda)",
        re.IGNORECASE,
    )
    for m in indiv_pat.finditer(text):
        val = m.group(0).strip()
        # Normalize capitalization
        parts = val.split()
        normalized = " ".join(p.capitalize() for p in parts)
        if normalized not in entities["substitute_trustee_individuals"]:
            entities["substitute_trustee_individuals"].append(normalized)

    entities["servicers"] = dedup_entities(entities["servicers"])
    entities["trustees"] = dedup_entities(entities["trustees"])
    entities["noteholders"] = dedup_entities(entities["noteholders"])
    entities["original_trustees"] = dedup_entities(entities["original_trustees"])
    entities["substitute_trustee_individuals"] = dedup_entities(entities["substitute_trustee_individuals"])
    return entities


def main() -> int:
    if not RESULTS_JSON.exists():
        print(f"Error: {RESULTS_JSON} not found", file=sys.stderr)
        return 1

    base_data = json.loads(RESULTS_JSON.read_text("utf-8"))
    enhanced = []

    for entry in base_data:
        month = entry.get("month", "")
        day = entry.get("day", 0)
        txt_path = DATA_DIR / f"{month}_{day}.txt"

        entities = {"servicers": [], "trustees": [], "noteholders": [], "original_trustees": [], "substitute_trustee_individuals": []}

        if txt_path.exists():
            text = txt_path.read_text("utf-8", errors="replace")
            entities = extract_entities(text)

        enhanced_entry = dict(entry)
        enhanced_entry["entities"] = entities
        enhanced.append(enhanced_entry)

    OUT_JSON.write_text(json.dumps(enhanced, indent=2), "utf-8")
    print(f"Wrote {OUT_JSON} ({len(enhanced)} entries with entities)")

    # Print summary
    all_servicers = set()
    all_trustees = set()
    all_noteholders = set()
    for e in enhanced:
        for s in e.get("entities", {}).get("servicers", []):
            all_servicers.add(s)
        for t in e.get("entities", {}).get("trustees", []):
            all_trustees.add(t)
        for n in e.get("entities", {}).get("noteholders", []):
            all_noteholders.add(n)

    print(f"\n=== Unique Mortgage Servicers ({len(all_servicers)}) ===")
    for s in sorted(all_servicers):
        print(f"  - {s}")

    print(f"\n=== Unique Substitute Trustees / Law Firms ({len(all_trustees)}) ===")
    for t in sorted(all_trustees):
        print(f"  - {t}")

    print(f"\n=== Unique Noteholders ({len(all_noteholders)}) ===")
    for n in sorted(all_noteholders):
        print(f"  - {n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
