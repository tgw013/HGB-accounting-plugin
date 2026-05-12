---
name: iks-pruefung
description: IKS-Bewertung nach IDW PS 261 — 5 COSO-Komponenten, operative Audit-Schwerpunkte, Reife-Score, Maßnahmen-Backlog.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (HGB/EStG/UStG/KStG/SGB Stand 2026-05, IDW Prüfungsstandards). **Ersetzt keine Steuerberatung oder Wirtschaftsprüfer-Beurteilung.** Output ist Selbst-Einschätzung — bei prüfungspflichtigen Gesellschaften ist die Beurteilung durch den Abschlussprüfer maßgeblich.

# IKS-Prüfung

**Typ:** `methodology`
**Anthropic-Pendant:** SOX-404-Skill (US-Pendant, in DE durch IDW PS 261 ersetzt)
**Geltungsbereich:** GmbH, UG (besondere Relevanz für prüfungspflichtige Gesellschaften)
**Config:** —
**Knowledge-Base:** `buchung-grundlagen`, `gobd-konformitaet`

---

## 1. Zweck

Strukturierte Selbst-Bewertung des Internen Kontroll-Systems (IKS) nach den 5 COSO-Komponenten, wie sie in **IDW PS 261 n.F.** (Feststellung und Beurteilung von Fehlerrisiken) und IDW PS 720 angewendet werden. Output: Reife-Score je Komponente + priorisierter Maßnahmen-Backlog. Für mittelgroße/große GmbHs (§ 267 HGB), die der Pflichtprüfung unterliegen, dient das Plugin als Vorbereitung — die maßgebliche Beurteilung bleibt beim WP.

## 2. Eingaben

- Größenklasse (§ 267 HGB)
- Aktuelle Prozess-Beschreibungen (Einkauf, Verkauf, Lohn, Treasury, Closing)
- Berechtigungskonzept Buchhaltungs-System
- Vier-Augen-Prinzip-Regeln (Limits, Freigaben)
- Funktionstrennungs-Konzept (Sarbanes-Box / Segregation of Duties)
- Bestehende Kontrollen-Liste (z.B. Bankauszugs-Abgleich, Inventur-Prozess)

## 3. Die 5 COSO-Komponenten

### 3.1 Kontrollumfeld (Control Environment)
- Tone-at-the-top: Geschäftsführung lebt Compliance vor?
- Ethik-Richtlinien / Code of Conduct
- Berichts-/Hierarchie-Struktur klar
- Personal-Praktiken (Schulung, Hintergrund-Prüfung sensibler Rollen)

### 3.2 Risikobeurteilung (Risk Assessment)
- Risiko-Inventar Buchhaltung/Finanzen (Fraud, Fehler, IT-Ausfall, externe Bedrohungen)
- Wesentlichkeitsgrenzen definiert
- Veränderungs-Risiken (M&A, Systemwechsel, neue Geschäftsfelder)

### 3.3 Kontrollaktivitäten (Control Activities)
- **Funktionstrennung** zwischen Anweisung, Ausführung, Kontrolle, Verbuchung
- **Vier-Augen-Prinzip** bei Zahlungen ab Schwellwert
- **Genehmigungen** (Bestellungen, Verträge, Personal)
- **Abstimmungen** (Bank, OP, USt, Lohn — siehe Skill `abstimmung`)
- **Physische Sicherungen** (Tresor, Kassenführung)
- **IT-Kontrollen** (Berechtigungen, Backup, Change Mgmt., Logs)

### 3.4 Information + Kommunikation (Information & Communication)
- Berichtswesen funktioniert (BWA, Liquiditätsplanung, KPIs)
- Whistleblower-Kanal (HinSchG-Pflicht ab 50 MA — siehe Skill `hinschg-meldewesen`)
- Eskalations-Pfade definiert

### 3.5 Überwachung (Monitoring)
- Laufende Überwachungs-Aktivitäten (BWA-Reviews, Stichproben)
- Periodische Bewertungen (Selbst-Audit, externe Revision)
- Fehler/Auffälligkeiten-Nachverfolgung

## 4. Workflow

1. Für jede Komponente: aktueller Zustand → Reife-Stufe (1: ad hoc, 2: definiert, 3: integriert, 4: gemessen, 5: optimiert)
2. Lücken-Identifikation
3. Risiko-Klassifikation (hoch / mittel / niedrig)
4. Maßnahmen mit Verantwortlichem + Frist
5. Re-Assessment-Zyklus (i.d.R. jährlich + nach wesentlichen Änderungen)

## 5. Output-Format

```
**IKS-Selbst-Bewertung 2026-Q2** (GmbH, mittelgroß § 267 Abs. 2)

KOMPONENTE                      REIFE  KRITISCHE LÜCKEN
1. Kontrollumfeld                  4    —
2. Risikobeurteilung               3    Cyber-Risiko-Inventar nicht aktualisiert
3. Kontrollaktivitäten             3    SoD: Buchhalter darf auch Zahlung freigeben
4. Information + Kommunikation     2    Whistleblower-Kanal HinSchG fehlt
5. Überwachung                     3    Stichproben dokumentiert, aber unregelmäßig

PRIORISIERTER MAßNAHMEN-BACKLOG
P1  HinSchG-konformer Meldekanal einrichten   bis 30.06.2026  GF
P1  SoD: Zahlungsfreigabe nur 2-Personen      bis 31.05.2026  GF
P2  Cyber-Risiko-Inventar                     bis 30.09.2026  IT-Verantwortl.
P3  Stichproben-Plan formalisieren            bis 31.12.2026  Buchhaltung

NÄCHSTE PRÜFUNG: 2027-Q1 (vor JA-Prüfung WP)
```

## 6. Validierung

- Alle 5 Komponenten bewertet
- Maßnahmen SMART (spezifisch, messbar, zugewiesen, realistisch, terminiert)
- Wesentlichkeit der Lücken zur Größenklasse passend
- Konsistenz mit GoBD-Selbst-Check (Skill `gobd-konformitaet`)

## 7. Quellen

- IDW PS 261 n.F. (Feststellung und Beurteilung von Fehlerrisiken bei der Abschlussprüfung) — IDW Verlag
- IDW PS 720 (Bericht über die Erweiterung der Abschlussprüfung nach § 53 HGrG) — IDW Verlag
- COSO Internal Control - Integrated Framework (2013, weltweit Standard)
- HGB §§ 91 Abs. 2 AktG analog für GmbH (Risikofrüherkennungssystem), § 267, § 316
- HinSchG (Hinweisgeberschutzgesetz, 02.07.2023)

## 8. Verwandte Skills

- `gobd-konformitaet` — IT-Kontrollen-Teil
- `hinschg-meldewesen` — Whistleblower-Kanal
- `abstimmung` — Kontroll-Aktivitäten in der Praxis
- `jahresabschluss` — bei Prüfungspflicht
- `steuerberater-handoff` — bei WP-Prüfung
