---
name: buchungssatz
type: command
language: de
version: "2026"
description: >
  Workflow zur Erstellung von Buchungssätzen nach HGB/GoB.
  Automatische Prüfung auf Soll-Haben-Gleichheit, Kontengültigkeit
  und Belegpflicht. Referenziert buchungssatz-vorbereitung für
  Grundlagenwissen.
dependencies:
  - buchungssatz-vorbereitung
config:
  rates: config/rates-2026.json
  accounts: config/kontenrahmen.json
tags:
  - buchungssatz
  - journal-entry
  - soll-haben
  - workflow
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.


# Buchungssatz

Dieses Skill steuert den Workflow zur Erstellung, Prüfung und Freigabe
von Buchungssätzen. Für Grundlagenwissen zu GoB, Abgrenzungen und
Rückstellungen siehe das Skill `buchungssatz-vorbereitung`.

---

## 1. Buchungssatz-Format

### 1.1 Pflichtfelder

Jeder Buchungssatz besteht aus folgenden Pflichtfeldern:

| Feld           | Format                  | Beschreibung                          |
|----------------|-------------------------|---------------------------------------|
| Datum          | TT.MM.JJJJ             | Buchungsdatum                         |
| Soll-Konto     | 4-stellig (SKR)        | Konto gemäß config/kontenrahmen.json  |
| Haben-Konto    | 4-stellig (SKR)        | Konto gemäß config/kontenrahmen.json  |
| Betrag         | 1.234,56 €             | Buchungsbetrag in EUR                 |
| Buchungstext   | Freitext (max. 60 Z.)  | Beschreibung des Geschäftsvorfalls (DATEV-Export-Pflichtgrenze)    |
| Beleg-Nr.      | JJJJ-NNNNN             | Eindeutige Belegnummer                |

### 1.2 Betragsformat

- **Dezimaltrennzeichen**: Komma (,)
- **Tausendertrennzeichen**: Punkt (.)
- **Währung**: EUR (€)
- Beispiel: `12.345,67 €`

### 1.3 Skalierung

| Kürzel     | Bedeutung         | Faktor       |
|------------|-------------------|--------------|
| €          | Euro              | 1            |
| T€ / TEUR | Tausend Euro      | 1.000        |
| Mio.€      | Millionen Euro    | 1.000.000    |

In Buchungssätzen immer **volle EUR-Beträge mit Cent** verwenden.
Skalierte Darstellung nur in Berichten und Auswertungen.

### 1.4 Datumsformat

Immer **TT.MM.JJJJ**, z.B. `15.03.2026`.

### 1.5 Kontenreferenz

Kontennummern werden aus `config/kontenrahmen.json` geladen:

- **Standardkontenrahmen**: SKR03 (Default) oder SKR04
- **Sachkonten**: 4-stellig (0000–9999)
- **Personenkonten**: 5-stellig
  - Debitoren: 10000–69999
  - Kreditoren: 70000–99999

---

## 2. Buchungssatz-Template

### 2.1 Einzelbuchung

```
┌─────────────────────────────────────────────────────────────────┐
│ BUCHUNGSSATZ                                                     │
├──────────────┬──────────────────────────────────────────────────┤
│ Datum:       │ TT.MM.JJJJ                                      │
│ Beleg-Nr.:   │ JJJJ-NNNNN                                      │
├──────────────┼────────────┬────────────┬────────────────────────┤
│ Konto        │ Soll (EUR) │ Haben (EUR)│ Buchungstext           │
├──────────────┼────────────┼────────────┼────────────────────────┤
│ XXXX Name    │  1.234,56  │            │ Geschäftsvorfall       │
│ XXXX Name    │            │  1.234,56  │ Geschäftsvorfall       │
├──────────────┼────────────┼────────────┼────────────────────────┤
│ SUMME        │  1.234,56  │  1.234,56  │ ✓ Soll = Haben        │
├──────────────┴────────────┴────────────┴────────────────────────┤
│ Freigabe:    │ Name / Datum / Stufe                             │
└──────────────┴──────────────────────────────────────────────────┘
```

### 2.2 Sammelbuchung (Splitbuchung)

```
┌─────────────────────────────────────────────────────────────────┐
│ SAMMELBUCHUNG                                                    │
├──────────────┬──────────────────────────────────────────────────┤
│ Datum:       │ TT.MM.JJJJ                                      │
│ Beleg-Nr.:   │ JJJJ-NNNNN                                      │
├──────────────┼────────────┬────────────┬────────────────────────┤
│ Konto        │ Soll (EUR) │ Haben (EUR)│ Buchungstext           │
├──────────────┼────────────┼────────────┼────────────────────────┤
│ XXXX Name    │    500,00  │            │ Teilbetrag 1           │
│ XXXX Name    │    734,56  │            │ Teilbetrag 2           │
│ XXXX Name    │            │  1.234,56  │ Gegenbuchung           │
├──────────────┼────────────┼────────────┼────────────────────────┤
│ SUMME        │  1.234,56  │  1.234,56  │ ✓ Soll = Haben        │
└──────────────┴────────────┴────────────┴────────────────────────┘
```

---

## 3. Automatische Prüfungen

Vor der Freigabe werden folgende Prüfungen automatisch durchgeführt:

### 3.1 Soll-Haben-Gleichheit

```
PRÜFUNG: Summe Soll-Beträge == Summe Haben-Beträge
ERGEBNIS: ✓ Ausgeglichen / ✗ Differenz: X.XXX,XX €
```

Differenzen sind **nicht zulässig**. Ein Buchungssatz mit
Soll-Haben-Differenz darf nicht verbucht werden.

### 3.2 Kontengültigkeit

```
PRÜFUNG: Konto XXXX existiert in config/kontenrahmen.json
ERGEBNIS: ✓ Gültig / ✗ Konto nicht gefunden
```

- Prüfung gegen den gewählten Kontenrahmen (SKR03 oder SKR04)
- Sachkonten: 4-stellig, Kontenklassen 0–9
- Personenkonten: 5-stellig, Bereiche gemäß kontenrahmen.json

### 3.3 Belegpflicht

```
PRÜFUNG: Beleg-Nr. vorhanden und eindeutig
ERGEBNIS: ✓ Beleg vorhanden / ✗ Kein Beleg zugeordnet
```

Keine Buchung ohne Beleg (GoB-Grundsatz).

### 3.4 Plausibilitätsprüfung

- **Datumsplausibilität**: Buchungsdatum liegt im aktuellen oder
  abzuschließenden Geschäftsjahr.
- **Betragsprüfung**: Negativbeträge sind nicht zulässig (Storno über
  Gegenbuchung).
- **Doppelte Beleg-Nr.**: Warnung bei bereits vergebener Belegnummer.
- **USt-Schlüssel**: Bei umsatzsteuerrelevanten Konten ist ein gültiger
  USt-Satz erforderlich (19 % / 7 % / 0 %).

---

## 4. Workflow

### 4.1 Übersicht

```
┌───────────────────┐
│ 1. Geschäftsvor-  │
│    fall identi-   │
│    fizieren       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 2. Konten         │
│    bestimmen      │
│    (SKR03/SKR04)  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 3. Betrag         │
│    ermitteln      │
│    (netto/brutto) │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 4. USt prüfen     │
│    (19%/7%/frei)  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 5. Buchungssatz   │
│    formulieren    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 6. Automatische   │
│    Prüfung        │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ 7. Freigabe       │
│    (Betragsstufe) │
└─────────────────  ┘
```

### 4.2 Schritt 1: Geschäftsvorfall identifizieren

- Art des Vorfalls bestimmen (Eingangsrechnung, Ausgangsrechnung,
  Bankbewegung, Lohn, Abschreibung, etc.)
- Beleg sichten und Pflichtangaben prüfen (Datum, Betrag, Leistung)
- Periodenrichtige Zuordnung klären

### 4.3 Schritt 2: Konten bestimmen

- Kontenrahmen aus `config/kontenrahmen.json` laden
- Sachkonto(en) für Soll und Haben identifizieren
- Bei Personenkonten: Debitor/Kreditor zuordnen
- Kostenstelle/Kostenträger zuweisen (sofern vorhanden)

### 4.4 Schritt 3: Betrag ermitteln

- **Nettobetrag** bestimmen
- **Bruttobetrag** bei Bedarf berechnen (Netto + USt)
- Fremdwährungsbeträge in EUR umrechnen (Tageskurs EZB)

### 4.5 Schritt 4: Umsatzsteuer prüfen

Steuersätze aus `config/rates-2026.json` → `umsatzsteuer`:

| USt-Satz         | Wert  | Anwendung                              |
|------------------|-------|----------------------------------------|
| Normalsatz       | 19 %  | Standard für Waren und Dienstleistungen|
| Ermäßigter Satz  | 7 %   | Lebensmittel, Bücher, ÖPNV u.a.       |
| Steuerfrei       | 0 %   | §4 UStG (Ausfuhr, Heilberufe etc.)    |
| Reverse Charge   | —     | §13b UStG (Steuerschuldnerschaft)      |
| Innergemeinsch.  | —     | §4 Nr.1b UStG i.V.m. §6a UStG (i.g. Lief.); §1a UStG (i.g. Erwerb)  |
| Kleinunternehmer | —     | §19 UStG (≤25.000 € Vorjahr / ≤100.000 € lfd. Jahr ab 2025)        |

**Vorsteuer-Konten (SKR03):** 1570–1579
**Vorsteuer-Konten (SKR04):** 1400–1409
**USt-Konten (SKR03):** 1770–1779
**USt-Konten (SKR04):** 3800–3809

### 4.6 Schritt 5: Buchungssatz formulieren

- Template gemäß Abschnitt 2 befüllen
- Buchungstext aussagekräftig formulieren (Was? Wer? Wofür? Zeitraum?)
- Beleg-Nr. zuweisen

### 4.7 Schritt 6: Automatische Prüfung

Alle Prüfungen gemäß Abschnitt 3 durchführen. Bei Fehlern zurück
zum entsprechenden Schritt.

### 4.8 Schritt 7: Freigabe

Freigabe gemäß Betragsgrenzen-Matrix (siehe `buchungssatz-vorbereitung`,
Abschnitt 3).

---

## 5. Standardbuchungen — Beispiele

### 5.1 Wareneingang mit Vorsteuer

**Sachverhalt:** Einkauf von Handelswaren, Rechnung 2.380,00 € brutto
(2.000,00 € netto + 380,00 € USt 19 %).

**SKR03:**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext              | Beleg-Nr.   |
|------------|-------|------------|-------------|---------------------------|-------------|
| 15.03.2026 | 3200  | 2.000,00   |             | Wareneingang Lief. Müller | 2026-00142  |
| 15.03.2026 | 1576  |   380,00   |             | Vorsteuer 19 %            | 2026-00142  |
| 15.03.2026 | 1600  |            | 2.380,00    | Verb. LuL Lief. Müller    | 2026-00142  |

**SKR04:**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext              | Beleg-Nr.   |
|------------|-------|------------|-------------|---------------------------|-------------|
| 15.03.2026 | 5200  | 2.000,00   |             | Wareneingang Lief. Müller | 2026-00142  |
| 15.03.2026 | 1406  |   380,00   |             | Vorsteuer 19 %            | 2026-00142  |
| 15.03.2026 | 3300  |            | 2.380,00    | Verb. LuL Lief. Müller    | 2026-00142  |

### 5.2 Umsatzerlöse mit Umsatzsteuer

**Sachverhalt:** Verkauf von Dienstleistungen, Rechnung 5.950,00 € brutto
(5.000,00 € netto + 950,00 € USt 19 %).

**SKR03:**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext                | Beleg-Nr.   |
|------------|-------|------------|-------------|-----------------------------|-------------|
| 20.03.2026 | 1400  | 5.950,00   |             | Ford. LuL Kunde Schmidt     | 2026-00201  |
| 20.03.2026 | 8400  |            | 5.000,00    | Umsatzerlöse 19 % DL        | 2026-00201  |
| 20.03.2026 | 1776  |            |   950,00    | USt 19 %                    | 2026-00201  |

**SKR04:**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext                | Beleg-Nr.   |
|------------|-------|------------|-------------|-----------------------------|-------------|
| 20.03.2026 | 1200  | 5.950,00   |             | Ford. LuL Kunde Schmidt     | 2026-00201  |
| 20.03.2026 | 4400  |            | 5.000,00    | Umsatzerlöse 19 % DL        | 2026-00201  |
| 20.03.2026 | 3806  |            |   950,00    | USt 19 %                    | 2026-00201  |

### 5.3 Lohn- und Gehaltsbuchung

**Sachverhalt:** Bruttogehalt 4.500,00 €, AG-SV-Anteile 951,75 € (KV+RV+AV+PV mit Kind, Nicht-Sachsen), AN-SV-Anteile 951,75 € (analog), Lohnsteuer 1.200,00 €. Netto = 4.500 − 1.200 − 951,75 = **2.348,25 €** (Sätze aus `config/rates-2026.json`).

**SKR03** (Konten gemäß DATEV-SKR03 2026 — 1740 ist "Verb. Lohn und Gehalt", 1741 ist "Verb. Lohn- und Kirchensteuer (kombiniert)", **1742 ist "Verb. soziale Sicherheit" = Verb. SV**):

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext               | Beleg-Nr.   |
|------------|-------|------------|-------------|----------------------------|-------------|
| 31.03.2026 | 4120  | 4.500,00   |             | Bruttogehalt März 2026     | 2026-LG-003 |
| 31.03.2026 | 4130  |   951,75   |             | AG-Anteil SV März 2026     | 2026-LG-003 |
| 31.03.2026 | 1742  |            | 1.903,50    | Verb. SV (AG+AN) März 2026 | 2026-LG-003 |
| 31.03.2026 | 1741  |            | 1.200,00    | Verb. LSt/KiSt März 2026   | 2026-LG-003 |
| 31.03.2026 | 1200  |            | 2.348,25    | Nettolohn Auszahlung       | 2026-LG-003 |

Soll = 5.451,75 €; Haben = 5.451,75 € ✓ ausgeglichen.

**SKR04** (Konten gemäß DATEV-SKR04 2026 — 3730 ist "Verb. Lohn- und Kirchensteuer (kombiniert)", **3740 ist "Verb. soziale Sicherheit" = Verb. SV**):

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext               | Beleg-Nr.   |
|------------|-------|------------|-------------|----------------------------|-------------|
| 31.03.2026 | 6020  | 4.500,00   |             | Bruttogehalt März 2026     | 2026-LG-003 |
| 31.03.2026 | 6100  |   951,75   |             | AG-Anteil SV März 2026     | 2026-LG-003 |
| 31.03.2026 | 3740  |            | 1.903,50    | Verb. SV (AG+AN) März 2026 | 2026-LG-003 |
| 31.03.2026 | 3730  |            | 1.200,00    | Verb. LSt/KiSt März 2026   | 2026-LG-003 |
| 31.03.2026 | 1800  |            | 2.348,25    | Nettolohn Auszahlung       | 2026-LG-003 |

### 5.4 Planmäßige Abschreibung

**Sachverhalt:** Maschine, AHK 60.000,00 €, ND 10 Jahre, linear.
Monatliche AfA: 500,00 €.

**SKR03:**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext              | Beleg-Nr.   |
|------------|-------|------------|-------------|---------------------------|-------------|
| 31.03.2026 | 4830  |   500,00   |             | AfA Maschine M-2024-01    | 2026-AFA-03 |
| 31.03.2026 | 0210  |            |   500,00    | Maschine M-2024-01        | 2026-AFA-03 |

**SKR04** (Konto 6220 ist "Abschreibungen auf Sachanlagen" gemäß DATEV-SKR04 2026 — 6200 ist "Abschreibungen auf immaterielle VG"):

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext              | Beleg-Nr.   |
|------------|-------|------------|-------------|---------------------------|-------------|
| 31.03.2026 | 6220  |   500,00   |             | AfA Maschine M-2024-01    | 2026-AFA-03 |
| 31.03.2026 | 0440  |            |   500,00    | Maschine M-2024-01        | 2026-AFA-03 |

### 5.5 Bankzahlung einer Eingangsrechnung

**Sachverhalt:** Überweisung an Lieferant Müller, 2.380,00 €.

**SKR03:**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext              | Beleg-Nr.   |
|------------|-------|------------|-------------|---------------------------|-------------|
| 22.03.2026 | 1600  | 2.380,00   |             | Zahlung Lief. Müller      | 2026-BK-087 |
| 22.03.2026 | 1200  |            | 2.380,00    | Bank Überweisung          | 2026-BK-087 |

**SKR04:**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext              | Beleg-Nr.   |
|------------|-------|------------|-------------|---------------------------|-------------|
| 22.03.2026 | 3300  | 2.380,00   |             | Zahlung Lief. Müller      | 2026-BK-087 |
| 22.03.2026 | 1800  |            | 2.380,00    | Bank Überweisung          | 2026-BK-087 |

### 5.6 Reverse Charge (§13b UStG)

**Sachverhalt:** Eingangsrechnung EU-Dienstleister, netto 10.000,00 €.
Steuerschuldnerschaft geht auf Leistungsempfänger über.

**SKR03:**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext                   | Beleg-Nr.   |
|------------|-------|------------|-------------|--------------------------------|-------------|
| 18.03.2026 | 3123  | 10.000,00  |             | EU-DL §13b Firma XY           | 2026-00155  |
| 18.03.2026 | 1577  |  1.900,00  |             | VSt §13b 19 %                  | 2026-00155  |
| 18.03.2026 | 1787  |            |  1.900,00   | USt §13b 19 %                  | 2026-00155  |
| 18.03.2026 | 1600  |            | 10.000,00   | Verb. LuL Firma XY            | 2026-00155  |

### 5.7 Umsatzsteuer-Vorauszahlung

**Sachverhalt:** USt-Voranmeldung März 2026, Zahllast 3.200,00 €.

**SKR03:**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext              | Beleg-Nr.   |
|------------|-------|------------|-------------|---------------------------|-------------|
| 10.04.2026 | 1780  | 3.200,00   |             | USt-Zahllast März 2026    | 2026-UST-03 |
| 10.04.2026 | 1200  |            | 3.200,00    | Überweisung FA            | 2026-UST-03 |

### 5.8 Rechnungsabgrenzung (ARAP)

**Sachverhalt:** Versicherungsprämie 01.10.2026–30.09.2027,
Zahlung 2.400,00 € am 01.10.2026. Abgrenzung für 9 Monate (Jan–Sep 2027):
1.800,00 €.

**SKR03 (Jahresabschluss 31.12.2026):**

| Datum      | Konto | Soll (EUR) | Haben (EUR) | Buchungstext                | Beleg-Nr.    |
|------------|-------|------------|-------------|-----------------------------|--------------|
| 31.12.2026 | 0980  | 1.800,00   |             | ARAP Versicherung 01–09/27  | 2026-ABG-012 |
| 31.12.2026 | 4360  |            | 1.800,00    | Auflösung Versicherung      | 2026-ABG-012 |

---

## 6. Fehlerbehandlung

### 6.1 Häufige Fehler und Korrekturen

| Fehler                           | Korrektur                                     |
|----------------------------------|-----------------------------------------------|
| Soll ≠ Haben                    | Beträge prüfen, fehlende Position ergänzen    |
| Ungültiges Konto                 | Kontenrahmen prüfen (config/kontenrahmen.json)|
| Fehlende Beleg-Nr.              | Beleg zuordnen oder Eigenbeleg erstellen      |
| Falscher USt-Satz               | USt-Pflicht des Vorgangs prüfen               |
| Falsche Periode                  | Periodenrichtige Zuordnung sicherstellen      |
| Negativbetrag                    | Storno über Gegenbuchung durchführen          |

### 6.2 Stornobuchung

Falsche Buchungen werden **nicht gelöscht**, sondern durch eine
Gegenbuchung (Storno) neutralisiert. Anschließend wird die korrekte
Buchung erfasst.

```
Originalbuchung:    Konto A (Soll) an Konto B (Haben) — 1.000,00 €
Stornobuchung:      Konto B (Soll) an Konto A (Haben) — 1.000,00 €
Korrekturbuchung:   Konto C (Soll) an Konto D (Haben) — 1.000,00 €
```

Stornobuchungen erfordern immer das **Vier-Augen-Prinzip**.

---

## 7. DATEV-Kompatibilität

### 7.1 Export-Format

Buchungssätze können im **DATEV-Buchungsstapel-Format** exportiert
werden:

- Feldtrenner: Semikolon (;)
- Zeichensatz: Windows-ANSI (Codepage 1252) als Default; UTF-8 mit BOM optional bei neueren DATEV-Versionen
- Datumsformat: TTMM (4-stellig, ohne Punkt; Jahr aus Header-Wirtschaftsjahr)
- Betragsformat: Komma als Dezimaltrennzeichen, kein Tausenderpunkt
- Soll/Haben-Kennzeichen: S/H

### 7.2 Pflichtfelder DATEV-Export

| Nr. | Feld                | Beschreibung                       |
|-----|---------------------|------------------------------------|
| 1   | Umsatz              | Betrag ohne Vorzeichen             |
| 2   | Soll/Haben          | S oder H                           |
| 3   | Konto               | Soll- oder Haben-Konto             |
| 4   | Gegenkonto          | Gegenkonto                         |
| 5   | BU-Schlüssel        | Umsatzsteuer-Automatik             |
| 6   | Belegdatum          | TTMM                               |
| 7   | Belegfeld 1         | Belegnummer                        |
| 8   | Buchungstext        | Max. 60 Zeichen                    |

---

## 8. Referenzen

- Skill `buchungssatz-vorbereitung` — Grundlagenwissen GoB, Abgrenzungen
- `config/rates-2026.json` — Aktuelle Steuersätze und SV-Beiträge
- `config/kontenrahmen.json` — Kontenrahmen SKR03 und SKR04
- DATEV-Dokumentation — Buchungsstapel-Schnittstelle
