---
name: monatsabschluss
description: Monatsabschluss-Checkliste — Konten-Abstimmung, Abgrenzungen, USt-VA-Vorbereitung, Lohnverbuchung, Bank-Reconciliation, BWA.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# Monatsabschluss

**Typ:** `workflow`
**Anthropic-Pendant:** `monthly-close`
**Geltungsbereich:** GmbH, UG
**Config:** `config/{active_year}/`
**Knowledge-Base:** `buchung-grundlagen`, `gobd-konformitaet`

---

## 1. Zweck

Strukturierter Monats-Closing-Lauf für GmbH/UG: alle Konten abgestimmt, Abgrenzungen gebucht, USt-VA-fähige Saldenliste, Lohnverbuchung verprobt, BWA erstellt. Output ist eine Checkliste mit Status pro Position und konkrete Buchungs-/Abstimmungs-Vorschläge.

## 2. Eingaben

- Closing-Monat (z.B. "2026-04")
- Aktuelle Saldenliste / Buchungsjournal des Monats
- Bankauszüge (alle Konten)
- Lohnjournal aus Vor-System (DATEV LODAS, Lexware, etc.)
- OP-Listen Debitoren/Kreditoren
- Hinweis auf Sonderfälle (Inventur, Anlagen-Zugänge/-Abgänge, Rückstellungs-Anpassungen, Periodenabgrenzungen)

## 3. Workflow (Closing-Checkliste)

### 3.1 Vorbereitung (T-1)
- Belege vollständig im System (Belegnummer-Lücken-Check)
- Bank-Endsalden lt. Auszug ≙ Konto-Salden im Buchhaltungs-System
- Lohnabrechnung des Monats abgeschlossen und übernommen

### 3.2 Buchungs-Erfassung
- Alle Eingangs-/Ausgangsrechnungen mit Belegdatum im Monat erfasst
- Bank vollständig kontiert (keine offenen Zahlungseingänge auf Verrechnungskonten)
- Kasse (sofern vorhanden) täglich gebucht (§ 146 Abs. 1 AO)
- Reisekosten-Abrechnungen erfasst (Verpflegungspauschalen aus `rates.json`)

### 3.3 Abgrenzungen (§ 250 HGB)
- **ARAP** (aktive Rechnungsabgrenzung): vorausgezahlte Aufwendungen → SKR04 1900 / SKR03 0980
- **PRAP** (passive Rechnungsabgrenzung): vorausgezahlte Erträge → SKR04 3900 / SKR03 0990
- **Sonstige Forderungen / Verbindlichkeiten**: noch nicht abgerechnete Leistungen (Honorar, Boni, ausstehende Eingangsrechnungen)
- **Urlaubsrückstellung** anteilig (1/12) hochrechnen — Konto SKR04 3079 / SKR03 0961
- **Tantieme-Rückstellung** GF (sofern vereinbart) — Konto SKR04 3070 / SKR03 0956 für GewSt-Verbindlichkeit; Tantieme i.d.R. 3072/0961-Komplex je Vertrag

### 3.4 Konten-Abstimmung (Pflicht-Konten)
| Konto | SKR03 | SKR04 | Abstimmungs-Quelle |
|---|---|---|---|
| Bank | 1200 | 1800 | Bankauszug |
| Kasse | 1000 | 1600 | Kassenbericht |
| Debitoren-OP | 1400 | 1200 | OP-Liste |
| Kreditoren-OP | 1600 | 3300 | OP-Liste |
| USt 19% | 1776 | 3806 | KZ 81 × 19% |
| USt 7% | 1771 | 3801 | KZ 86 × 7% |
| Vorsteuer | 1576 | 1406 | Eingangsrechnungs-Liste |
| Lohn-Verb. SV | 1742 | 3740 | Lohnjournal |
| Lohn-Verb. LSt | 1741 | 3730 | Lohnjournal |
| § 13b USt | 1787 | 3837 | KZ 46/47, 73/74, 84/85 |

### 3.5 USt-VA vorbereiten
- Skill `ust-voranmeldung` aufrufen mit Closing-Monat
- Aufstellung archivieren, Frist-Hinweis prüfen (siehe `fristen.json`)

### 3.6 Plausibilitätsanalyse
- BWA generieren: Vergleich Monat ggü. Vormonat + Vorjahresmonat
- Auffällige Konto-Bewegungen kommentieren (Skill `abweichungsanalyse`)
- Marge / Personalkostenquote ggü. Plan

### 3.7 Festschreibung (GoBD)
- Buchungs-Periode in DATEV "festschreiben" (unveränderbar)
- Status dokumentieren in Closing-Protokoll

## 4. Output-Format

```
**Monatsabschluss 04/2026** — GmbH (SKR04)

CHECKLISTE
[x] 3.1 Belege vollständig (BN 5141–5418, keine Lücke)
[x] 3.1 Bank Volksbank: 47.892,11 € ≙ Saldo Konto 1800
[x] 3.2 Eingangs-/Ausgangsrechnungen erfasst
[!] 3.3 Urlaubsrückstellung: Anpassung +1.250 € erforderlich
        Buchung: 6072 / 3079 1.250 €
[x] 3.4 USt-Konten verprobt (Diff ≤ 0,01 €)
[!] 3.4 Debitoren-OP-Diff: 320 € (offener Skonto-Abzug Mandant X)
[x] 3.5 USt-VA 04/2026 vorbereitet → Zahllast 6.471,00 € (Frist DFV 10.06.)
[x] 3.6 BWA generiert — Personalkostenquote 38% (Plan 36%, +2pp)
[ ] 3.7 Festschreibung 04/2026 — ausstehend bis StB-Review

ABSTIMMUNGS-DIFFERENZEN
- Debitor X: 320 € → Klärung Skonto-Buchung
- Kreditor Y: 12,30 € → Rundung, vernachlässigbar

VORGESCHLAGENE NACHBUCHUNGEN
1. 6072 an 3079 Urlaubsrückstellung    1.250,00 €
2. 1900 an Bank ARAP Wartungsvertrag     800,00 €  (Mai-Anteil 200 €)
```

## 5. Validierung

- **Vollständigkeit**: keine Belegnummer-Lücke
- **Bank-Reconciliation**: Differenz = 0 oder dokumentierte offene Posten
- **OP-Listen**: Saldo ≙ Sammelkonto
- **USt-Konten**: Steuer rechnerisch aus Erlösen / Eingängen ableitbar
- **Lohn**: Lohnjournal-Salden ≙ Verbindlichkeits-Konten 3730/3740 (SKR04) bzw. 1741/1742 (SKR03)
- **Festschreibungs-Pflicht** GoBD: spätestens vor USt-VA-Übermittlung

## 6. Quellen

- HGB §§ 238, 250, 252, 266 — gesetze-im-internet.de/hgb/
- AO §§ 146, 147 — gesetze-im-internet.de/ao_1977/
- GoBD BMF-Schreiben 28.11.2019
- DATEV SKR03/04 Art.-Nr. 11174/11175 — siehe `config/2026/kontenrahmen.json`
- `config/{active_year}/fristen.json`

## 7. Verwandte Skills

- `buchungssatz` — produziert die laufenden Buchungen
- `ust-voranmeldung` — wird hier integriert aufgerufen
- `abstimmung` — Konten-Abstimmung im Detail
- `abweichungsanalyse` — Plan-Ist-Vergleich, BWA-Kommentierung
- `gobd-konformitaet` — Festschreibungs-Pflicht
- `jahresabschluss` — Monatsabschlüsse rollen ins Jahres-Closing
