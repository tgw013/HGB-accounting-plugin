---
name: buchungssatz
description: Erstellt aus einem Beleg ODER einem Abschluss-/Abgrenzungsvorgang (RAP § 250, Rückstellungen § 249, Auflösungen) einen prüffähigen HGB-Buchungssatz (SKR03/SKR04, Soll/Haben, USt-Behandlung, §-Begründung) und gleichzeitig einen strukturierten JSON-Handoff für `datev-export`. Anwenden bei Eingangs-/Ausgangsrechnungen, § 13b Reverse Charge, ig-Erwerb, Bewirtung/Reisekosten/GwG sowie bei Urlaubs-/Steuer-/Pensions-/Garantierückstellungen, ARAP/PRAP und deren Auflösung. Deutsches Pendant zu `journal-entry`.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/KSVG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# Buchungssatz

**Typ:** `workflow` · **Anthropic-Pendant:** `journal-entry` (erzeugt) zu `journal-entry-prep` (beschreibt) · **Geltungsbereich:** GmbH, UG · **Config:** `config/{active_year}/` · **Knowledge-Base:** `buchung-grundlagen`

```
/buchungssatz <Sachverhalt oder Beleg> [| beleg|rückstellung|arap|prap|auflösung] [SKR03|SKR04]
```

---

## 1. Zweck

Wandelt **(a)** einen konkreten Beleg (Rechnung, Bankbewegung, Vertrag) **oder (b)** einen Abschluss-/Abgrenzungsvorgang aus dem Skill `buchung-grundlagen` (RAP § 250, Rückstellungen § 249, Auflösungen) in einen ordnungsgemäßen Buchungssatz nach SKR03/SKR04 um — mit Soll/Haben-Konten, Beträgen, USt-Behandlung, kurzer Begründung und §-Verweis.

Zwei Ausgaben gleichzeitig, damit der Skill **eigenständig** und als **Zulieferer** nutzbar ist:
- **(a) Menschenlesbarer Buchungsvorschlag** — als Referenz-Buchungssatz direkt verwendbar (Abschnitt 8).
- **(b) Strukturierter JSON-Handoff** — den der Skill `datev-export` ohne Transformation in eine upload-fertige DATEV-EXTF-Buchungsstapel-CSV überführt (Abschnitt 9). Wer keine CSV braucht, ignoriert (b).

`buchung-grundlagen` beschreibt die **Vorgänge** (Soll/Haben-Muster, Bewertung, HGB-vs-StB); dieser Skill erzeugt den **konkreten Satz mit Beträgen** — analog `journal-entry` ↔ `journal-entry-prep`.

## 2. Zwei Modi — Einzelbeleg vs. Abschlussbuchung

Kein starrer Pflicht-Typ-Parameter. Der Skill erkennt den Modus selbst aus dem free-form Sachverhalt; ein optionales Schlüsselwort übersteuert.

**Routing (in dieser Reihenfolge):**
1. **Explizites Schlüsselwort** im Aufruf (`beleg`, `rückstellung`/`rst`, `arap`, `prap`, `abgrenzung`, `auflösung`) → Modus direkt gesetzt.
2. **Trigger-Begriffe → Abschlussbuchung:** Rückstellung, Urlaubs-/Steuer-/Pensions-/Garantie-/Drohverlustrückstellung, Tantieme, Bonus, Künstlersozialabgabe/KSK, ausstehende Eingangsrechnung, Abgrenzung, ARAP, PRAP, periodengerecht/Stichtag, auflösen/Inanspruchnahme/Überdotierung.
3. **Beleg-Indikatoren → Einzelbeleg:** Rechnung, Lieferant, RE-Nr., netto/brutto/USt, „vom Geschäftskonto bezahlt", Bewirtung, Reisekosten, GwG, Wareneinkauf, SaaS, § 13b, ig-Erwerb, Kleinunternehmer.
4. **Mehrdeutig** (z. B. „Stromnachzahlung geschätzt, Rechnung fehlt") → **eine** Rückfrage: *„Liegt eine Rechnung vor? → Verbindlichkeit/Beleg; geschätzt/keine Rechnung → Rückstellung"* (Faustregel `buchung-grundlagen` § 7).
5. **SKR-Variante:** explizit im Aufruf > Mandanten-Default > **Skill-Default SKR04** (näher an HGB-Bilanzgliederung; Config-`default` SKR03 bleibt unberührt). SKR03-Eingabe → Konten über `kontenrahmen.json` spiegeln.

Ein Sachverhalt kann **mehrere** Buchungszeilen erzeugen (Splitt). Der Skill gibt dafür einen **einzigen** `buchungen`-Array aus.

## 3. Eingaben

**Pflicht (Einzelbeleg):** Beleg-Inhalt; Netto- oder Bruttobetrag (eindeutig markiert); Belegdatum; SKR-Variante (sonst SKR04-Default).
**Pflicht (Abschlussbuchung):** Vorgangsart bzw. erkennbarer Trigger; Bewertungsgrundlage/Betrag (oder Berechnung); Stichtag/Periode.
**Optional:** Gegenkonto-Hinweis (z. B. „vom Geschäftskonto bezahlt" → 1800); Kostenstelle/-träger (`kost1`/`kost2`); Belegnummer (`belegfeld_1`); Mandanten-Spezifika (IST- vs. SOLL-Versteuerung § 20 UStG); bei § 13b/ig die USt-IdNr. des Lieferanten.
**Abzuleiten:** USt-Tatbestand (19/7 %, steuerfrei, § 13b, ig-Erwerb, KU); Buchungslogik (Aufwand/Ertrag, Bestandskonto, Abgrenzung, Rückstellung); ggf. Abzinsung/Stichtagsprinzip (→ `buchung-grundlagen`).

## 4. Workflow Einzelbeleg

1. **Beleg klassifizieren:** Art der Leistung, Parteien, Zeitraum.
2. **USt-Tatbestand bestimmen:**
   - Inländischer Lieferant + Inlandsleistung → 19 % / 7 %.
   - EU-Lieferant + B2B-Sonstige Leistung → § 13b Abs. 1 UStG Reverse Charge (KZ 46/47).
   - EU-Lieferant + Warenkauf → ig-Erwerb (KZ 89/93).
   - Drittland-Import → EUSt + ggf. § 13b Abs. 2 UStG.
   - Bauleistung/Gebäudereinigung B2B → § 13b Abs. 2 Nr. 4/8 UStG (KZ 84/85).
   - Kleinunternehmer-Rechnung → keine VSt (§ 19 UStG).
3. **Konto wählen** aus `config/{active_year}/kontenrahmen.json` (SKR je Eingabe); bei Konten außerhalb des kuratierten Auszugs gegen den vollständigen DATEV-SKR (Art.-Nr. 11174/11175) prüfen.
4. **Buchungssatz formulieren:** `Soll an Haben`, ggf. Aufteilung Netto + Vorsteuer.
5. **Begründung** (1–2 Sätze, §-Verweis UStG/EStG/HGB).
6. **Plausibilität:** Brutto = Netto + USt? Konto passt? GwG-Grenze (§ 6 Abs. 2 EStG: 800 € netto Sofortabschreibung, Sammelposten 250–1.000 €)?

## 5. Workflow Abschlussbuchung

1. **Vorgang erkennen** (Routing § 2) und in `buchung-grundlagen` nachschlagen.
2. **Konto/Gegenkonto** aus dem Vorgang-Katalog (§ 6).
3. **Bewertung/Splitt:** Betrag aus Eingabe/Berechnung; mehrere Aufwands-Soll-Konten gegen ein Rückstellungs-Haben-Konto → Splittbuchung (mehrere Zeilen).
4. **HGB-vs-StB-Kurzhinweis** in den lesbaren Output aufnehmen (Detail an `buchung-grundlagen` delegieren) — z. B. Urlaub: Stichtagsprinzip § 6 Abs. 1 Nr. 3a Buchst. f EStG; Drohverlust: Steuerverbot § 5 Abs. 4a EStG; GewSt-RST: Hinzurechnung § 4 Abs. 5b EStG.
5. **Auflösungslogik** (falls Auflösung): Inanspruchnahme / Überdotierung (Ertrag) / Unterdotierung (Aufwand) — § 6 des Katalogs.
6. **GoBD-Hinweis:** Eigenbeleg + Berechnungsschema; bei kurzfristigen Rückstellungen Auto-Reversal-Hinweis.

## 6. Vorgang-Katalog (Abschlussbuchungen, SKR04)

Soll = Aufwand/Aktiv (bei Bildung), Haben = Rückstellung/Abgrenzung. Konten gegen Mandanten-Kontenrahmen prüfen; Quelle der Muster: Skill `buchung-grundlagen`.

| Vorgang | Soll | Haben | §-Verweis |
|---|---|---|---|
| ARAP Bildung | 1900 ARAP | Aufwandskonto (6400 …) | § 250 Abs. 1 HGB |
| ARAP Auflösung | Aufwandskonto | 1900 ARAP | § 250 Abs. 1 HGB |
| PRAP Bildung | 1800 Bank / 4400 Erlöse | 3900 PRAP | § 250 Abs. 2 HGB |
| PRAP Auflösung | 3900 PRAP | 4400 Erlöse 19 % | § 250 Abs. 2 HGB |
| Steuer-RST KSt (+ SolZ) | 7600 KSt | 3040 KSt-RST | § 249 HGB; § 4 Abs. 5b EStG |
| Steuer-RST GewSt | 7610 GewSt | 3035 GewSt-RST | § 249 HGB; § 4 Abs. 5b EStG (StB-Hinzurechnung!) |
| Urlaubsrückstellung | 6072 Aufw. Urlaubs-RST (alt. 6020 + 6100) | 3079 Urlaubsrückstellungen | § 249 Abs. 1 HGB; R 6.11 EStR |
| JA-/Prüfungskosten | 6825 Abschluss-/Prüfung + 6827 StB | 3070 Sonstige RST | § 249 HGB; H 5.7(3) EStH |
| Ausstehende Eingangsrechnungen | Aufwand (6605 Strom …) | 3070 Sonstige RST | § 249 Abs. 1 HGB |
| Tantieme Gesellschafter-GF | 6027 Vergütung Ges.-GF (+ 6100) | 3074 Personalkosten-RST | § 249 HGB; **§ 8 Abs. 3 KStG vGA** |
| Bonus Mitarbeiter | 6020 Gehälter (+ 6100) | 3070 Sonstige RST | § 249 HGB |
| Garantie/Gewährleistung | 6510 Garantiekosten | 3070 Sonstige RST | § 249 Abs. 1 S. 2 Nr. 2 HGB; BFH I R 71/00 |
| Pensionsrückstellung | 6140 Altersversorgung (Ges.-GF 6149) | 3010 RST für Direktzusagen | § 249 HGB; § 6a EStG (StB 6 %) |
| Unterlassene Instandhaltung | 6470 Instandhaltung Räume | 3070 Sonstige RST | § 249 Abs. 1 S. 2 Nr. 1 HGB; R 5.7 Abs. 11 EStR |
| Drohverlust | 6960 periodenfremder Aufw. | 3092 Drohverlust-RST (Konto prüfen) | § 249 Abs. 1 HGB; **§ 5 Abs. 4a EStG StB-Verbot** |
| Künstlersozialabgabe (KSK) | 6135 KSK (alt. 6855) | 3070 Sonstige RST (laufend: 3740 Verb. KSK) | § 24 KSVG; § 249 HGB |
| Auflösung – Inanspruchnahme | 3070/3xxx RST | 1800 Bank (o. 3300 Verb.) | § 249 HGB |
| Auflösung – Überdotierung (Ertrag) | 3070/3xxx RST | Ertrag a. d. Auflösung von RST (4830/4930 prüfen) | § 252 Abs. 1 Nr. 6 HGB |
| Auflösung – Unterdotierung (Aufwand) | 3070/3xxx RST + 6960 period. Aufw. | 1800 Bank | § 249 HGB |

## 7. USt-Tatbestände & EXTF-Abbildung

Der lesbare Vorschlag zeigt Netto + Vorsteuer/USt didaktisch getrennt. Im JSON-Handoff (= DATEV-EXTF) gilt: **jede Zeile trägt `konto` UND `gegenkonto` und ist damit in sich ausgeglichen** — eine vollständige Buchung. **Keine Spiegel-/Gegenzeilen erzeugen** (das würde beim Mandanten-Import doppelt buchen). Mehrere Zeilen nur bei echten Splittbuchungen (mehrere Soll-Konten gegen dasselbe Haben-Konto bzw. paarweise zugeordnet). Über den Stapel muss gelten: jede Zeile Konto ≠ Gegenkonto, `umsatz` > 0.

Deterministische Regeln:
- **R1 – Abschlussbuchung / steuerfrei / KU (keine USt):** je Soll/Haben-Paar **eine** Zeile, `bu_schluessel` = `"0"`/leer, `umsatz` = Nettobetrag. Splitt → eine Zeile je Aufwands-Soll-Konto gegen das gemeinsame Rückstellungs-/Kreditor-Konto.
- **R2 – Einzelbeleg mit Vorsteuer 19 %/7 % (Inland):** **zwei** Zeilen, beide `S`, beide gegen den Kreditor/die Bank — (i) Nettobetrag auf das Aufwandskonto, (ii) Vorsteuerbetrag auf 1406 (19 %) bzw. 1401 (7 %). `umsatz` je Zeile = der jeweilige Teilbetrag. *Alternative bei Automatik-Konten:* **eine** Zeile mit `umsatz` = Brutto und leerem `bu_schluessel` (das Konto trägt die USt-Automatik) — **kein** BU-Schlüssel auf Automatikkonten (sonst DATEV-Importfehler REW00305).
- **R3 – § 13b Reverse Charge / ig-Erwerb:** **zwei** Zeilen — (i) Nettoaufwand `S` Aufwandskonto → Kreditor (z. B. 6840 → 3300); (ii) Vorsteuer § 13b `S` 1407 → USt § 13b 3837, mit `eu_land_ustid_bestimmung` = USt-IdNr. des Lieferanten und `sachverhalt_l_l` = `"1"`. `bu_schluessel` leer; § 13b läuft über die expliziten Kontenpaare, **nicht** über einen Automatik-Schlüssel (prüfprogramm-verifiziert). KZ-Aggregation (46/47/67 bzw. 89/93/61) macht `ust-voranmeldung`.
- **R4 – Zahlung:** eigene Zeile (z. B. 3300 → 1800 Bank).

## 8. Output (a) — menschenlesbarer Buchungsvorschlag

```
**Buchungsvorschlag** (SKR04) — <Modus/Vorgang>

Konto Soll        | Konto Haben         | Netto/Betrag | USt    | Brutto
<konto> <bez.>    | <gegenkonto> <bez.> | …            | …      | …

Belegdatum:     TT.MM.JJJJ      Leistungsdatum: TT.MM.JJJJ
USt-Tatbestand: <§-Verweis / „keiner (Abgrenzung)">
Begründung:     <1–2 Sätze mit §-Verweis (UStG/EStG/HGB)>
HGB vs. StB:    <nur bei Rückstellungen — Kurzhinweis, Detail → buchung-grundlagen>
Plausibilität:  ✓ <Brutto/Saldo> | ✓ Konto-Klasse | ✓ <GwG/USt/Abzinsung>
```

Bei mehreren plausiblen Varianten: Top-Vorschlag + 1–2 Alternativen mit Begründung der Wahl.

## 9. Output (b) — strukturierter JSON-Handoff für `datev-export`

Direkt unter dem lesbaren Block in einem ` ```json `-Fence ausgeben. Format **exakt** wie vom Serializer `scripts/generate_extf.py` erwartet — `buchungssatz` liefert `skr` + `buchungen`; den `header` (Berater-/Mandanten-Nr., WJ, Zeitraum) ergänzt `datev-export`:

```json
{
  "skr": "SKR04",
  "buchungen": [ <Buchungszeile>, ... ]
}
```

**`<Buchungszeile>`** — Feld-Keys exakt:

| Feld | Pflicht | Regel |
|---|---|---|
| `umsatz` | ja | positiv, Komma-Dezimal, genau 2 Nachkommastellen (`"3000,00"`); nie `"0,00"` |
| `soll_haben_kennzeichen` | ja | `"S"` oder `"H"` — bezieht sich auf `konto` |
| `wkz_umsatz` | — | `"EUR"` (Default) |
| `konto` | ja | Sachkonto; ≠ `gegenkonto` |
| `gegenkonto` | ja* | Sachkonto (*leer nur bei echter Splittsatz-Teilzeile) |
| `bu_schluessel` | — | `"0"`/leer (Default, auch § 13b); USt-Automatik via Automatikkonto, **nicht** zusätzlich BU setzen |
| `belegdatum` | ja | `TTMM` (4-stellig, Tag+Monat im Wirtschaftsjahr) |
| `belegfeld_1` | — | Belegnummer; Zeichensatz `\w$&%*+-/`, ≤ 36, **keine** Leerzeichen/Umlaute/Punkt/Komma |
| `buchungstext` | — | ≤ 60 Zeichen, CP1252-sicher (keine Emojis/seltene Unicode-Zeichen) |
| `kost1`, `kost2` | — | Kostenstelle/-träger |
| `kost_allocations` | — | `[{ "kost1": "...", "anteil_prozent": "60,00" }, …]`, Σ = `"100,00"` — splittet eine Zeile kostenstellenseitig |
| `eu_land_ustid_bestimmung` | — | nur § 13b/ig — USt-IdNr. des Lieferanten (z. B. `"IE9999999X"`) |
| `sachverhalt_l_l` | — | nur § 13b/ig — `"1"` (1–3-stellig, ≠ 0) |
| `__comment` | — | menschenlesbarer Vermerk; **wird vom Serializer ignoriert** (alle `__`-Felder) |

**Saldenregel (vom Serializer geprüft):** Σ `umsatz` der Soll-Seiten = Σ `umsatz` der Haben-Seiten. Da jede vollständige Konto-an-Gegenkonto-Zeile in sich ausgeglichen ist, ist das bei korrekt gebildeten Zeilen automatisch erfüllt.

## 10. Beispiele

### Beispiel 1 — ARAP-Bildung (Versicherung 6.000 €, 3.000 € Folgejahr), ohne USt

```
**Buchungsvorschlag** (SKR04) — Abschlussbuchung / Aktive Rechnungsabgrenzung

Konto Soll          | Konto Haben          | Betrag
1900 ARAP           | 6400 Versicherungen  | 3.000,00 €

Belegdatum:     31.12.2026 (Bilanzstichtag)
USt-Tatbestand: keiner (reine Periodenabgrenzung)
Begründung:     12-Monats-Prämie 6.000 € am 01.07. gezahlt; 6/12 = 3.000 €
                betreffen das Folgejahr. ARAP nach § 250 Abs. 1 HGB,
                steuerlich identisch § 5 Abs. 5 S. 1 Nr. 1 EStG.
HGB vs. StB:    identisch; Bagatell-Wahlrecht § 5 Abs. 5 S. 2 EStG (≤ 800 €)
                hier nicht einschlägig. Detail → buchung-grundlagen § 3.1.
Plausibilität:  ✓ Konto-Klasse passt | ✓ keine USt | ✓ Periodenabgrenzung
Auflösung:      Folgejahr monatlich 1/12 (6400 an 1900) oder Einmal-Auflösung.
```

```json
{
  "skr": "SKR04",
  "buchungen": [
    {
      "umsatz": "3000,00",
      "soll_haben_kennzeichen": "S",
      "konto": "1900",
      "gegenkonto": "6400",
      "bu_schluessel": "",
      "belegdatum": "3112",
      "belegfeld_1": "ARAP-VERS-2026",
      "buchungstext": "ARAP Versicherung anteilig Folgejahr",
      "__comment": "Bildung ARAP § 250 Abs.1 HGB; 3.000 von 6.000 EUR"
    }
  ]
}
```

### Beispiel 2 — Urlaubsrückstellung (Splitt 6020 + 6100 an 3079), ohne USt

```
**Buchungsvorschlag** (SKR04) — Abschlussbuchung / Urlaubsrückstellung

Konto Soll                   | Konto Haben               | Betrag
6020 Gehälter                | 3079 Urlaubsrückstellung  |  8.500,00 €
6100 Soziale Abgaben (AG-SV) | 3079 Urlaubsrückstellung  |  1.700,00 €
                             | Summe                     | 10.200,00 €

Belegdatum:     31.12.2026 (Bilanzstichtag)
USt-Tatbestand: keiner
Begründung:     Resturlaub × Tagessatz Bruttopersonalkosten inkl. AG-SV
                (IDW HFA 5.7). Pflicht-Rückstellung § 249 Abs. 1 S. 1 HGB.
HGB vs. StB:    Stichtagsprinzip § 6 Abs. 1 Nr. 3a Buchst. f EStG — StB ohne
                künftige Lohnsteigerungen; AG-Anteile einbezogen (R 6.11 EStR).
                Detail → buchung-grundlagen § 4.2.
Plausibilität:  ✓ Σ Soll = Σ Haben (10.200) | ✓ keine USt | ✓ Konto 3079
                (alt. einzeiliger Aufwand 6072 an 3079)
```

```json
{
  "skr": "SKR04",
  "buchungen": [
    {
      "umsatz": "8500,00",
      "soll_haben_kennzeichen": "S",
      "konto": "6020",
      "gegenkonto": "3079",
      "bu_schluessel": "",
      "belegdatum": "3112",
      "belegfeld_1": "URL-RST-2026",
      "buchungstext": "Urlaubsrueckstellung 2026 Loehne",
      "__comment": "Splitt 1/2 Personalkosten"
    },
    {
      "umsatz": "1700,00",
      "soll_haben_kennzeichen": "S",
      "konto": "6100",
      "gegenkonto": "3079",
      "bu_schluessel": "",
      "belegdatum": "3112",
      "belegfeld_1": "URL-RST-2026",
      "buchungstext": "Urlaubsrueckstellung 2026 AG-SV",
      "__comment": "Splitt 2/2 AG-Anteil SV; 3079 = 10.200,00"
    }
  ]
}
```

### Beispiel 3 — Einzelbeleg § 13b Reverse Charge (Acme Cloud Ltd. IE, 1.500 € netto SaaS)

```
**Buchungsvorschlag** (SKR04) — Einzelbeleg / § 13b Abs. 1 UStG Reverse Charge

Konto Soll              | Konto Haben          | Betrag
6840 EDV-/Softwarekosten| 3300 Verb. aLuL      | 1.500,00 €   (Netto = Brutto, RC)
1407 Vorsteuer § 13b    | 3837 USt § 13b 19 %  |   285,00 €   (saldenneutral)

Belegdatum:     03.05.2026     Leistungsdatum: Mai 2026
USt-Tatbestand: § 13b Abs. 1 UStG — sonstige Leistung eines im übrigen
                Gemeinschaftsgebiet ansässigen Unternehmers (IE); Empfänger
                schuldet USt, VSt-Abzug § 15 Abs. 1 S. 1 Nr. 4 UStG.
USt-VA:         KZ 46/47 (BG/Steuer § 13b) + KZ 67 (VSt) — IE9999999X.
                Aggregation → ust-voranmeldung.
Plausibilität:  ✓ keine VSt vom Lieferanten | ✓ VSt 285 = USt 285 | ✓ Σ S = Σ H
```

```json
{
  "skr": "SKR04",
  "buchungen": [
    {
      "umsatz": "1500,00",
      "soll_haben_kennzeichen": "S",
      "konto": "6840",
      "gegenkonto": "3300",
      "bu_schluessel": "",
      "belegdatum": "0305",
      "belegfeld_1": "CLOUD-MAI-26",
      "buchungstext": "SaaS-Abo Acme Cloud Mai 2026",
      "__comment": "Netto-Aufwand Reverse Charge; Brutto = Netto"
    },
    {
      "umsatz": "285,00",
      "soll_haben_kennzeichen": "S",
      "konto": "1407",
      "gegenkonto": "3837",
      "bu_schluessel": "",
      "belegdatum": "0305",
      "belegfeld_1": "CLOUD-MAI-26",
      "buchungstext": "VSt 13b 19% EU-Sonstige",
      "eu_land_ustid_bestimmung": "IE9999999X",
      "sachverhalt_l_l": "1",
      "__comment": "Vorsteuer/USt 13b saldenneutral; prueffprogramm-verifiziert"
    }
  ]
}
```

## 11. Review / Validierung (vor Ausgabe des JSON-Blocks)

- [ ] **Saldengleichheit:** Σ `umsatz`(S) = Σ `umsatz`(H); jede Zeile Konto ≠ Gegenkonto, `umsatz` > 0. **Keine** Spiegelzeilen.
- [ ] **Netto + USt = Brutto** im lesbaren Block (Rundung ≤ 0,01 € tolerieren).
- [ ] **Konto-Existenz:** `konto`/`gegenkonto` im gewählten SKR (kontenrahmen.json bzw. vollständiger DATEV-SKR).
- [ ] **Soll/Haben-Logik:** Aufwand/Aktiv-Zugang im Soll, Passiv/Rückstellung/Verbindlichkeit im Haben, Vorsteuer im Soll, USt im Haben.
- [ ] **USt-Plausibilität:** KU → keine VSt; § 13b → keine VSt vom Lieferanten, saldenneutrale 1407/3837-Buchung + `eu_land_ustid_bestimmung`/`sachverhalt_l_l`; Automatikkonto → `bu_schluessel` leer (REW00305).
- [ ] **GwG-Grenze:** Netto > 800 € + Anlagegut-Indikator → Hinweis Aktivierung statt Aufwand (rates.json `gwg`-Grenzen).
- [ ] **Belegdatum** im Wirtschaftsjahr (`TTMM`); Stichtagsbuchungen = letzter Tag des WJ.
- [ ] **Feld-Format:** `buchungstext` ≤ 60 (CP1252-sicher); `belegfeld_1` ≤ 36 ohne Leerzeichen/Umlaute/Komma.
- [ ] **GoBD-Belegfunktion:** bei Abschlussbuchungen Eigenbeleg + Berechnungsschema vermerken (→ `buchung-grundlagen` § 8); Import als **Vorabbuchungsstapel**, vor Freigabe prüfen.
- [ ] **Reversal-Flag** bei kurzfristigen Rückstellungen (ausstehende Eingangsrechnungen) im `__comment`/lesbaren Block markieren (DATEV ohne Auto-Reversal → zwei Stapel).
- [ ] **Splitt-Konsistenz:** `kost_allocations` Σ `anteil_prozent` = `"100,00"`; Mehrzeiler-Summe = Gesamtbetrag.

## 12. Quellen

- UStG §§ 12, 13b, 14, 15, 19, 20 — gesetze-im-internet.de/ustg_1980/
- EStG §§ 4 Abs. 5/5b, 5 Abs. 4a/5, 6 Abs. 1 Nr. 3a, 6 Abs. 2, 6a — gesetze-im-internet.de/estg/
- HGB §§ 238, 249, 250, 252, 253, 257, 266, 275 — gesetze-im-internet.de/hgb/
- KStG § 8 Abs. 3 (vGA); KSVG §§ 24, 28 (KSK)
- BMF Vordruckmuster USt 1 A 2026 (KZ-Codes) — `config/2026/kz-codes-ust-va.json`
- DATEV SKR03 Art.-Nr. 11174 / SKR04 Art.-Nr. 11175, Stand 2026-01-01 — `config/2026/kontenrahmen.json`
- DATEV-Format EXTF-Buchungsstapel (Formatkategorie 21, Version 13) — Eingabe-Vertrag siehe `datev-export`
- `config/{active_year}/rates.json` (USt-Sätze, Pauschalen, GwG-Grenzen, KSK-Satz, Abzinsung)

## 13. Verwandte Skills

- `buchung-grundlagen` — beschreibt die Abschlussbuchungs-Vorgänge (Muster, Bewertung, HGB-vs-StB), die dieser Skill in konkrete Sätze umsetzt
- `datev-export` — konsumiert den JSON-Handoff (Abschnitt 9) und erzeugt die DATEV-EXTF-Buchungsstapel-CSV
- `ust-voranmeldung` — aggregiert § 13b-/ig-Buchungen zu KZ-Werten
- `monatsabschluss` — konsumiert laufende Buchungssätze, fügt Abgrenzungen hinzu
- `abstimmung` — prüft Buchungs-Salden gegen externe Belege (Bank, OP-Listen)
- `wiederkehrende-buchungen` — für wiederkehrende ARAP-Auflösung u. ä. (DATEV-Format Kategorie 65)
