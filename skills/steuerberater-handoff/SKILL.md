---
name: steuerberater-handoff
description: Strukturierte Übergabe an Steuerberater/WP — Sachverhalt, eigener Vorschlag, §-Grundlagen, Belege, offene Fragen. Spart StB-Stunden.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (HGB/EStG/UStG/KStG/SGB Stand 2026-05, DATEV-SKR03/04 Art.-Nr. 11174/11175). **Ersetzt keine Steuerberatung.** Inhalt des Übergabe-Pakets ist Vorschlag — Steuerberater entscheidet final.

# Steuerberater-Handoff

**Typ:** `workflow`
**Anthropic-Pendant:** (kein direktes Pendant)
**Geltungsbereich:** GmbH, UG
**Config:** —
**Knowledge-Base:** alle anderen Skills (referenziert situationsabhängig)

---

## 1. Zweck

Erstellt ein **strukturiertes Übergabepaket** für den Steuerberater oder Wirtschaftsprüfer. Ziel: maximale Vorarbeit aus Mandanten-Sicht, damit StB nicht Sachverhalt aufnehmen, Konten suchen und §§ heraussuchen muss — sondern nur noch beurteilen. Spart StB-Stunden, beschleunigt Closings, erhöht Qualität der StB-Entscheidung.

## 2. Wann verwenden

- **Monats-Closing-Übergabe** an StB für Review
- **Jahresabschluss-Erstellungs-Übergabe** (großes Paket mit Saldenliste, Anlagengitter, Inventur)
- **Einzelner Sondersachverhalt** (z.B. komplexe §-13b-Konstellation, Pensionszusage, Umstrukturierung)
- **Betriebsprüfungs-Vorbereitung** (Verfahrensdokumentation, Belegsammlung)

## 3. Eingaben

- Anlass (Monats-Closing / JA / Einzelsachverhalt / BP)
- Zeitraum
- Eigene Buchungs-/Klassifikations-Vorschläge mit Begründung
- Offene Fragen / Unsicherheiten
- Belege (Anhang oder Pfad-Referenz)

## 4. Struktur des Handoff-Pakets

### 4.1 Deckblatt
- Mandant (Firma, Adresse, Steuer-Nr.)
- Anlass + Zeitraum
- Ansprechpartner Mandant
- Datum, Versions-Nr.

### 4.2 Executive Summary (max. 1 Seite)
- Was wurde gemacht
- Was ist offen
- Was wird vom StB erbeten (konkret)
- Frist-Hinweis

### 4.3 Sachverhalts-Darstellung
Pro Sachverhalt:
- **Sachverhalt** (1–3 Sätze, ohne Wertung)
- **Eigener Vorschlag** (Buchung, Klassifikation, Steuer-Behandlung)
- **§-Begründung** (HGB / EStG / UStG / KStG, mit Absatz und Nummer)
- **Alternativen, die geprüft wurden** (kurz, warum verworfen)
- **Offene Fragen** an StB

### 4.4 Anhänge
- Saldenliste (Stand X)
- Buchungsjournal-Auszug
- Buchungs-Stapel-CSV (für DATEV-Übernahme)
- USt-VA-Aufstellung (falls Closing)
- Anlagengitter (falls JA)
- Belege als PDF (oder DMS-Verweise)
- BWA, Forecast (optional)
- IKS-/GoBD-Selbst-Check-Status

## 5. Workflow

1. Anlass + Zeitraum aufnehmen
2. Aus jeweiligem Vorgang (z.B. Monatsabschluss-Output) Sachverhalte extrahieren
3. Klärungsbedürftige Punkte priorisieren (Top 3–5)
4. Eigenen Vorschlag mit §-Verweis dokumentieren
5. Frist berechnen + setzen (z.B. "Rückmeldung bis 5 Werktage vor Frist USt-VA")
6. Paket zusammenstellen (Markdown + Anhänge in PDF/CSV)
7. Sicheren Übertragungsweg wählen (verschlüsselter Mail-Anhang, DMS, DATEV-Mandant-Online)

## 6. Output-Format

```
**STB-HANDOFF · GmbH XYZ · Monatsabschluss 04/2026**
Stand: 2026-05-10 · Version 1.0 · Ansprechp.: T. Weidemüller · Frist Rückmeldung: 2026-05-15

EXECUTIVE SUMMARY
- Closing 04/2026 abgeschlossen, USt-VA-Entwurf anbei
- 2 Punkte offen für StB-Klärung (siehe §4 + §5)
- Erbeten: Freigabe Buchungsstapel + Übernahme ELSTER-Übermittlung

§1  USt-VA 04/2026 (Zahllast 6.471 €, Frist mit DFV 10.06.)
    Vorschlag: anbei als DATEV-CSV + KZ-Aufstellung
    StB-Aufgabe: ELSTER-Übermittlung

§2  Urlaubsrückstellungs-Anpassung +1.250 €
    Buchung: 6072 / 3079
    §-Grundlage: § 249 HGB i.V.m. § 253 Abs. 1 (vernünftige kaufm. Beurteilung)
    Offen: Bemessungs-Methode (Lohn x Urlaubstage-Saldo)

§3  EWB Forderung Mandant Z (4.500 €)
    Sachverhalt: Insolvenzantrag 30.04.2026
    Vorschlag: 100% Wertberichtigung (6923/1247)
    §: § 253 Abs. 4 HGB (strenges Niederstwertprinzip)
    Offen: Anzeige bei Insolvenzverwalter erfolgt? Steuerlich: § 6 Abs. 1 Nr. 1 EStG?

§4  OFFEN: § 13b auf neue Bauleistung Lieferant DE
    Sachverhalt: Lieferant ist Subunternehmer, eigentlich kein Bauleister-Status,
                 aber Leistung ist Bauleistung
    Frage: greift § 13b Abs. 2 Nr. 4 UStG? Welche Nachweise gegenüber FA?

ANHÄNGE
- A1: Saldenliste_04-2026.xlsx
- A2: Buchungsstapel_EXTF_04-2026.csv
- A3: USt-VA_04-2026.pdf
- A4: Belege.zip
```

## 7. Validierung

- Executive Summary lesbar in < 1 Minute
- Alle Sachverhalte mit Vorschlag + §-Verweis
- Offene Fragen klar markiert
- Frist gesetzt + realistisch
- Anhänge alle vorhanden, Pfade korrekt
- Datenschutz: personenbezogene Daten (z.B. Lohn-Details) verschlüsselt

## 8. Quellen

- StBerG (Steuerberatungsgesetz) — Grenze Mandanten-Mitwirkung vs. StB-Tätigkeit
- HGB §§ 238 ff., 264 ff., 316
- §§ 18, 149, 150 AO (Steuererklärungs-Fristen)
- DSGVO Art. 5, 32 (Datenschutz bei Übermittlung)

## 9. Verwandte Skills

- alle Workflow-Skills — liefern die Sachverhalte
- `datev-export` — produziert CSV als Anhang
- `gobd-konformitaet` — bei BP-Vorbereitung
- `iks-pruefung` — bei JA-Prüfung
