---
name: jahresabschluss
description: HGB-Jahresabschluss-Aufstellung GmbH/UG — Bilanz §266, GuV §275, Anhang §284-288, Größenklassen §267, Offenlegung §325.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# Jahresabschluss

**Typ:** `workflow`
**Anthropic-Pendant:** `close-management` + `financial-statements` (sinngemäß; HGB-Aufstellung statt US-GAAP) (siehe [anthropics/knowledge-work-plugins/finance](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance))
 GmbH, UG
**Config:** `config/{active_year}/`
**Knowledge-Base:** `buchung-grundlagen`

---

## 1. Zweck

**Aufstellung** des HGB-Jahresabschlusses für GmbH/UG (Bilanz, GuV, Anhang) und Vorbereitung der Steuerpositionen (KSt, GewSt, Solz). Keine Prüfung, kein Bundesanzeiger-Versand — Übergabe an StB/WP via `steuerberater-handoff` oder eigene Übernahme in DATEV.

## 2. Eingaben

- Geschäftsjahr (i.d.R. KJ; abweichendes WJ möglich, § 240 Abs. 2 HGB)
- Abschluss-Saldenliste (alle Konten, vor Umbuchungen)
- Inventur-Ergebnisse (§ 240 HGB)
- Anlagengitter / AfA-Tabellen (§ 7 EStG, AfA-Tabellen BMF)
- Rückstellungs-Anforderungen (Tantieme, Urlaub, Pension, drohende Verluste, Garantien)
- Vorjahres-Abschluss (für Vergleichsspalte § 265 Abs. 2 HGB)
- Größenklassen-Status (§ 267, 267a HGB)

## 3. Workflow

### 3.1 Größenklasse bestimmen (§ 267, 267a HGB)
Zwei der drei Schwellen in zwei aufeinanderfolgenden Jahren überschritten? Schwellen (Stand 2026, nach BilanzG-Anpassung):

| Klasse | Bilanzsumme | Umsatz | MA-Zahl |
|---|---|---|---|
| Kleinstkapges (§ 267a) | ≤ 450 T€ | ≤ 900 T€ | ≤ 10 |
| Klein (§ 267 Abs. 1) | ≤ 7,5 M€ | ≤ 15 M€ | ≤ 50 |
| Mittel (§ 267 Abs. 2) | ≤ 25 M€ | ≤ 50 M€ | ≤ 250 |
| Groß | darüber | darüber | darüber |

Konsequenzen: Aufstellungsfristen, Prüfungspflicht (§ 316 HGB ab mittelgroß), Offenlegungstiefe (§ 326 ff. HGB).

### 3.2 Anlage-/Umlaufvermögen
- AfA-Lauf abschließen (lineare/degressive, GwG-Sammelposten)
- Sonder-AfA prüfen (§ 7g EStG IAB/SoAfA — falls voraussetzungs-konform)
- Niederstwertprinzip Umlaufvermögen (§ 253 Abs. 4 HGB)
- Forderungen: Einzelwertberichtigung (EWB) und Pauschalwertberichtigung (PWB)
  - SKR04: EWB 1246/1247, PWB 1248/1249, EWB-Aufwand 6923, PWB-Aufwand 6920
  - SKR03: EWB 0998/0999, PWB 0996/0997, EWB-Aufwand 2451, PWB-Aufwand 2450

### 3.3 Rückstellungen (§ 249 HGB)
- **Steuerrückstellungen**: KSt + Solz, GewSt
  - SKR04: KSt-RST **3040**, GewSt-RST **3035**, Aufwand KSt **7600**, GewSt **7610**
  - SKR03: KSt-RST **0963**, GewSt-RST **0956**, Aufwand KSt **2200**, GewSt **2280**
- **Sonstige Rückstellungen**: Urlaub, Tantieme, Prozesskosten, Gewährleistung, Aufbewahrung, Abschluss- und Prüfungskosten
- Bewertung § 253 Abs. 1, 2 HGB: vernünftige kaufmännische Beurteilung; Abzinsung bei RLZ > 1 Jahr mit BBank-Durchschnittszins

### 3.4 Eigenkapital
- Jahresergebnis ermitteln (vorläufig, vor Steuern → nach Steuern)
- UG-Sonderfall: Rücklagenpflicht § 5a Abs. 3 GmbHG (25% bis Stammkapital 25 T€ erreicht ist)
- Gewinnverwendungsvorschlag (Vorbehalt Gesellschafterbeschluss)

### 3.5 Bilanz / GuV erstellen
- Bilanz nach § 266 HGB-Gliederung (klein vs. mittel/groß — § 266 Abs. 1 S. 3 erlaubt Verkürzung für kleine)
- GuV nach § 275 HGB: Gesamtkostenverfahren (GKV) oder Umsatzkostenverfahren (UKV)
- Vorjahres-Vergleichsspalte (§ 265 Abs. 2 HGB)

### 3.6 Anhang (§§ 284–288 HGB)
- Bilanzierungs- und Bewertungsmethoden
- Anlagengitter (§ 284 Abs. 3)
- Verbindlichkeitenspiegel (Restlaufzeiten § 285 Nr. 1)
- Haftungsverhältnisse (§ 285 Nr. 3)
- Organbezüge (§ 285 Nr. 9, mit Erleichterungen für kleine)
- Mitarbeiterzahl (§ 285 Nr. 7)

### 3.7 Lagebericht (entfällt für kleine + Kleinst, § 264 Abs. 1 S. 4)

## 4. Output-Format

- Bilanz und GuV als Markdown-Tabelle + Excel-Export-Option
- Anhang als strukturiertes Markdown-Dokument
- Steuerrückstellungs-Berechnungs-Begleitblatt (KSt/GewSt-Schätzung)
- Hinweis-Liste auf StB-Klärungsbedarf

## 5. Validierung

- **Bilanzgleichung**: Aktiva = Passiva (Toleranz 0,00 €)
- **GuV-Saldo** = Veränderung EK (Jahresergebnis)
- **§-266-Gliederung** vollständig (keine Position vergessen)
- **Vorjahres-Vergleichsspalte** vorhanden
- **Größenklassen-Konsequenz** korrekt angewendet (Erleichterungen genutzt / Pflichten erfüllt)
- **UG-Rücklagenpflicht** geprüft
- **Aufstellungs-Frist** § 264 Abs. 1 HGB (3 Mon. mittelgr./groß, 6 Mon. klein/Kleinst)
- **Offenlegungs-Frist** § 325 HGB (12 Mon., elektronisch zum Unternehmensregister seit 2022)

## 6. Quellen

- HGB §§ 240–289 (Buchführung, Aufstellung, Anhang, Lagebericht) — gesetze-im-internet.de/hgb/
- HGB §§ 325, 326 (Offenlegung)
- EStG §§ 5, 6, 7, 7g (Steuerbilanz, AfA, IAB)
- KStG, GewStG (Steuern vom Einkommen und Ertrag)
- GmbHG § 5a (UG-Rücklagenpflicht)
- AfA-Tabellen BMF (allgemeine + branchenbezogene)
- `config/2026/kontenrahmen.json`, `rates.json`, `fristen.json`

## 7. Verwandte Skills

- `buchung-grundlagen`, `monatsabschluss` — Vorarbeiten
- `abstimmung` — Konten-Verprobung
- `ebilanz` — XBRL-Datenpaket aus Jahresabschluss erzeugen
- `steuerberater-handoff` — Übergabe an StB für ELSTER/Bundesanzeiger
- `datev-export` — Sachkonten-Salden in DATEV
- `iks-pruefung` — falls Prüfungspflicht (mittelgr./groß)
