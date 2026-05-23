"""
Deterministic DATEV-Format EXTF Buchungsstapel CSV serializer.

Implements PRD v1.2 (PRD-deterministic-extf-serializer.md) §1-§9.

Replaces inline LLM CSV generation in the `datev-export` skill with a
byte-deterministic Python implementation. Same input JSON → identical CSV
output across runs, machines, and Python 3.10+ versions.

Spec source: developer.datev.de, Formatkategorie 21 Buchungsstapel
Formatversion 13. Field inventory loaded from
config/shared/datev-extf-fields.json (31 header fields + 125 data columns,
PORTAL-verified 2026-05-22).

Architecture per PRD §8:
    input.json  →  parse + validate  →  CSV (CP1252 + CRLF) + sidecar .report.md

Usage:
    python scripts/generate_extf.py \
        --input /path/to/buchungen.json \
        --output /path/to/EXTF_buchungsstapel.csv \
        [--format-version 13] \
        [--encoding cp1252]

The .report.md sidecar is written next to the CSV automatically.

No third-party dependencies. Python 3.10+ stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
FIELDS_JSON = REPO_ROOT / "config" / "shared" / "datev-extf-fields.json"

DEFAULT_FORMAT_VERSION = 13
DEFAULT_ENCODING = "cp1252"
SUPPORTED_ENCODINGS = {"cp1252", "utf-8-sig"}

# DATEV CSV conventions
FIELD_SEPARATOR = ";"
LINE_ENDING = "\r\n"

# Per PRD §6: row-2 column-header overrides (Einstieg example deviates from field-table Überschrift)
ROW2_OVERRIDES = {
    1: "Umsatz (ohne Soll/Haben-Kz)",
    8: "Gegenkonto (ohne BU-Schlüssel)",
}

# SKR input → portal output mapping (header field #27 Sachkontenrahmen)
SKR_TO_SACHKONTENRAHMEN = {
    "SKR03": "03",
    "SKR04": "04",
    "SKR07": "07",
    "SKR14": "14",
}


# ---------------------------------------------------------------------------
# Custom errors
# ---------------------------------------------------------------------------

class ExtfSerializerError(Exception):
    """Base error for the serializer."""


class InputValidationError(ExtfSerializerError):
    """Input JSON failed validation."""


class FieldValidationError(ExtfSerializerError):
    """A field value failed its regex / business rule."""


class SaldoError(ExtfSerializerError):
    """Σ Soll != Σ Haben."""


class EncodingError(ExtfSerializerError):
    """A character cannot be encoded in the target codec."""


# ---------------------------------------------------------------------------
# Field-inventory loader
# ---------------------------------------------------------------------------

def load_field_inventory(format_version: int) -> dict:
    """Load and return the buchungsstapel field inventory for the given Formatversion."""
    with FIELDS_JSON.open("r", encoding="utf-8") as f:
        inventory = json.load(f)
    fv_key = str(format_version)
    if fv_key not in inventory["buchungsstapel"]:
        raise InputValidationError(
            f"Formatversion {format_version} not in inventory. "
            f"Available: {sorted(inventory['buchungsstapel'].keys())}"
        )
    return inventory["buchungsstapel"][fv_key]


# ---------------------------------------------------------------------------
# Per-field formatters
# ---------------------------------------------------------------------------

# Belegfeld 1/2 character whitelist per portal regex: word chars + $&%*+-/
_BELEGFELD_RE = re.compile(r"^[\w$&%*+\-/]{0,36}$", re.UNICODE)


def _format_quoted_empty_or_text(value: Any, max_len: int | None = None) -> str:
    """Text field: emit as quoted; empty value emits as bare empty-quoted "" ."""
    if value is None or value == "":
        return '""'
    s = str(value)
    if max_len is not None and len(s) > max_len:
        raise FieldValidationError(
            f"Text field exceeds max length {max_len}: {s[:30]}... ({len(s)} chars)"
        )
    # Escape internal double-quotes per RFC 4180 (DATEV convention per portal #20 example)
    escaped = s.replace('"', '""')
    return f'"{escaped}"'


def _format_numeric_optional(value: Any) -> str:
    """Numeric optional field: empty emits as bare nothing; non-empty as raw digits."""
    if value is None or value == "":
        return ""
    return str(value)


def _format_quoted_text_required(value: Any, max_len: int) -> str:
    """Text field that must always be present (header) — empty allowed if max_len permits."""
    if value is None:
        value = ""
    s = str(value)
    if len(s) > max_len:
        raise FieldValidationError(
            f"Text field exceeds max length {max_len}: {s} ({len(s)} chars)"
        )
    escaped = s.replace('"', '""')
    return f'"{escaped}"'


def _format_umsatz(value: Any) -> str:
    """Field #1 Umsatz: max 10 integer digits + comma + exactly 2 decimal digits; >0,00."""
    if value is None or value == "":
        raise FieldValidationError("Umsatz darf nicht leer sein")
    s = str(value)
    if not re.fullmatch(r"\d{1,10}\,\d{2}", s):
        raise FieldValidationError(
            f"Umsatz '{s}' verletzt Format ^\\d{{1,10}}\\,\\d{{2}}$ (z.B. 12100,00)"
        )
    if re.fullmatch(r"0{1,10}\,00", s):
        raise FieldValidationError("Umsatz 0,00 ist unzulässig (portal-Regel)")
    return s


def _format_soll_haben(value: Any) -> str:
    """Field #2 Soll/Haben-Kennzeichen: S or H, quoted."""
    if value not in ("S", "H"):
        raise FieldValidationError(f"Soll/Haben-Kennzeichen muss S oder H sein, war: {value}")
    return f'"{value}"'


def _format_wkz(value: Any, default: str = "EUR") -> str:
    """Field #3 WKZ Umsatz / header #22 WKZ: 3 uppercase letters, quoted. Empty → default."""
    if value is None or value == "":
        value = default
    s = str(value).upper()
    if not re.fullmatch(r"[A-Z]{3}", s):
        raise FieldValidationError(f"WKZ '{value}' muss 3-stelliger ISO-Code sein")
    return f'"{s}"'


def _format_konto(value: Any, sachkonten_laenge: int, field_label: str = "Konto") -> str:
    """Fields #7 Konto / #8 Gegenkonto: max sachkonten_laenge digits (Sachkonto) or +1 (Personenkonto)."""
    if value is None or value == "":
        raise FieldValidationError(f"{field_label} darf nicht leer sein")
    s = str(value)
    if not re.fullmatch(r"\d{1,9}", s):
        raise FieldValidationError(f"{field_label} '{s}' muss 1-9 Ziffern sein")
    if re.fullmatch(r"0{1,9}", s):
        raise FieldValidationError(f"{field_label} '{s}' darf nicht nur aus Nullen bestehen")
    if len(s) > sachkonten_laenge + 1:
        raise FieldValidationError(
            f"{field_label} '{s}' ({len(s)} Ziffern) überschreitet "
            f"Sachkontenlänge {sachkonten_laenge} + 1 (Personenkonto)"
        )
    return s


def _format_bu_schluessel(value: Any) -> str:
    """Field #9 BU-Schlüssel: 4-digit zero-padded, quoted. Empty allowed (Automatikkonto)."""
    if value is None or value == "":
        return ""
    s = str(value).strip()
    if not s:
        return ""
    if not re.fullmatch(r"\d{1,4}", s):
        raise FieldValidationError(f"BU-Schlüssel '{s}' muss 1-4 Ziffern sein")
    padded = s.zfill(4)
    return f'"{padded}"'


def _format_belegdatum(value: Any) -> str:
    """Field #10 Belegdatum: exactly 4 digits TTMM (Tag + Monat)."""
    if value is None or value == "":
        return ""
    s = str(value)
    if not re.fullmatch(r"\d{4}", s):
        raise FieldValidationError(
            f"Belegdatum '{s}' muss exakt 4-stellig TTMM sein (z.B. 3004 für 30. April)"
        )
    tag = int(s[:2])
    monat = int(s[2:])
    if not (1 <= tag <= 31) or not (1 <= monat <= 12):
        raise FieldValidationError(f"Belegdatum '{s}' hat ungültigen Tag/Monat")
    return s


def _format_belegfeld(value: Any, field_label: str = "Belegfeld") -> str:
    """Fields #11/#12 Belegfeld 1/2: word chars + $&%*+-/, max 36, quoted."""
    if value is None or value == "":
        return ""
    s = str(value)
    if len(s) > 36:
        raise FieldValidationError(
            f"{field_label} '{s}' überschreitet 36 Zeichen ({len(s)} Zeichen)"
        )
    if not _BELEGFELD_RE.match(s):
        raise FieldValidationError(
            f"{field_label} '{s}' enthält unzulässige Zeichen. "
            "Erlaubt: Buchstaben/Ziffern/_ + $ & % * + - / . "
            "VERBOTEN: Leerzeichen, Umlaute, Punkt, Komma, Semikolon, Doppelpunkt"
        )
    return f'"{s}"'


def _format_buchungstext(value: Any) -> str:
    """Field #14 Buchungstext: 0-60 chars, any char (incl. spaces/umlauts), quoted."""
    if value is None or value == "":
        return '""'
    s = str(value)
    if len(s) > 60:
        raise FieldValidationError(
            f"Buchungstext '{s[:30]}...' überschreitet 60 Zeichen ({len(s)} Zeichen)"
        )
    escaped = s.replace('"', '""')
    return f'"{escaped}"'


def _format_kost_menge(value: Any) -> str:
    """Field #39 KOST-Menge: strict 12 Vorkomma + 4 Nachkomma digits."""
    if value is None or value == "":
        return ""
    s = str(value)
    if not re.fullmatch(r"\d{12}\,\d{4}", s):
        raise FieldValidationError(
            f"KOST-Menge '{s}' muss exakt 12 Vorkomma + Komma + 4 Nachkomma Ziffern sein"
        )
    return s


def _format_generalumkehr(value: Any) -> str:
    """
    Field #118 Generalumkehr — portal inconsistency.

    Portal regex accepts only quoted (0|1); description says 'G or 1'.
    Serializer accepts input "G", "1", or boolean true → emits "1".
    Input "0" or boolean false → empty (no Generalumkehr).
    """
    if value is None or value == "" or value is False or value == "0":
        return ""
    if value is True or str(value).strip().upper() in ("G", "1", "TRUE"):
        return '"1"'
    raise FieldValidationError(
        f"Generalumkehr Wert '{value}' nicht erkannt — erlaubt: G, 1, true, oder leer/0/false"
    )


def _format_skontosperre(value: Any) -> str:
    """
    Field #106 Skontosperre — portal inconsistency.

    Portal regex ^[0|1]$ is a character class (literal pipe); serializer enforces ^(0|1)$.
    """
    if value is None or value == "":
        return ""
    s = str(value)
    if s not in ("0", "1"):
        raise FieldValidationError(
            f"Skontosperre Wert '{s}' nicht erlaubt — nur 0 oder 1 (Portal-Typo-Interpretation)"
        )
    return s


def _format_bvv_position(value: Any) -> str:
    """
    Field #122 BVV-Position — portal inconsistency.

    Portal regex ^([1|2|3|4|5])$ is a character class (literal pipe);
    serializer enforces ^(1|2|3|4|5)$.
    """
    if value is None or value == "":
        return ""
    s = str(value)
    if s not in ("1", "2", "3", "4", "5"):
        raise FieldValidationError(
            f"BVV-Position Wert '{s}' muss 1-5 sein (Portal-Typo-Interpretation)"
        )
    return s


# ---------------------------------------------------------------------------
# Header builder
# ---------------------------------------------------------------------------

def build_header_row(header_input: dict, inventory: dict) -> list[str]:
    """
    Build the 31-field header row from input dict + field inventory.

    Returns a list of 31 string elements, each already correctly quoted/formatted.
    """
    h = header_input
    sachkontenrahmen_input = h.get("sachkontenrahmen", "")
    # If caller passed an SKR alias, map it
    if sachkontenrahmen_input in SKR_TO_SACHKONTENRAHMEN:
        sachkontenrahmen_input = SKR_TO_SACHKONTENRAHMEN[sachkontenrahmen_input]

    fields = [
        # 1 Kennzeichen
        f'"{h.get("kennzeichen", "EXTF")}"',
        # 2 Versionsnummer
        str(h.get("versionsnummer", 700)),
        # 3 Formatkategorie
        str(h.get("formatkategorie", 21)),
        # 4 Formatname
        f'"{h.get("formatname", "Buchungsstapel")}"',
        # 5 Formatversion
        str(h.get("formatversion", 13)),
        # 6 Erzeugt am (17 digits YYYYMMDDHHMMSSFFF)
        _validate_erzeugt_am(h.get("erzeugt_am", "")),
        # 7 Importiert (Leerfeld)
        "",
        # 8 Herkunft
        _format_quoted_text_required(h.get("herkunft", ""), 2),
        # 9 Exportiert von
        _format_quoted_text_required(h.get("exportiert_von", ""), 25),
        # 10 Importiert von
        _format_quoted_text_required(h.get("importiert_von", ""), 25),
        # 11 Beraternummer
        _validate_int_range(h.get("berater_nr"), "Beraternummer", 1001, 9999999),
        # 12 Mandantennummer
        _validate_int_range(h.get("mandanten_nr"), "Mandantennummer", 1, 99999),
        # 13 WJ-Beginn
        _validate_yyyymmdd(h.get("wj_beginn"), "WJ-Beginn"),
        # 14 Sachkontenlänge
        _validate_sachkontenlaenge(h.get("sachkonten_laenge", 4)),
        # 15 Datum von
        _validate_yyyymmdd(h.get("datum_von"), "Datum von"),
        # 16 Datum bis
        _validate_yyyymmdd(h.get("datum_bis"), "Datum bis"),
        # 17 Bezeichnung
        _format_bezeichnung(h.get("bezeichnung", "")),
        # 18 Diktatkürzel
        _format_diktatkuerzel(h.get("diktatkuerzel", "")),
        # 19 Buchungstyp
        _validate_choice(h.get("buchungstyp", 1), "Buchungstyp", {1, 2}),
        # 20 Rechnungslegungszweck
        _validate_choice(h.get("rechnungslegungszweck", 0), "Rechnungslegungszweck",
                         {0, 30, 40, 50, 64}),
        # 21 Festschreibung
        _validate_choice(h.get("festschreibung", 0), "Festschreibung", {0, 1}),
        # 22 WKZ
        _format_wkz(h.get("wkz", "EUR")),
        # 23 Reserviert (Leerfeld)
        "",
        # 24 Derivatskennzeichen (empty-quoted)
        '""',
        # 25 Reserviert (Leerfeld)
        "",
        # 26 Reserviert (Leerfeld)
        "",
        # 27 Sachkontenrahmen
        f'"{sachkontenrahmen_input}"',
        # 28 ID der Branchenlösung
        _format_numeric_optional(h.get("id_branchenloesung", "")),
        # 29 Reserviert (Leerfeld)
        "",
        # 30 Reserviert (empty-quoted)
        '""',
        # 31 Anwendungsinformation
        _format_quoted_text_required(h.get("anwendungsinformation", ""), 16),
    ]
    return fields


def _validate_erzeugt_am(value: Any) -> str:
    if value is None or value == "":
        raise FieldValidationError("Header 'erzeugt_am' ist Pflicht (YYYYMMDDHHMMSSFFF)")
    s = str(value)
    if not re.fullmatch(
        r"20\d{2}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])"
        r"(2[0-3]|[01]\d)[0-5]\d[0-5]\d\d{3}",
        s,
    ):
        raise FieldValidationError(
            f"'erzeugt_am' '{s}' muss YYYYMMDDHHMMSSFFF mit Jahr-Präfix 20 sein (17 Ziffern)"
        )
    return s


def _validate_yyyymmdd(value: Any, label: str) -> str:
    if value is None or value == "":
        raise FieldValidationError(f"Header '{label}' ist Pflicht (YYYYMMDD)")
    s = str(value)
    if not re.fullmatch(r"20\d{2}(0[1-9]|1[0-2])(0[1-9]|[1-2]\d|3[0-1])", s):
        raise FieldValidationError(
            f"'{label}' '{s}' muss YYYYMMDD mit Jahr-Präfix 20 sein (8 Ziffern)"
        )
    return s


def _validate_int_range(value: Any, label: str, lo: int, hi: int) -> str:
    if value is None or value == "":
        raise FieldValidationError(f"Header '{label}' ist Pflicht")
    try:
        n = int(value)
    except (ValueError, TypeError):
        raise FieldValidationError(f"'{label}' '{value}' muss ganzzahlig sein")
    if not (lo <= n <= hi):
        raise FieldValidationError(f"'{label}' {n} liegt außerhalb [{lo}..{hi}]")
    return str(n)


def _validate_sachkontenlaenge(value: Any) -> str:
    try:
        n = int(value)
    except (ValueError, TypeError):
        raise FieldValidationError(f"Sachkontenlänge '{value}' muss ganzzahlig sein")
    if n not in {4, 5, 6, 7, 8}:
        raise FieldValidationError(f"Sachkontenlänge {n} muss in {{4,5,6,7,8}} liegen")
    return str(n)


def _validate_choice(value: Any, label: str, allowed: set) -> str:
    try:
        n = int(value)
    except (ValueError, TypeError):
        raise FieldValidationError(f"'{label}' '{value}' muss ganzzahlig sein")
    if n not in allowed:
        raise FieldValidationError(
            f"'{label}' {n} nicht erlaubt — erlaubt: {sorted(allowed)}"
        )
    return str(n)


def _format_bezeichnung(value: Any) -> str:
    s = str(value or "")
    if not re.fullmatch(r"[\w.\-/ ]{0,30}", s):
        raise FieldValidationError(
            f"Bezeichnung '{s}' enthält unzulässige Zeichen (erlaubt: word + .-/ + Leerzeichen, max 30)"
        )
    return f'"{s}"'


def _format_diktatkuerzel(value: Any) -> str:
    s = str(value or "").upper()
    if not re.fullmatch(r"([A-Z]{2}){0,2}", s):
        raise FieldValidationError(
            f"Diktatkürzel '{s}' muss 0, 2 oder 4 Großbuchstaben sein"
        )
    return f'"{s}"'


# ---------------------------------------------------------------------------
# Column-header row (row 2)
# ---------------------------------------------------------------------------

def build_column_header_row(inventory: dict) -> list[str]:
    """
    Build the 125-element row-2 column-name list.

    Each name comes from data_columns[i].name verbatim, except where
    ROW2_OVERRIDES specifies a different string (fields #1 and #8 per
    Einstieg-page example — see PRD §6).
    """
    cols = inventory["data_columns"]
    if len(cols) != 125:
        raise InputValidationError(
            f"Field inventory has {len(cols)} data columns, expected 125"
        )
    out = []
    for col in cols:
        name = ROW2_OVERRIDES.get(col["n"], col["name"])
        out.append(f'"{name}"')
    return out


# ---------------------------------------------------------------------------
# Data-row builder
# ---------------------------------------------------------------------------

# Each data field maps to a (input_json_key, formatter_callable) tuple.
# Formatters receive the raw input value and return the CSV-ready string.
# Unspecified-in-input fields → formatter receives None / "" and emits the
# appropriate empty representation (text → "", numeric → bare).

def _make_field_handlers(sachkontenlaenge: int):
    """Build the 125-element list of (input_key, formatter) tuples for data rows."""
    text_empty = lambda v: _format_quoted_empty_or_text(v) if v not in (None, "") else ""
    text_max20 = lambda v: _format_quoted_empty_or_text(v, max_len=20) if v not in (None, "") else ""
    text_max30 = lambda v: _format_quoted_empty_or_text(v, max_len=30) if v not in (None, "") else ""
    text_max35 = lambda v: _format_quoted_empty_or_text(v, max_len=35) if v not in (None, "") else ""
    text_max36 = lambda v: _format_quoted_empty_or_text(v, max_len=36) if v not in (None, "") else ""
    text_max50 = lambda v: _format_quoted_empty_or_text(v, max_len=50) if v not in (None, "") else ""
    text_max76 = lambda v: _format_quoted_empty_or_text(v, max_len=76) if v not in (None, "") else ""
    text_max210 = lambda v: _format_quoted_empty_or_text(v, max_len=210) if v not in (None, "") else ""

    def kost(v):  # Field #37/#38: word + space, max 36, quoted
        if v in (None, ""):
            return ""
        s = str(v)
        if len(s) > 36 or not re.fullmatch(r"[\w ]{0,36}", s):
            raise FieldValidationError(
                f"KOST-Kostenstelle '{s}' verletzt Format (word + Leerzeichen, max 36)"
            )
        return f'"{s}"'

    def opt_numeric(v):
        return _format_numeric_optional(v)

    def opt_two_letter_quoted(v):  # e.g. EU-Mitgliedstaat #98 / #120: 2 uppercase letters or empty
        if v in (None, ""):
            return ""
        s = str(v).upper()
        if not re.fullmatch(r"[A-Z]{2}", s):
            raise FieldValidationError(f"2-Letter-Code '{v}' muss 2 Großbuchstaben sein")
        return f'"{s}"'

    def opt_decimal(v, pat):
        if v in (None, ""):
            return ""
        s = str(v)
        if not re.fullmatch(pat, s):
            raise FieldValidationError(f"Wert '{s}' verletzt Pattern {pat}")
        return s

    def opt_date_ttmmjjjj(v):
        if v in (None, ""):
            return ""
        s = str(v)
        if not re.fullmatch(
            r"(0[1-9]|[1-2]\d|3[0-1])(0[1-9]|1[0-2])20\d{2}", s
        ):
            raise FieldValidationError(f"Datum '{s}' muss TTMMJJJJ sein")
        return s

    handlers = [
        # 1 Umsatz
        ("umsatz", _format_umsatz),
        # 2 Soll/Haben-Kennzeichen
        ("soll_haben_kennzeichen", _format_soll_haben),
        # 3 WKZ Umsatz
        ("wkz_umsatz", lambda v: _format_wkz(v) if v not in (None, "") else ""),
        # 4 Kurs
        ("kurs", lambda v: opt_decimal(v, r"[1-9]\d{0,3}\,\d{2,6}")),
        # 5 Basis-Umsatz
        ("basis_umsatz",
            lambda v: ("" if v in (None, "")
                       else (_format_umsatz(v)))),
        # 6 WKZ Basis-Umsatz
        ("wkz_basis_umsatz", lambda v: _format_wkz(v) if v not in (None, "") else ""),
        # 7 Konto
        ("konto", lambda v: _format_konto(v, sachkontenlaenge, "Konto")),
        # 8 Gegenkonto
        ("gegenkonto", lambda v: _format_konto(v, sachkontenlaenge, "Gegenkonto")),
        # 9 BU-Schlüssel
        ("bu_schluessel", _format_bu_schluessel),
        # 10 Belegdatum
        ("belegdatum", _format_belegdatum),
        # 11 Belegfeld 1
        ("belegfeld_1", lambda v: _format_belegfeld(v, "Belegfeld 1")),
        # 12 Belegfeld 2
        ("belegfeld_2", lambda v: _format_belegfeld(v, "Belegfeld 2")),
        # 13 Skonto
        ("skonto", lambda v: opt_decimal(v, r"[1-9]\d{0,7}\,\d{2}")),
        # 14 Buchungstext
        ("buchungstext", _format_buchungstext),
        # 15 Postensperre
        ("postensperre", lambda v: _validate_choice(v, "Postensperre", {0, 1}) if v not in (None, "") else ""),
        # 16 Diverse Adressnummer
        ("diverse_adressnummer",
            lambda v: ("" if v in (None, "")
                       else (f'"{str(v)}"' if re.fullmatch(r"\w{0,9}", str(v))
                             else (_ for _ in ()).throw(
                                 FieldValidationError(f"Diverse Adressnummer '{v}' max 9 word chars"))))),
        # 17 Geschäftspartnerbank
        ("geschaeftspartnerbank",
            lambda v: ("" if v in (None, "")
                       else (str(v) if re.fullmatch(r"\d{3}", str(v))
                             else (_ for _ in ()).throw(
                                 FieldValidationError(f"Geschäftspartnerbank '{v}' muss 3 Ziffern sein"))))),
        # 18 Sachverhalt
        ("sachverhalt",
            lambda v: ("" if v in (None, "")
                       else (str(v) if re.fullmatch(r"\d{2}", str(v))
                             else (_ for _ in ()).throw(
                                 FieldValidationError(f"Sachverhalt '{v}' muss 2 Ziffern sein"))))),
        # 19 Zinssperre
        ("zinssperre", lambda v: _validate_choice(v, "Zinssperre", {0, 1}) if v not in (None, "") else ""),
        # 20 Beleglink
        ("beleglink", text_max210),
        # 21-36 Beleginfo Art/Inhalt 1-8 (alternating max 20 / max 210)
        ("beleginfo_art_1", text_max20), ("beleginfo_inhalt_1", text_max210),
        ("beleginfo_art_2", text_max20), ("beleginfo_inhalt_2", text_max210),
        ("beleginfo_art_3", text_max20), ("beleginfo_inhalt_3", text_max210),
        ("beleginfo_art_4", text_max20), ("beleginfo_inhalt_4", text_max210),
        ("beleginfo_art_5", text_max20), ("beleginfo_inhalt_5", text_max210),
        ("beleginfo_art_6", text_max20), ("beleginfo_inhalt_6", text_max210),
        ("beleginfo_art_7", text_max20), ("beleginfo_inhalt_7", text_max210),
        ("beleginfo_art_8", text_max20), ("beleginfo_inhalt_8", text_max210),
        # 37 KOST1
        ("kost1", kost),
        # 38 KOST2
        ("kost2", kost),
        # 39 KOST-Menge
        ("kost_menge", _format_kost_menge),
        # 40 EU-Land u. UStID (Bestimmung)
        ("eu_land_ustid_bestimmung", lambda v: _format_quoted_empty_or_text(v, max_len=15) if v not in (None, "") else ""),
        # 41 EU-Steuersatz (Bestimmung)
        ("eu_steuersatz_bestimmung", lambda v: opt_decimal(v, r"\d{2}\,\d{2}")),
        # 42 Abw. Versteuerungsart
        ("abw_versteuerungsart",
            lambda v: ("" if v in (None, "")
                       else (f'"{str(v).upper()}"' if str(v).upper() in {"I", "K", "P", "S"}
                             else (_ for _ in ()).throw(
                                 FieldValidationError(f"Abw. Versteuerungsart '{v}' muss I/K/P/S sein"))))),
        # 43 Sachverhalt L+L
        ("sachverhalt_l_l",
            lambda v: ("" if v in (None, "")
                       else (str(v) if re.fullmatch(r"\d{1,3}", str(v)) and str(v) != "0"
                             else (_ for _ in ()).throw(
                                 FieldValidationError(f"Sachverhalt L+L '{v}' muss 1-3 Ziffern, nicht 0"))))),
        # 44 Funktionsergänzung L+L
        ("funktionsergaenzung_l_l", lambda v: opt_numeric(v)),
        # 45 BU 49 Hauptfunktiontyp
        ("bu_49_hauptfunktiontyp", lambda v: opt_numeric(v)),
        # 46 BU 49 Hauptfunktionsnummer
        ("bu_49_hauptfunktionsnummer", lambda v: opt_numeric(v)),
        # 47 BU 49 Funktionsergänzung
        ("bu_49_funktionsergaenzung", lambda v: opt_numeric(v)),
        # 48-87 Zusatzinformation Art/Inhalt 1-20 (alternating max 20 / max 210)
        *[(f"zusatzinfo_art_{i}", text_max20) if k % 2 == 0
          else (f"zusatzinfo_inhalt_{i}", text_max210)
          for i in range(1, 21)
          for k in range(2)
          if (k == 0)] + [
        ],  # placeholder; we'll override below
    ]
    # Manual expansion for Zusatzinformation (clearer than mixed list-comp)
    zusatz = []
    for i in range(1, 21):
        zusatz.append((f"zusatzinfo_art_{i}", text_max20))
        zusatz.append((f"zusatzinfo_inhalt_{i}", text_max210))
    # Replace the last placeholder entry with the real Zusatzinfo list
    handlers = handlers[:47] + zusatz

    # 88 Stück
    handlers.append(("stueck", lambda v: opt_numeric(v)))
    # 89 Gewicht
    handlers.append(("gewicht", lambda v: opt_decimal(v, r"\d{1,8}\,\d{2}")))
    # 90 Zahlweise
    handlers.append(("zahlweise", lambda v: opt_numeric(v)))
    # 91 Forderungsart
    handlers.append(("forderungsart",
        lambda v: ("" if v in (None, "")
                   else (f'"{str(v)}"' if re.fullmatch(r"\w{0,10}", str(v))
                         else (_ for _ in ()).throw(
                             FieldValidationError(f"Forderungsart '{v}' max 10 word chars"))))))
    # 92 Veranlagungsjahr
    handlers.append(("veranlagungsjahr",
        lambda v: ("" if v in (None, "")
                   else (str(v) if re.fullmatch(r"20\d{2}", str(v))
                         else (_ for _ in ()).throw(
                             FieldValidationError(f"Veranlagungsjahr '{v}' muss YYYY mit 20-Präfix sein"))))))
    # 93 Zugeordnete Fälligkeit (TTMMJJJJ)
    handlers.append(("zugeordnete_faelligkeit", opt_date_ttmmjjjj))
    # 94 Skontotyp
    handlers.append(("skontotyp", lambda v: opt_numeric(v)))
    # 95 Auftragsnummer
    handlers.append(("auftragsnummer", text_max30))
    # 96 Buchungstyp (data row)
    handlers.append(("buchungstyp_data",
        lambda v: ("" if v in (None, "")
                   else (f'"{str(v).upper()}"' if re.fullmatch(r"[A-Z]{2}", str(v).upper())
                         else (_ for _ in ()).throw(
                             FieldValidationError(f"Buchungstyp data '{v}' muss 2 Großbuchstaben sein"))))))
    # 97 USt-Schlüssel (Anzahlungen)
    handlers.append(("ust_schluessel_anzahlungen", lambda v: opt_numeric(v)))
    # 98 EU-Mitgliedstaat (Anzahlungen)
    handlers.append(("eu_mitgliedstaat_anzahlungen", opt_two_letter_quoted))
    # 99 Sachverhalt L+L (Anzahlungen)
    handlers.append(("sachverhalt_l_l_anzahlungen", lambda v: opt_numeric(v)))
    # 100 EU-Steuersatz (Anzahlungen)
    handlers.append(("eu_steuersatz_anzahlungen", lambda v: opt_decimal(v, r"\d{1,2}\,\d{2}")))
    # 101 Erlöskonto (Anzahlungen)
    handlers.append(("erloeskonto_anzahlungen", lambda v: opt_numeric(v)))
    # 102 Herkunft-Kz
    handlers.append(("herkunft_kz", opt_two_letter_quoted))
    # 103 Leerfeld
    handlers.append(("leerfeld_103", text_max36))
    # 104 KOST-Datum
    handlers.append(("kost_datum", opt_date_ttmmjjjj))
    # 105 SEPA-Mandatsreferenz
    handlers.append(("sepa_mandatsreferenz", text_max35))
    # 106 Skontosperre — portal inconsistency
    handlers.append(("skontosperre", _format_skontosperre))
    # 107 Gesellschaftername
    handlers.append(("gesellschaftername", text_max76))
    # 108 Beteiligtennummer
    handlers.append(("beteiligtennummer",
        lambda v: ("" if v in (None, "")
                   else (str(v) if re.fullmatch(r"\d{4}", str(v))
                         else (_ for _ in ()).throw(
                             FieldValidationError(f"Beteiligtennummer '{v}' muss 4 Ziffern sein"))))))
    # 109 Identifikationsnummer
    handlers.append(("identifikationsnummer", lambda v: _format_quoted_empty_or_text(v, max_len=11) if v not in (None, "") else ""))
    # 110 Zeichnernummer
    handlers.append(("zeichnernummer", text_max20))
    # 111 Postensperre bis
    handlers.append(("postensperre_bis", opt_date_ttmmjjjj))
    # 112 Bezeichnung SoBil-Sachverhalt
    handlers.append(("bezeichnung_sobil", text_max30))
    # 113 Kennzeichen SoBil-Buchung
    handlers.append(("kennzeichen_sobil", lambda v: opt_numeric(v)))
    # 114 Festschreibung (data row)
    handlers.append(("festschreibung_data",
        lambda v: ("" if v in (None, "") else _validate_choice(v, "Festschreibung (data)", {0, 1}))))
    # 115 Leistungsdatum
    handlers.append(("leistungsdatum", opt_date_ttmmjjjj))
    # 116 Datum Zuord. Steuerperiode
    handlers.append(("datum_zuord_steuerperiode", opt_date_ttmmjjjj))
    # 117 Fälligkeit
    handlers.append(("faelligkeit", opt_date_ttmmjjjj))
    # 118 Generalumkehr — portal inconsistency
    handlers.append(("generalumkehr", _format_generalumkehr))
    # 119 Steuersatz
    handlers.append(("steuersatz", lambda v: opt_decimal(v, r"\d{1,2}\,\d{2}")))
    # 120 Land
    handlers.append(("land", opt_two_letter_quoted))
    # 121 Abrechnungsreferenz
    handlers.append(("abrechnungsreferenz", text_max50))
    # 122 BVV-Position — portal inconsistency
    handlers.append(("bvv_position", _format_bvv_position))
    # 123 EU-Land u. UStID (Ursprung)
    handlers.append(("eu_land_ustid_ursprung", lambda v: _format_quoted_empty_or_text(v, max_len=15) if v not in (None, "") else ""))
    # 124 EU-Steuersatz (Ursprung)
    handlers.append(("eu_steuersatz_ursprung", lambda v: opt_decimal(v, r"\d{2}\,\d{2}")))
    # 125 Abw. Skontokonto
    handlers.append(("abw_skontokonto", lambda v: opt_numeric(v)))

    assert len(handlers) == 125, f"Internal: built {len(handlers)} handlers, expected 125"
    return handlers


def build_data_row(buchung: dict, sachkontenlaenge: int) -> list[str]:
    """Build a 125-element data row from a single Buchung dict."""
    handlers = _make_field_handlers(sachkontenlaenge)
    out = []
    for key, formatter in handlers:
        value = buchung.get(key)
        try:
            out.append(formatter(value))
        except FieldValidationError as e:
            raise FieldValidationError(
                f"Buchung (Konto={buchung.get('konto')}, Belegfeld 1={buchung.get('belegfeld_1')}): {e}"
            ) from e
    assert len(out) == 125
    return out


# ---------------------------------------------------------------------------
# Saldo validation
# ---------------------------------------------------------------------------

def validate_saldo(buchungen: list[dict]) -> tuple[Decimal, Decimal]:
    """
    Validate that Σ Umsatz where Soll/Haben = "S" equals Σ where = "H".

    Returns (sum_soll, sum_haben). Raises SaldoError if unbalanced.
    """
    sum_soll = Decimal("0.00")
    sum_haben = Decimal("0.00")
    for i, b in enumerate(buchungen, 1):
        u = b.get("umsatz")
        sh = b.get("soll_haben_kennzeichen", "S")
        if u in (None, ""):
            raise SaldoError(f"Buchung #{i}: Umsatz fehlt")
        try:
            amount = Decimal(str(u).replace(",", "."))
        except InvalidOperation:
            raise SaldoError(f"Buchung #{i}: Umsatz '{u}' ist kein gültiger Decimal")
        if sh == "S":
            sum_soll += amount
        elif sh == "H":
            sum_haben += amount
        else:
            raise SaldoError(f"Buchung #{i}: Soll/Haben '{sh}' nicht S/H")
    if sum_soll != sum_haben:
        diff = sum_soll - sum_haben
        raise SaldoError(
            f"Σ Soll ({sum_soll}) != Σ Haben ({sum_haben}); Differenz {diff}. "
            f"Buchungen-Anzahl: {len(buchungen)}"
        )
    return sum_soll, sum_haben


# ---------------------------------------------------------------------------
# CSV writer
# ---------------------------------------------------------------------------

def write_csv(rows: list[list[str]], path: Path, encoding: str) -> None:
    """Write rows to path with explicit CRLF and the specified encoding."""
    if encoding not in SUPPORTED_ENCODINGS:
        raise InputValidationError(
            f"Encoding '{encoding}' nicht unterstützt. Erlaubt: {sorted(SUPPORTED_ENCODINGS)}"
        )
    # Build the full text in memory, then write bytes — guarantees CRLF + encoding
    lines = [FIELD_SEPARATOR.join(row) for row in rows]
    text = LINE_ENDING.join(lines) + LINE_ENDING  # trailing CRLF after last row per PRD §6
    try:
        encoded = text.encode(encoding, errors="strict")
    except UnicodeEncodeError as e:
        # Find which character + line failed for a useful error
        raise EncodingError(
            f"Zeichen kann nicht in {encoding} kodiert werden: {e!r}. "
            "Häufige Ursache: Emoji oder seltene Unicode-Zeichen im Buchungstext / "
            "Beleginfo. Falls absichtlich, '--encoding utf-8-sig' verwenden."
        ) from e
    path.write_bytes(encoded)


# ---------------------------------------------------------------------------
# Sidecar .report.md writer
# ---------------------------------------------------------------------------

def write_report(
    report_path: Path,
    csv_path: Path,
    header_input: dict,
    buchungen: list[dict],
    sum_soll: Decimal,
    sum_haben: Decimal,
    encoding: str,
    format_version: int,
    interpretations_applied: list[str],
) -> None:
    """Write sidecar Markdown report next to the CSV."""
    csv_bytes = csv_path.read_bytes()
    sha256 = hashlib.sha256(csv_bytes).hexdigest()
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # distinct accounts used
    konten_used = sorted({str(b.get("konto", "")) for b in buchungen if b.get("konto")} |
                         {str(b.get("gegenkonto", "")) for b in buchungen if b.get("gegenkonto")})
    bu_used = sorted({str(b.get("bu_schluessel", "")) for b in buchungen
                      if b.get("bu_schluessel") not in (None, "")})

    interpretations_block = "\n".join(
        f"- {i}" for i in interpretations_applied
    ) or "- (keine portal-Inkonsistenz-Regel ausgelöst)"

    konten_block = ", ".join(konten_used) if konten_used else "(keine)"
    bu_block = ", ".join(bu_used) if bu_used else "(keine — alle Buchungen auf Automatikkonten oder ohne BU-Schlüssel)"

    diff = sum_soll - sum_haben
    saldo_status = "✓ ausgeglichen (0,00)" if diff == Decimal("0.00") else f"✗ Differenz {diff}"

    md = f"""# EXTF-Buchungsstapel — Generierungs-Bericht

**CSV-Datei:** `{csv_path.name}`
**Generiert:** {timestamp} (UTC)
**SHA-256:** `{sha256}`

## Eckdaten

| Feld | Wert |
|---|---|
| Formatkategorie | 21 (Buchungsstapel) |
| Formatversion | {format_version} |
| Encoding | `{encoding}` |
| Anzahl Buchungssätze | {len(buchungen)} |
| Berater-Nr. | {header_input.get("berater_nr", "—")} |
| Mandanten-Nr. | {header_input.get("mandanten_nr", "—")} |
| WJ-Beginn | {header_input.get("wj_beginn", "—")} |
| Datum von / bis | {header_input.get("datum_von", "—")} / {header_input.get("datum_bis", "—")} |
| Sachkontenrahmen | {header_input.get("sachkontenrahmen", "—")} |
| Sachkontenlänge | {header_input.get("sachkonten_laenge", "—")} |
| Bezeichnung | {header_input.get("bezeichnung", "—")} |

## Saldo

- Σ Soll: **{sum_soll}**
- Σ Haben: **{sum_haben}**
- Status: **{saldo_status}**

## Verwendete Konten

{konten_block}

## Verwendete BU-Schlüssel

{bu_block}

## Portal-Inkonsistenz-Interpretationsregeln, die ausgelöst wurden

{interpretations_block}

## Wichtiger Hinweis

⚠ **Import als Vorabbuchungsstapel.** Vor Freigabe durch Anwender / Steuerberater stichprobenartig prüfen.
Dieser Bericht ist Teil der GoBD-relevanten Verfahrensdokumentation.
"""
    report_path.write_text(md, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def generate(
    input_path: Path,
    output_path: Path,
    format_version: int = DEFAULT_FORMAT_VERSION,
    encoding_override: str | None = None,
) -> Path:
    """End-to-end: read JSON, validate, write CSV + report. Returns report path."""
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise InputValidationError("Eingabe-JSON muss ein Objekt auf Top-Level sein")

    header_input = data.get("header", {})
    buchungen = data.get("buchungen", [])
    encoding = encoding_override or data.get("encoding", DEFAULT_ENCODING)

    if not isinstance(buchungen, list) or not buchungen:
        raise InputValidationError("Eingabe-JSON muss 'buchungen' (non-empty array) enthalten")

    # SKR shortcut → sachkontenrahmen header field (top-level wins)
    if "skr" in data:
        header_input = dict(header_input)
        header_input["sachkontenrahmen"] = data["skr"]

    inventory = load_field_inventory(format_version)
    sachkontenlaenge = int(header_input.get("sachkonten_laenge", 4))

    # 1. Saldo check (fast-fail before formatting)
    sum_soll, sum_haben = validate_saldo(buchungen)

    # 2. Build rows
    header_row = build_header_row(header_input, inventory)
    col_header_row = build_column_header_row(inventory)
    data_rows = [build_data_row(b, sachkontenlaenge) for b in buchungen]

    # Sanity: every row 125 fields, header 31
    assert len(header_row) == 31, f"Header has {len(header_row)} fields"
    assert len(col_header_row) == 125, f"Column header has {len(col_header_row)} fields"
    for i, r in enumerate(data_rows):
        assert len(r) == 125, f"Data row {i} has {len(r)} fields"

    rows = [header_row, col_header_row] + data_rows

    # 3. Write CSV
    write_csv(rows, output_path, encoding)

    # 4. Determine which interpretation rules fired (by scanning the inventory + actual usage)
    interpretations_applied = _collect_interpretations(buchungen, inventory)

    # 5. Write report
    report_path = output_path.with_suffix(output_path.suffix + ".report.md")
    write_report(
        report_path=report_path,
        csv_path=output_path,
        header_input=header_input,
        buchungen=buchungen,
        sum_soll=sum_soll,
        sum_haben=sum_haben,
        encoding=encoding,
        format_version=format_version,
        interpretations_applied=interpretations_applied,
    )

    return report_path


def _collect_interpretations(buchungen: list[dict], inventory: dict) -> list[str]:
    """Return the list of portal-inconsistency rules that actually fired this run."""
    notes = []
    # Header #5 always interpreted (we emit only 13, so the rule is documented but moot — skip)

    # Data #106 Skontosperre: fired if any Buchung has skontosperre set
    if any(b.get("skontosperre") not in (None, "") for b in buchungen):
        notes.append(
            "Feld #106 Skontosperre: Portal-Regex ^[0|1]$ als Character-Class "
            "ausgelegt; Serializer erzwingt Alternation ^(0|1)$."
        )

    # Data #118 Generalumkehr: fired if any Buchung has generalumkehr truthy
    if any(b.get("generalumkehr") not in (None, "", False, "0") for b in buchungen):
        notes.append(
            "Feld #118 Generalumkehr: Portal-Beschreibung erlaubt 'G oder 1' "
            "aber Regex nur '0|1'; Serializer nimmt G/1/true an, gibt \"1\" aus."
        )

    # Data #122 BVV-Position: fired if any Buchung has bvv_position set
    if any(b.get("bvv_position") not in (None, "") for b in buchungen):
        notes.append(
            "Feld #122 BVV-Position: Portal-Regex ^([1|2|3|4|5])$ als "
            "Character-Class ausgelegt; Serializer erzwingt Alternation ^(1|2|3|4|5)$."
        )

    return notes


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic DATEV-Format EXTF-Buchungsstapel CSV serializer.",
    )
    parser.add_argument("--input", "-i", required=True, type=Path,
                        help="Path to input JSON with buchungen + header")
    parser.add_argument("--output", "-o", required=True, type=Path,
                        help="Path to output CSV (sidecar .report.md written alongside)")
    parser.add_argument("--format-version", "-f", type=int, default=DEFAULT_FORMAT_VERSION,
                        help=f"Buchungsstapel Formatversion (default: {DEFAULT_FORMAT_VERSION})")
    parser.add_argument("--encoding", "-e", default=None,
                        help=f"Output encoding (default: {DEFAULT_ENCODING}; also: utf-8-sig)")
    args = parser.parse_args(argv)

    try:
        report_path = generate(
            input_path=args.input,
            output_path=args.output,
            format_version=args.format_version,
            encoding_override=args.encoding,
        )
    except ExtfSerializerError as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        return 1

    print(f"OK: {args.output} geschrieben ({args.output.stat().st_size} bytes)")
    print(f"OK: {report_path} (Begleit-Bericht)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
