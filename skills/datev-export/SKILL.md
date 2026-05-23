---
name: datev-export
description: Buchungsvorschläge als DATEV-Buchungsstapel-CSV (EXTF-Format) exportieren — importfähig in DATEV-Anwendungen.
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

- Liste von Buchungssätzen (aus `buchungssatz` oder strukturiert übergeben)
- Mandant: Berater-Nr., Mandanten-Nr., WJ-Beginn, Sachkontenlänge (4 oder 5)
- SKR-Variante (SKR03 / SKR04) — beeinflusst Konto-Validierung
- Buchungs-Zeitraum (von / bis)

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

**Implementation:** Die Generierung der CSV-Datei erfolgt deterministisch über das Hilfsscript `scripts/generate_extf.py`. Nach Erstellung des strukturierten Buchungssatz-JSON ruft dieser Skill das Script auf:

```bash
python scripts/generate_extf.py \
  --input /tmp/buchungen_2026-04.json \
  --output /tmp/EXTF_buchungsstapel_20260520_1430.csv \
  --format-version 13 \
  --encoding cp1252
```

Das Script validiert Eingaben (Saldengleichheit, Konto-Existenz, Belegfeld-Whitelist, Datums-Format), schreibt CSV mit korrekter Codierung (CP1252 default) und CRLF-Zeilenenden, und erzeugt einen `.report.md`-Begleitbericht mit SHA-256, Σ Soll / Σ Haben, verwendeten Konten + BU-Schlüsseln, und ausgelösten Portal-Inkonsistenz-Interpretationsregeln. Bei Validierungsfehlern bricht das Script mit klarer Fehlermeldung ab (Exit-Code 1).

Das Feld-Inventar (31 Header-Felder + 125 Datenspalten mit Regex + Beschreibung pro Formatversion) liegt deklarativ in `config/shared/datev-extf-fields.json` und ist PORTAL-verifiziert gegen developer.datev.de.

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

## 12. Determinism guarantee

Das Script `scripts/generate_extf.py` ist **byte-deterministisch**: identische Eingabe erzeugt identische CSV-Ausgabe (verifizierbar über SHA-256). Dies ist GoBD-relevant für die Verfahrensdokumentation: dieselbe Buchungssatz-Eingabe produziert reproduzierbar dieselbe Exportdatei, sodass jede Prüfung (Steuerberater-Review, Betriebsprüfung) dieselbe Datei zur Inspektion vorfindet.

Der Determinismus wird durchgesetzt durch (siehe `tests/test_extf_serializer.py::TestFormat::test_determinism_5_runs`):
- Keine Reihenfolgen-Manipulation (Input-Reihenfolge = Output-Reihenfolge; kein `sorted()`)
- Keine Zeitstempel innerhalb der CSV (nur im Begleit-`.report.md`)
- Keine locale-abhängige Zahlenformatierung (explizit `,` als Dezimaltrennzeichen)
- Explizites CRLF + CP1252-Encoding am Schreib-Boundary

Plus: vier dokumentierte Portal-Inkonsistenz-Interpretationsregeln (Header-Feld #5 Formatversion, Daten-Felder #106 Skontosperre, #118 Generalumkehr, #122 BVV-Position) werden im Begleit-Bericht ausgewiesen, wann immer sie ausgelöst wurden — Audit-Trail über jegliche Abweichung von der Portal-Literal-Regex.
