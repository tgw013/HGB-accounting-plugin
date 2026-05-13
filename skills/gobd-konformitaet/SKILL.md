---
name: gobd-konformitaet
description: GoBD-Anforderungen (BMF 28.11.2019) — Verfahrensdokumentation, Festschreibung, Datenzugriff Z1/Z2/Z3, Belegfunktion, E-Rechnung.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# GoBD-Konformität

**Typ:** `knowledge`
**Geltungsbereich:** GmbH, UG (gilt für alle Buchführungspflichtigen)
**Config:** `config/{active_year}/rates.json` (Aufbewahrungsfristen)
**Knowledge-Base:** `buchung-grundlagen`

---

## 1. Zweck

Erklärt die zentralen GoBD-Anforderungen für Buchführung mit IT-Unterstützung und gibt Anwendern eine Selbst-Check-Liste zur Verfahrensdokumentation. Wissensbasis — kein eigener Workflow-Output, andere Skills referenzieren.

## 2. GoBD im Überblick

**Grundsätze zur ordnungsmäßigen Führung und Aufbewahrung von Büchern, Aufzeichnungen und Unterlagen in elektronischer Form sowie zum Datenzugriff** — BMF-Schreiben vom 28.11.2019, ergänzt um BMF-Schreiben 11.07.2022 (E-Rechnung-Anforderungen).

Bindende Verwaltungsanweisung. Rechtsgrundlage: §§ 145–147 AO, §§ 238–239, 257 HGB.

## 3. Kern-Anforderungen

### 3.1 Allgemeine Ordnungsmäßigkeit (Tz. 21 ff.)
- **Vollständigkeit** — alle Geschäftsvorfälle erfasst
- **Richtigkeit** — sachlich + rechnerisch korrekt
- **Zeitgerecht** — laufende Buchungen "zeitnah"; Kasse täglich (§ 146 Abs. 1 AO); sonst spätestens 10. Folgemonat (faktischer Praxis-Standard, kein harter Gesetzes-Text — Risiko bei längeren Verzögerungen)
- **Ordnung** — systematische Belegfolge, klare Klassifikation
- **Unveränderbarkeit** — Festschreibung (Tz. 107 ff.)
- **Nachvollziehbarkeit + Nachprüfbarkeit** — Sachverständiger Dritter muss sich in angemessener Zeit zurechtfinden (§ 145 AO)

### 3.2 Belegfunktion (Tz. 61 ff.)
- "Keine Buchung ohne Beleg"
- Eindeutige Beleg-Nummer / -Referenz
- Beleg-Inhalt nach § 14 UStG für Rechnungen
- Eigenbelege nur Notlösung, mit klarer Begründung

### 3.3 Unveränderbarkeit / Festschreibung (Tz. 107 ff.)
- Buchungen müssen nach Erfassung gegen unbemerkte Änderung gesichert sein
- "Festschreibung" — in DATEV: explizit auf Periodenebene
- **Spätester Festschreibungs-Zeitpunkt**: vor Übermittlung der USt-VA (vorgangsbezogene Sicht); zumindest aber bis zum gesetzlichen Bilanzaufstellungstermin

### 3.4 Aufbewahrung (Tz. 119 ff., § 147 AO)
- Buchungsbelege:
  - vor 01.01.2025 entstanden: **10 Jahre**
  - ab 01.01.2025 entstanden: **8 Jahre** (Viertes Bürokratieentlastungsgesetz)
- Handels-/Geschäftsbriefe: 6 Jahre
- Jahresabschlüsse, Inventare, Buchungsjournale: 10 Jahre
- **Format-Treue**: elektronische Originalrechnung muss elektronisch bleiben — Papier-Ausdruck genügt nicht

### 3.5 Datenzugriff (Tz. 159 ff., § 147 Abs. 6 AO)
- **Z1**: unmittelbarer Lesezugriff durch Prüfer auf das System
- **Z2**: mittelbarer Zugriff (Auswertungen über Unternehmen / StB anfordern)
- **Z3**: Datenträgerüberlassung (z.B. GDPdU/Z3-Export)
- DATEV bietet alle drei Wege; Praxis-Standard ist Z3-Export bei Betriebsprüfung

### 3.6 Verfahrensdokumentation (Tz. 151 ff.)
**Pflicht** — beschreibt das gesamte DV-gestützte Buchführungs-Verfahren:
- Allgemeine Beschreibung (System, Prozesse, Beteiligte)
- Anwender-Dokumentation
- Technische Dokumentation
- Betriebsdokumentation
- Vor jeder Betriebsprüfung verlangt; Fehlen kann Buchführung ordnungswidrig machen → Schätzungsbefugnis FA § 162 AO

### 3.7 Ersetzendes Scannen
- Papierbeleg darf **nach** Scan vernichtet werden, wenn:
  - Scan-Prozess revisionssicher (Verfahrensdokumentation!)
  - Scan inhalts- und bildgleich
  - Aufbewahrung im elektronischen System gewährleistet

### 3.8 E-Rechnung (B2B Inland)
- **Pflicht zum Empfang**: ab 01.01.2025
- **Pflicht zur Ausstellung** im strukturierten Format (XRechnung, ZUGFeRD 2.0.1+):
  - ab 01.01.2027 für Unternehmen > 800 T€ Vorjahres-Umsatz
  - ab 01.01.2028 für alle
- Übergangsweise erlaubt: sonstige elektronische Rechnungen (PDF) bis 31.12.2026, danach kontingentiert (Wachstumschancengesetz)

## 4. Selbst-Check (kurz)

- [ ] Verfahrensdokumentation existiert, aktuell, einsehbar
- [ ] Beleg-Nummern lückenlos
- [ ] Buchungen werden zeitnah erfasst
- [ ] Festschreibung erfolgt regelmäßig (vor USt-VA-Versand)
- [ ] E-Rechnungs-Empfang-Fähigkeit vorhanden
- [ ] Scan-Prozess revisionssicher dokumentiert
- [ ] Backup + Archivierung mit Aufbewahrungsfristen-Beachtung
- [ ] Berechtigungskonzept (wer darf was im Buchhaltungs-System)
- [ ] Z3-Export-Fähigkeit für Betriebsprüfung getestet

## 5. Quellen

- BMF-Schreiben 28.11.2019 (GoBD) + 11.07.2022 (E-Rechnung-Ergänzung) — bundesfinanzministerium.de
- AO §§ 145, 146, 147, 148, 162 — gesetze-im-internet.de/ao_1977/
- HGB §§ 238, 239, 257 — gesetze-im-internet.de/hgb/
- UStG § 14 (E-Rechnungs-Anforderungen)
- Viertes Bürokratieentlastungsgesetz (10/8-Jahres-Aufbewahrungsänderung)

## 6. Verwandte Skills

- `buchung-grundlagen` — Grundlagen-Überblick (kürzer)
- `monatsabschluss` — Festschreibungs-Schritt
- `iks-pruefung` — IKS schließt GoBD-Komponenten ein
- `steuerberater-handoff` — bei Betriebsprüfung
