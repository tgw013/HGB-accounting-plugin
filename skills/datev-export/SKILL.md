---
name: datev-export
description: Buchungsvorschläge als DATEV-Buchungsstapel-CSV (EXTF-Format) exportieren — importfähig in DATEV-Anwendungen. Deterministisch (identische Eingabe → byte-identische CSV via SHA-256, GoBD-relevant) und DATEV-Prüfprogramm-validiert.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-EXTF-Formatbeschreibung, Header-Version 700/810, Stand 2026-05). **Ersetzt keine Steuerberatung.** Erzeugter Buchungsstapel ist Vorschlag — vor produktivem Import in DATEV-Mandant Stichprobe prüfen und Test-Import in Vorabbuchungsstapel ausführen.

# DATEV-Export

**Typ:** `workflow`
**Geltungsbereich:** GmbH, UG
**Config:** `config/{active_year}/kontenrahmen.json`, `config/shared/formats.json`
**Knowledge-Base:** `buchung-grundlagen`

---

## 1. Zweck

Wandelt einen oder mehrere Buchungsvorschläge (z.B. aus Skill `buchungssatz`) in eine **DATEV-EXTF-Buchungsstapel-CSV** um. Die Datei kann in DATEV (Rechnungswesen, Kanzlei-Rechnungswesen, Unternehmen online) als Vorabbuchungsstapel importiert und dort vom Anwender/StB geprüft und übernommen werden.

**Wichtig:** Direkter automatischer Import gegen Produktiv-Buchungen erfolgt nicht. Plugin produziert nur die Import-Datei.

## 2. Eingaben

- **Buchungssätze als JSON-Handoff** — kanonisch aus Skill `buchungssatz` (dessen Section 9). `buchungssatz` liefert `skr` + `buchungen[]`; dieser Skill ergänzt den `header` (Mandanten-Daten) und ruft den Serializer.
- Mandant: Berater-Nr., Mandanten-Nr., WJ-Beginn, Sachkontenlänge (4 oder 5)
- SKR-Variante (SKR03 / SKR04) — beeinflusst Konto-Validierung
- Buchungs-Zeitraum (von / bis)

### 2.1 Kanonisches Eingabe-Schema (Vertrag mit `buchungssatz`)

Der Serializer `scripts/generate_extf.py` liest ein Top-Level-Objekt:

```json
{ "header": { … 31 Mandanten-/Format-Felder … }, "skr": "SKR04", "buchungen": [ … ] }
```

- **`buchungssatz` liefert** `skr` + `buchungen[]` (Section 9 dort). **Dieser Skill ergänzt** den `header` aus den Mandanten-Eingaben.
- **`skr`** → Header-Feld Sachkontenrahmen: `"SKR03"`→`"03"`, `"SKR04"`→`"04"` (Mapping im Serializer).
- **Felder je Buchungszeile** (exakte Keys): `umsatz` (positiv, Komma-Dezimal), `soll_haben_kennzeichen` (`S`/`H`, bezieht sich auf `konto`), `wkz_umsatz` (`EUR`), `konto`, `gegenkonto`, `bu_schluessel` (leer = keine Automatik), `belegdatum` (`TTMM`), `belegfeld_1` (≤ 36, Zeichensatz `\w$&%*+-/`), `buchungstext` (≤ 60), optional `kost1`/`kost2`/`kost_allocations`, sowie bei § 13b/ig `eu_land_ustid_bestimmung` + `sachverhalt_l_l`.
- **`__`-präfigierte Felder** (z. B. `__comment`) werden **verworfen** und landen nicht in der CSV.
- **Saldo:** jede vollständige Zeile (Konto + Gegenkonto) ist in sich ausgeglichen; der Serializer prüft Σ Soll = Σ Haben über den Stapel. `buchungssatz` erzeugt deshalb **keine Spiegelzeilen** (vermeidet Doppelbuchung beim Import). Nur echte Splittsatz-Teilzeilen lassen `gegenkonto` leer.
- **§ 13b / ig-Erwerb:** als zwei vollständige Zeilen (Nettoaufwand → Kreditor; Vorsteuer 1407 → USt 3837 mit `eu_land_ustid_bestimmung` + `sachverhalt_l_l`), `bu_schluessel` leer — kein Automatik-Schlüssel.

## 3. EXTF-Format Grundlagen

DATEV-Buchungsstapel-CSV besteht aus:
- **Header-Zeile** (Zeile 1): Format-Identifikation, Versions-Header (700 oder 810), Mandanten-Daten, Codierung "CP1252" (Windows-1252 mit Umlauten)
- **Spalten-Header-Zeile** (Zeile 2): Feldnamen
- **Datenzeilen** ab Zeile 3: ein Buchungssatz pro Zeile

**Zeichensatz:** Windows-1252 (NICHT UTF-8). Umlaute korrekt nur in CP1252 — bei UTF-8-Export Import-Warnungen.

**Trenner:** Semikolon (`;`)
**Text-Quoting:** Anführungszeichen (`"`)
**Dezimaltrenner:** Komma (`,`)
**Datum:** TTMM (4-stellig, Tag+Monat des Wirtschaftsjahres)

## 4. Pflicht-Felder je Buchungssatz (Auszug)

| Feld | Beschreibung | Beispiel |
|---|---|---|
| Umsatz | Betrag (positiv) | 100,00 |
| Soll/Haben-Kennzeichen | "S" oder "H" für Vorzeichen Umsatz | S |
| WKZ Umsatz | Währung (i.d.R. EUR) | EUR |
| Konto | Sachkonto / Personenkonto | 6815 |
| Gegenkonto | (Sachkonto) | 3300 |
| BU-Schlüssel | USt-Automatik-Code (siehe DATEV-Liste) | 9 (19% Vorsteuer) |
| Belegdatum | TTMM | 1205 |
| Belegfeld 1 | Belegnummer | RE-2026-0418 |
| Buchungstext | Beschreibung | Büromaterial Lieferant XY |
| Kost1, Kost2 | Kostenstelle / -träger | (optional) |
| EU-Land u. UStID | bei §13b / ig | (optional) |

Vollständige Feldliste siehe DATEV-Format-Beschreibung "DATEV-Format" (DATEV-Online-Hilfedokument 1036228) oder DATEV-Schnittstellen-Entwicklerhandbuch.

## 5. BU-Schlüssel (gängige)

| Code | Bedeutung |
|---|---|
| 0 | keine USt-Automatik |
| 1 | steuerfreie Lieferung § 4 Nr. 1a, 6a |
| 2 | steuerfreie Leistung § 4 Nr. 8 ff. |
| 7 | Vorsteuer 7% |
| 8 | Vorsteuer 19% (alt — heute meist automatisch via Konto) |
| 9 | Vorsteuer 19% Soll |
| (weitere) | siehe DATEV-Doku |

**Hinweis:** Moderne DATEV-Praxis verwendet meist Automatik-Konten (Konto trägt USt-Code intrinsisch) — BU-Schlüssel dann 0 oder leer.

## 6. Workflow

1. Eingangs-Buchungen normalisieren (Datum, Beträge, Konten validieren gegen `kontenrahmen.json`)
2. Header-Zeile aufbauen (Berater-, Mandanten-Nr., WJ, Sachkontenlänge, Bezeichnung)
3. Strukturierten Input für den Serializer als JSON-Datei schreiben (siehe `tests/fixtures/` für Beispiele)
4. Serializer aufrufen (siehe §6.5) — Script schreibt CSV (31 Header-Felder + 125 Datenspalten-Header + N Buchungszeilen) + Begleit-Bericht

### 6.5 Implementation

**Implementation:** Die CSV-Generierung erfolgt deterministisch über das mitgelieferte Script `generate_extf.py` (Python 3.10+, stdlib-only). Es liegt im Plugin-Verzeichnis unter `scripts/generate_extf.py` und **findet seine Config selbst** (über `__file__` → `config/shared/datev-extf-fields.json` + `datev-automatik-konten.json`), ist also von **jedem** Arbeitsverzeichnis lauffähig — entscheidend ist nur der korrekte **absolute** Pfad zum Script.

**Pfad-Auflösung** (NICHT auf ein relatives `scripts/...` gegenüber dem aktuellen Arbeitsverzeichnis verlassen — das CWD ist i. d. R. nicht der Plugin-Root):
- **Claude Code:** Plugin-Root über `${CLAUDE_PLUGIN_ROOT}` auflösen, falls gesetzt; sonst das Plugin-Installationsverzeichnis ermitteln (dort liegt `scripts/generate_extf.py`).
- **Cowork:** das Script liegt im hochgeladenen Plugin-Ordner unter `scripts/generate_extf.py`.
- Im Zweifel `generate_extf.py` im Plugin-Verzeichnis lokalisieren und mit absolutem Pfad aufrufen.

```bash
# <PLUGIN_ROOT> = ${CLAUDE_PLUGIN_ROOT} (Claude Code) bzw. absoluter Plugin-Ordner (Cowork)
python "<PLUGIN_ROOT>/scripts/generate_extf.py" \
  --input /tmp/buchungen_2026-04.json \
  --output /tmp/EXTF_buchungsstapel_20260520_1430.csv \
  --format-version 13 \
  --encoding cp1252
```

Das Script validiert Eingaben (Saldengleichheit, Konto-Existenz, Belegfeld-Whitelist, Datums-Format), schreibt CSV mit korrekter Codierung (CP1252 default) und CRLF-Zeilenenden, und erzeugt einen `.report.md`-Begleitbericht mit SHA-256, Σ Soll / Σ Haben, verwendeten Konten + BU-Schlüsseln, und ausgelösten Portal-Inkonsistenz-Interpretationsregeln. Bei Validierungsfehlern bricht das Script mit klarer Fehlermeldung ab (Exit-Code 1).

Das Feld-Inventar (31 Header-Felder + 125 Datenspalten mit Regex + Beschreibung pro Formatversion) liegt deklarativ in `config/shared/datev-extf-fields.json` und ist PORTAL-verifiziert gegen developer.datev.de.

### 6.7 KOST-Splitt mit `kost_allocations` (v2.6+)

Wenn ein logischer Vorgang (z. B. 1000 € Miete) auf mehrere Kostenstellen verteilt werden soll, kann eine Buchung statt mehrfach copy-paste mit einem `kost_allocations`-Array geschrieben werden. Der Serializer expandiert sie automatisch in N flache Buchungen mit proportionalem Umsatz.

```json
{
  "umsatz": "1000,00",
  "soll_haben_kennzeichen": "S",
  "konto": "6310",
  "gegenkonto": "3300",
  "buchungstext": "Miete 04/2026",
  "kost_allocations": [
    {"kost1": "VERTRIEB",   "kost2": "", "anteil_prozent": "40,00"},
    {"kost1": "VERWALTUNG", "kost2": "", "anteil_prozent": "30,00"},
    {"kost1": "FundE",      "kost2": "", "anteil_prozent": "30,00"}
  ]
}
```

Semantik:

- `Σ anteil_prozent` muss exakt `100,00` ergeben — sonst Abbruch.
- Pro Allocation: `umsatz = original × anteil / 100`, kaufmännisch (Decimal, ROUND_HALF_EVEN) auf 2 Nachkommastellen gerundet.
- Rundungs-Residual landet auf der **letzten** Allocation — cent-exakte Summe garantiert.
- `konto`, `gegenkonto`, `belegfeld_1`, `buchungstext`, `belegdatum` werden geteilt; nur `kost1`/`kost2`/`kost_menge`/`umsatz` unterscheiden sich pro Output-Zeile.
- Saldo-Check läuft **nach** Expansion: die expandierten S-Zeilen summieren weiterhin gegen die H-Buchung.
- Backwards-compat: Buchungen ohne `kost_allocations` (flache `kost1`/`kost2`-Felder) bleiben unverändert.
- Der Sidecar-`.report.md` enthält eine Sektion `## KOST-Splittbuchungen (v2.6)` mit Quell-Buchung + Allocations-Breakdown zur Audit-Sichtbarkeit der Rundungs-Verteilung.

`[REASONED]` — kein DATEV-Portal-Pattern; pure Input-Schema-Erweiterung. Output-CSV bleibt 100 % Buchungsstapel-konform.

## 7. Output

- **CSV-Datei** (CP1252 / CRLF) mit Header-Zeile (31 Felder) + Spalten-Header-Zeile (125 Felder) + N Buchungs-Zeilen (je 125 Felder)
- **Begleit-`.report.md`-Datei** mit:
  - Anzahl Buchungssätze
  - Σ Soll / Σ Haben / Differenz (muss 0,00 sein)
  - Liste der verwendeten Konten + BU-Schlüssel
  - **SHA-256-Hash** der CSV-Datei (für GoBD-Verfahrensdokumentation)
  - Generierungs-Zeitstempel (ISO-8601 UTC)
  - Liste der ausgelösten Portal-Inkonsistenz-Interpretationsregeln
  - Import-Hinweis: "In DATEV als **Vorabbuchungsstapel** importieren, prüfen, dann erst freigeben"

## 8. Validierung

- **Saldengleichheit**: Σ Soll = Σ Haben (oder Aufteilung über Splittsätze konsistent)
- **Konto-Existenz** in `kontenrahmen.json` für gewählten SKR
- **Datum** im angegebenen Wirtschaftsjahr
- **Beleg-Pflichtfelder** vorhanden
- **Encoding-Check**: keine multibyte-Zeichen nach Konvertierung
- **Format-Konformität**: Header-Version unterstützt vom Ziel-DATEV-System

## 9. Out of Scope

- Direkter automatischer Import in DATEV-Mandant (Verantwortung beim Anwender/StB)
- Berichtigung bereits importierter Buchungen (über DATEV-Funktionen)
- DATEV-Anlagenverwaltung-Import (separate Schnittstelle)
- DATEV-Lohnimport (LODAS / Lohn und Gehalt — eigenes Format)

## 10. Quellen

- DATEV-Online-Hilfe: Format-Dokument "DATEV-Format" (Dokument-Nr. 1036228)
- DATEV-Entwicklerportal: Schnittstellen-Spezifikation EXTF
- `config/2026/kontenrahmen.json`
- `config/shared/formats.json` (Output-Format-Definitionen)

## 11. Verwandte Skills

- `buchungssatz` — liefert Einzel-Buchungen
- `monatsabschluss` — produziert Sammel-Buchungen
- `ust-voranmeldung` — kann als CSV exportieren
- `steuerberater-handoff` — Buchungsstapel ist Anlage zur StB-Übergabe
- `wiederkehrende-buchungen` — für **wiederholende** Buchungen (Monats-Beitragsübertrag etc.) statt einzelner Buchungen: DATEV-Format Kategorie 65, Version 4 (v2.5+)

## 11.1 Automatikkonten-Schutz (v2.3)

Das Plugin lehnt Buchungssätze ab, in denen ein Automatikkonto (AM- oder AV-Prefix der DATEV-Programmverbindung) mit einem nicht-leeren BU-Schlüssel verwendet wird — außer BU-Schlüssel `"0040"` (Aufhebung der Automatik).

**Hintergrund:** Automatikkonten haben USt-Automatik eingebaut. Wenn man trotzdem einen BU-Schlüssel setzt, weist DATEV den Import mit Fehler **REW00305** zurück ("Funktion 0 unzulässig, da Konto bereits einen automatischen Steuerschlüssel enthält"). Das Plugin fängt das vor dem Export ab.

**Konfiguration:** `config/shared/datev-automatik-konten.json` listet die Konten je SKR. Generiert mit `scripts/generate_automatik_konten.py` aus den DATEV-PDF-Extraktoren. Re-generieren bei jedem Jahres-Update (siehe `UPDATE_CHECKLIST.md` §3).

**Beispiel-Fehler:**
```
Buchung #1: REW00305-Verletzung — Konto 4400 ist Automatikkonto (Programmverbindung 'AM') +
BU-Schlüssel '9' ist gesetzt. Lösung: entweder BU-Schlüssel entfernen (Konto handhabt USt
automatisch), oder ein nicht-Automatikkonto wählen, oder BU-Schlüssel '0040' (Aufhebung
der Automatik) setzen wenn die Automatik explizit deaktiviert werden soll.
```

## 12. Determinism guarantee

Das Script `scripts/generate_extf.py` ist **byte-deterministisch**: identische Eingabe erzeugt identische CSV-Ausgabe (verifizierbar über SHA-256). Dies ist GoBD-relevant für die Verfahrensdokumentation: dieselbe Buchungssatz-Eingabe produziert reproduzierbar dieselbe Exportdatei, sodass jede Prüfung (Steuerberater-Review, Betriebsprüfung) dieselbe Datei zur Inspektion vorfindet.

Der Determinismus wird durchgesetzt durch (siehe `tests/test_extf_serializer.py::TestFormat::test_determinism_5_runs`):
- Keine Reihenfolgen-Manipulation (Input-Reihenfolge = Output-Reihenfolge; kein `sorted()`)
- Keine Zeitstempel innerhalb der CSV (nur im Begleit-`.report.md`)
- Keine locale-abhängige Zahlenformatierung (explizit `,` als Dezimaltrennzeichen)
- Explizites CRLF + CP1252-Encoding am Schreib-Boundary

Plus: vier dokumentierte Portal-Inkonsistenz-Interpretationsregeln (Header-Feld #5 Formatversion, Daten-Felder #106 Skontosperre, #118 Generalumkehr, #122 BVV-Position) werden im Begleit-Bericht ausgewiesen, wann immer sie ausgelöst wurden — Audit-Trail über jegliche Abweichung von der Portal-Literal-Regex.
