#!/usr/bin/env python3
"""
Multi-county foreclosure notice fetcher for Central Texas counties.

Currently supports Bell County (PDF OCR pipeline).
Extensible for: Coryell, McLennan, Williamson, Burnet, Milam, Lampasas.

Usage:
  python3 scripts/fetch_county_foreclosures.py --county bell
  python3 scripts/fetch_county_foreclosures.py --all
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote, quote_plus

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
USER_AGENT = "Mozilla/5.0 (compatible; CloudFrontsHUD/1.0; +https://cloudfrontsgroup.org)"

COUNTIES: dict[str, dict] = {
    "bell": {
        "name": "Bell",
        "clerk_url": "https://www.bellcountytx.com/county_government/county_clerk/foreclosures.php",
        "base_url": "https://cms3.revize.com/revize/bellcountytx/",
        "pattern": "{month}%20{day}.pdf",
        "batches": [
            ("July", [4, 3, 2, 1]),
            ("June", [8, 7, 6, 5, 4, 3, 2, 1]),
            ("May", [8, 7, 6, 5, 4, 3, 2, 1]),
        ],
        "has_ocr": True,
    },
    "coryell": {
        "name": "Coryell",
        "clerk_url": "https://www.coryellcounty.org/departments/county-clerk/foreclosure-notices/",
        "base_url": "https://www.coryellcounty.org/",
        "pattern": None,
        "batches": [],
        "has_ocr": False,
    },
    "mclennan": {
        "name": "McLennan",
        "clerk_url": "https://www.mclennancountytx.gov/873/Foreclosure-Notices",
        "base_url": None,
        "pattern": None,
        "batches": [],
        "has_ocr": False,
    },
    "williamson": {
        "name": "Williamson",
        "clerk_url": "https://www.wilco.org/departments/county-clerk/foreclosure-notices",
        "base_url": None,
        "pattern": None,
        "batches": [],
        "has_ocr": False,
    },
    "burnet": {
        "name": "Burnet",
        "clerk_url": "https://www.burnetcountytexas.org/departments/county-clerk/",
        "base_url": None,
        "pattern": None,
        "batches": [],
        "has_ocr": False,
    },
    "milam": {
        "name": "Milam",
        "clerk_url": "https://www.milamcountytx.gov/page/milam.county.clerk",
        "base_url": None,
        "pattern": None,
        "batches": [],
        "has_ocr": False,
    },
    "lampasas": {
        "name": "Lampasas",
        "clerk_url": "https://www.lampasas.org/departments/county-clerk/",
        "base_url": None,
        "pattern": None,
        "batches": [],
        "has_ocr": False,
    },
}

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
    r"NATIONSTAR\s+MORTGAGE",
    r"MR\.?\s*COOPER",
    r"PHH\s+MORTGAGE",
    r"ONITY\s+MORTGAGE",
    r"MIDFIRST\s+BANK",
    r"FLAGSTAR\s+BANK",
    r"CALIBER\s+HOME\s+LOANS",
    r"BOKF",
    r"FIRST\s+UNITED\s+BANK\s+AND\s+TRUST",
]

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
]

CITY_RE = (
    r"(?:Killeen|Temple|Belton|Troy|Nolanville|Harker\s*Heights|HARKERHEIGHTS|HARKER|"
    r"Copperas\s*Cove|Salado|Academy|Rogers|Holland|Bartlett|Little\s*River|"
    r"Gatesville|Waco|Georgetown|Round Rock|Cedar Park|Austin|Burnet|"
    r"Cameron|Rockdale|Lampasas)"
)


def download_pdf(url: str, dest: Path) -> tuple[int, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        status = resp.getcode()
        data = resp.read()
    dest.write_bytes(data)
    return status, len(data)


def pdf_to_text(pdf: Path) -> str:
    try:
        r = subprocess.run(
            ["pdftotext", str(pdf), "-"],
            capture_output=True, text=True, timeout=120,
        )
        return r.stdout or ""
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""


def ocr_pdf(pdf: Path, work: Path) -> str:
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    prefix = work / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "200", str(pdf), str(prefix)],
        check=True, capture_output=True, timeout=300,
    )
    images = sorted(work.glob("page-*.png")) or sorted(work.glob("page*.png"))
    parts = []
    for img in images:
        r = subprocess.run(
            ["tesseract", img.name, "stdout", "-l", "eng"],
            cwd=str(work), capture_output=True, text=True, timeout=300,
        )
        if r.stdout:
            parts.append(r.stdout)
    return "\n\n--- PAGE BREAK ---\n\n".join(parts)


def extract_addresses(text: str) -> list[str]:
    items = []

    for pat in [
        r"(?i)(?:Reported\s*Add(?:ress|less|rcss)|Reportcd\s*Adilress|Property\s*Add(?:ress|rcss))\s*:\s*([^\n]+)",
        r"(?i)(?:more\s+commonly\s+referred\s+to\s+as|commonly\s+referred\s+to\s+as)\s*:\s*([^\n]+)",
        r"(?i)commonly known as\s+([^\n]+?765\d{2}[^\n]{0,50}?)(?:,|\s+which|\s+The\s+legal|\.)",
        rf"(?i)\b(\d{{1,6}}\s[^,\n]{{3,90}},\s*{CITY_RE}[^,\n]{{0,50}},\s*(?:TX|Texas)\s*765\d{{2}}(?:-\d{{4}})?)",
    ]:
        for m in re.finditer(pat, text):
            items.append(re.sub(r"\s+", " ", m.group(1)).strip())

    seen = set()
    out = []
    for addr in items:
        if len(addr) < 12:
            continue
        low = addr.lower()
        if any(x in low for x in ("1201 huey", "justice complex")):
            continue
        if not re.search(r"765\d{2}", addr):
            continue
        if not re.match(r"^\d", addr):
            continue
        key = re.sub(r"[^a-z0-9]", "", low)[:120]
        if key in seen or len(key) < 10:
            continue
        seen.add(key)
        out.append(addr)
    out.sort(key=str.lower)
    return out


def extract_entities(text: str) -> dict:
    entities = {"servicers": [], "trustees": [], "noteholders": []}
    for pat in SERVICER_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            val = re.sub(r"\s+", " ", m.group(0)).strip()
            if val not in entities["servicers"]:
                entities["servicers"].append(val)
    for pat in TRUSTEE_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            val = re.sub(r"\s+", " ", m.group(0)).strip()
            if val not in entities["trustees"]:
                entities["trustees"].append(val)
    return entities


def fetch_bell_county() -> list[dict]:
    """Fetch Bell County foreclosure PDFs (existing pipeline)."""
    out_dir = DATA_DIR / "bell_foreclosure_ocr"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    config = COUNTIES["bell"]

    for month, days in config["batches"]:
        for day in days:
            fname = f"{month} {day}.pdf"
            url = config["base_url"] + quote(fname)
            pdf_path = out_dir / f"{month}_{day}.pdf"
            entry = {"month": month, "day": day, "url": url, "county": "Bell"}

            try:
                status, size = download_pdf(url, pdf_path)
                entry["bytes"] = size
            except urllib.error.HTTPError as e:
                entry["error"] = f"HTTP {e.code}"
                results.append(entry)
                print(f"  FAIL {fname}: HTTP {e.code}", file=sys.stderr)
                continue
            except Exception as e:
                entry["error"] = str(e)
                results.append(entry)
                print(f"  FAIL {fname}: {e}", file=sys.stderr)
                continue

            raw_txt = pdf_to_text(pdf_path)
            if len(raw_txt.strip()) < 200:
                with tempfile.TemporaryDirectory(prefix="ocr_") as td:
                    ocr_text = ocr_pdf(pdf_path, Path(td) / "ppm")
                entry["ocr"] = True
                text = ocr_text
            else:
                entry["ocr"] = False
                text = raw_txt

            (out_dir / f"{month}_{day}.txt").write_text(text, errors="replace")
            entry["text_chars"] = len(text)
            entry["addresses"] = extract_addresses(text)
            entry["entities"] = extract_entities(text)
            entry["address_count"] = len(entry["addresses"])
            results.append(entry)
            print(f"  OK {fname}: {size} bytes, {entry['address_count']} addresses")

    return results


def fetch_county(county_key: str) -> list[dict]:
    config = COUNTIES.get(county_key)
    if not config:
        print(f"Unknown county: {county_key}", file=sys.stderr)
        return []

    print(f"\nFetching {config['name']} County...")
    if county_key == "bell":
        return fetch_bell_county()

    print(f"  {config['name']} County: manual setup required. See clerk page:")
    print(f"  {config['clerk_url']}")
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch county foreclosure notices")
    parser.add_argument("--county", choices=list(COUNTIES.keys()), help="Specific county to fetch")
    parser.add_argument("--all", action="store_true", help="Fetch all available counties")
    args = parser.parse_args()

    if args.all:
        for key in COUNTIES:
            fetch_county(key)
    elif args.county:
        fetch_county(args.county)
    else:
        print("Specify --county <name> or --all")
        print(f"Available: {', '.join(COUNTIES.keys())}")
        return 1

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
