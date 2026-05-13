---
name: ust-voranmeldung
description: USt-Voranmeldung vorbereiten — BMF Vordruckmuster USt 1 A 2026, KZ-Mapping, Dauerfristverlängerung, ELSTER-fähige Datenaufstellung.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# USt-Voranmeldung

**Typ:** `workflow`
**Geltungsbereich:** GmbH, UG
**Config:** `config/{active_year}/kz-codes-ust-va.json`, `rates.json`, `fristen.json`
**Knowledge-Base:** `buchung-grundlagen`

---

## 1. Zweck

Sammelt USt-relevante Buchungen eines Voranmeldungs-Zeitraums (Monat oder Quartal), mappt sie auf die KZ-Codes des BMF-Vordruckmusters **USt 1 A 2026**, berechnet die Zahllast/Erstattung und produziert eine **Aufstellung zur Übernahme in ELSTER**. Plugin übermittelt nicht direkt — Aufgabe von Anwender/StB.

## 2. Eingaben

**Pflicht:**
- Voranmeldungs-Zeitraum (z.B. "2026-04" oder "2026-Q2")
- Buchungs-Salden je relevantem Konto (entweder Saldenliste oder Buchungsjournal des Zeitraums)
- SKR-Variante (SKR03 / SKR04)
- Anmelde-Rhythmus: monatlich (default ab Zahllast 9.000 €/Vorjahr) oder vierteljährlich
- Dauerfristverlängerung: ja/nein (§ 46 UStDV)

**Optional, aber empfohlen:**
- Vorjahres-Zahllast (für Sondervorauszahlung 1/11)
- Saldo SV-Konten zur Plausibilität gegen Lohnabrechnung
- Hinweise auf §-13b-Sachverhalte, ig-Erwerbe, ig-Lieferungen, Drittland

## 3. Workflow

1. **Zeitraum-Abgrenzung**: Buchungen mit Leistungs- bzw. Vereinnahmungsdatum im VA-Zeitraum (SOLL- vs IST-Versteuerung § 20 UStG beachten)
2. **KZ-Mapping** je Buchungs-Sachverhalt aus `config/{active_year}/kz-codes-ust-va.json`:
   - Umsätze 19% → KZ **81** (Bemessungsgrundlage); Steuer wird vom System errechnet
   - Umsätze 7% → KZ **86**
   - ig-Erwerbe 19% → KZ **89** / 7% → KZ **93**
   - § 13b Abs. 1 (EU-Sonstige) → KZ **46** (BG) / **47** (Steuer), Zeile 30
   - § 13b Abs. 2 Nr. 3 (GrEStG) → KZ **73** / **74**, Zeile 31
   - § 13b Abs. 2 Nr. 1, 2, 4–12 (u.a. Bau, Reinigung, Schrott, Mobilfunk) → KZ **84** / **85**, Zeile 32
   - Eigene §-13b-Umsätze (als Leistender) → KZ **60**, Zeile 34
   - ig-Lieferungen § 6a → KZ **41**
   - Ausfuhren Drittland § 4 Nr. 1a → KZ **43**
   - Andere steuerfrei mit VSt → KZ **44**
   - Vorsteuer aus Rechnungen → KZ **66**
   - Vorsteuer aus ig-Erwerben → KZ **61**
   - Vorsteuer aus § 13b → KZ **67**, Zeile 41
   - Sondervorauszahlung anrechnen (Dezember-VA) → KZ **39**
3. **Aggregation**: Summen je KZ über alle relevanten Buchungen
4. **Zahllast/Erstattung** → KZ **83**
5. **Plausibilität**:
   - § 13b: Steuer aus BG-KZ rechnerisch = automatischer Steuer-KZ
   - VSt aus § 13b ≤ § 13b-Steuer (sofern voll vorsteuerabzugsberechtigt)
   - Frist-Check gegen `config/{active_year}/fristen.json`
6. **Ausgabe**: Markdown-Tabelle KZ → Betrag + DATEV-Export-Option

## 4. Output-Format

```
**USt-Voranmeldung 04/2026** (GmbH, SKR04, SOLL-Versteuerung)

Frist (mit DFV): 10.06.2026  [§ 46 UStDV]
Frist (ohne DFV): 10.05.2026 [§ 18 Abs. 1 UStG]

A. Umsätze
KZ 81 (BG 19%)            48.500,00 €  →  USt automatisch  9.215,00 €
KZ 86 (BG  7%)             2.800,00 €  →  USt automatisch    196,00 €

C. ig-Erwerbe
KZ 89 (BG 19%)             1.200,00 €  →  USt automatisch    228,00 €

D. § 13b — Leistungsempfänger
KZ 46 (BG, Z.30)           1.500,00 €
KZ 47 (Steuer, Z.30)         285,00 €

E. Steuerfreie Umsätze
KZ 41 (ig-Lief.)           5.000,00 €
KZ 43 (Ausfuhr Drittland)  3.200,00 €

F. Vorsteuer
KZ 66 (aus Rechnungen)                          -2.940,00 €
KZ 61 (aus ig-Erwerben)                           -228,00 €
KZ 67 (aus § 13b, Z.41)                           -285,00 €

H. Dauerfristverlängerung
KZ 39 (Sondervorauszahlung, nur Dez-VA)          0,00 €

────────────────────────────────────────────
KZ 83  Zahllast                              6.471,00 €
────────────────────────────────────────────

Quellen-Buchungen: siehe Anhang (Journal-Auszug)
```

## 5. Validierung

- **KZ-Existenz** in `kz-codes-ust-va.json` (BMF-Verbatim)
- **Steuersatz-Plausibilität**: BG × Satz ≈ rechnerische Steuer (Rundung ≤ 0,01 €)
- **§13b-Doppelung**: Empfänger-Steuer auf Eingangsseite muss gegenüber Vorsteuer ausgeglichen sein (sofern voll abzugsberechtigt)
- **Frist-Check** via `fristen.json`: Wochenende/Feiertag-Verschiebung § 108 Abs. 3 AO
- **DFV-Logik**: bei DFV verschiebt sich Abgabe + Zahlung um 1 Monat; Sondervorauszahlung 1/11 in Dezember-VA anzurechnen
- **Saldo-Sanity**: Erlöskonten-Saldo SKR04 (4xxx) entspricht USt-relevanten Erlösen
- **Out-of-Scope-Hinweis**: Reiseleistungen § 25, Differenzbesteuerung § 25a, OSS/IOSS — wenn erkannt, Steuerberater einbeziehen

## 6. Quellen

- UStG §§ 18, 18a, 18b, 13b, 15, 20 — gesetze-im-internet.de/ustg_1980/
- UStDV § 46 (Dauerfristverlängerung)
- BMF-Vordruckmuster USt 1 A 2026, BMF-Schreiben 29.12.2025 (GZ III C 3 - S 7344/00040/008/034)
- `config/2026/kz-codes-ust-va.json` (verbatim aus BMF-Quelle)
- `config/2026/fristen.json` (Frist-Kalender)
- AO § 108 Abs. 3 (Fristenende auf Werktag)

## 7. Verwandte Skills

- `buchungssatz` — liefert die einzelnen Buchungen, die hier aggregiert werden
- `monatsabschluss` — USt-VA ist Teil des Monats-Closing
- `datev-export` — Buchungsstapel + VA-Aufstellung in DATEV importieren
- `steuerberater-handoff` — falls StB die ELSTER-Übermittlung übernimmt
- `abstimmung` — Verprobung USt-Konten gegen Saldo
