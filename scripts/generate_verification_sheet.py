"""
Generates a side-by-side TSV for human spot-check:

  konto | rahmen | v2-bezeichnung (paraphrased) | PDF-bezeichnung (extracted) | bold

Open in Excel: File → Open → konten-verification.tsv → Delimited → Tab.

Usage:
  python scripts/generate_verification_sheet.py
"""
import json


def load_tsv(p):
    rows = {}
    with open(p, encoding="utf-8") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                rows[parts[0]] = {"bold": parts[1], "bez": parts[2]}
    return rows


def main():
    data = json.load(open("config/2026/kontenrahmen.json", encoding="utf-8"))
    skr03 = load_tsv(".skr03-clean.tsv")
    skr04 = load_tsv(".skr04-clean.tsv")
    sources = {"SKR03": skr03, "SKR04": skr04}

    out = ["konto\trahmen\tbold\tv2_bezeichnung_paraphrased\tpdf_bezeichnung_extracted"]
    for rahmen in ("SKR03", "SKR04"):
        konten = data[rahmen]["haeufige_konten"]
        rows = []
        for key, val in konten.items():
            if not (isinstance(val, dict) and "konto" in val):
                continue
            k = val["konto"]
            v2 = val.get("bezeichnung", "")
            pdf = sources[rahmen].get(k, {})
            rows.append((k, rahmen, pdf.get("bold", ""), v2, pdf.get("bez", "<NOT FOUND>")))
        rows.sort(key=lambda r: r[0])
        for r in rows:
            out.append("\t".join(r))

    with open("konten-verification.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote konten-verification.tsv  ({len(out) - 1} konten)")


if __name__ == "__main__":
    main()
