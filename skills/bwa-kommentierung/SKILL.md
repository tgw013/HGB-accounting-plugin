---
name: bwa-kommentierung
description: BWA-/GuV-Kommentierung GmbH/UG — kanonische Markdown-Aufstellung aus DATEV-BWA, Materialitäts-Flagging, Folgefragen für vertiefende Analyse. Anwenden bei monatlicher/quartalsweiser/jährlicher BWA-Auswertung, Management-Reporting, GuV-Kommentar. Deutsches Pendant zu `financial-statements`.
---

> ⚠ **Hinweis:** Dieser Command ist konzipiert als Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-BWA-Formen 01/04/05, HGB §§ 266/275 Stand 2026-05). **Der Output beinhaltet keine Beratungsleistung.** Output ist als Vorschlag gedacht — vor Versand fachlich prüfen lassen.

# /bwa-kommentierung

**Typ:** `workflow` · **Anthropic-Pendant:** `financial-statements` (Kommentierungs-Teil; HGB-GKV-Gliederung statt US-GAAP, DATEV-BWA als Input) · **Geltungsbereich:** GmbH, UG · **Config:** `config/{active_year}/` · **Knowledge-Base:** `buchung-grundlagen`, `abweichungsanalyse`

Erzeugt aus einer DATEV-BWA (oder gleichwertigen P&L-Auswertung anderer Buchhaltungssoftware) sowie optional weiteren Inputs wie Excel-Planungsdateien, ERP-/CRM-/Sales-System-Datenexporten eine **kompakte Übersicht der wesentlichen Veränderungen**: kanonische GuV-Tabelle, gekennzeichnete materielle Abweichungen, Folgefragen für unerklärte Veränderungen, Verweis auf vertiefende Analyse mit `/abweichungsanalyse`.

**Was die Skill liefert:**
- Kanonische GuV-Markdown-Tabelle (einheitliches Format unabhängig von der Quell-Software)
- Kennzahlen-Übersicht (Margen-Kaskade, Cash-Conversion)
- Tabelle der materiellen Abweichungen mit Treiber-Hypothesen, soweit aus den Daten ableitbar
- Folgefragen an den Anwender für nicht erklärbare Bewegungen
- Hinweis-Liste für Detail-Analysen via `/abweichungsanalyse`

## Verwendung

```
/bwa-kommentierung <Periodenart> <Periode>
```

## Eingaben

- `Periodenart` — die Art der Berichtsperiode:
  - `Monat` — GuV für einen einzelnen Monat mit Vormonat sowie Vorjahresmonat als Vergleichsperioden
  - `Quartal` — Quartals-GuV mit Vorquartal sowie Vorjahresquartal als Vergleichsperioden
  - `Geschäftsjahr` — Geschäftsjahres-GuV mit Vorjahr als Vergleichsperiode
  - `YTD` — Jahr-bis-jetzt GuV mit Vorjahres-YTD als Vergleichsperiode
- `Periode` — Berichtsperiode (e.g., `Dezember 2026`, `Q4 2026`, `2026`)

## Workflow

### 1. Finanzdaten einlesen

Bitte den User nach folgenden Inputs, wenn sie nicht bereits vorliegen:

#### Pflicht-Inputs

- **Berichtsperiode/Berichtsperiodenart** (z.B. "März 2026", "Q1 2026", "YTD 2026-04")
- **GuV-/BWA-Auswertung** für die Periode — eines der folgenden Formate:
  * DATEV BWA-Form 01 (Standard-BWA, Kostenarten-Gliederung)
  * DATEV BWA-Form 05 (Gesamtkostenverfahren-BWA, § 275 Abs. 2 HGB-Gliederung)
  * DATEV BWA-Form 04 (Controllingreport-BWA, inkl. Kapitalflussrechnung)
  * Vergleichbarer Export aus Lexware, SAP B1, Sage, Xero, sonstigen — Format wird erkannt
- **Format:** PDF, Excel/CSV, oder Text-Paste der BWA-Tabelle

#### Optionale Inputs

- **Vorjahres-/Vormonats-Vergleich** — meist schon Teil der BWA (Entwicklungsübersicht / 3-Jahresvergleich bei DATEV)
- **Plan / Budget** — entweder als Soll-/Ist-Vergleich aus DATEV (selten, weil die meisten GmbHs in DATEV nicht planen) oder als separate Excel-/CSV-Datei mit Plan-Werten je GuV-Position
- **Kontextangaben zu bekannten Sondereffekten** (Einmal-Effekte, Timing-Effekte, strategische Maßnahmen) — z.B. in Form von ERP-/CRM-/Sales-System-Datenexporten

#### Format-Erkennung

Die Skill erkennt automatisch die GuV-Gliederungslogik:

| Gliederungs-Indikator                                                                            | Zugeordnete Form                  | GuV-Methode                                                       |
| ------------------------------------------------------------------------------------------------ | --------------------------------- | ----------------------------------------------------------------- |
| Zeile "Kostenarten:" → Personal-, Raum-, Fahrzeug-, Werbe-, Reisekosten etc.                     | DATEV BWA-Form 01                 | GKV-nah, aber nach Kostenarten gruppiert (kein reines § 275 HGB)  |
| "Personalaufwand", "Materialaufwand", "Abschreibungen", "Sonstiger betrieblicher Aufwand"        | DATEV BWA-Form 05 oder gleichwertig | GKV nach § 275 Abs. 2 HGB                                         |
| "Bruttoergebnis vom Umsatz", "Vertriebskosten", "Allgemeine Verwaltungskosten"                   | § 275 Abs. 3 HGB                  | UKV (selten in monatlicher BWA — meist Zwischenabschluss-Kontext) |
| Zusätzliche Sektion "Kapitalflussrechnung" mit Cashflow lfd./Investition/Finanzierung           | DATEV BWA-Form 04 oder gleichwertig | GKV-nah + Cashflow-Sektion                                        |

**Bei Unklarheit:** Skill fragt den Anwender: *"Ich erkenne die GuV-Gliederung nicht eindeutig. Handelt es sich um (a) GKV nach § 275 Abs. 2 HGB, (b) UKV nach § 275 Abs. 3 HGB, oder (c) DATEV-Kostenarten-BWA (BWA-Form 01)?"*

### 2. GuV tabellarisch aufbereiten

- BWA-Tabelle parsen, Werte extrahieren
- In kanonische Markdown-Tabelle überführen mit Überschrift: **Gewinn- und Verlustrechnung**, dann **Berichtsperiode: [Berichtsperiode benennen]**, dann Zahlenformaterklärung wie z.B. **(Beträge in Tausend € soweit nicht anders angegeben)**, dann Spalten: **Position | Berichts-Periode | Vergleichs-Periode | Δ absolut (€) | Δ % | Plan (falls vorhanden) | Δ vs. Plan**
- Bei DATEV-Form 01: Kostenarten-Struktur beibehalten
- Bei DATEV-Form 05 / § 275 HGB-Gliederung: § 275 Abs. 2 Reihenfolge
- Bei BWA-Form 04: zusätzliche Cashflow-Tabelle anhängen
- **Plan-Abweichungs-Berechnung** (falls Plan aus separater Quelle): Δ Plan-Ist je Position als € und %
- **Validierung:** Gesamtleistung – Gesamtkosten – Neutraler Aufwand + Neutraler Ertrag – Steuern = Vorläufiges Ergebnis (Toleranz 0,50 €)

### 3. Abweichungsanalyse

Für jede GuV-Position Berechnung und Bewertung der Abweichungen.

#### Berechnung pro Position

- **€ -Abweichung:** Berichts-Periode – Vergleichs-Periode (Vormonat / VJ-Monat / Plan)
- **%-Abweichung:** (Berichts – Vergleich) / |Vergleich| × 100
- **Basispunkte-Veränderung:** Für Margen und Quoten in Basispunkten (1 bp = 0,01 %) ausweisen

#### Materialitäts-Schwellen

Die Skill bestimmt, was als materielle Abweichung gilt. Übliche Ansätze:

- **Fester € -Schwellwert:** Abweichungen ab einem festen € -Betrag (z.B. 10 T€, 50 T€)
- **Fester %-Schwellwert:** Abweichungen ab einem festen Prozentwert (z.B. 5 %, 10 %, 15 %)
- **Kombiniert:** Entweder die €- oder die %-Schwelle wird überschritten
- **Skaliert:** Unterschiedliche Schwellen je nach Größe und Volatilität der Position

*Beispiel-Schwellen (an Mandanten-Größe und -Volatilität anpassen):*

| Positions-Größe (Berichts-Periode) | € -Schwelle | %-Schwelle |
| ---------------------------------- | ----------- | ---------- |
| > 1 Mio. €                         | 50 T€       | 5 %        |
| 100 T€ – 1 Mio. €                  | 10 T€       | 10 %       |
| < 100 T€                           | 5 T€        | 15 %       |

**Vorgehen:**
- Default: Skill schlägt einen Ansatz vor (i.d.R. *Kombiniert* mit der Beispiel-Skala oben) und macht das im Output transparent
- Anwender kann im Aufruf eigene Schwellen vorgeben (z.B. *"materielle Grenze € 25k oder 3%"*) — gilt dann für die laufende Konversation
- Optional kann ein Mandanten-spezifischer Default in `config/{active_year}/materialitaet.json` hinterlegt sein

#### Decomposition

Wesentliche Abweichungen, wenn möglich, in Treiber-Komponenten zerlegen:

- **Mengen-/Volumen-Effekt:** Mengen-Änderung zu Vorperiodenraten
- **Preis-/Tarif-Effekt:** Preis-/Tarif-Änderung bei aktueller Menge
- **Mix-Effekt:** Verschiebung der Zusammensetzung zwischen Positionen mit unterschiedlichen Raten/Margen
- **Neue / weggefallene Positionen:** in einer Periode vorhanden, in der anderen nicht
- **Einmal- / nicht-wiederkehrende Effekte:** Positionen, die sich nicht wiederholen werden
- **Timing-Effekte:** Verschiebungen zwischen Perioden (keine echte Run-Rate-Änderung)
- **Währungs-Effekte:** FX-Einfluss auf umgerechnete Werte (sofern Fremdwährungs-Konten vorhanden)

Eine vollständige Decomposition erfolgt nicht im Rahmen dieser Skill — sie wird an `/abweichungsanalyse` delegiert. Hier nur erste Hypothesen, soweit aus den Daten/Anwender-Kontext ableitbar.

#### Untersuchung und Erst-Hypothese

Für jede materielle Abweichung:

1. **Größe quantifizieren** (€ und %, ggü. welcher Vergleichsbasis)
2. **Richtung einordnen** — Verbesserung oder Verschlechterung (Achtung: bei Aufwendungen ist *Anstieg* eine Verschlechterung)
3. **Treiber-Hypothesen** aufstellen aus verfügbaren Daten:
   * Aus dem Kontoplan: welche Unterkonten sind die größten Bewegungs-Treiber? (DATEV-BWA zeigt das nicht — ggf. Saldenliste anfragen)
   * Aus Vorjahres-/Saisonalitätsmuster: ist die Bewegung erwartet?
   * Aus Anwender-Kontext (siehe Pflicht- und Optionale Inputs in §1 *Finanzdaten einlesen*): passt die Bewegung zu einem bekannten Sondereffekt?
4. **Unbekannte Treiber explizit benennen** statt zu spekulieren — Folgefragen für den Anwender formulieren
5. **Bei € 50T+ Abweichung in einer Einzelposition oder auf Anwender-Wunsch:** `/abweichungsanalyse` anbieten

#### Folgefragen

Liste von 3–8 spezifischen Fragen zu Punkten, die aus den Daten allein nicht erklärbar sind:

- *"Personalkosten +18 T€ ggü. März VJ — gab es Einstellungen, Tariferhöhung oder Bonus-Periodisierung?"*
- *"Reparatur/Instandhaltung 4.135 € (April) vs. 1.343 € (März) — handelt es sich um eine konkrete Maßnahme oder regelmäßige Wartung?"*

#### Abschlussangebot

Standardmäßig am Ende des Outputs:

> *"Für eine Detail-Decomposition (Preis/Menge/Mix, Personal: Headcount-Effekt vs. Tarif-Effekt, etc.) einer einzelnen Position bitte `/abweichungsanalyse <position> <periode>` aufrufen."*

### 4. Kennzahlen-Übersicht

Kompakte Tabelle mit den zentralen Kennzahlen, immer ausgewiesen:

| Kennzahl                                                              | Berichts-Periode | Vergleich | Δ              |
| --------------------------------------------------------------------- | ---------------- | --------- | -------------- |
| Gesamtleistung (€)                                                    | ...              | ...       | € / %          |
| Rohertrag-Marge (% von Gesamtleistung)                                | ...              | ...       | Basispunkte    |
| Betriebsergebnis-Marge (% von Gesamtleistung)                         | ...              | ...       | Basispunkte    |
| Ergebnis-Marge vor Steuern (% von Gesamtleistung)                     | ...              | ...       | Basispunkte    |
| Ergebnis-Marge nach Steuern (% von Gesamtleistung)                    | ...              | ...       | Basispunkte    |
| Cashflow lfd. Geschäftstätigkeit (% von Ergebnis nach Steuern)\*      | ...              | ...       | Basispunkte    |
| FCF / Gesamtleistung (FCF = Cashflow lfd. Geschäftstätigkeit + Cashflow Investition; in %)\* | ...              | ...       | Basispunkte    |

*\*nur bei BWA-Form 04 / Form 51 (Cashflow-Daten verfügbar)*

**Hinweis Cash-Conversion:** Bei sehr kleinem oder negativem Ergebnis nach Steuern ist die Cash-Conversion-Quote nicht aussagekräftig. Skill weist in solchen Fällen "n/a (Nenner ≈ 0)" oder den absoluten Cashflow-Wert aus und kommentiert die Verzerrung.

### 5. Tabelle materielle Abweichungen

Alle Positionen, die die Materialitätsschwelle (siehe §3 *Abweichungsanalyse*) reißen — kompakt in Tabellenform, ohne Prosa-Erläuterung:

| Position | Δ absolut (€) | Δ %   | Vergleichsbasis     | Richtung                       | Treiber-Hypothese (falls erkennbar) | Aktion             |
| -------- | ------------- | ----- | ------------------- | ------------------------------ | ----------------------------------- | ------------------ |
| ...      | ...           | ...   | Vormonat/VJ/Plan    | Verbesserung / Verschlechterung | ...                                 | Investigate / `/abweichungsanalyse` |

**Treiber-Hypothesen** nur eintragen, wenn aus den verfügbaren Daten ableitbar (Saisonalitätsmuster, bekannter Anwender-Kontext, eindeutiger Konto-Trigger). Spekulation wird nicht in die Tabelle aufgenommen, sondern in die Folgefragen (siehe §3 *Abweichungsanalyse*) verschoben.

**Aktion-Spalte:**
- `Investigate` — Anwender soll prüfen / Kontext liefern
- `/abweichungsanalyse` — bei Bewegungen ≥ € 50k in einer Einzelposition oder bei expliziter Anwender-Anfrage

### 6. Output-Format

```
# BWA-Übersicht [GmbH-Name]
## Berichtsperiode: [Monat/Quartal/YTD] [Jahr]
## Quelle: DATEV BWA-Form [01/04/05], Buchungs-Stand [Datum]

## 1. GuV-Übersicht
[Kanonische Markdown-Tabelle, siehe 2.]

## 2. Kennzahlen-Übersicht
[Tabelle, siehe 4.]

## 3. Materielle Abweichungen
[Tabelle, siehe 5.]

## 4. Offene Punkte / Folgefragen
[Liste, siehe 3.]

## 5. Hinweise
- Buchungs-Stand: [Datum]
- Abgrenzungs-/Abschlussbuchungen noch ausstehend: [ja/nein]
- Festschreibung (GoBD): [erfolgt/ausstehend]
- Quelle: [DATEV-BWA-Form X / Excel-Export von Software Y]
- Materialitäts-Schwellen verwendet: [Default-Beispiel-Skala / Anwender-Override / Mandanten-Config]

```

**Optional:** Excel-Begleit-Export der GuV-Tabelle (XLSX) mit Conditional-Formatting (rot/grün ab Materialitäts-Schwelle).

### 7. Validierung

- **GuV-Vollständigkeit:** alle Pflicht-Positionen vorhanden (Umsatzerlöse, Gesamtleistung, Rohertrag, Personalkosten, Abschreibungen, Sonstiger Aufwand, Betriebsergebnis, Steuern, Vorläufiges Ergebnis)
- **Rechnerische Konsistenz:** GuV-Saldo schlüssig (siehe 2.)
- **Materialitäts-Schwellen** korrekt angewendet, im Output transparent ausgewiesen
- **Hypothesen vs. Spekulation:** Treiber-Hypothesen nur in der Tabelle, wenn aus Daten/Kontext ableitbar — spekulative Treiber wandern in die Folgefragen
- **Plan-Daten-Provenienz:** wenn Plan kommentiert wird, Quelle benannt (DATEV-Soll-Werte / separate Excel-Datei / Anwender-Angabe)
- **Keine erfundenen Zahlen:** wenn Daten fehlen, im Output erwähnen ("Liquiditätsstand nicht in BWA-Form 01 enthalten")
- **Cash-Conversion-Verzerrung:** bei Nenner ≈ 0 oder negativ keine irreführende Quote ausweisen

## Quellen und Referenz-Material

### Primärquellen

- **HGB § 266** (Bilanzgliederung — Kontext): https://www.gesetze-im-internet.de/hgb/__266.html
- **HGB § 275** (GuV-Gliederung GKV/UKV): https://www.gesetze-im-internet.de/hgb/__275.html
- **DATEV-Dokumentation BWA-Formen** (Dok.-Nr. 9211723 — Übersicht; sowie Form-spezifisch 9211724 / 9211726 / 1021549)
- `config/{active_year}/materialitaet.json` (Schwellen-Override, optional)
- `config/{active_year}/kontenrahmen.json` (SKR03/SKR04-Mapping)

### Gliederungs-Referenz § 266 HGB (Bilanz)

Vollständige Gliederung der Bilanz nach § 266 Abs. 2 (Aktiva) und Abs. 3 (Passiva) HGB. Kleine Kapitalgesellschaften (§ 267 Abs. 1) dürfen eine verkürzte Bilanz aufstellen (nur die mit Buchstaben und römischen Zahlen bezeichneten Posten), Kleinst-Kapitalgesellschaften (§ 267a) eine weiter verkürzte (nur Buchstaben).

**Aktiva (§ 266 Abs. 2):**

```
A. Anlagevermögen
   I. Immaterielle Vermögensgegenstände
      1. Selbst geschaffene gewerbliche Schutzrechte und ähnliche Rechte und Werte
      2. entgeltlich erworbene Konzessionen, gewerbliche Schutzrechte und ähnliche
         Rechte und Werte sowie Lizenzen an solchen Rechten und Werten
      3. Geschäfts- oder Firmenwert
      4. geleistete Anzahlungen
   II. Sachanlagen
      1. Grundstücke, grundstücksgleiche Rechte und Bauten einschließlich der
         Bauten auf fremden Grundstücken
      2. technische Anlagen und Maschinen
      3. andere Anlagen, Betriebs- und Geschäftsausstattung
      4. geleistete Anzahlungen und Anlagen im Bau
   III. Finanzanlagen
      1. Anteile an verbundenen Unternehmen
      2. Ausleihungen an verbundene Unternehmen
      3. Beteiligungen
      4. Ausleihungen an Unternehmen, mit denen ein Beteiligungsverhältnis besteht
      5. Wertpapiere des Anlagevermögens
      6. sonstige Ausleihungen

B. Umlaufvermögen
   I. Vorräte
      1. Roh-, Hilfs- und Betriebsstoffe
      2. unfertige Erzeugnisse, unfertige Leistungen
      3. fertige Erzeugnisse und Waren
      4. geleistete Anzahlungen
   II. Forderungen und sonstige Vermögensgegenstände
      1. Forderungen aus Lieferungen und Leistungen
      2. Forderungen gegen verbundene Unternehmen
      3. Forderungen gegen Unternehmen, mit denen ein Beteiligungsverhältnis besteht
      4. sonstige Vermögensgegenstände
   III. Wertpapiere
      1. Anteile an verbundenen Unternehmen
      2. sonstige Wertpapiere
   IV. Kassenbestand, Bundesbankguthaben, Guthaben bei Kreditinstituten und Schecks

C. Rechnungsabgrenzungsposten

D. Aktive latente Steuern

E. Aktiver Unterschiedsbetrag aus der Vermögensverrechnung
```

**Passiva (§ 266 Abs. 3):**

```
A. Eigenkapital
   I. Gezeichnetes Kapital
   II. Kapitalrücklage
   III. Gewinnrücklagen
      1. gesetzliche Rücklage
      2. Rücklage für Anteile an einem herrschenden oder mehrheitlich
         beteiligten Unternehmen
      3. satzungsmäßige Rücklagen
      4. andere Gewinnrücklagen
   IV. Gewinnvortrag / Verlustvortrag
   V. Jahresüberschuss / Jahresfehlbetrag

B. Rückstellungen
   1. Rückstellungen für Pensionen und ähnliche Verpflichtungen
   2. Steuerrückstellungen
   3. sonstige Rückstellungen

C. Verbindlichkeiten
   1. Anleihen, davon konvertibel
   2. Verbindlichkeiten gegenüber Kreditinstituten
   3. erhaltene Anzahlungen auf Bestellungen
   4. Verbindlichkeiten aus Lieferungen und Leistungen
   5. Verbindlichkeiten aus der Annahme gezogener Wechsel und der
      Ausstellung eigener Wechsel
   6. Verbindlichkeiten gegenüber verbundenen Unternehmen
   7. Verbindlichkeiten gegenüber Unternehmen, mit denen ein
      Beteiligungsverhältnis besteht
   8. sonstige Verbindlichkeiten, davon aus Steuern, davon im Rahmen
      der sozialen Sicherheit

D. Rechnungsabgrenzungsposten

E. Passive latente Steuern
```

**Bei Forderungen und Verbindlichkeiten** ist jeweils der Betrag mit einer Restlaufzeit von mehr als einem Jahr gesondert anzugeben (§ 268 Abs. 4 / 5 HGB).

### Gliederungs-Referenz § 275 Abs. 2 HGB (GKV)

Vollständige Reihenfolge der Posten beim Gesamtkostenverfahren:

```
 1. Umsatzerlöse
 2. Erhöhung oder Verminderung des Bestands an fertigen und unfertigen Erzeugnissen
 3. andere aktivierte Eigenleistungen
 4. sonstige betriebliche Erträge
 5. Materialaufwand:
      a) Aufwendungen für Roh-, Hilfs- und Betriebsstoffe und für bezogene Waren
      b) Aufwendungen für bezogene Leistungen
 6. Personalaufwand:
      a) Löhne und Gehälter
      b) soziale Abgaben und Aufwendungen für Altersversorgung und Unterstützung,
         davon für Altersversorgung
 7. Abschreibungen:
      a) auf immaterielle Vermögensgegenstände des Anlagevermögens und Sachanlagen
      b) auf Vermögensgegenstände des Umlaufvermögens, soweit diese die im
         Unternehmen üblichen Abschreibungen überschreiten
 8. sonstige betriebliche Aufwendungen
 9. Erträge aus Beteiligungen, davon aus verbundenen Unternehmen
10. Erträge aus anderen Wertpapieren und Ausleihungen des Finanzanlagevermögens,
    davon aus verbundenen Unternehmen
11. sonstige Zinsen und ähnliche Erträge, davon aus verbundenen Unternehmen
12. Abschreibungen auf Finanzanlagen und auf Wertpapiere des Umlaufvermögens
13. Zinsen und ähnliche Aufwendungen, davon an verbundene Unternehmen
14. Steuern vom Einkommen und vom Ertrag
15. Ergebnis nach Steuern
16. sonstige Steuern
17. Jahresüberschuss / Jahresfehlbetrag
```

### Gliederungs-Referenz § 275 Abs. 3 HGB (UKV)

Vollständige Reihenfolge der Posten beim Umsatzkostenverfahren:

```
 1. Umsatzerlöse
 2. Herstellungskosten der zur Erzielung der Umsatzerlöse erbrachten Leistungen
 3. Bruttoergebnis vom Umsatz
 4. Vertriebskosten
 5. allgemeine Verwaltungskosten
 6. sonstige betriebliche Erträge
 7. sonstige betriebliche Aufwendungen
 8. Erträge aus Beteiligungen, davon aus verbundenen Unternehmen
 9. Erträge aus anderen Wertpapieren und Ausleihungen des Finanzanlagevermögens,
    davon aus verbundenen Unternehmen
10. sonstige Zinsen und ähnliche Erträge, davon aus verbundenen Unternehmen
11. Abschreibungen auf Finanzanlagen und auf Wertpapiere des Umlaufvermögens
12. Zinsen und ähnliche Aufwendungen, davon an verbundene Unternehmen
13. Steuern vom Einkommen und vom Ertrag
14. Ergebnis nach Steuern
15. sonstige Steuern
16. Jahresüberschuss / Jahresfehlbetrag
```

### DATEV-BWA-Form-01 Standard-Struktur

Die Kurzfristige Erfolgsrechnung in DATEV-Form-01 folgt einer Kostenarten-Gliederung, die der HGB-GKV-Logik ähnelt, aber davon abweicht. Typische Reihenfolge (SKR03/04):

```
   Umsatzerlöse
   Bestandsveränderung FE/UE
   Aktivierte Eigenleistungen
 = Gesamtleistung
   Material-/Wareneinkauf
 = Rohertrag
   Sonstige betriebliche Erlöse
 = Betrieblicher Rohertrag
   Kostenarten:
      Personalkosten
      Raumkosten
      Betriebliche Steuern
      Versicherungen / Beiträge
      Besondere Kosten
      Fahrzeugkosten (ohne Steuer)
      Werbe- / Reisekosten
      Kosten Warenabgabe
      Abschreibungen
      Reparatur / Instandhaltung
      Sonstige Kosten
 = Gesamtkosten
 = Betriebsergebnis
   Neutraler Aufwand (Zinsaufwand, sonstiger neutraler Aufwand)
   Neutraler Ertrag (Zinserträge, sonstiger neutraler Ertrag,
                     verrechnete kalkulatorische Kosten)
 = Ergebnis vor Steuern
   Steuern Einkommen und Ertrag
 = Vorläufiges Ergebnis
```

### Gliederungs-Referenz Cashflow (E-DRS 28 / DRS 21)

E-DRS 28 (bzw. der finale DRS 21) ist formal ein **Konzern-Standard** (Tz. 2-7: gilt für Mutterunternehmen nach § 290 HGB). Für den Einzelabschluss einer GmbH/UG ist er nicht bindend, dient hier aber als methodische Referenz: die DATEV-Kapitalflussrechnung in BWA-Form 04 / Form 51 lehnt sich strukturell eng an dieses Schema an.

**Grundprinzipien (E-DRS 28 Tz. 14-15, 23):**

- Drei Tätigkeitsbereiche: **laufende Geschäftstätigkeit, Investitionstätigkeit, Finanzierungstätigkeit**
- Cashflow aus der laufenden Geschäftstätigkeit: wahlweise **direkte** oder **indirekte** Methode
- Cashflow aus Investitions- und Finanzierungstätigkeit: **immer direkte** Methode
- Ausgangspunkt der indirekten Methode: **Periodenergebnis** (Jahresüberschuss/-fehlbetrag)
- Erhaltene Zinsen und Dividenden → Investitionstätigkeit (Tz. 45)
- Gezahlte Zinsen und Dividenden → Finanzierungstätigkeit (Tz. 48)
- Ertragsteuerzahlungen → grundsätzlich laufende Geschäftstätigkeit, gesondert auszuweisen (Tz. 17)

#### Mindestgliederungsschema I — Direkte Methode (E-DRS 28 Anlage 1)

```
 1.   Einzahlungen von Kunden für den Verkauf von Erzeugnissen, Waren und Dienstleistungen
 2.  – Auszahlungen an Lieferanten und Beschäftigte
 3.  + Sonstige Einzahlungen, die nicht der Investitions- oder Finanzierungstätigkeit
       zuzuordnen sind
 4.  – Sonstige Auszahlungen, die nicht der Investitions- oder Finanzierungstätigkeit
       zuzuordnen sind
 5.  + Einzahlungen aus außerordentlichen Posten
 6.  – Auszahlungen aus außerordentlichen Posten
 7. –/+ Ertragsteuerzahlungen
 8.  = Cashflow aus der laufenden Geschäftstätigkeit (Summe 1 bis 7)

 9.  + Einzahlungen aus Abgängen von Gegenständen des immateriellen Anlagevermögens
10.  – Auszahlungen für Investitionen in das immaterielle Anlagevermögen
11.  + Einzahlungen aus Abgängen von Gegenständen des Sachanlagevermögens
12.  – Auszahlungen für Investitionen in das Sachanlagevermögen
13.  + Einzahlungen aus Abgängen von Gegenständen des Finanzanlagevermögens
14.  – Auszahlungen für Investitionen in das Finanzanlagevermögen
15.  + Einzahlungen aus Abgängen aus dem Konsolidierungskreis
16.  – Auszahlungen für Zugänge zum Konsolidierungskreis
17.  + Einzahlungen aufgrund von Finanzmittelanlagen im Rahmen der kurzfristigen
       Finanzdisposition
18.  – Auszahlungen aufgrund von Finanzmittelanlagen im Rahmen der kurzfristigen
       Finanzdisposition
19.  + Einzahlungen aus außerordentlichen Posten
20.  – Auszahlungen aus außerordentlichen Posten
21.  + Erhaltene Zinsen
22.  + Erhaltene Dividenden
23.  = Cashflow aus der Investitionstätigkeit (Summe 9 bis 22)

24.  + Einzahlungen aus Eigenkapitalzuführungen von Gesellschaftern des Mutterunternehmens
25.  + Einzahlungen aus Eigenkapitalzuführungen von anderen Gesellschaftern
26.  – Auszahlungen aus Eigenkapitalherabsetzungen an Gesellschafter des Mutterunternehmens
27.  – Auszahlungen aus Eigenkapitalherabsetzungen an andere Gesellschafter
28.  + Einzahlungen aus der Begebung von Anleihen und der Aufnahme von (Finanz-) Krediten
29.  – Auszahlungen aus der Tilgung von Anleihen und (Finanz-) Krediten
30.  + Einzahlungen aus außerordentlichen Posten
31.  – Auszahlungen aus außerordentlichen Posten
32.  – Gezahlte Zinsen
33.  – Gezahlte Dividenden an Gesellschafter des Mutterunternehmens
34.  – Gezahlte Dividenden an die anderen Gesellschafter
35.  = Cashflow aus der Finanzierungstätigkeit (Summe 24 bis 34)

36.    Zahlungswirksame Veränderungen des Finanzmittelfonds (Summe 8, 23, 35)
37. +/– Wechselkurs- und bewertungsbedingte Änderungen des Finanzmittelfonds
38. +/– Konsolidierungskreisbedingte Änderungen des Finanzmittelfonds
39.  + Finanzmittelfonds am Anfang der Periode
40.  = Finanzmittelfonds am Ende der Periode (Summe 36 bis 39)
```

#### Mindestgliederungsschema II — Indirekte Methode (E-DRS 28 Anlage 1)

Identisch mit Schema I für die Bereiche Investition und Finanzierung; abweichend nur in der Herleitung des Cashflows aus der laufenden Geschäftstätigkeit:

```
 1.    Periodenergebnis (Jahresüberschuss/-fehlbetrag)
 2. +/– Abschreibungen/Zuschreibungen auf Gegenstände des Anlagevermögens
 3. +/– Zunahme/Abnahme der Rückstellungen
 4. +/– Sonstige zahlungsunwirksame Aufwendungen/Erträge
 5. –/+ Zunahme/Abnahme der Vorräte, der Forderungen aus Lieferungen und Leistungen
        sowie anderer Aktiva, die nicht der Investitions- oder Finanzierungstätigkeit
        zuzuordnen sind
 6. +/– Zunahme/Abnahme der Verbindlichkeiten aus Lieferungen und Leistungen sowie
        anderer Passiva, die nicht der Investitions- oder Finanzierungstätigkeit
        zuzuordnen sind
 7. –/+ Gewinn/Verlust aus dem Abgang von Gegenständen des Anlagevermögens
 8. +/– Zinsaufwendungen/Zinserträge
 9.  –  Sonstige Beteiligungserträge
10. +/– Aufwendungen/Erträge aus außerordentlichen Posten
11. +/– Ertragsteueraufwand/-ertrag
12.  +  Einzahlungen aus außerordentlichen Posten
13.  –  Auszahlungen aus außerordentlichen Posten
14. –/+ Ertragsteuerzahlungen
15.  =  Cashflow aus der laufenden Geschäftstätigkeit (Summe 1 bis 14)

[Investitions- und Finanzierungstätigkeit sowie Finanzmittelfonds-Überleitung:
 Positionen 16-47, identisch mit Schema I Positionen 9-40]
```

**Bezug zur DATEV-Kapitalflussrechnung (BWA-Form 04 / Form 51):** Die DATEV-Auswertung folgt strukturell dem direkten Schema (siehe Schema I oben), allerdings mit derivativer Ermittlung der Zahlungsströme aus den Konten der Finanzbuchhaltung. Abweichungen zu tatsächlichen Zahlungsströmen sind methodisch bedingt möglich.

### Typische Sondereffekte in der monatlichen BWA

Erfahrungswerte für die Hypothesen-Bildung — Bewegungen in der BWA können auf folgende **buchhalterische** Effekte zurückgehen, die keine Run-Rate-Aussage erlauben:

- **Abgrenzungs-Buchungen** (§ 250 HGB): ARAP/PRAP-Anpassungen zum Monatswechsel können einzelne Aufwands-/Ertragspositionen verschieben
- **Urlaubsrückstellung anteilig** (1/12 oder gemäß Mandanten-Methodik): erhöht Personalkosten ohne Cash-Effekt
- **Tantieme-Rückstellung GF:** typisch zum Quartals- oder Jahresende
- **AfA-Buchung:** monatliche Abschreibungs-Buchung kann verzögert sein, je nach Mandanten-Praxis
- **USt-Periodisierung:** Vorsteuer-Erstattungen / Zahllasten verschieben Liquidität, nicht das GuV-Ergebnis
- **Festschreibungs-Status (GoBD):** unfertige Periode kann sich noch ändern — Skill sollte den Stand ausweisen
- **Sonder-AfA / IAB nach § 7g EStG:** möglich, aber typisch nur zum Jahresabschluss gebucht

### Reklassifizierungen mit GuV-Auswirkung

- **Skonto-Aufwand vs. Erlös-Minderung:** je nach Mandanten-Praxis unterschiedlich verbucht — kann Umsatzerlöse oder Sonstigen Aufwand betreffen
- **Reisekosten-Klassifizierung:** Werbe-/Reisekosten vs. Fahrzeug- vs. Sonstige Kosten — SKR-Konto-Wahl beeinflusst BWA-Zeile
- **EWB / PWB Forderungen:** Wertberichtigungs-Buchungen schlagen sich in sonstigen betrieblichen Aufwendungen nieder

### DRS-Referenz (Hintergrund)

- **DRS 20** (Konzernlagebericht) und **E-DRS 28 / DRS 21** (Kapitalflussrechnung) sind Konzern-Standards, gelten formal nicht für Einzelabschlüsse von GmbH/UG. Dienen aber als methodische Referenz für Wesentlichkeits-Konzept und Kommentar-Struktur (DRS 20) sowie Cashflow-Gliederung (siehe Abschnitt *Gliederungs-Referenz Cashflow*). Siehe https://www.drsc.de

## Verwandte Skills

- `monatsabschluss` — vorgelagert: schließt die Bücher und stellt die BWA bereit
- `jahresabschluss` — vorgelagert für Jahres-BWA / Jahresabschluss-Kontext
- `abweichungsanalyse` — nachgelagert: Tiefenanalyse einer einzelnen Position (Preis/Menge/Mix-Decomposition)
- `buchung-grundlagen` — Hintergrund: Abschlussbuchungen, GoBD, SKR-Logik
- `steuerberater-handoff` — falls Output Teil eines StB-Pakets wird
