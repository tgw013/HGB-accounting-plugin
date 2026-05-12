---
name: datev-export
description: Buchungsvorschläge als DATEV-Buchungsstapel-CSV (EXTF-Format) exportieren — importfähig in DATEV-Anwendungen.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-EXTF-Formatbeschreibung, Header-Version 700/810, Stand 2026-05). **Ersetzt keine Steuerberatung.** Erzeugter Buchungsstapel ist Vorschlag — vor produktivem Import in DATEV-Mandant Stichprobe prüfen und Test-Import in Vorabbuchungsstapel ausführen.

# DATEV-Export

**Typ:** `workflow`
**Anthropic-Pendant:** (neu — DACH-spezifisch)
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
3. Spalten-Header gemäß Format-Version (700 oder 810 — 810 ist aktueller, mehr Felder)
4. Pro Buchung Zeile generieren
5. Encoding-Konvertierung UTF-8 → CP1252
6. Datei speichern (`.csv`) mit DATEV-Namens-Konvention: `EXTF_buchungsstapel_YYYYMMDD_HHMM.csv`

## 7. Output

- CSV-Datei mit Header + Buchungen
- Begleit-Markdown mit:
  - Anzahl Buchungssätze
  - Summe Soll / Summe Haben (muss übereinstimmen)
  - Validierungs-Status (alle Konten existieren? alle Pflicht-Felder?)
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
