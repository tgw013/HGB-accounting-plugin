---
description: "Prüft GoBD-, HinSchG-, DCGK-Compliance und Aufbewahrungsfristen."
---

# /compliance

Prueft die Einhaltung von GoBD, Hinweisgeberschutzgesetz (HinSchG), DCGK und Aufbewahrungsfristen.

## Referenzierter Skill

- `compliance`

## Workflow

1. **Unternehmen identifizieren** — Erfasse die relevanten Stammdaten:
   - Rechtsform (GmbH, AG, Einzelunternehmen, etc.)
   - Mitarbeiterzahl (relevant fuer HinSchG-Schwellenwerte)
   - Boersennotierung (relevant fuer DCGK)
   - Branche (branchenspezifische Anforderungen)

2. **GoBD-Checkliste durchfuehren** — Pruefe die Grundsaetze zur ordnungsmaessigen Fuehrung und Aufbewahrung von Buechern, Aufzeichnungen und Unterlagen in elektronischer Form (BMF-Schreiben vom 28.11.2019):

   | Nr. | Anforderung | Pruefpunkt |
   |-----|-------------|------------|
   | 1 | Nachvollziehbarkeit | Belegprinzip, Buchungskette |
   | 2 | Nachpruefbarkeit | Verfahrensdokumentation vorhanden |
   | 3 | Vollstaendigkeit | Lueckenlose Erfassung aller Geschaeftsvorfaelle |
   | 4 | Richtigkeit | Sachliche und rechnerische Korrektheit |
   | 5 | Zeitgerechte Buchung | Erfassung innerhalb von 10 Tagen |
   | 6 | Ordnung | Systematische Ablage, Kontierungen |
   | 7 | Unveraenderbarkeit | Keine nachtraegliche Aenderung ohne Protokollierung |
   | 8 | Datenzugriff | Z1 (unmittelbar), Z2 (mittelbar), Z3 (Datentraeger) |

3. **HinSchG-Anforderungen pruefen** — Hinweisgeberschutzgesetz (seit Juli 2023):
   - Ab 50 Mitarbeiter: interne Meldestelle einrichten
   - Ab 250 Mitarbeiter: erweiterte Anforderungen
   - Anonyme Meldemoeglickeit pruefen
   - Dokumentation und Fristeneinhaltung (3 Monate Rueckmeldung)

4. **Aufbewahrungsfristen verifizieren** — Pruefe die Einhaltung der gesetzlichen Fristen (BEG IV / JStG 2024):

   | Dokumentenart | Frist | Rechtsgrundlage |
   |---------------|-------|-----------------|
   | Jahresabschluesse, Bilanzen, Inventare, Lageberichte | **10 Jahre** | §257 Abs. 4 Nr. 1 HGB |
   | Buchungsbelege (bis 31.12.2024 entstanden) | 10 Jahre | §257 Abs. 4 HGB a.F. |
   | Buchungsbelege (ab 01.01.2025 entstanden) | **8 Jahre** | §257 Abs. 4 HGB n.F. / §147 Abs. 3 AO n.F. |
   | Rechnungen (ab 01.01.2025) | **8 Jahre** | §14b UStG n.F. |
   | Rechnungen (vor 01.01.2025) | 10 Jahre | §14b UStG a.F. |
   | Handelsbriefe | 6 Jahre | §257 Abs. 4 Nr. 2 HGB |
   | Lohnunterlagen | 6 Jahre | §41 EStG |
   | Vertraege | 6-10 Jahre | je nach Art (Handelsbrief 6 J., Dauerschuld 10 J.) |
   | Verfahrensdokumentation | 10 Jahre | GoBD Tz. 151 |

5. **Compliance-Score berechnen** — Bewerte die Gesamtcompliance:
   - Je Bereich (GoBD, HinSchG, DCGK, Aufbewahrung): 0-100 %
   - Gewichteter Gesamtscore
   - Ampelbewertung: gruen (>80 %), gelb (50-80 %), rot (<50 %)

6. **Luecken berichten** — Erstelle einen Compliance-Bericht:
   ```
   ══════════════════════════════════════
   Compliance-Bericht
   Unternehmen: [Name]
   Stichtag: [Datum]
   ══════════════════════════════════════
   Bereich              Score    Status
   ─────────────────────────────────────
   GoBD                  85 %    gruen
   HinSchG               60 %    gelb
   Aufbewahrungsfristen  90 %    gruen
   DCGK                  n/a     ---
   ─────────────────────────────────────
   Gesamt                78 %    gelb
   ```
   Fuer jede Luecke: Massnahme, Verantwortlicher und Frist empfehlen.

## Erwartete Eingaben

- Unternehmensstammdaten (Rechtsform, Groesse, Branche)
- Vorhandene Dokumentation (Verfahrensdokumentation, Richtlinien)
- Informationen zu IT-Systemen und Archivierung

## Erwartete Ausgaben

- Compliance-Bericht mit Scoring pro Bereich
- GoBD-Checkliste mit Erfuellungsstatus
- HinSchG-Statusbewertung
- Liste der Aufbewahrungsfristen mit Pruefungsergebnis
- Massnahmenkatalog fuer identifizierte Luecken

## Hinweise

- GoBD betrifft alle buchfuehrungspflichtigen Unternehmen. Aktueller Stand: BMF-Schreiben vom 28.11.2019, aktualisiert per 14.07.2025 (2. Aenderung wegen E-Rechnungs-Pflicht).
- HinSchG gilt seit 02.07.2023 (50-249 MA seit 17.12.2023); Bussgeldrahmen gemaess § 40 HinSchG: **bis 500.000 EUR** fuer Behinderung von Meldungen, Vergeltungsmassnahmen oder Vertraulichkeitsbruch; **bis 20.000 EUR** fuer mangelhafte interne Meldestelle.
- DCGK (Fassung 28.04.2022) nur fuer boersennotierte AG verpflichtend (Comply or Explain nach § 161 AktG); fuer GmbH als Best Practice empfohlen.
- Aufbewahrungsfristen beginnen mit Ablauf des Kalenderjahres der Erstellung/Empfang.
- E-Rechnungs-Pflicht: 01.01.2025 Empfangspflicht (alle Unternehmen); 01.01.2027 Versandpflicht (Umsatz > 800.000 EUR Vorjahr); 01.01.2028 Versandpflicht (alle).
