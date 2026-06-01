#!/usr/bin/env python3
"""
Download Bell County Revize foreclosure notice PDFs, OCR (image PDFs), and parse addresses.

URL pattern (per user):
  https://cms3.revize.com/revize/bellcountytx/{Month}%20{day}.pdf

Batches (order requested):
  1) July 4 down through July 1
  2) May 8 down through May 1
  3) June 8 down through June 1
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote

BASE = "https://cms3.revize.com/revize/bellcountytx/"
USER_AGENT = "Mozilla/5.0 (compatible; CloudFrontsHUD/1.0; +https://example.invalid)"

# (month_name, list of day integers in download order)
BATCHES: list[tuple[str, list[int]]] = [
    ("July", [4, 3, 2, 1]),
    ("May", [8, 7, 6, 5, 4, 3, 2, 1]),
    ("June", [8, 7, 6, 5, 4, 3, 2, 1]),
]

SCRIPT_DIR = Path(__file__).resolve().parent
OUT_DIR = SCRIPT_DIR.parent / "data" / "bell_foreclosure_ocr"
EXCLUDE = (
    "1201 huey",
    "huey drive",
    "justice complex",
    "6101 southwest",
    "houston",
    "west des moines",
    "mac 2301",
    "wells fargo",
    "mortgage servicer",
)

CITY_RE = (
    r"(?:Killeen|Temple|Belton|Troy|Nolanville|Harker\s*Heights|HARKERHEIGHTS|HARKER|"
    r"Copperas\s*Cove|Salado|Academy|Rogers|Holland|Bartlett|Little\s*River)"
)


def download(url: str, dest: Path) -> tuple[int, int]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        status = resp.getcode()
        data = resp.read()
    dest.write_bytes(data)
    return status, len(data)


def pdf_to_text_pdftotext(pdf: Path) -> str:
    try:
        r = subprocess.run(
            ["pdftotext", str(pdf), "-"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        return r.stdout or ""
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return ""


def ocr_pdf(pdf: Path, work: Path) -> str:
    """Rasterize with pdftoppm, then tesseract each page (cwd = image dir)."""
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    prefix = work / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "200", str(pdf), str(prefix)],
        check=True,
        capture_output=True,
        timeout=300,
    )
    images = sorted(work.glob("page-*.png"))
    if not images:
        images = sorted(work.glob("page*.png"))
    parts: list[str] = []
    for img in images:
        r = subprocess.run(
            ["tesseract", img.name, "stdout", "-l", "eng"],
            cwd=str(work),
            capture_output=True,
            text=True,
            timeout=300,
        )
        if r.stdout:
            parts.append(r.stdout)
    return "\n\n--- PAGE BREAK ---\n\n".join(parts)


def norm_city(s: str) -> str:
    s = re.sub(r"(?i)harker\s*heights", "Harker Heights", s)
    s = re.sub(r"(?i)harkerheights", "Harker Heights", s)
    s = re.sub(r"(?i)kii?j\.?een", "Killeen", s)
    s = re.sub(r"(?i)\bkillen\b", "Killeen", s)
    s = re.sub(r"(?i)temole|temfi\.?e|fanpfe", "Temple", s)
    return s


def extract_addresses(text: str) -> list[str]:
    items: list[str] = []

    label_pat = re.compile(
        r"(?i)(?:Reported\s*Add(?:ress|less|rcss)|Reportcd\s*Adilress|Property\s*Add(?:ress|rcss))\s*:\s*([^\n]+)",
    )
    for m in label_pat.finditer(text):
        items.append(_clean(m.group(1)))

    ref_pat = re.compile(
        r"(?i)(?:more\s+commonly\s+referred\s+to\s+as|commonly\s+referred\s+to\s+as)\s*:\s*([^\n]+)",
    )
    for m in ref_pat.finditer(text):
        items.append(_clean(m.group(1)))

    cka_pat = re.compile(
        r"(?i)commonly known as\s+([^\n]+?765\d{2}[^\n]{0,50}?)(?:,|\s+which|\s+The\s+legal|\.)",
    )
    for m in cka_pat.finditer(text):
        items.append(_clean(m.group(1)))

    two_comma = re.compile(
        rf"(?i)\b(\d{{1,6}}\s[^,\n]{{3,90}},\s*{CITY_RE}[^,\n]{{0,50}},\s*(?:TX|Texas)\s*765\d{{2}}(?:-\d{{4}})?)",
    )
    for m in two_comma.finditer(text):
        items.append(_clean(m.group(1)))

    seen: set[str] = set()
    out: list[str] = []
    for addr in items:
        addr = norm_city(_clean(addr))
        if len(addr) < 12:
            continue
        low = addr.lower()
        if any(x in low for x in EXCLUDE):
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


def _clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r",\s*which$", "", s, flags=re.I)
    return s


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []

    for month, days in BATCHES:
        for day in days:
            fname = f"{month} {day}.pdf"
            url = BASE + quote(fname)
            pdf_path = OUT_DIR / f"{month}_{day}.pdf"
            entry: dict = {"month": month, "day": day, "url": url, "pdf": str(pdf_path)}
            try:
                status, size = download(url, pdf_path)
                entry["http_status"] = status
                entry["bytes"] = size
            except urllib.error.HTTPError as e:
                entry["error"] = f"HTTP {e.code}"
                results.append(entry)
                print(f"FAIL {month} {day}: HTTP {e.code}", file=sys.stderr)
                continue
            except Exception as e:
                entry["error"] = str(e)
                results.append(entry)
                print(f"FAIL {month} {day}: {e}", file=sys.stderr)
                continue

            raw_txt = pdf_to_text_pdftotext(pdf_path)
            if len(raw_txt.strip()) < 200:
                with tempfile.TemporaryDirectory(prefix="bellocr_") as td:
                    work = Path(td)
                    try:
                        ocr_text = ocr_pdf(pdf_path, work / "ppm")
                    except Exception as e:
                        entry["ocr_error"] = str(e)
                        ocr_text = ""
                entry["ocr"] = True
                text = ocr_text
            else:
                entry["ocr"] = False
                text = raw_txt

            (OUT_DIR / f"{month}_{day}.txt").write_text(text, errors="replace")
            entry["text_chars"] = len(text)
            addrs = extract_addresses(text)
            entry["addresses"] = addrs
            entry["address_count"] = len(addrs)
            results.append(entry)
            print(f"OK {month} {day}: {size} bytes, {len(addrs)} addresses")

    summary_path = OUT_DIR / "results.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    # Human-readable summary
    lines = ["# Bell County foreclosure PDFs — OCR address parse\n"]
    for r in results:
        lines.append(f"\n## {r.get('month')} {r.get('day')}\n")
        lines.append(f"- URL: `{r.get('url')}`\n")
        if r.get("error"):
            lines.append(f"- **Error:** {r['error']}\n")
            continue
        lines.append(f"- Bytes: {r.get('bytes')} | OCR: {r.get('ocr')} | chars: {r.get('text_chars')}\n")
        for a in r.get("addresses") or []:
            lines.append(f"  - {a}\n")
    (OUT_DIR / "RESULTS.md").write_text("".join(lines), encoding="utf-8")

    print(f"\nWrote {summary_path} and {OUT_DIR / 'RESULTS.md'}")

    build = Path(__file__).resolve().parent / "build_foreclosures_page.py"
    try:
        subprocess.run([sys.executable, str(build)], check=False, timeout=60)
    except Exception as e:
        print(f"Note: could not rebuild foreclosures.html: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
