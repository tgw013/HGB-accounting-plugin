---
name: abstimmung
description: Konten-Abstimmung Bank/Kasse/OP-Debitoren/OP-Kreditoren/USt/Intercompany — Differenz-Analyse, Klärungsvorschläge, EWB/PWB-Prüfung.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# Abstimmung

**Typ:** `workflow`
**Anthropic-Pendant:** `reconciliation` (siehe [anthropics/knowledge-work-plugins/finance](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance))
 GmbH, UG
**Config:** `config/{active_year}/kontenrahmen.json`
**Knowledge-Base:** `buchung-grundlagen`

---

## 1. Zweck

Verprobt Konto-Salden gegen externe Belege/Listen, identifiziert und klassifiziert Differenzen, schlägt Korrektur- oder Wertberichtigungs-Buchungen vor. Standardlauf im Monats- und Jahres-Closing.

## 2. Eingaben

- Stichtag (Monatsende / Jahresende)
- Buchhaltungs-Salden (Konto-Salden zu Stichtag)
- Externe Referenzen:
  - Bankauszüge (alle Konten)
  - Kassenbuch / Kassenbericht
  - OP-Listen Debitoren + Kreditoren
  - Inventur-Liste (Bestände)
  - Lohnjournal (für SV-/LSt-Verb.)
  - Saldenmitteilungen von verbundenen Unternehmen (Intercompany)
- Eskalations-Schwellen (Default: > 100 € klärungspflichtig, > 1.000 € sofort melden)

## 3. Workflow je Abstimmungs-Sektion

### 3.1 Bank
- Endsaldo Bankauszug ≙ Konto-Saldo SKR04 **1800** / SKR03 **1200**
- Differenzen klassifizieren: schwebende Buchung, Wertstellung, Bankgebühr ungebucht, Doppelbuchung

### 3.2 Kasse
- Kassenbericht (täglich!) ≙ Konto SKR04 **1600** / SKR03 **1000**
- Negativsalden → GoBD-Verstoß-Hinweis (Kasse kann nicht negativ werden)

### 3.3 Debitoren (OP-Liste)
- Summe Einzel-OP ≙ Sammelkonto SKR04 **1200** / SKR03 **1400**
- Altersstruktur: 0–30 / 31–60 / 61–90 / 91–180 / > 180 Tage
- **EWB-Prüfung**: konkrete Risiken (Insolvenz, Mahnstufe, Zahlungsverzug > 90 Tage)
  - SKR04: EWB-Konto **1247**, Einstellung **6923**
  - SKR03: EWB-Konto **0999**, Einstellung **2451**
- **PWB-Prüfung**: Pauschal 1–3% Restbestand uneinbringliche Forderungen (Branchen-erfahrungswert)
  - SKR04: PWB-Konto **1249**, Einstellung **6920**
  - SKR03: PWB-Konto **0997**, Einstellung **2450**

### 3.4 Kreditoren (OP-Liste)
- Summe Einzel-OP ≙ Sammelkonto SKR04 **3300** / SKR03 **1600**
- Altersstruktur: überfällige Verbindlichkeiten (Skonto-Verlust prüfen)
- Saldo-Mitteilungen Lieferanten (saldenbestätigung-konform JA)

### 3.5 USt-Konten
- USt 19% Saldo ≙ 19% der KZ-81-BG (Monat)
- USt  7% Saldo ≙  7% der KZ-86-BG
- Vorsteuer-Saldo ≙ Summe abzugsfähiger Vorsteuer aus Eingangsrechnungen
- §-13b-Konten: Steuer + Vorsteuer-Pendant (i.d.R. saldennull bei voller Abzugsberechtigung)

### 3.6 Lohnverbindlichkeiten
- SKR04 **3730** (LSt) ≙ LSt-Anmeldung
- SKR04 **3740** (SV) ≙ SV-Beitragsnachweis (alle Krankenkassen)
- (SKR03 1741, 1742)

### 3.7 Anlagenkonten (jährlich)
- Anlagengitter ≙ Saldenkonten (Anlagevermögen + kumulierte AfA)

### 3.8 Intercompany
- Forderung Mutter ≙ Verbindlichkeit Tochter (und v.v.); Saldennull konsolidiert

## 4. Output-Format

```
**Konten-Abstimmung 30.04.2026** (SKR04)

Konto / Bereich                          | Soll-Saldo  | Ist-Saldo  | Differenz | Status
1800 Bank Volksbank                      |  47.892,11  |  47.892,11 |     0,00  | ✓
1600 Kasse                               |     320,50  |     320,50 |     0,00  | ✓
1200 Debitoren (vs OP-Liste)             |  18.450,00  |  18.770,00 |   320,00  | !  Skonto Mandant X
3300 Kreditoren (vs OP-Liste)            | -12.700,00  | -12.700,00 |     0,00  | ✓
3806 USt 19%                             |   9.215,00  |   9.215,00 |     0,00  | ✓
3730 LSt-Verb.                           |   4.230,00  |   4.230,00 |     0,00  | ✓
3740 SV-Verb.                            |   8.812,00  |   8.815,40 |     3,40  | →  Rundung KV (ignorierbar)

EWB-/PWB-VORSCHLÄGE
- EWB Mandant Z (Insolvenz angemeldet): 100% auf 4.500 € → 6923/1247  4.500,00 €
- PWB Restforderungen 13.625 € × 1% = 136,25 € → 6920/1249  136,25 €

ESKALATIONEN
- Debitor X 320 € → 8736 (Skonto-Aufwand 19% USt) /1200 — Buchungsvorschlag
```

## 5. Validierung

- Differenz > Eskalations-Schwelle → in "Klärungspflichtig" markiert
- Banken-Differenz 0 oder via "schwebende Buchung"-Liste erklärt
- OP-Sammelkonto-Identität (Σ Einzel-OP = Sammel)
- USt-Konten rechnerisch konsistent
- EWB/PWB-Konto-Wahl korrekt je SKR (kein Verwechseln Aufwand vs. Wertberichtigung)

## 6. Quellen

- HGB §§ 252, 253, 266 — gesetze-im-internet.de/hgb/
- AO § 146 (Kasse, Festschreibung)
- DATEV SKR03/04 Art.-Nr. 11174/11175 — `config/2026/kontenrahmen.json`

## 7. Verwandte Skills

- `monatsabschluss` / `jahresabschluss` — ruft `abstimmung` auf
- `buchungssatz` — Korrektur-/EWB-/PWB-Buchungen
- `ust-voranmeldung` — USt-Konten-Verprobung
- `abweichungsanalyse` — Folge-Analyse bei Saldo-Anomalien
