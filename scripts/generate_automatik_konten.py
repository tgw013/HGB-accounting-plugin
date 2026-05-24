"""
Generate config/shared/datev-automatik-konten.json from the clean TSV extracts.

Identifies Automatikkonten via Programmverbindungs-Prefix in column 3.

We flag ONLY {AM, AV} as Automatik for REW00305 purposes:
  - "AM" = Automatikkonto with Mehrwertsteuer-Automatik (Erlöse, Umsatzerlöse, etc.)
  - "AV" = Automatikkonto Vorsteuer-Automatik (Wareneingang + spezifischer Steuersatz)

For both, setting a BU-Schlüssel on a booking against the konto triggers
DATEV import error REW00305 ("Funktion 0 unzulässig, da Konto bereits einen
automatischen Steuerschlüssel enthält"). The exception is BU-Schlüssel "0040"
(Aufhebung der Automatik), which is explicitly allowed.

Other prefixes are deliberately NOT flagged:
  - "S"  = Sammelkonto (Debitoren-Sammel 1200/1400, Kreditoren-Sammel 3300/1600,
           Vorsteuer-/USt-Sammel). These have other rules (e.g. Debitoren-Sammel
           can't be booked directly — must use Personenkonto), but the REW00305
           BU-Schlüssel-clash rule does NOT apply uniformly. Flagging them
           would create false-positive validation errors.
  - "F"  = Festkonto / freies Konto (no automatic)
  - "R"  = Reserviert / Range-Marker (placeholder, not a real konto)
  - "B"  = Bold-rendered Hauptkonto (rendering metadata, not Automatik)

The generated file contains ONLY konto numbers (no bezeichnungen) — DATEV
copyright concerns don't apply to bare digit-numbers + a boolean.

Usage:
  python scripts/generate_automatik_konten.py

Requires the clean TSVs from extract_datev_pdf.py:
  .skr03-clean.tsv  (gitignored, DATEV-copyright bezeichnungen)
  .skr04-clean.tsv  (gitignored, DATEV-copyright bezeichnungen)

Output:
  config/shared/datev-automatik-konten.json  (committed; DATEV-copyright-safe)
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SHARED_DIR = REPO_ROOT / "config" / "shared"

# Programmverbindungs-Prefixes that mark a konto as Automatik for the purpose
# of REW00305 (BU-Schlüssel must not be set, except BU "0040" Aufhebung)
AUTOMATIK_PREFIXES = {"AM", "AV"}

# DATEV's "Aufhebung der Automatik" BU-Schlüssel
BU_AUFHEBUNG = "0040"


def load_tsv_konten(tsv_path: Path) -> list[tuple[str, str]]:
    """Read TSV emitted by extract_datev_pdf.py; return list of (konto, prefix)."""
    out = []
    with tsv_path.open("r", encoding="utf-8") as f:
        next(f)  # skip header line
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                out.append((parts[0], parts[2]))
    return out


def derive_automatik_set(konten: list[tuple[str, str]]) -> dict:
    """Return a dict of {konto: prefix} for all Automatik konten."""
    return {k: p for k, p in konten if p in AUTOMATIK_PREFIXES}


def main():
    skr03_tsv = REPO_ROOT / ".skr03-clean.tsv"
    skr04_tsv = REPO_ROOT / ".skr04-clean.tsv"

    for p in (skr03_tsv, skr04_tsv):
        if not p.exists():
            sys.exit(
                f"ERROR: {p.name} not found. Run scripts/extract_datev_pdf.py "
                "against the DATEV-PDF first."
            )

    skr03_konten = load_tsv_konten(skr03_tsv)
    skr04_konten = load_tsv_konten(skr04_tsv)

    skr03_am = derive_automatik_set(skr03_konten)
    skr04_am = derive_automatik_set(skr04_konten)

    out = {
        "_purpose": (
            "Automatikkonten by SKR. Used by scripts/generate_extf.py to "
            "reject bookings with a non-empty BU-Schlüssel (other than 0040 "
            "Aufhebung) against these konten — prevents DATEV import error REW00305."
        ),
        "_source": (
            "Auto-derived from DATEV-PDF Programmverbindungs-Prefix via "
            "scripts/generate_automatik_konten.py. Prefixes flagged as Automatik: "
            f"{sorted(AUTOMATIK_PREFIXES)}. Re-generate via UPDATE_CHECKLIST §3 "
            "after each yearly DATEV-PDF update."
        ),
        "_generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "_bu_aufhebung": BU_AUFHEBUNG,
        "_counts": {
            "SKR03": len(skr03_am),
            "SKR04": len(skr04_am),
        },
        "automatikkonten": {
            "SKR03": {k: p for k, p in sorted(skr03_am.items())},
            "SKR04": {k: p for k, p in sorted(skr04_am.items())},
        },
    }

    out_path = SHARED_DIR / "datev-automatik-konten.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"wrote {out_path}")
    print(f"  SKR03: {len(skr03_am)} Automatikkonten")
    print(f"  SKR04: {len(skr04_am)} Automatikkonten")


if __name__ == "__main__":
    main()
