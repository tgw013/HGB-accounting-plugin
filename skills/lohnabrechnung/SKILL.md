---
name: lohnabrechnung
description: Lohn-/Gehaltsabrechnung GmbH/UG — Brutto-Netto, SV-Beiträge, LSt/KiSt/Solz, bAV §3 Nr.63, Minijob/Midijob, Sachbezug, Buchungsverprobung.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# Lohnabrechnung

**Typ:** `workflow`
**Geltungsbereich:** GmbH, UG
**Config:** `config/{active_year}/rates.json`, `kontenrahmen.json`, `fristen.json`
**Knowledge-Base:** `buchung-grundlagen`

---

## 1. Zweck

Brutto-Netto-Berechnung und korrekte Verbuchung von Gehältern (Geschäftsführer + Mitarbeiter) sowie Hilfestellung bei Lohnsteueranmeldung, SV-Beitragsnachweis und Jahresmeldungen. Tatsächliche Abrechnung läuft i.d.R. in DATEV LODAS / Lexware Lohn — dieser Skill **verprobt und verbucht** das Lohnjournal, übernimmt nicht die laufende Lohnsteuerprogrammierung.

## 2. Eingaben

- Abrechnungsmonat
- Mitarbeiter-Stammdaten: Geburtsdatum, StKl., Kinderfreibeträge, Religion, KV-Wahltarif/Zusatzbeitrag, Kind ja/nein (PV-Zuschlag)
- Bruttogehalt, ggf. Sonderzahlungen, Sachbezüge
- bAV: Entgeltumwandlung + AG-Zuschuss
- Minijob (bis 603 €) / Midijob (Übergangsbereich bis 2.000 €) Klassifikation
- Lohnjournal aus Vor-System (falls vorhanden, dann Verprobung statt Neuberechnung)

## 3. Workflow

### 3.1 Sätze aus `rates.json` laden
- **Mindestlohn 2026:** 13,90 €/h (ab 2027: 14,60 €)
- **BBG (Stand 2026, einheitlich Ost/West seit 2025):**
  - RV/ALV: prüfen `rates.json`
  - GKV/PV: prüfen `rates.json`
- **PV-Satz:** Grundsatz; **+0,6 pp Zuschlag** für Kinderlose ≥ 23 J. (§ 55 Abs. 3 SGB XI); **Abschläge pro Kind** ab 2. Kind (§ 55 Abs. 3a SGB XI, gestaffelt)
- **Sachbezugswerte 2026:** Mittag/Abend 4,57 € (Frühstück abweichend)
- **Verpflegungspauschalen:** aus BMF-Liste in `rates.json`
- **Solz-Freigrenze 2026:** 20.350 € / 40.700 € (Einzel-/Zusammenveranlagung Jahres-LSt)

### 3.2 Brutto → SV-Brutto → St-Brutto → Netto
1. Brutto inkl. Sachbezüge, abzgl. Entgeltumwandlung bAV (bis 8% BBG-West RV steuer- und bis 4% BBG-West RV SV-frei, § 3 Nr. 63 EStG / § 1 SvEV)
2. SV-Brutto: getrennt KV/PV-Brutto vs. RV/ALV-Brutto (BBG-Cappung)
3. AN-Anteile SV
4. St-Brutto: weiterhin Sachbezüge berücksichtigen, bAV-Entgeltumwandlung mindert
5. LSt nach individuellem Tarif (Lohnsteuertabelle / ELStAM)
6. KiSt (8% oder 9% je Bundesland), SolZ (5,5% LSt, nur über Freigrenze)
7. Netto = St-Brutto − LSt − KiSt − SolZ − AN-SV

### 3.3 Arbeitgeber-Anteile
- AG-Anteil zur SV (spiegelbildlich zu AN, ohne PV-Zuschlag Kinderlose)
- **U1** (Krankheitskosten-Umlage, bis 30 MA Pflicht), **U2** (Mutterschutz-Umlage, alle), **Insolvenzgeldumlage** (alle)
- Unfallversicherung BG (jahrespauschal, Vorschuss + Spitzabrechnung)
- **bAV-Pflichtzuschuss 15%** bei Entgeltumwandlung (§ 1a Abs. 1a BetrAVG), soweit AG SV-Beiträge einspart

### 3.4 Sonderfälle
- **GF-Gehalt**: i.d.R. sozialversicherungsfrei bei beherrschend (≥ 50% oder Sperrminorität); Statusprüfung Clearingstelle. Auf jeden Fall LSt-pflichtig.
- **Minijob 603 €**: pauschal AG-Abgaben (KV 13% Gewerbe / 5% Privathaushalt, RV 15% / 5%, LSt 2% pauschal oder ELStAM); MA ggf. RV-Befreiung möglich
- **Midijob (Übergangsbereich 538,01–2.000 €)**: reduzierter AN-SV-Anteil
- **Sachbezüge** (Tankgutschein, Jobticket, Sachgeschenke): 50-€-Freigrenze § 8 Abs. 2 S. 11 EStG; Aufmerksamkeiten 60 € § 8 Abs. 1 S. 3
- **Kfz-Privatnutzung GF**: 1%-Regelung oder Fahrtenbuch; SV-pflichtig

### 3.5 Verbuchung (SKR04 / SKR03)
| Position | SKR04 | SKR03 |
|---|---|---|
| Gehälter (Lohnaufwand) | 6020 | 4120 |
| Geschäftsführer-Gehalt | 6027 | 4127 |
| AG-Anteil SV | 6110 | 4130 |
| Aufwand bAV | 6140 | 4165 |
| Pauschale Steuer auf sonstige Bezüge | 6147 | 4167 |
| Verb. LSt | 3730 | 1741 |
| Verb. SV | 3740 | 1742 |
| Verrechnungskonto Lohn/Gehalt | 3790 | 1755 (häufig) |

Buchungslogik gegen Verrechnungskonto, dann bei Zahlung gegen Bank.

### 3.6 Meldungen + Fristen (aus `fristen.json`)
- **LSt-Anmeldung**: bis 10. Folgemonat (§ 41a EStG)
- **SV-Beitragsnachweis**: 5 Arbeitstage vor Fälligkeit (§ 28h SGB IV)
- **SV-Fälligkeit**: drittletzter Bankarbeitstag (§ 23 SGB IV)
- **SV-Jahresmeldung** (DEÜV): bis 15.02. Folgejahr
- **LSt-Bescheinigung** (an FA + MA): bis 28.02. Folgejahr (§ 41b EStG)
- **UV-Jahresmeldung BG**: bis 16.02. Folgejahr

## 4. Output-Format

- Brutto-Netto-Übersicht je MA als Markdown-Tabelle
- Summen-/Salden-Tabelle für Verbuchung
- Buchungsvorschläge gegen Verrechnungskonto
- Frist-Hinweise mit Datum (verschoben bei WE/Feiertag § 108 Abs. 3 AO)
- StB-Hinweis-Liste bei Sonderfällen

## 5. Validierung

- **BBG-Kappung** auf SV-Brutto korrekt angewendet
- **PV-Zuschlag/-Abschlag** logisch (Kinderlos / N Kinder)
- **Solz-Freigrenze** beachtet
- **bAV ≤ 8% BBG RV-West** (Steuerfreiheit-Grenze § 3 Nr. 63 EStG)
- **Mindestlohn** eingehalten
- **Midijob-Berechnung** falls 538,01–2.000 € Brutto
- **Salden-Sanity**: Σ Gehälter + Σ AG-SV − Σ AN-SV − Σ LSt/KiSt/SolZ = Netto-Auszahlung MA + Zahlungen FA + SV-Träger

## 6. Quellen

- EStG §§ 3 Nr. 63, 8, 9, 19, 38, 39, 39b, 41, 41a, 41b — gesetze-im-internet.de/estg/
- SolzG (Solidaritätszuschlaggesetz)
- SGB IV §§ 23, 28h; SGB V; SGB VI; SGB XI § 55
- BetrAVG § 1, § 1a (Entgeltumwandlung + 15% AG-Zuschuss)
- MiLoG (Mindestlohn)
- Sozialversicherungs-Rechengrößenverordnung — jährlich BGBl
- Sachbezugswerte: Sozialversicherungsentgeltverordnung jährlich
- Mindestlohnkommission (mindestlohn-kommission.de)
- DEÜV (Datenerfassungs- und -übermittlungsverordnung)
- `config/2026/rates.json`, `fristen.json`, `kontenrahmen.json`

## 7. Verwandte Skills

- `buchungssatz` — Übernahme Lohn-Sammelbuchung
- `monatsabschluss` — verprobt Lohn-Konten
- `ust-voranmeldung` — keine direkte Berührung, aber gleiche Frist 10.
- `steuerberater-handoff` — bei komplexen GF-Konstellationen
