---
name: wiederkehrende-buchungen
description: Wiederkehrende Buchungen für DATEV — monatliche/quartalsweise wiederkehrende Buchungen (Beitragsüberträge, Bestandsprovisionen, Miete, etc.) als Serien-Definition statt Copy-Paste. DATEV-Format Kategorie 65, Version 4.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-Format-Portal developer.datev.de — Wiederkehrende Buchungen Formatkategorie 65 Version 4, 101 Felder; Stand 2026-05). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktivem Import in DATEV-Mandant per Vorabbuchungsstapel prüfen.

# Wiederkehrende Buchungen

**Typ:** `workflow`
**Geltungsbereich:** GmbH, UG
**Config:** `config/shared/datev-extf-fields.json` (Section `wiederkehrende_buchungen.4`)
**Knowledge-Base:** `buchung-grundlagen`
**Related:** `datev-export` (Buchungsstapel — Kategorie 21), `monatsabschluss`

---

## 1. Zweck

Erstellt eine **Serien-Definition** für wiederkehrende Buchungen, die in DATEV monatlich/quartalsweise/jährlich automatisch verbucht werden. Beispiele:

- Bestandsprovisionen-Übertrag (monatlich)
- Beitragsüberträge bei Versicherungsmaklern (monatlich)
- Miet-Buchungen Anlagen (monatlich)
- Wartungsvertrags-Buchungen (quartalsweise)
- Abschreibungs-Serien-Buchungen (monatlich)

Statt jeden Monat im Monatsabschluss-Workflow eine identische Buchung manuell zu erfassen, schreibt der Anwender einmal die Serien-Definition (Beginn, Intervall, Konten, Betrag), importiert sie in DATEV-Rechnungswesen, und DATEV bucht ab Beginndatum automatisch monatlich/quartalsweise.

## 2. Unterschied zu Buchungsstapel (`datev-export` / Formatkategorie 21)

| Aspekt | Buchungsstapel (21) | Wiederkehrende (65) |
|---|---|---|
| Zweck | Einmalige Buchung | Serien-Definition |
| Saldo-Pflicht | Ja (Σ Soll = Σ Haben) | Nein (jede WK-Buchung ist eigenständig) |
| Felder pro Buchung | 125 | 101 |
| Belegdatum | TTMM (Jahr aus Header) | — (stattdessen Beginndatum TTMMJJJJ) |
| Belegfeld 1 erlaubte Zeichen | word + `$ & % * + - /` | word + `$ % - /` (DROPS `& * +`) |
| Belegfeld 2 max Länge | 36 | 12 |
| Recurrence-Felder | — | B1, Beginndatum, Zeitintervallart, Zeitabstand, Wochentag, Ordnungszahl Tag im Monat, Ordnungszahl Wochentag, Endetyp, Zuletzt per, Nächste Fälligkeit, Enddatum |
| Output-Datei | `EXTF_buchungsstapel_*.csv` | `EXTF_wiederkehrende_*.csv` |

## 3. Recurrence-Felder im Überblick

### `b1` — Schlüssel für Belegfeld-1-Verarbeitung
- `1` = Rechnungsnummer 36-stellig, unverändert
- `2` = 34-stellig + 2-stellige Verarbeitungs-Ergänzung von rechts
- `3` = wird beim Import automatisch hochgezählt (Start-Rechnungsnummer)

### `beginndatum` — TTMMJJJJ (quoted)
Wann die Serie startet.

### `zeitintervallart` + `zeitabstand`
- `TAG` + 1–999 = täglich-Intervall
- `MON` + 1–99 = monatlich-Intervall

### `wochentag` (bitmask, nur bei `MON`)
1=Mo, 2=Di, 4=Mi, 8=Do, 16=Fr, 32=Sa, 64=So. Summe = mehrere Tage.

### `ordnungszahl_tag_im_monat` (1–31) + `ordnungszahl_wochentag` (1=erster ... 5=letzter)
"Jeden ersten Montag", "jeden letzten Werktag", etc.

### `endetyp`
- `1` = kein Enddatum (Serie läuft unbefristet)
- `2` = Endzeitpunkt bei Anzahl Ereignissen
- `3` = Endet am (`enddatum` füllen)

## 4. Workflow

1. Sachverhalt erfassen (was wiederholt sich, wie oft, wie lange)
2. Pro Serie: Buchungs-Felder + Recurrence-Felder befüllen
3. Serialisieren via `scripts/generate_extf.py --format-version 4`:
   ```bash
   python scripts/generate_extf.py \
     --input /tmp/wk_beitraege.json \
     --output /tmp/EXTF_wiederkehrende_2026_06.csv \
     --format-version 4 \
     --encoding cp1252
   ```
4. CSV als **Vorabbuchungsstapel** in DATEV importieren — DATEV-Rechnungswesen erkennt es automatisch als Wiederkehrende-Buchungs-Datei (Formatkategorie 65 + Formatname im Header)
5. In DATEV-Rechnungswesen die Serie aktivieren (1× pro Serie)

## 5. Output-Format

Wie Buchungsstapel: CSV mit 31 Header-Feldern + 101 Spalten-Header + N Buchungs-Zeilen. Encoding CP1252, CRLF-Zeilenenden, Header-Felder #3/#4/#5 = `65 / "Wiederkehrende Buchungen" / 4`.

Plus Begleit-`.report.md` mit SHA-256 + Anzahl WK-Definitionen + Recurrence-Übersicht.

## 6. Validierung

- Alle 101 Felder via Inventory aus `config/shared/datev-extf-fields.json`
- 3 Portal-Inkonsistenz-Interpretationsregeln aktiv (Felder #4 Soll/Haben, #81 Zeitintervallart, #97 Generalumkehr — alle Character-Class-zu-Alternation-Korrekturen)
- Belegfeld-1 WK-Regex (`& * +` verboten) deutlich strikter als Buchungsstapel — Validator weist mit klarer Meldung darauf hin
- **Kein Saldo-Check** (WK ist Serien-Spec, nicht balanced Stapel)

## 7. Beispiel-Eingabe

Siehe `tests/fixtures/wiederkehrend_premium_accrual/input.json` — Monats-Beitragsübertrag und Quartalsbeitrag.

## 8. Quellen

- developer.datev.de `/format-description/recurring-bookings` — 101 Felder verbatim
- developer.datev.de `/appendix/format-categorynameversion` — Formatkategorie 65, Formatversion 4
- DATEV-Format-Prüfprogramm `Format_Wiederkehrende Buchungen.xml` — Cross-reference
- PRD §14.4 — Typische Anwendungsfälle: Beitragsüberträge, Bestandsprovisionen

## 9. Verwandte Skills

- `datev-export` — einmalige Buchungen (Buchungsstapel)
- `monatsabschluss` — WK-Definitionen ergänzen den Monats-Closing-Prozess
- `buchung-grundlagen` — Doppik / GoBD-Grundlagen
- `steuerberater-handoff` — bei Erstellung neuer WK-Serien empfohlen, Stb. informieren
