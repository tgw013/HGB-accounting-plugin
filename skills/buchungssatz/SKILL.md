---
name: buchungssatz
description: Beleg in Buchungsvorschlag umwandeln (SKR03/SKR04, USt-Behandlung, Begründung mit §-Verweis). DATEV-konform.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# Buchungssatz

**Typ:** `workflow`
**Anthropic-Pendant:** `journal-entry-prep` (Workflow-Anteil)
**Geltungsbereich:** GmbH, UG
**Config:** `config/{active_year}/`
**Knowledge-Base:** `buchung-grundlagen`

---

## 1. Zweck

Aus einem konkreten Beleg (Rechnung, Bankbewegung, Vertrag) einen ordnungsgemäßen Buchungssatz nach SKR03 oder SKR04 vorschlagen — mit Soll/Haben-Konten, Beträgen, USt-Behandlung, kurzer Begründung und §-Verweis. Optional als DATEV-Buchungsstapel-CSV ausgeben (via `datev-export`).

## 2. Eingaben

**Pflicht:**
- Beleg-Inhalt (Text, Foto-OCR-Ergebnis, oder strukturierte Daten)
- Nettobetrag oder Bruttobetrag (eindeutig markiert)
- Belegdatum
- SKR-Variante (SKR03 oder SKR04) — falls unklar, nachfragen oder Mandanten-Default annehmen

**Optional:**
- Gegenkonto-Hinweis (z.B. "vom Geschäftskonto bezahlt" → 1200/1800)
- Kostenstelle / Kostenträger
- Mandanten-Spezifika (z.B. IST- vs SOLL-Versteuerung § 20 UStG)

**Aus Eingabe abzuleiten:**
- Vorgangsart (Wareneinkauf, Dienstleistung, Anlagengut, GwG, Bewirtung, Reisekosten, …)
- USt-Behandlung (19%, 7%, steuerfrei, § 13b UStG Reverse Charge, ig-Erwerb, Drittland-Import)
- Buchungslogik (Aufwand/Ertrag, Bestandskonto-Umbuchung, Abgrenzung)

## 3. Workflow

1. **Beleg klassifizieren**: Art der Leistung, beteiligte Parteien, Zeitraum
2. **USt-Tatbestand bestimmen**:
   - Inländischer Lieferant + Inlands-Leistung + Regelfall → 19% oder 7%
   - EU-Lieferant + B2B-Sonstige Leistung → § 13b Abs. 1 UStG Reverse Charge (KZ 46/47)
   - EU-Lieferant + Warenkauf → ig-Erwerb (KZ 89/93)
   - Drittland-Import → EUSt + ggf. § 13b Abs. 2 UStG
   - Bauleistung B2B / Gebäudereinigung B2B → § 13b Abs. 2 Nr. 4/8 UStG (KZ 84/85)
   - Kleinunternehmer-Rechnung → keine VSt, Hinweis prüfen (§ 19 UStG)
3. **Konto wählen** aus `config/{active_year}/kontenrahmen.json` (SKR03 oder SKR04 je Eingabe)
4. **Buchungssatz formulieren**: `Soll-Konto an Haben-Konto Betrag`, ggf. mit Aufteilung Netto + Vorsteuer / USt
5. **Begründung** in 1–2 Sätzen, mit §-Verweis (UStG, EStG, HGB)
6. **Plausibilitäts-Check**: Brutto = Netto + USt? Konto passt zur Vorgangsart? GwG-Grenze beachtet (§ 6 Abs. 2 EStG: 800 € netto Sofortabschreibung, oder Sammelposten 250–1.000 €)?

## 4. Output-Format

```
**Buchungsvorschlag** (SKR04)

Konto Soll   | Konto Haben | Netto   | USt    | Brutto
6815 Bürobed.| 3300 Verb.  | 84,03 € | 15,97 €| 100,00 €
1406 Vorst.  |             | 15,97 € |        |

Belegdatum:     2026-05-12
Leistungsdatum: 2026-05-12
USt-Tatbestand: § 12 Abs. 1 UStG (19%)
Begründung:     Büromaterial Inlandseinkauf, sofort abziehbarer Aufwand,
                Vorsteuer nach § 15 Abs. 1 S. 1 Nr. 1 UStG abzugsfähig.

Plausibilität: ✓ Brutto stimmt | ✓ Konto-Klasse passt | ✓ unter GwG-Grenze
```

Bei mehreren plausiblen Buchungsvarianten: Top-Vorschlag + 1–2 Alternativen mit Begründung der Wahl.

## 5. Validierung

- **Beträge:** Netto + USt = Brutto (Rundungsdifferenzen ≤ 0,01 € tolerieren)
- **Konto-Existenz:** Nummer existiert in `config/{active_year}/kontenrahmen.json` für gewählten SKR
- **Soll/Haben-Logik:** Aufwand im Soll, Verbindlichkeit im Haben, Vorsteuer im Soll
- **USt-Plausibilität:** Wenn KU-Rechnung erkannt → keine VSt; bei § 13b → keine VSt vom Lieferant + eigene §-13b-Buchung
- **GwG-Grenze:** Netto > 800 € + Anlagevermögen-Indikator → Hinweis auf Aktivierung statt Aufwand
- **Bewirtungsbelege:** 70/30-Regel (§ 4 Abs. 5 Nr. 2 EStG) — 30% nicht abziehbar als BA, aber VSt voll abziehbar
- **Reisekosten:** Verpflegungspauschalen je nach Jahr (BMF jährlich) — aus `config/{active_year}/rates.json`

## 6. Quellen

- UStG §§ 12, 13b, 14, 15, 19, 20 — gesetze-im-internet.de/ustg_1980/
- EStG §§ 4 Abs. 5, 6 Abs. 2 — gesetze-im-internet.de/estg/
- HGB §§ 238, 257, 266 — gesetze-im-internet.de/hgb/
- BMF Vordruckmuster USt 1 A 2026 (KZ-Codes) — siehe `config/2026/kz-codes-ust-va.json`
- DATEV SKR03 Art.-Nr. 11174 / SKR04 Art.-Nr. 11175, Stand 2026-01-01 — siehe `config/2026/kontenrahmen.json`
- `config/{active_year}/rates.json` (USt-Sätze, Pauschalen, GwG-Grenzen)

## 7. Verwandte Skills

- `buchung-grundlagen` — Doppik-Theorie, GoBD, SKR-Auswahl, Aufbewahrungsfristen
- `datev-export` — Buchungsvorschlag in DATEV-Buchungsstapel-CSV überführen
- `ust-voranmeldung` — sammelt §-13b-Buchungen für KZ-Aggregation
- `monatsabschluss` — konsumiert laufende Buchungssätze, fügt Abgrenzungen hinzu
- `abstimmung` — prüft Buchungs-Salden gegen externe Belege (Bank, OP-Listen)
