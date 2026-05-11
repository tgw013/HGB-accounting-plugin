# Changes applied — 2026-05-11

This file documents the corrections applied to the plugin based on the findings in `ACCOUNTING_REVIEW_FIRST_PASS.md`. All changes are based on authoritative sources fetched and verified during the review session (DATEV-Kontenrahmen 2026 PDF, gesetze-im-internet.de, BMF, BMG, BMAS, Deutsche Rentenversicherung).

**⚠ Steuerberater-Pflicht:** Diese Änderungen sind eine erste Fix-Iteration auf Basis öffentlich verifizierter Quellen. Vor produktiver Nutzung sollten alle Änderungen durch einen qualifizierten Steuerberater oder Wirtschaftsprüfer geprüft und freigegeben werden.

---

## Files modified (16)

### Configs (2)

#### `config/rates-2026.json`
- Mindestlohn-Vollzeit: 2410 € → split in `_exakt: 2408.67` und `_gerundet: 2410` (+ Berechnungsformel als Quelle)
- **Aufbewahrungsfristen** — komplett neu strukturiert: Trennung zwischen Jahresabschlüssen (10 J.) und Buchungsbelegen (10 J. bis 2024 / 8 J. ab 2025) gemäß BEG IV; Rechnungen (§14b UStG), Lohnunterlagen, Verfahrensdokumentation einzeln benannt
- **Neu hinzugefügt:** `solidaritaetszuschlag_freigrenze_2026` (20.350 € Einzel / 40.700 € Zusammen; Milderungszone 11,9 %)
- **Neu hinzugefügt:** `sachbezugswerte_2026` (Mittag/Abend 4,57 €, Frühstück 2,37 €, Monat 137/345 €) — SvEV 2026, Bundesrat 19.12.2025
- **Neu hinzugefügt:** `gwg_und_afa_grenzen` (250 € Sofortabschreibung, 800 € GWG, 250-1000 € Pool, degressive AfA-Hinweis für 2026, § 7g Abs. 5 EStG 40 % verteilt auf 5 Jahre)

#### `config/kontenrahmen.json`
- **Vollständig neu strukturiert** als authoritative DATEV-2026-Referenz
- SKR03 Klasse 2: Label korrigiert ("Sonstige Erträge und Aufwendungen / Neutrale Aufwendungen" statt "Abgrenzungskonten — Rückstellungen/ARAP/PRAP/latente Steuern")
- `häufige_konten` für SKR03: 50 Einträge (vorher 16), alle mit `bezeichnung`-Feld verbatim aus DATEV-PDF Art.-Nr. 11174
- `häufige_konten` für SKR04: 43 Einträge (vorher 16), verbatim aus DATEV-PDF Art.-Nr. 11175
- Konkrete Korrekturen:
  - **Urlaubsrückstellung SKR03:** 0968 → **0961** (0968 ist "Passive latente Steuern")
  - **Urlaubsrückstellung SKR04:** 3050 → **3079** (3050 ist "Steuerrückstellung aus Steuerstundungen")
  - **Abschreibungen SAV SKR04:** 6200 → **6220** (6200 ist "Abschreibungen auf immaterielle VG")
  - **Löhne** (4100/6000) und **Gehälter** (4120/6020) jetzt separat
  - **KSt-/GewSt-Aufwand-Konten** korrekt zugeordnet (SKR03: 2200 KSt, 4320 GewSt; SKR04: 7600 KSt, 7610 GewSt)
  - **KSt-/GewSt-Rückstellungs-Konten** korrekt (SKR03: 0963 KSt, 0956 GewSt; SKR04: 3035 GewSt)
  - **Pensionsrückstellungs-Konten** korrekt (SKR03: 0953; SKR04: 3000)
  - **bAV-Aufwand**: SKR03 4165 / SKR04 6140 (vorher 4170/6170 — das sind VL bzw. Sonstige soziale Abgaben, NICHT bAV)
  - **Verb. SV** in SKR03: explizit 1742 (NICHT 1740 wie früher fälschlich angenommen — 1740 ist "Verb. Lohn und Gehalt")
  - **EWB/PWB-Konten** richtig zugeordnet: 2450 = PWB, 2451 = EWB (vorher vertauscht)
- Footer-Block `_aenderungslog_2026_05_11` mit Liste aller Änderungen

### Skills (9)

#### `skills/buchungssatz/SKILL.md`
- Buchungstext: max. 120 Z. → 60 Z. (DATEV-Export-Pflichtgrenze)
- §-Citations präzisiert: §4b → §4 Nr.1b i.V.m. §6a UStG; §19 erweitert um 25k/100k seit 2025
- **Section 5.3 Lohnbuchung — komplett neu geschrieben:**
  - AN-SV-Anteil (951,75 €) jetzt korrekt enthalten
  - Netto = 2.348,25 € (vorher fälschlich 3.300 €)
  - SKR03-Konten korrigiert: 4120 Gehalt (statt 4100), 1742 Verb. SV (statt 1740), 1741 Verb. LSt/KiSt
  - SKR04 Lohn-Konto auf 6020 Gehälter spezifiziert
- Section 5.4: SKR04 Abschreibung-Konto 6200 → 6220
- Section 7.1: DATEV-Zeichensatz UTF-8 → Windows-ANSI (CP1252) als Default; UTF-8 nur optional

#### `skills/buchungssatz-vorbereitung/SKILL.md`
- Section 1.4 Aufbewahrungsfristen: Tabelle neu strukturiert mit klarer Differenzierung 10 J. / 8 J. ab 2025 / 6 J. / Lohnunterlagen / Verfahrensdoku
- Section 2.1 Urlaubsrückstellung: Konten korrigiert (SKR03 0961 statt 0968; SKR04 3079 statt 3050) + Aufwandskonten realistischer
- Section 2.5 bAV: Komplett überarbeitet
  - Buchungslogik korrigiert (Entgeltumwandlung erzeugt KEINEN zusätzlichen Aufwand)
  - 4172/6175 (erfunden) entfernt
  - Korrekte DATEV-Konten: SKR03 4165 / SKR04 6140 für AG-Zuschuss bAV
  - Pensionsrückstellungen: SKR03 0953 / SKR04 3000 (statt erfundene 4190/6190)
  - Klarstellung: 4170/6170 ≠ bAV; 4170 = VL, 6170 = Sonstige soziale Abgaben
- Section 2.5 Pensionsrückstellungs-Abzinsung: 10 → **15-Jahres-Durchschnitt** gemäß § 253 Abs. 2 S. 2 HGB
- Section 2.5 AG-Zuschuss-Datum: "Neuverträge seit 2019, Altverträge seit 01.01.2022" (vorher fälschlich verkürzt)
- Section 2.7 Degressive AfA: 2,5-fach / 25 % entfernt — Hinweis dass für 2026 derzeit NICHT zulässig; historisch 2-fach / 20 % bei letzten Wiedereinführungen
- Section 2.7 Sonder-AfA § 7g: "40 % im Anschaffungsjahr" → "bis 40 % insgesamt verteilt auf 5 Jahre"

#### `skills/lohnabrechnung/SKILL.md`
- Section 4.4 SolZ-Freigrenze: 18.130/36.260 € → **20.350/40.700 €** für 2026 (+ Milderungszone 11,9 %)
- Section 9.1 § 3b EStG SV-Freiheit: 50 €/Std. → **25 €/Std.** gemäß § 1 Abs. 1 S. 1 Nr. 1 SvEV (Steuerfreiheit bleibt bei 50 €/Std.)
- Section 9.2 Sachbezugswert Mahlzeit: 4,23 € → **4,57 €** (SvEV 2026)
- Section 8.1 Konten-Tabelle: Löhne/Gehälter separat (4100/4120 für SKR03; 6000/6020 für SKR04); Verb. SV korrekt auf **1742** (SKR03) / 3740 (SKR04); LSt/KiSt kombiniert auf 1741/3730 mit klarem Hinweis
- Section 8.2 Buchungssatz-Beispiel: Konten-Beschriftung angepasst

#### `skills/ust-voranmeldung/SKILL.md`
- Section 1.2 Tabelle: Existenzgründer-Zeile umformuliert — Aussetzung der monatlichen VA-Pflicht für VZ 2021-2026 durch BEG III
- Section 1.3: Existenzgründer-Regelung komplett umgeschrieben mit klarem Hinweis auf Aussetzung

#### `skills/abstimmung/SKILL.md`
- Section 2.5 EWB-Konten: Klarer Hinweis dass DATEV 2450 = PWB (nicht EWB), 2451 = EWB (nicht PWB); SKR04 6920 = PWB
- Konten 1289/1290 für PWB/EWB-Forderungen mit Verify-Hinweis (DATEV-SKR04 belegt 1290 anders als "EWB Forderungen LuL")

#### `skills/jahresabschluss/SKILL.md`
- Section 5.5 Steuerrückstellungen — komplett korrigiert:
  - SKR03 KSt-Aufwand: 4300 → **2200** (4300 = "Nicht abziehbare Vorsteuer")
  - SKR03 GewSt-Rückstellung: 0955 → **0956**
  - SKR03 KSt-Rückstellung: 0956 → **0963**
  - Hinweis-Block ergänzt mit DATEV-Quelle
- Section 7.3 Aufstellungsfristen — Reihenfolge korrigiert:
  - **3 Monate**: mittelgroße + große KapGes (§ 264 Abs. 1 S. 3 HGB)
  - **6 Monate**: kleine + Kleinst KapGes (§ 264 Abs. 1 S. 4 HGB)
  - (Plugin hatte sie vertauscht)
- StB-Frist: 31.07. des Zweitfolgejahres → **28.02. des Zweitfolgejahres** (§ 149 Abs. 3 AO regulär nach Corona-Verlängerungen)

#### `skills/monatsabschluss/SKILL.md`
- Section 1 Checkliste: Urlaubsrückstellungs-Konto 0968/3050 → **0961/3079**
- Steuerkalender-Tabelle: Aufstellungsfristen korrigiert (3 Mon. mittelgr/groß; 6 Mon. klein/Kleinst); StB-Frist auf 28.02. korrigiert
- Konten-Tabelle: Urlaubsrückstellungs-Konten korrigiert

#### `skills/compliance/SKILL.md`
- Section "Jährliche Pflichten": Jahresabschluss-Aufstellung mit Differenzierung nach Größenklasse; Steuererklärung mit StB auf 28.02. korrigiert

#### `skills/ebilanz/SKILL.md`
- Section 10 Aufbewahrungsfristen: Tabelle mit klarer 2025-Trennung
- SKR03/SKR04 Mapping-Tabellen: Urlaubsrückstellungs-Konto 0968/3050 → **0961/3079**

### Commands (5)

#### `commands/lohnabrechnung.md`
- **Schritt 2 Mindestlohn**: 12,82 € → **13,90 €** (2026)
- **Schritt 3 SV-Tabelle**:
  - KV-Zusatzbeitrag-Durchschnitt erläutert (14,6 % + 2,9 % = 17,5 %)
  - PV-Satz: 3,4 → **3,6 %**
  - BBG KV/PV: 5.175 € → **5.812,50 €**
  - BBG RV/AV: 7.550 € → **8.450 €**
  - Sachsen-Sonderregel ergänzt
- **Schritt 5 bAV**: 302 € → **676 € (Steuer-frei) / 338 € (SV-frei)**; AG-Zuschuss-Datum präzisiert; korrekte Konten 4165/6140
- Hinweise:
  - Minijob 556 → **603 €**
  - Midijob untere Grenze 556,01 → **603,01 €**
  - Märzklausel-Hinweis ergänzt

#### `commands/ust-voranmeldung.md`
- **Schritt 1 Schwellen**:
  - Monatlich: > 7.500 € → **> 9.000 €**
  - Vierteljährlich: 1.000-7.500 € → **2.001-9.000 €**
  - Befreiung: < 1.000 € → **≤ 2.000 €**
  - Existenzgründer-Aussetzung ergänzt
- **Schritt 2 Kleinunternehmer**:
  - Vorjahr: 22.000 € → **25.000 €**
  - Laufendes Jahr: 50.000 € → **100.000 €**
  - Sofort-Pflicht bei Überschreitung ergänzt
- Hinweis Schluss: Nonsensical §-Citation "§20 Satz 1 UStG i.V.m. §1 Abs. 1 Satz 1 KStG analog" durch korrekte Rundungs-Toleranz-Info ersetzt

#### `commands/compliance.md`
- Aufbewahrungstabelle: Erweitert um 2025-Trennung (10 J. bis 2024 / 8 J. ab 2025 für Buchungsbelege und Rechnungen)
- HinSchG-Bußgeld: 50.000 € → korrekte Sätze **20.000 € / 500.000 €** gemäß § 40 HinSchG
- HinSchG-Inkrafttreten präzisiert (02.07.2023 für ≥250 MA; 17.12.2023 für 50-249 MA)
- GoBD-Update 14.07.2025 (2. Änderung wegen E-Rechnung) ergänzt
- E-Rechnungs-Pflicht ergänzt (Empfangspflicht 2025, Versandpflicht 2027/2028)

#### `commands/ebilanz.md`
- Taxonomie-Version: 6.8 → **6.9** (Pflichtanwendung GJ ab 2026, BMF-Schreiben 10.06.2025)
- Mapping-Beispiel: Sinnlose XBRL-IDs ("worksEquip" für Forderungen/Bank) ersetzt durch fachliche Taxonomie-Bereiche
- Steuererklärungs-Frist mit StB: 28.02. (gesetzliche Frist nach § 149 Abs. 3 AO; nicht 28./29.)

#### `commands/iks-pruefung.md`
- "9 Kontrollbereiche nach IDW PS 261" → aufgeteilt in **A. 5 IDW PS 261 Komponenten** + **B. 4 operative Audit-Schwerpunkte** mit korrekter Zuordnung (vorher konzeptionell falsch)

---

## Items intentionally NOT fixed (require Steuerberater verification or are scope-out)

1. **B.12 SKR04 Wertberichtigungs-Konten** — DATEV-PDF zeigt keine eindeutige Belegung für EWB/PWB-Forderungs-Gegenkonten in SKR04; abstimmung-skill nun mit "verify" markiert
2. **B.14 §13b KZ-Codes** — abstimmung-skill und ust-voranmeldung-skill widersprechen sich für KZ 46/47/73/84/67; benötigt Abgleich mit aktuellem ELSTER USt-1-A-Formular 2026
3. **GbR/MoPeG-Detail** in jahresabschluss-skill — bleibt mit Hinweis "offene Rechtsfrage" stehen
4. **Konkrete SKR03/SKR04 Sub-Konten für bAV-Komponenten** — nur Sammelkonto-Empfehlung (4165/6140); Sub-Konten für AN-Anteil vs. AG-Zuschuss vs. Pensionsrückstellungs-Zuführung müssten unternehmensspezifisch angelegt werden
5. **Sektor-spezifische Anpassungen** (Banken, Versicherungen, Krankenhäuser etc.) — out of scope
6. **Tarifverträge und branchenspezifische Mindestlöhne** — out of scope
7. **Aktuelle BMF-Schreiben zu Spezialthemen** (z.B. § 7g, Reisekosten Edge Cases) — Steuerberater

---

## Validation done

- JSON-Validität beider Configs geprüft (`python -m json.tool`)
- Alle Änderungen referenzieren ihre DATEV-/Gesetz-Quelle inline
- Vor-/Nach-Werte sind in dieser Liste dokumentiert
- Master-Report `ACCOUNTING_REVIEW_FIRST_PASS.md` enthält die ursprünglichen Befunde mit allen 4 Addenda

## Summary

| Status | Anzahl |
|---|---|
| Files modified | 16 |
| Sections rewritten significantly | ~25 |
| Konto-Nummern korrigiert | ~15 |
| Rate-/Wert-Updates | ~10 |
| §-Citation-Korrekturen | ~8 |
| Konzeptionelle Korrekturen (Buchungslogik, Cross-Skill-Konsistenz) | ~5 |
| Items mit Verify-Markierung statt Edit | ~5 |

End of changelog.
