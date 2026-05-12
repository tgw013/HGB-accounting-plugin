"""
Column-aware DATEV-Kontenrahmen PDF extractor.

The DATEV PDFs (SKR03 Art.-Nr. 11174, SKR04 Art.-Nr. 11175) use a two-column
page layout. Naive `pdftotext -layout` extraction places the columns side-by-side
on the same line, which makes grepping for konto labels unreliable. Worse, many
labels span multiple lines and follow-on accounts inherit a label prefix via a
leading dash (e.g. "1248 Pauschalwertberichtigung auf Forderungen – Restlaufzeit
bis 1 Jahr" / "1249 – Restlaufzeit größer 1 Jahr").

This script:
  1) Splits each page horizontally at the column gap (computed from word x-coords).
  2) Concatenates wrapped label lines into single logical entries per konto.
  3) Resolves leading-dash continuation labels against the most-recent full label.

Output: a clean TSV "konto<TAB>label" file, sorted by konto.

Usage:
  python extract_datev_pdf.py <input.pdf> <output.tsv>
"""
import re
import sys
import pdfplumber

KONTO_RE = re.compile(r"^\s*(?:[A-Z]{1,3}\s+)?(\d{4})\s+(.*)$")
CONT_RE  = re.compile(r"^\s*[–-]\s*(.+)$")


def extract_column_lines(page):
    words = page.extract_words(use_text_flow=False, keep_blank_chars=False)
    if not words:
        return []

    xs = sorted(w["x0"] for w in words)
    midpoint = (xs[0] + xs[-1]) / 2
    left_words  = [w for w in words if w["x0"] <  midpoint]
    right_words = [w for w in words if w["x0"] >= midpoint]

    def group_by_line(ws, y_tol=3):
        ws = sorted(ws, key=lambda w: (round(w["top"] / y_tol), w["x0"]))
        lines, cur, cur_top = [], [], None
        for w in ws:
            if cur_top is None or abs(w["top"] - cur_top) <= y_tol:
                cur.append(w)
                cur_top = w["top"] if cur_top is None else cur_top
            else:
                lines.append(" ".join(x["text"] for x in cur))
                cur, cur_top = [w], w["top"]
        if cur:
            lines.append(" ".join(x["text"] for x in cur))
        return lines

    return group_by_line(left_words) + group_by_line(right_words)


def parse_konten(lines):
    """
    Walk lines, group into (konto, label) tuples.
    A new konto starts on a line beginning with an optional prefix-letter group
    plus 4 digits. Subsequent lines without a konto number are wrap-continuations
    of the most-recent konto label. A label beginning with "– " is a sub-variant
    that inherits the most-recent FULL label prefix (up to but excluding any
    existing dash-suffix).
    """
    konten = {}
    last_konto = None
    last_full_label = None
    base_label = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        m = KONTO_RE.match(line)
        if m:
            konto = m.group(1)
            rest  = m.group(2).strip()

            if CONT_RE.match(rest):
                suffix = CONT_RE.match(rest).group(1).strip()
                label = (base_label + " – " + suffix) if base_label else rest
                last_full_label = label
            else:
                label = rest
                base_label = rest.split(" – ")[0] if " – " in rest else rest
                last_full_label = label

            if konto in konten:
                konten[konto] += " " + label
            else:
                konten[konto] = label
            last_konto = konto
        else:
            if last_konto and last_full_label is not None:
                konten[last_konto] = (konten[last_konto] + " " + line).strip()
                if base_label and " – " not in konten[last_konto]:
                    base_label = konten[last_konto]
                last_full_label = konten[last_konto]

    cleaned = {}
    for k, v in konten.items():
        v = re.sub(r"\s+", " ", v).strip()
        cleaned[k] = v
    return cleaned


def main(in_pdf, out_tsv):
    all_konten = {}
    with pdfplumber.open(in_pdf) as pdf:
        for page in pdf.pages:
            lines = extract_column_lines(page)
            page_konten = parse_konten(lines)
            for k, v in page_konten.items():
                if k not in all_konten:
                    all_konten[k] = v

    with open(out_tsv, "w", encoding="utf-8", newline="\n") as f:
        for k in sorted(all_konten):
            f.write(f"{k}\t{all_konten[k]}\n")

    print(f"wrote {len(all_konten)} konten to {out_tsv}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
