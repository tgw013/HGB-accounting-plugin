---
description: "eBilanz-Daten für XBRL/ERiC-Übermittlung aufbereiten."
---

# /ebilanz

Bereitet die E-Bilanz-Daten fuer die elektronische Uebermittlung im XBRL-Format via ERiC an die Finanzverwaltung vor.

## Referenzierter Skill

- `ebilanz`

## Workflow

1. **Anwendbarkeit pruefen** — Stelle fest, ob eine E-Bilanz-Pflicht besteht:
   - **Pflicht**: Alle bilanzierenden Steuerpflichtigen (§5b EStG)
   - **Keine E-Bilanz**: Steuerpflichtige mit EUER (§4 Abs. 3 EStG) — Hinweis geben und ggf. auf `/jahresabschluss` verweisen
   - Rechtsform bestimmt die anzuwendende Taxonomie (Kern, Ergaenzung, Branche)

2. **Taxonomie bestimmen** — Waehle die korrekte XBRL-Taxonomie:
   - **Kerntaxonomie 6.9** (vom 01.04.2025, BMF-Schreiben 10.06.2025): **Pflichtanwendung fuer Geschaeftsjahre ab 2026**
   - **Ergaenzungstaxonomien**: Krankenhaeuser, Pflegeeinrichtungen, Land- und Forstwirtschaft, etc.
   - **Branchentaxonomien**: Banken (RechKredV), Versicherungen (RechVersV)
   - Taxonomie-Version dem Wirtschaftsjahr zuordnen

3. **Konten auf Taxonomiepositionen mappen** — Ordne jeden Kontenrahmen-Eintrag (SKR03/SKR04) der entsprechenden Taxonomieposition zu (Beispiele illustrativ; exakte XBRL-IDs aus der jeweiligen Taxonomie-Veroeffentlichung):
   ```
   SKR03-Konto | DATEV-Bezeichnung 2026                 | Taxonomie-Bereich
   ──────────────────────────────────────────────────────────────────────
   0440        | Werkzeuge                              | Sachanlagen → Werkzeuge / Betriebsausstattung
   1200        | Bank                                   | Umlaufvermoegen → Guthaben bei Kreditinstituten
   1400        | Forderungen aus L+L                    | Umlaufvermoegen → Forderungen aus L+L
   ...
   ```

4. **Mussfelder befuellen** — Stelle sicher, dass alle Mussfelder (Pflichtpositionen) der Taxonomie ausgefuellt sind:
   - Mussfelder ohne Alternative: muessen immer befuellt werden
   - Mussfelder mit Auffangposition: koennen in Sammelposition eingehen
   - NIL-Werte: nur zulassig, wenn Position tatsaechlich nicht vorhanden
   - Pruefe Vollstaendigkeit aller Mussfelder

5. **Validierung durchfuehren** — Pruefe die E-Bilanz-Daten auf:
   - **Rechnerische Richtigkeit**: Aktiva = Passiva, GuV schliesst auf Jahresueberschuss
   - **Taxonomiekonformitaet**: Alle Positionen sind gueltige Taxonomie-IDs
   - **Mussfeld-Vollstaendigkeit**: Keine Pflichtfelder fehlen
   - **Plausibilitaet**: Summen stimmen, Vorzeichenlogik korrekt
   - Validierungsfehler auflisten mit konkreten Korrekturhinweisen

6. **Filing-Daten generieren** — Erstelle die uebermittlungsfertigen Daten:
   ```
   ══════════════════════════════════════════
   E-Bilanz — Uebermittlungsdaten
   Steuernummer: [XXX/XXX/XXXXX]
   Wirtschaftsjahr: [Beginn] bis [Ende]
   Taxonomie: Kerntaxonomie [Version]
   ══════════════════════════════════════════
   Bilanz (Aktiva)
     Anlagevermoegen:        xxx.xxx,xx EUR
       Immaterielle VG:        x.xxx,xx EUR
       Sachanlagen:          xxx.xxx,xx EUR
       Finanzanlagen:          x.xxx,xx EUR
     Umlaufvermoegen:        xxx.xxx,xx EUR
     ARAP:                     x.xxx,xx EUR
   ──────────────────────────────────────────
   Summe Aktiva:           x.xxx.xxx,xx EUR
   ...
   Validierungsstatus: bestanden / fehlerhaft
   ```

## Erwartete Eingaben

- Saldenliste mit Kontenzuordnungen (SKR03/SKR04)
- Rechtsform, Steuernummer, Wirtschaftsjahr
- Optional: Vorjahres-E-Bilanz fuer Vergleich

## Erwartete Ausgaben

- Mapping aller Konten auf Taxonomiepositionen
- Vollstaendigkeitspruefung der Mussfelder
- Validierungsbericht
- Uebermittlungsfertige E-Bilanz-Daten (tabellarisch)

## Hinweise

- E-Bilanz-Pflicht besteht seit 2013 fuer alle bilanzierenden Steuerpflichtigen.
- Uebermittlung ueber ELSTER (ERiC-Schnittstelle) oder zertifizierte Software.
- Abgabefrist entspricht der Steuererklaerungsfrist nach § 149 AO: **31.07. des Folgejahres** (ohne StB, § 149 Abs. 2 AO); **28.02. des Zweitfolgejahres** (mit StB, § 149 Abs. 3 AO — fuer VZ 2025 und folgende; in Schaltjahren faellt der 28.02. nicht auf den 29.02., da die gesetzliche Frist explizit "Februar" / Monatsende ist).
- Taxonomie-Updates jaehrlich pruefen — die Version muss zum Wirtschaftsjahr passen.
- Auffangpositionen nur nutzen, wenn eine genaue Zuordnung nicht moeglich ist.
