"""
Tests for scripts/generate_extf.py — deterministic EXTF Buchungsstapel serializer.

Per PRD §11. Groups:
  - Header tests
  - Data-row tests
  - Format / encoding / determinism
  - Saldo + business rules
  - Portal-inconsistency interpretation
  - Synthetic fixtures (Lohn, Bewirtung 70/30, EU §13b, USt-VA-Saldierung)

Target ≥90% line coverage on scripts/generate_extf.py.
Run: pytest tests/test_extf_serializer.py -v
"""

from __future__ import annotations

import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import generate_extf as G  # noqa: E402


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

def _minimal_header(**overrides) -> dict:
    base = {
        "kennzeichen": "EXTF",
        "versionsnummer": 700,
        "formatkategorie": 21,
        "formatname": "Buchungsstapel",
        "formatversion": 13,
        "erzeugt_am": "20260520143000000",
        "herkunft": "RE",
        "exportiert_von": "tgw013",
        "importiert_von": "",
        "berater_nr": 12345,
        "mandanten_nr": 1,
        "wj_beginn": "20260101",
        "sachkonten_laenge": 4,
        "datum_von": "20260401",
        "datum_bis": "20260430",
        "bezeichnung": "Test-Stapel",
        "diktatkuerzel": "TG",
        "buchungstyp": 1,
        "rechnungslegungszweck": 0,
        "festschreibung": 0,
        "wkz": "EUR",
        "derivatskennzeichen": "",
        "sachkontenrahmen": "04",
        "id_branchenloesung": "",
        "anwendungsinformation": "04/2026",
    }
    base.update(overrides)
    return base


def _minimal_buchung(**overrides) -> dict:
    base = {
        "umsatz": "100,00",
        "soll_haben_kennzeichen": "S",
        "wkz_umsatz": "",
        "konto": "6815",
        "gegenkonto": "3300",
        "bu_schluessel": "",
        "belegdatum": "1504",
        "belegfeld_1": "TEST-001",
        "belegfeld_2": "",
        "skonto": "",
        "buchungstext": "Test-Buchung",
    }
    base.update(overrides)
    return base


def _balanced_pair(**overrides) -> list[dict]:
    """Two balanced Buchungen (S 100,00 / H 100,00)."""
    s = _minimal_buchung(**overrides)
    h = _minimal_buchung(soll_haben_kennzeichen="H", konto=s["gegenkonto"], gegenkonto=s["konto"])
    h.update(overrides)
    h["soll_haben_kennzeichen"] = "H"
    return [s, h]


def _write_input(tmp_path: Path, **kwargs) -> Path:
    """Write a minimal input JSON to tmp_path/input.json and return the path."""
    payload = {
        "header": _minimal_header(**kwargs.get("header_overrides", {})),
        "skr": kwargs.get("skr", "SKR04"),
        "buchungen": kwargs.get("buchungen", _balanced_pair()),
        "encoding": kwargs.get("encoding", "cp1252"),
    }
    p = tmp_path / "input.json"
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def _run(tmp_path: Path, **kwargs) -> tuple[Path, Path]:
    """Run generator on a freshly written input; return (csv_path, report_path)."""
    inp = _write_input(tmp_path, **kwargs)
    out = tmp_path / "out.csv"
    report = G.generate(inp, out, format_version=13)
    return out, report


# ---------------------------------------------------------------------------
# Header tests
# ---------------------------------------------------------------------------

class TestHeader:
    def test_minimal_31_fields(self, tmp_path):
        csv_path, _ = _run(tmp_path)
        lines = csv_path.read_bytes().decode("cp1252").split("\r\n")
        header_fields = lines[0].split(";")
        assert len(header_fields) == 31

    def test_erzeugt_am_17_digits(self, tmp_path):
        # Valid
        _run(tmp_path)
        # Invalid: 16 digits
        with pytest.raises(G.FieldValidationError, match="erzeugt_am"):
            _run(tmp_path, header_overrides={"erzeugt_am": "2026052014300000"})
        # Invalid: wrong century prefix
        with pytest.raises(G.FieldValidationError, match="erzeugt_am"):
            _run(tmp_path, header_overrides={"erzeugt_am": "19260520143000000"})

    def test_sachkonten_laenge_4_through_8(self, tmp_path):
        for n in (4, 5, 6, 7, 8):
            _run(tmp_path, header_overrides={"sachkonten_laenge": n})
        with pytest.raises(G.FieldValidationError, match="Sachkontenlänge"):
            _run(tmp_path, header_overrides={"sachkonten_laenge": 3})
        with pytest.raises(G.FieldValidationError, match="Sachkontenlänge"):
            _run(tmp_path, header_overrides={"sachkonten_laenge": 9})

    def test_rechnungslegungszweck_values(self, tmp_path):
        for n in (0, 30, 40, 50, 64):
            _run(tmp_path, header_overrides={"rechnungslegungszweck": n})
        with pytest.raises(G.FieldValidationError, match="Rechnungslegungszweck"):
            _run(tmp_path, header_overrides={"rechnungslegungszweck": 99})

    def test_sachkontenrahmen_skr_mapping(self, tmp_path):
        csv_path, _ = _run(tmp_path, skr="SKR03")
        line0 = csv_path.read_bytes().decode("cp1252").split("\r\n")[0]
        # Field 27 (1-indexed) is Sachkontenrahmen — should be "03"
        assert line0.split(";")[26] == '"03"'

        csv_path, _ = _run(tmp_path, skr="SKR04")
        line0 = csv_path.read_bytes().decode("cp1252").split("\r\n")[0]
        assert line0.split(";")[26] == '"04"'


# ---------------------------------------------------------------------------
# Data-row tests
# ---------------------------------------------------------------------------

class TestDataRow:
    def test_umsatz_rejects_zero(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="0,00 ist unzulässig"):
            _run(tmp_path, buchungen=_balanced_pair(umsatz="0,00"))

    def test_umsatz_valid_range(self, tmp_path):
        # 0,01 valid
        _run(tmp_path, buchungen=_balanced_pair(umsatz="0,01"))
        # 9999999999,99 (max 10 integer + 2 decimal) valid
        _run(tmp_path, buchungen=_balanced_pair(umsatz="9999999999,99"))

    def test_umsatz_rejects_too_many_integer_digits(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="Umsatz"):
            _run(tmp_path, buchungen=_balanced_pair(umsatz="12345678901,00"))

    def test_bu_schluessel_4_digit_quoted(self, tmp_path):
        csv_path, _ = _run(tmp_path, buchungen=_balanced_pair(bu_schluessel="9"))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        # Field 9 = BU-Schlüssel
        assert data_line.split(";")[8] == '"0009"'

        csv_path, _ = _run(tmp_path, buchungen=_balanced_pair(bu_schluessel="40"))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        assert data_line.split(";")[8] == '"0040"'

    def test_bu_schluessel_empty_emits_quoted_empty(self, tmp_path):
        """BU-Schlüssel is a text field; empty (Automatikkonto) emits as "" not bare.

        Per PRD §6 + Prüfprogramm Meldung 110.
        """
        csv_path, _ = _run(tmp_path)
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        assert data_line.split(";")[8] == '""'  # quoted-empty for text field

    def test_belegfeld_1_character_whitelist(self, tmp_path):
        # Allowed
        _run(tmp_path, buchungen=_balanced_pair(belegfeld_1="R-2026-04812"))
        _run(tmp_path, buchungen=_balanced_pair(belegfeld_1="LOHN-04-2026"))
        # Rejected: contains space + period
        with pytest.raises(G.FieldValidationError, match="Belegfeld 1"):
            _run(tmp_path, buchungen=_balanced_pair(belegfeld_1="Rg. 32029/2024"))

    def test_belegdatum_TTMM_format(self, tmp_path):
        _run(tmp_path, buchungen=_balanced_pair(belegdatum="3004"))
        with pytest.raises(G.FieldValidationError, match="Belegdatum"):
            _run(tmp_path, buchungen=_balanced_pair(belegdatum="30042026"))
        with pytest.raises(G.FieldValidationError, match="Belegdatum"):
            _run(tmp_path, buchungen=_balanced_pair(belegdatum="3004.04"))

    def test_buchungstext_60_char_limit(self, tmp_path):
        # 60 chars OK
        _run(tmp_path, buchungen=_balanced_pair(buchungstext="A" * 60))
        # 61 chars rejected
        with pytest.raises(G.FieldValidationError, match="Buchungstext"):
            _run(tmp_path, buchungen=_balanced_pair(buchungstext="A" * 61))

    def test_konto_max_9_digits(self, tmp_path):
        # 9 digits with sachkontenlaenge 8 → personenkonto, OK
        _run(tmp_path,
             header_overrides={"sachkonten_laenge": 8},
             buchungen=_balanced_pair(konto="123456789"))
        # 10 digits — too many
        with pytest.raises(G.FieldValidationError, match="Konto"):
            _run(tmp_path, buchungen=_balanced_pair(konto="1234567890"))

    def test_konto_personenkonto_one_digit_longer(self, tmp_path):
        # sachkontenlaenge=4: sachkonto 1-4 digits, personenkonto up to 5
        _run(tmp_path, buchungen=_balanced_pair(konto="12345"))  # personenkonto
        with pytest.raises(G.FieldValidationError, match="Konto"):
            _run(tmp_path, buchungen=_balanced_pair(konto="123456"))

    def test_generalumkehr_normalisation(self, tmp_path):
        # "G" → "1"
        csv_path, _ = _run(tmp_path, buchungen=_balanced_pair(generalumkehr="G"))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        assert data_line.split(";")[117] == '"1"'
        # true → "1"
        csv_path, _ = _run(tmp_path, buchungen=_balanced_pair(generalumkehr=True))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        assert data_line.split(";")[117] == '"1"'
        # false → quoted-empty (text field per PRD §6)
        csv_path, _ = _run(tmp_path, buchungen=_balanced_pair(generalumkehr=False))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        assert data_line.split(";")[117] == '""'

    def test_kost_menge_strict_format(self, tmp_path):
        _run(tmp_path, buchungen=_balanced_pair(kost_menge="000000000001,2345"))
        with pytest.raises(G.FieldValidationError, match="KOST-Menge"):
            _run(tmp_path, buchungen=_balanced_pair(kost_menge="1,23"))


# ---------------------------------------------------------------------------
# Format / encoding / determinism
# ---------------------------------------------------------------------------

class TestFormat:
    def test_crlf_line_endings(self, tmp_path):
        csv_path, _ = _run(tmp_path)
        raw = csv_path.read_bytes()
        # Every line ends with CRLF and there is a trailing CRLF
        assert raw.endswith(b"\r\n")
        # No lone LF
        assert b"\n" not in raw.replace(b"\r\n", b"")

    def test_encoding_cp1252_strict(self, tmp_path):
        # Emoji is not in CP1252 → should fail
        with pytest.raises(G.EncodingError):
            _run(tmp_path, buchungen=_balanced_pair(buchungstext="Test 🚀"))

    def test_encoding_utf8_sig_opt_in(self, tmp_path):
        # Emoji ok with UTF-8-sig
        csv_path, _ = _run(tmp_path,
                           encoding="utf-8-sig",
                           buchungen=_balanced_pair(buchungstext="Test 🚀"))
        raw = csv_path.read_bytes()
        # UTF-8 BOM
        assert raw.startswith(b"\xef\xbb\xbf")

    def test_row_count(self, tmp_path):
        csv_path, _ = _run(tmp_path)
        lines = [l for l in csv_path.read_bytes().decode("cp1252").split("\r\n") if l]
        # 1 header + 1 column-header + 2 data rows
        assert len(lines) == 4

    def test_row_2_field_count(self, tmp_path):
        csv_path, _ = _run(tmp_path)
        lines = csv_path.read_bytes().decode("cp1252").split("\r\n")
        assert len(lines[1].split(";")) == 125

    def test_row_3_plus_field_count(self, tmp_path):
        csv_path, _ = _run(tmp_path)
        lines = csv_path.read_bytes().decode("cp1252").split("\r\n")
        for data_line in lines[2:4]:
            assert len(data_line.split(";")) == 125

    def test_row_2_overrides(self, tmp_path):
        csv_path, _ = _run(tmp_path)
        col_header = csv_path.read_bytes().decode("cp1252").split("\r\n")[1].split(";")
        assert col_header[0] == '"Umsatz (ohne Soll/Haben-Kz)"'
        assert col_header[7] == '"Gegenkonto (ohne BU-Schlüssel)"'

    def test_quote_escaping(self, tmp_path):
        csv_path, _ = _run(tmp_path,
                           buchungen=_balanced_pair(buchungstext='Test "quoted" inside'))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        # Buchungstext is field 14 (index 13)
        assert data_line.split(";")[13] == '"Test ""quoted"" inside"'

    def test_empty_optional_text_field_emits_quoted_empty(self, tmp_path):
        csv_path, _ = _run(tmp_path,
                           buchungen=_balanced_pair(buchungstext=""))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        # Buchungstext default is _format_buchungstext which emits "" for empty
        assert data_line.split(";")[13] == '""'

    def test_empty_optional_numeric_field_emits_bare(self, tmp_path):
        csv_path, _ = _run(tmp_path)
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        # Field 4 (Kurs) — not set → bare empty
        assert data_line.split(";")[3] == ""

    def test_determinism_5_runs(self, tmp_path):
        """PRD §7: identical input → identical SHA-256 across 5 runs."""
        hashes = []
        for i in range(5):
            target = tmp_path / f"out_{i}.csv"
            inp = _write_input(tmp_path)
            G.generate(inp, target, format_version=13)
            hashes.append(hashlib.sha256(target.read_bytes()).hexdigest())
        assert len(set(hashes)) == 1, f"Non-deterministic outputs: {hashes}"


# ---------------------------------------------------------------------------
# Saldo + business rules
# ---------------------------------------------------------------------------

class TestSaldo:
    def test_balanced(self, tmp_path):
        _run(tmp_path)  # _balanced_pair default

    def test_unbalanced_raises_with_amounts(self, tmp_path):
        bs = [
            _minimal_buchung(umsatz="100,00", soll_haben_kennzeichen="S"),
            _minimal_buchung(umsatz="99,99", soll_haben_kennzeichen="H"),
        ]
        with pytest.raises(G.SaldoError, match="Σ Soll"):
            _run(tmp_path, buchungen=bs)

    def test_decimal_precision_balanced(self, tmp_path):
        bs = [
            _minimal_buchung(umsatz="33,33", soll_haben_kennzeichen="S"),
            _minimal_buchung(umsatz="33,33", soll_haben_kennzeichen="S"),
            _minimal_buchung(umsatz="33,34", soll_haben_kennzeichen="S"),
            _minimal_buchung(umsatz="100,00", soll_haben_kennzeichen="H",
                             konto="3300", gegenkonto="6815"),
        ]
        _run(tmp_path, buchungen=bs)


# ---------------------------------------------------------------------------
# Portal-inconsistency interpretations
# ---------------------------------------------------------------------------

class TestPortalInconsistency:
    def test_skontosperre_alternation_not_charclass(self, tmp_path):
        # 0 OK, 1 OK, anything else rejected (even the literal "|" the portal regex would allow)
        _run(tmp_path, buchungen=_balanced_pair(skontosperre="0"))
        _run(tmp_path, buchungen=_balanced_pair(skontosperre="1"))
        with pytest.raises(G.FieldValidationError, match="Skontosperre"):
            _run(tmp_path, buchungen=_balanced_pair(skontosperre="|"))

    def test_bvv_position_alternation_not_charclass(self, tmp_path):
        for v in ("1", "2", "3", "4", "5"):
            _run(tmp_path, buchungen=_balanced_pair(bvv_position=v))
        with pytest.raises(G.FieldValidationError, match="BVV-Position"):
            _run(tmp_path, buchungen=_balanced_pair(bvv_position="|"))

    def test_generalumkehr_accepts_g_or_1(self, tmp_path):
        for v in ("G", "1", "g", True):
            csv_path, _ = _run(tmp_path, buchungen=_balanced_pair(generalumkehr=v))
            data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
            assert data_line.split(";")[117] == '"1"', f"input {v} should emit '1'"

    def test_report_lists_interpretations(self, tmp_path):
        _, report = _run(tmp_path, buchungen=_balanced_pair(generalumkehr="G", skontosperre="1", bvv_position="3"))
        md = report.read_text(encoding="utf-8")
        assert "Skontosperre" in md
        assert "Generalumkehr" in md
        assert "BVV-Position" in md


# ---------------------------------------------------------------------------
# Synthetic fixtures
# ---------------------------------------------------------------------------

class TestSyntheticFixtures:
    """
    Spec-based fixtures per PRD §11.
    Marked unverified until promoted by Prüfprogramm (v2.2.0).
    """

    def test_lohn_sammelbuchung(self, tmp_path):
        """Lohn-Sammelbuchung: Gehalt 8.000 € + bAV 250 €; SV/LSt aufgeteilt."""
        bs = [
            _minimal_buchung(umsatz="8000,00", soll_haben_kennzeichen="S",
                             konto="6020", gegenkonto="3790",
                             belegfeld_1="LOHN-04-2026", buchungstext="Gehalt Mitarbeiter A 04/2026"),
            _minimal_buchung(umsatz="287,50", soll_haben_kennzeichen="S",
                             konto="6140", gegenkonto="3550",
                             belegfeld_1="BAV-04-2026", buchungstext="bAV-Beitrag 04/2026"),
            _minimal_buchung(umsatz="8287,50", soll_haben_kennzeichen="H",
                             konto="3790", gegenkonto="6020",
                             belegfeld_1="LOHN-04-2026", buchungstext="Sammelbuchung Lohn-Verb."),
        ]
        csv_path, report = _run(tmp_path, buchungen=bs)
        # Saldo balanced
        assert "✓ ausgeglichen" in report.read_text(encoding="utf-8")
        # 3 data rows
        lines = [l for l in csv_path.read_bytes().decode("cp1252").split("\r\n") if l]
        assert len(lines) == 5  # 1 header + 1 col header + 3 data

    def test_bewirtung_70_30_split(self, tmp_path):
        """Bewirtung: 70% abziehbar (Soll 70€), 30% n.a. (Soll 30€), VSt 19€, Kreditor 119€."""
        bs = [
            _minimal_buchung(umsatz="70,00", soll_haben_kennzeichen="S",
                             konto="6640", gegenkonto="3300",
                             belegfeld_1="REST-2026-0411", buchungstext="Bewirtung 70% abziehbar"),
            _minimal_buchung(umsatz="30,00", soll_haben_kennzeichen="S",
                             konto="6644", gegenkonto="3300",
                             belegfeld_1="REST-2026-0411", buchungstext="Bewirtung 30% n.a."),
            _minimal_buchung(umsatz="19,00", soll_haben_kennzeichen="S",
                             konto="1406", gegenkonto="3300",
                             belegfeld_1="REST-2026-0411", buchungstext="Vorsteuer 19%"),
            _minimal_buchung(umsatz="119,00", soll_haben_kennzeichen="H",
                             konto="3300", gegenkonto="6640",
                             belegfeld_1="REST-2026-0411", buchungstext="Kreditor"),
        ]
        _run(tmp_path, buchungen=bs)

    def test_eu_reverse_charge_13b(self, tmp_path):
        """§ 13b Abs. 1 EU-Sonstige Leistung: SaaS 1.500€."""
        bs = [
            _minimal_buchung(umsatz="1500,00", soll_haben_kennzeichen="S",
                             konto="6840", gegenkonto="3300",
                             belegfeld_1="CLOUD-MAI-26", buchungstext="SaaS-Abo Mai 2026"),
            _minimal_buchung(umsatz="285,00", soll_haben_kennzeichen="S",
                             konto="1407", gegenkonto="3837",
                             belegfeld_1="CLOUD-MAI-26", buchungstext="VSt 13b 19%",
                             eu_land_ustid_bestimmung="IE9999999X",
                             sachverhalt_l_l="1"),
            _minimal_buchung(umsatz="285,00", soll_haben_kennzeichen="H",
                             konto="3837", gegenkonto="1407",
                             belegfeld_1="CLOUD-MAI-26", buchungstext="USt 13b 19%"),
            _minimal_buchung(umsatz="1500,00", soll_haben_kennzeichen="H",
                             konto="3300", gegenkonto="6840",
                             belegfeld_1="CLOUD-MAI-26", buchungstext="Kreditor Acme Cloud"),
        ]
        _run(tmp_path, buchungen=bs)

    def test_ust_va_saldierung(self, tmp_path):
        """USt-VA-Saldierung Monatsende: USt 19% / VSt / Zahllast an Finanzamt."""
        bs = [
            _minimal_buchung(umsatz="9215,00", soll_haben_kennzeichen="S",
                             konto="3806", gegenkonto="1780",
                             belegfeld_1="USTVA-04-2026", buchungstext="USt 19% 04/2026 saldieren"),
            _minimal_buchung(umsatz="2940,00", soll_haben_kennzeichen="H",
                             konto="1406", gegenkonto="1780",
                             belegfeld_1="USTVA-04-2026", buchungstext="VSt 19% 04/2026 saldieren"),
            _minimal_buchung(umsatz="6275,00", soll_haben_kennzeichen="H",
                             konto="1780", gegenkonto="1789",
                             belegfeld_1="USTVA-04-2026", buchungstext="USt-Zahllast 04/2026"),
        ]
        _run(tmp_path, buchungen=bs)


# ---------------------------------------------------------------------------
# Additional coverage tests
# ---------------------------------------------------------------------------

class TestMisc:
    def test_invalid_format_version_raises(self, tmp_path):
        with pytest.raises(G.InputValidationError, match="Formatversion"):
            inp = _write_input(tmp_path)
            G.generate(inp, tmp_path / "out.csv", format_version=99)

    def test_unsupported_encoding_raises(self, tmp_path):
        with pytest.raises(G.InputValidationError, match="Encoding"):
            _run(tmp_path, encoding="latin-1")

    def test_input_must_be_object(self, tmp_path):
        inp = tmp_path / "input.json"
        inp.write_text("[]", encoding="utf-8")
        with pytest.raises(G.InputValidationError, match="Objekt"):
            G.generate(inp, tmp_path / "out.csv")

    def test_input_must_have_buchungen(self, tmp_path):
        inp = tmp_path / "input.json"
        inp.write_text(json.dumps({"header": _minimal_header(), "buchungen": []}), encoding="utf-8")
        with pytest.raises(G.InputValidationError, match="buchungen"):
            G.generate(inp, tmp_path / "out.csv")

    def test_header_erzeugt_am_missing(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="erzeugt_am"):
            _run(tmp_path, header_overrides={"erzeugt_am": ""})

    def test_header_berater_nr_out_of_range(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="Beraternummer"):
            _run(tmp_path, header_overrides={"berater_nr": 100})

    def test_header_wkz_invalid(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="WKZ"):
            _run(tmp_path, header_overrides={"wkz": "XX"})

    def test_header_bezeichnung_invalid_chars(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="Bezeichnung"):
            _run(tmp_path, header_overrides={"bezeichnung": "Test;mit;Semikolon"})

    def test_header_diktatkuerzel_lowercase_normalized(self, tmp_path):
        csv_path, _ = _run(tmp_path, header_overrides={"diktatkuerzel": "tg"})
        line0 = csv_path.read_bytes().decode("cp1252").split("\r\n")[0]
        assert line0.split(";")[17] == '"TG"'

    def test_data_konto_empty_rejected(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="Konto"):
            _run(tmp_path, buchungen=_balanced_pair(konto=""))

    def test_data_konto_zeros_rejected(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="Nullen"):
            _run(tmp_path, buchungen=_balanced_pair(konto="0000"))

    def test_data_soll_haben_invalid(self, tmp_path):
        bs = [
            _minimal_buchung(soll_haben_kennzeichen="X"),
            _minimal_buchung(soll_haben_kennzeichen="H"),
        ]
        with pytest.raises(G.SaldoError, match="Soll/Haben"):
            _run(tmp_path, buchungen=bs)

    def test_data_umsatz_missing(self, tmp_path):
        bs = [{"soll_haben_kennzeichen": "S", "konto": "6815", "gegenkonto": "3300"}]
        with pytest.raises(G.SaldoError, match="Umsatz fehlt"):
            _run(tmp_path, buchungen=bs)

    def test_data_umsatz_not_decimal(self, tmp_path):
        bs = [_minimal_buchung(umsatz="abc"), _minimal_buchung(soll_haben_kennzeichen="H", umsatz="abc")]
        with pytest.raises(G.SaldoError, match="Decimal"):
            _run(tmp_path, buchungen=bs)

    def test_belegdatum_invalid_tag(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="Tag/Monat"):
            _run(tmp_path, buchungen=_balanced_pair(belegdatum="3213"))

    def test_kost1_invalid_chars(self, tmp_path):
        with pytest.raises(G.FieldValidationError, match="KOST"):
            _run(tmp_path, buchungen=_balanced_pair(kost1="Test;mit;Semikolon"))

    def test_eu_two_letter_quoted(self, tmp_path):
        csv_path, _ = _run(tmp_path, buchungen=_balanced_pair(land="de"))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        assert data_line.split(";")[119] == '"DE"'

    def test_skontotyp_numeric(self, tmp_path):
        csv_path, _ = _run(tmp_path, buchungen=_balanced_pair(skontotyp="1"))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        assert data_line.split(";")[93] == "1"

    def test_zusatzinfo_round_trips(self, tmp_path):
        csv_path, _ = _run(tmp_path,
                           buchungen=_balanced_pair(
                               zusatzinfo_art_1="Filiale",
                               zusatzinfo_inhalt_1="Berlin Nord"))
        data_line = csv_path.read_bytes().decode("cp1252").split("\r\n")[2]
        fields = data_line.split(";")
        # Field 48 = Zusatzinfo Art 1, Field 49 = Inhalt 1 (1-indexed → index 47 / 48)
        assert fields[47] == '"Filiale"'
        assert fields[48] == '"Berlin Nord"'


class TestCLI:
    def test_cli_runs(self, tmp_path):
        inp = _write_input(tmp_path)
        out = tmp_path / "out.csv"
        rc = G.main(["--input", str(inp), "--output", str(out)])
        assert rc == 0
        assert out.exists()
        assert (tmp_path / "out.csv.report.md").exists()

    def test_cli_returns_1_on_error(self, tmp_path, capsys):
        inp = _write_input(tmp_path, buchungen=[_minimal_buchung(umsatz="0,00")])
        out = tmp_path / "out.csv"
        rc = G.main(["--input", str(inp), "--output", str(out)])
        assert rc == 1
        captured = capsys.readouterr()
        assert "FEHLER" in captured.err


class TestPruefprogrammMeldung110:
    """
    Regression tests for Prüfprogramm Meldung 110:
    "Das Textfeld 'X' ist nicht mit dem Textkennzeichen umgeben."

    Per PRD §6: text fields emit quoted-empty "" when empty;
    numeric/structured fields emit bare. Sample of text fields that previously
    leaked bare-empty due to handler-lambda short-circuits.
    """

    def _data_line(self, tmp_path):
        csv_path, _ = _run(tmp_path)
        return csv_path.read_bytes().decode("cp1252").split("\r\n")[2].split(";")

    def test_text_fields_empty_emit_quoted(self, tmp_path):
        fields = self._data_line(tmp_path)
        # Index = field_number - 1
        # Text fields known to be empty in the default minimal_buchung:
        text_empties = {
            3: "WKZ Umsatz",
            6: "WKZ Basis-Umsatz",
            9: "BU-Schlüssel",
            12: "Belegfeld 2",
            16: "Diverse Adressnummer",
            20: "Beleglink",
            21: "Beleginfo - Art 1",
            22: "Beleginfo - Inhalt 1",
            37: "KOST1",
            38: "KOST2",
            40: "EU-Land u. UStID (Bestimmung)",
            42: "Abw. Versteuerungsart",
            48: "Zusatzinformation - Art 1",
            91: "Forderungsart",
            95: "Auftragsnummer",
            96: "Buchungstyp",
            98: "EU-Mitgliedstaat (Anzahlungen)",
            102: "Herkunft-Kz",
            105: "SEPA-Mandatsreferenz",
            107: "Gesellschaftername",
            109: "Identifikationsnummer",
            110: "Zeichnernummer",
            118: "Generalumkehr",
            120: "Land",
            121: "Abrechnungsreferenz",
            123: "EU-Land u. UStID (Ursprung)",
        }
        for n, name in text_empties.items():
            assert fields[n - 1] == '""', (
                f"Field #{n} ({name}) emitted as {fields[n-1]!r}, expected '\"\"' "
                f"(text field empty per PRD §6)"
            )

    def test_numeric_fields_empty_emit_bare(self, tmp_path):
        fields = self._data_line(tmp_path)
        # Numeric/structured fields known to be empty in default minimal_buchung
        numeric_empties = {
            4: "Kurs",
            5: "Basis-Umsatz",
            15: "Postensperre",
            17: "Geschäftspartnerbank",
            41: "EU-Steuersatz",
            106: "Skontosperre",
            119: "Steuersatz",
            122: "BVV-Position",
            124: "EU-Steuersatz Ursprung",
            125: "Abw. Skontokonto",
        }
        for n, name in numeric_empties.items():
            assert fields[n - 1] == "", (
                f"Field #{n} ({name}) emitted as {fields[n-1]!r}, expected bare empty "
                f"(numeric field per PRD §6)"
            )
