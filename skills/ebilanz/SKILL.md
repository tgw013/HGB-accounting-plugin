---
name: ebilanz
description: eBilanz-Datenpaket vorbereiten — Taxonomie-Mapping HGB 6.9, Mussfeld-Prüfung, Datenexport für ERiC/DATEV. Übermittlung selbst out-of-scope.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# eBilanz

**Typ:** `workflow`
**Anthropic-Pendant:** (kein direktes Pendant)
**Geltungsbereich:** GmbH, UG
**Config:** `config/{active_year}/kontenrahmen.json`, `fristen.json`
**Knowledge-Base:** `buchung-grundlagen`, `jahresabschluss`

---

## 1. Zweck

Bereitet **Datenpaket** für eBilanz-Übermittlung an Finanzverwaltung (§ 5b EStG) vor: Mapping Saldenliste → Taxonomie-Positionen, Prüfung Mussfelder, Auffüllung freier Positionen. **Plugin übermittelt nicht** — Versand via ERiC erfolgt durch StB/DATEV.

## 2. Eingaben

- Saldenliste Geschäftsjahr (post-Closing, inkl. Steuerumbuchungen)
- HGB-Taxonomie-Version (aktuell 6.9, wird jährlich aktualisiert)
- Branchen-Taxonomie (Kerntaxonomie / Spezial: Banken, Versicherungen, etc.)
- Größenklasse (entscheidet Mussfeld-Tiefe)
- Steuerbilanz vs. Handelsbilanz-Differenz (Überleitungsrechnung § 5b EStG)

## 3. Workflow

### 3.1 Taxonomie-Auswahl
- Aktuelle HGB-Taxonomie (Version + Stand) prüfen — BMF veröffentlicht jährlich
- Kerntaxonomie für allgemeine GmbH/UG; Spezial-Taxonomien für regulierte Branchen

### 3.2 Konto-Mapping
- DATEV-SKR-Konto → Taxonomie-Position
- DATEV liefert Standard-Mapping; manuelle Korrekturen bei abweichend genutzten Konten
- Sammlung in einer Mapping-Tabelle (Saldenliste → XBRL-Element)

### 3.3 Mussfeld-Prüfung
- Pflichtfelder je Größenklasse vollständig befüllt
- Bei nicht vorhandenen Sachverhalten: "leer" zulässig, aber dokumentiert

### 3.4 Überleitungsrechnung Handels- → Steuerbilanz (§ 5b EStG Abs. 1 S. 2)
- HB-Positionen
- StB-Korrekturen (z.B. Pensionsrückstellungen § 6a EStG, Drohverlustrückstellungen — bilanziell HGB ja / steuerlich nein, AfA-Differenzen)
- StB-Werte

### 3.5 Plausibilitäts-Checks
- Bilanz aktiv = passiv in StB-Werten
- GuV-Saldo entspricht Bilanz-EK-Veränderung
- Steuern vom Einkommen und Ertrag (KSt, GewSt, Solz) konsistent
- Anlagenspiegel-Werte (AHK, Zugänge, Abgänge, AfA, Restbuchwerte) Plausi

### 3.6 Übergabe an ERiC/DATEV
- Export im XBRL- oder CSV-Format (je nach Programm)
- Übermittlung **nicht** durch dieses Plugin
- Frist: parallel zur Steuererklärung; ohne StB **31.07. des Folgejahres** (§ 149 Abs. 2 AO); mit StB **28.02. des Zweitfolgejahres** (§ 149 Abs. 3 AO)

## 4. Output-Format

- Mapping-Tabelle Konto → XBRL-Position
- Mussfeld-Status-Liste (vollständig / leer-zulässig / fehlt)
- Überleitungsrechnung HB → StB als Markdown-Tabelle
- Hinweis-Liste auf StB-Klärungs-Punkte
- Optional: CSV für DATEV-Import

## 5. Validierung

- Bilanz-Identität in beiden Wertebenen (HB + StB)
- Mussfelder vollständig oder begründet leer
- KSt-/GewSt-/Solz-Rückstellungen konsistent zur Steuerberechnung
- Vorjahres-Vergleichswerte vorhanden (Pflicht in Taxonomie)
- Anlagengitter-Werte konsistent zum Anlagenspiegel des Jahresabschlusses

## 6. Quellen

- EStG § 5b — gesetze-im-internet.de/estg/
- AO §§ 149, 150 — gesetze-im-internet.de/ao_1977/
- HGB-Taxonomie 6.9 (jährliches BMF-Schreiben — esteuer.de / xbrl-deutschland.de)
- BMF-Schreiben zur eBilanz (jeweils aktuell)
- DATEV-Programmhilfe "eBilanz online"
- `config/2026/fristen.json`

## 7. Verwandte Skills

- `jahresabschluss` — Vorarbeit, liefert HB-Werte
- `steuerberater-handoff` — Übergabe inkl. eBilanz-Paket
- `datev-export` — falls direkt in DATEV importiert wird
