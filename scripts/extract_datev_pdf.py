"""
DATEV-Kontenrahmen PDF extractor — structure-aware (v5).

v5 change: capture the Programmverbindungs-Prefix (F/S/R/KU/AM/U/...) per konto
so callers can identify Automatikkonten (prefix "AM" or "AM-derived" — used by
DATEV to mark accounts with built-in USt-Automatik). Output TSV gains a fourth
column `pv_prefix` (the literal letter prefix, empty if none). Downstream of
this: scripts/generate_extf.py rejects bookings on Automatikkonten with a
non-empty BU-Schlüssel (REW00305 error class).

Models the DATEV-PDF layout:

  Per page: 2 main halves (LHS, RHS), independent konto ranges.
  Per half: 3 sub-columns
    (1) Bilanzposten        — grouping label, drawn as a box spanning multiple konten
    (2) Programmverbindung  — prefix code (F, S, KU, AM, …) with range or single id;
                              may include lone range-markers like "-69" on a row
                              IMPORTANT: prefix "AM" = Automatikkonto (USt-Automatik built in)
    (3) Konto + Bezeichnung — 4-digit konto number, BOLD for main konten, regular
                              for sub-konten; bezeichnungen wrap over 2-4 lines

  Some BOLD entries in sub-column (3) are HEADINGS only (no konto number), e.g.
  "Finanzanlagen". These are NOT konten.

  Konto labels may use DASH-CONTINUATION: a follow-on konto with "– …" inherits
  the prefix of the most-recent full label.

Implementation notes:
  - PyMuPDF returns text as spans. A line may be split across several spans when
    fonts change (e.g. "0810" alone + " " bold + "Ausleihungen an" regular).
  - We treat a konto anchor as ANY span whose stripped text begins with `\\d{4}`,
    optionally followed by a space + rest. Bezeichnung-spans on the same y-line
    as a digit-only anchor are merged in.
  - Bold spans WITHOUT a leading konto, sitting at konto-column-x and visually
    separating konto blocks, are HEADINGS — they break the wrap-continuation
    chain but do not become konten.
  - Pure range-markers (`^-\\d{1,3}$`) are skipped.
  - Footer band (last ~25pt of page height) is excluded.
  - Programmverbindungs-Prefix is captured from the konto-anchor regex's optional
    group; "AM" prefix → Automatikkonto.

Output TSV columns: konto<TAB>bold<TAB>pv_prefix<TAB>bezeichnung
"""
import re
import sys
import fitz


KONTO_ANY  = re.compile(r"^(?:([A-Z]{1,3})\s+)?(\d{4})(?:\s+(.*))?$")
RANGE_MARK = re.compile(r"^-\d{1,3}$")
DASH_CONT  = re.compile(r"^\s*[–-]\s*(.+)$")

KEEP_HYPHEN_BEFORE = {
    "und", "oder", "auf", "im", "in", "der", "die", "des", "vom", "von",
    "zu", "an", "bei", "mit", "aus", "für", "fuer", "über", "ueber",
}

HYPHEN_WRAP = re.compile(r"(\w)-\s+(\w[\wäöüÄÖÜß]*)", re.UNICODE)


def join_hyphenated(text):
    def repl(m):
        prev, nxt = m.group(1), m.group(2)
        if nxt.lower() in KEEP_HYPHEN_BEFORE:
            return f"{prev}- {nxt}"
        return f"{prev}{nxt}"
    return HYPHEN_WRAP.sub(repl, text)

LINE_TOL    = 1.0
FOOTER_PT   = 25.0


def collect_spans(page):
    spans = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for s in line.get("spans", []):
                text = s["text"].strip()
                if not text:
                    continue
                x0, top, x1, bottom = s["bbox"]
                spans.append({
                    "text": text,
                    "x0": x0, "x1": x1,
                    "top": top, "bottom": bottom,
                    "font": s.get("font", ""),
                    "bold": "Bold" in s.get("font", ""),
                })
    return spans


def detect_konto_x_bands(spans, page_width):
    """LHS and RHS konto-column x0 from spans whose text begins with 4 digits."""
    anchors = [s for s in spans if KONTO_ANY.match(s["text"])]
    if not anchors:
        return None, None
    mid = page_width / 2
    lhs = [s["x0"] for s in anchors if s["x0"] < mid]
    rhs = [s["x0"] for s in anchors if s["x0"] >= mid]
    return (min(lhs) if lhs else None,
            min(rhs) if rhs else None)


def extract_half(spans, konto_x, half_right_edge, page_bottom, tol=2.5, gap_pt=4.5):
    """Extract konten from one half (LHS or RHS).

    A 'konto-column span' has x0 in [konto_x − tol, half_right_edge).
    Heading-break heuristics that close the current entry:
      a) Bold span at konto-x (no konto-digit prefix) — section heading
      b) ANY bold span whose top is > gap_pt below the previous wrap's bottom
         (catches "Finanzanlagen" et al. that sit at wrap-x but with a vertical gap)
    """
    if konto_x is None:
        return []

    cutoff = page_bottom - FOOTER_PT
    col = [s for s in spans
           if s["x0"] >= (konto_x - tol)
           and s["x0"] < half_right_edge
           and s["top"] < cutoff
           and not RANGE_MARK.match(s["text"])]
    col.sort(key=lambda s: (s["top"], s["x0"]))

    entries = []
    current = None
    in_heading_break = False
    last_bottom = None

    def flush(c):
        if c is None:
            return
        joined = " ".join(p for p in c["parts"] if p)
        joined = re.sub(r"\s+", " ", joined).strip()
        joined = join_hyphenated(joined)
        c["bezeichnung"] = joined
        entries.append(c)

    for s in col:
        m = KONTO_ANY.match(s["text"])
        if m:
            flush(current)
            in_heading_break = False
            current = {
                "konto":     m.group(2),
                "pv_prefix": (m.group(1) or ""),
                "bold":      s["bold"],
                "parts":     [],
                "top":       s["top"],
            }
            rest = (m.group(3) or "").strip()
            if rest:
                current["parts"].append(rest)
            last_bottom = s["bottom"]
            continue

        if s["bold"] and (
            abs(s["x0"] - konto_x) < tol
            or (last_bottom is not None and (s["top"] - last_bottom) > gap_pt)
        ):
            in_heading_break = True
            continue

        if current is None or in_heading_break:
            continue

        current["parts"].append(s["text"])
        last_bottom = max(last_bottom or 0, s["bottom"])

    flush(current)
    return entries


PREFIX_SPLIT = re.compile(r"\s+[-–]\s+")


def resolve_dash_continuations(entries):
    last_prefix = None
    for e in entries:
        b = e["bezeichnung"]
        m = DASH_CONT.match(b)
        if m and last_prefix:
            e["bezeichnung"] = f"{last_prefix} – {m.group(1).strip()}"
        else:
            last_prefix = PREFIX_SPLIT.split(b, maxsplit=1)[0]
    return entries


def extract_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    ordered = []
    for page in doc:
        page_width  = page.rect.width
        page_height = page.rect.height
        spans = collect_spans(page)
        lhs_x, rhs_x = detect_konto_x_bands(spans, page_width)

        if lhs_x is not None and rhs_x is not None:
            lhs_right = (lhs_x + rhs_x) / 2
            rhs_right = page_width
        elif lhs_x is not None:
            lhs_right = page_width / 2
            rhs_right = page_width
        else:
            lhs_right = page_width / 2
            rhs_right = page_width

        lhs = extract_half(spans, lhs_x, lhs_right, page_height)
        rhs = extract_half(spans, rhs_x, rhs_right, page_height)
        ordered.extend(lhs)
        ordered.extend(rhs)

    ordered = resolve_dash_continuations(ordered)

    by_konto = {}
    for e in ordered:
        k = e["konto"]
        if k not in by_konto:
            by_konto[k] = e
    return by_konto


def main(in_pdf, out_tsv):
    konten = extract_pdf(in_pdf)
    with open(out_tsv, "w", encoding="utf-8", newline="\n") as f:
        f.write("konto\tbold\tpv_prefix\tbezeichnung\n")
        for k in sorted(konten):
            e = konten[k]
            f.write(
                f"{e['konto']}\t{'B' if e['bold'] else ''}\t"
                f"{e.get('pv_prefix', '')}\t{e['bezeichnung']}\n"
            )
    am_count = sum(1 for e in konten.values() if e.get("pv_prefix") == "AM")
    print(f"wrote {len(konten)} konten to {out_tsv} ({am_count} Automatikkonten flagged via AM-prefix)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
