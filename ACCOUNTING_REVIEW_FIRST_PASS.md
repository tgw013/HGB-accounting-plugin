# Accounting Content Review — First Pass

**Date:** 2026-05-11
**Reviewer:** Claude (Sonnet 4.6) — automated first-pass screening, NOT a Steuerberater audit
**Scope:** All 23 content files in the plugin (2 configs, 11 skills, 10 commands)
**Method:** Sequential file-by-file review with cross-reference ledger
**Purpose:** Filter list of candidates for a qualified Steuerberater / Wirtschaftsprüfer to confirm or dismiss before production use

⚠️ **This is not a certification.** Findings should be reviewed by a qualified professional before relying on the plugin's output for real client work. Items marked "verify" require external sources I cannot access. Items marked "high-confidence error" are reasonably certain but should also be confirmed.

---

## Headline assessment

The plugin's **skill files are mostly good** with a manageable number of specific errors. The **command files are systematically more outdated** — they appear to have been written against pre-2025 legal values and never refreshed for the post-Wachstumschancengesetz / post-BEG-IV regime, even though the plugin claims "Stand 2026" throughout.

If you imagine a user running `/lohnabrechnung` or `/ust-voranmeldung` interactively, they would receive several materially wrong rates and thresholds. The skills behind them carry the correct values, but the user-facing command surface doesn't.

**Total findings**: 14 high-confidence errors, ~20 likely-errors-to-verify, multiple cross-skill inconsistencies. Plus ~6 internal cross-references where two parts of the plugin disagree with each other.

---

## A. High-confidence errors (correct or fix)

Each of these I am ≥90% confident is materially wrong. They should be corrected before deployment.

### A.1 Stale rates in `commands/lohnabrechnung.md` — systemic

The entire concrete-rates surface of this command file uses pre-2026 values labeled as 2026:

| Line | Field | Used | Correct (2026) | Where the wrong value comes from |
|---|---|---|---|---|
| 24 | Mindestlohn | 12,82 €/h | **13,90 €/h** | 2025 value |
| 33 | BBG KV monatlich | 5.175,00 € | **5.812,50 €** | 2024 value |
| 34 | PV-Beitragssatz | 3,4 % | **3,6 %** | pre-July-2023 value |
| 35 | BBG RV monatlich | 7.550,00 € | **8.450,00 €** | 2024 value |
| 48 | bAV Steuer-frei monatlich | 302 € | **676 €** (= 8 % BBG-RV / 12) | 2024 value |
| 49 | bAV SV-frei monatlich | 302 € | **338 €** (= 4 % BBG-RV / 12) | 2024 value (and conflated with the steuer-frei limit) |
| 111 | Minijob-Grenze monatlich | 556 € | **603 €** | 2025 value |
| 112 | Midijob untere Grenze | 556,01 € | **603,01 €** | 2025 value |

**Fix:** Pull all numeric rates from `config/rates-2026.json` instead of hardcoding them inline. The config already has the correct 2026 values.

### A.2 Stale thresholds in `commands/ust-voranmeldung.md` — pre-Wachstumschancengesetz

| Line | Field | Used | Correct (2026) |
|---|---|---|---|
| 17 | VA-Schwelle monatlich (Vorjahres-Zahllast) | > 7.500 € | **> 9.000 €** (§ 18 Abs. 2 S. 2 UStG n.F. ab 2025) |
| 18 | VA-Schwelle vierteljährlich | 1.000–7.500 € | **2.001–9.000 €** |
| 19 | VA-Befreiungs-Schwelle | < 1.000 € | **≤ 2.000 €** |
| 23 | Kleinunternehmer Vorjahresumsatz | ≤ 22.000 € | **≤ 25.000 €** (§ 19 UStG n.F. ab 2025) |
| 23 | Kleinunternehmer laufender Umsatz | ≤ 50.000 € | **≤ 100.000 €** |

All five changed with the Wachstumschancengesetz / JStG 2024 (Inkrafttreten 1.1.2025).

**Also line 91:** "alle Beträge auf volle Euro gerundet (§ 20 Satz 1 UStG i.V.m. § 1 Abs. 1 Satz 1 KStG analog)" — this citation is **nonsense**. § 20 UStG regelt die Istversteuerung, hat nichts mit Rundung zu tun. § 1 KStG regelt Steuerpflicht der Körperschaft. Falls hier eine Rundungsregel beabsichtigt war: USt-Rundung folgt der kaufmännischen Praxis bzw. § 16 Abs. 1 UStG; keine Ankerregel "§ 20 UStG" oder "KStG analog".

### A.3 `commands/compliance.md` line 92 — HinSchG-Bußgeldrahmen falsch

> "HinSchG gilt seit Juli 2023, Bussgeldrahmen bis 50.000 EUR."

50.000 € entspricht keinem realen Bußgeldsatz nach § 40 HinSchG. Tatsächliche Sätze:
- **500.000 €**: Behinderung von Meldungen, Vergeltungsmaßnahmen, Verletzung der Vertraulichkeitspflicht
- **20.000 €**: Keine oder mangelhafte interne Meldestelle

Das Skill `compliance` (lines 261-264) hat es korrekt. Das Command hat eine erfundene Zahl.

### A.4 `commands/compliance.md` lines 44 + 47 — Aufbewahrungsfristen ohne 2025-Split

Das Command lists Buchungsbelege/Rechnungen pauschal mit 10 Jahren. Mit § 257 Abs. 4 HGB n.F. / § 147 Abs. 3 AO n.F. / § 14b UStG n.F. (alle Wachstumschancengesetz / BEG IV) sind seit 1.1.2025 **8 Jahre** vorgesehen für ab 2025 entstandene Belege/Rechnungen. Skill und Config wissen es; das Command nicht.

### A.5 `skills/buchungssatz/SKILL.md` Section 5.3 — Lohnbuchung fehlt AN-Anteil zur SV

Section 5.3 zeigt Brutto 4.500 → LSt 1.200 → Netto 3.300 €. Korrektes Netto bei diesen Annahmen wäre **2.348,25 €** (Brutto − LSt − AN-Anteil SV von 951,75 €). Die Buchung formal-Soll-Haben balanciert nur, weil der AN-SV-Anteil komplett unterschlagen wird. Same error in der SKR04-Variante.

Das paired Skill `lohnabrechnung` (Section 8.2) zeigt es korrekt: "an Verb. SV 1.903,50 €" (AG + AN).

### A.6 `skills/buchungssatz-vorbereitung/SKILL.md` Section 2.5 — Pensionsrückstellung-Abzinsung "10 Jahre"

§ 253 Abs. 2 S. 2 HGB n.F. (seit BilMoG-Anpassung 2016): Pensionsrückstellungen mit **15-Jahres-Durchschnittszinssatz** abzuzinsen. Sonstige Rückstellungen mit 7-Jahres-Durchschnitt. "10-Jahres-Durchschnitt" passt zu keiner Vorschrift.

### A.7 `skills/buchungssatz-vorbereitung/SKILL.md` Section 2.5 — bAV-Direktversicherungs-Buchung als "Vermögenswirksame Leistungen"

Konten 4170 (SKR03) / 6170 (SKR04) sind als "Vermögenswirksame Leistungen" beschrieben. VL (5. VermBG) und bAV-Entgeltumwandlung sind **konzeptionell unterschiedliche Tatbestände**. Eine Direktversicherungs-Buchung gehört nicht auf VL-Konten — Standard wäre 4180/6180 ("Beiträge zur Direktversicherung").

### A.8 `skills/buchungssatz-vorbereitung/SKILL.md` Section 2.7 — Degressive AfA "Max. 25 % / 2,5-fach"

Diese Sätze galten zuletzt für Anschaffungen bis 31.12.2022. Wiedereinführungen 2024 (Wachstumschancengesetz) und 2025 (JStG 2024) waren auf **2-fach max. 20 %** beschränkt. Für Anschaffungen ab 1.1.2026 ist die degressive AfA derzeit **nicht zulässig** (Stand bekannter Gesetzgebung).

### A.9 `skills/buchungssatz-vorbereitung/SKILL.md` Section 2.7 — Sonder-AfA § 7g "40 % im Anschaffungsjahr"

§ 7g Abs. 5 EStG erlaubt **bis zu 40 % insgesamt verteilt** über Anschaffungsjahr + 4 Folgejahre (freie jährliche Verteilung). "40 % im Anschaffungsjahr" suggeriert irrtümlich Sofort-Abschreibung.

### A.10 `skills/lohnabrechnung/SKILL.md` line 459 — § 3b EStG SV-Freiheit "50 €/Std."

Steuerfreiheit nach § 3b EStG: Grundlohn max. **50 €/Std.** ✓ Korrekt.
SV-Freiheit: Grundlohn max. **25 €/Std.** (§ 1 Abs. 1 S. 1 Nr. 1 SvEV). Skill setzt fälschlich beide Grenzen gleich.

### A.11 `skills/jahresabschluss/SKILL.md` line 591-595 — § 264 Abs. 1 HGB Aufstellungsfristen vertauscht

> "3 Monate nach Stichtag (kleine) | 6 Monate (große/mittelgr.)"

Korrekt nach § 264 Abs. 1 HGB:
- **Kleine + Kleinst KapGes**: bis 6 Monate (§ 264 Abs. 1 S. 4 HGB)
- **Mittelgroße + Große KapGes**: 3 Monate (§ 264 Abs. 1 S. 3 HGB)

Das **Command** jahresabschluss line 63 hat es korrekt; das **Skill** hat es vertauscht.

### A.12 `skills/abstimmung/SKILL.md` line 247/296 — Konto 1777 als "USt ig Lieferung"

Innergemeinschaftliche Lieferungen sind nach § 4 Nr. 1 b UStG i.V.m. § 6a UStG **steuerfrei** — es fällt keine deutsche USt an. Konto 1777 in SKR03 ist tatsächlich "USt aus innergemeinschaftlichem **Erwerb** 19 %". Label und Konto-Funktion passen nicht zusammen.

### A.13 `skills/ust-voranmeldung/SKILL.md` line 47 + 51-55 — Existenzgründer-Pflicht zur monatlichen VA

Skill stellt die Pflicht zur monatlichen USt-VA in den ersten 2 Geschäftsjahren als geltend dar. Diese Pflicht wurde durch das **Bürokratieentlastungsgesetz III** für die Veranlagungszeiträume 2021-2026 **ausgesetzt** (§ 18 Abs. 2 UStG i.V.m. Übergangsvorschrift). Aktuell gelten für Existenzgründer die normalen Schwellenwerte gemäß Schätzung.

### A.14 `rates-2026.json` + propagiert in mehreren Skills — Aufbewahrungsfristen-Doppeleintrag

`rates-2026.json` listet:
```json
"jahresabschluesse_buchungsbelege": 10,
"buchungsbelege_ab_2025": 8,
```

Die zwei Einträge widersprechen sich für Buchungsbelege (Row 1 sagt 10 J. für Buchungsbelege, Row 2 sagt 8 J. ab 2025).

Korrekte Differenzierung:
- Jahresabschlüsse, Bilanzen, Inventare, Lageberichte: 10 Jahre
- Buchungsbelege (ab 1.1.2025 entstanden): 8 Jahre
- Buchungsbelege (vor 1.1.2025 entstanden, noch nicht abgelaufen): 10 Jahre
- Handelsbriefe: 6 Jahre

Skill `compliance` und `iks-pruefung` haben es korrekt differenziert; `rates-2026`, `buchungssatz-vorbereitung`, `ebilanz`, `commands/compliance` propagieren den inkonsistenten/alten Wert.

---

## B. Likely errors / verify with Steuerberater

These I'd flag for confirmation. Most need external source access (BMF-Schreiben, aktuelle Verordnungen) that I don't have.

### B.1 KSt-Senkungspfad 2028→2032 (rates-2026.json + jahresabschluss-skill)
14 → 13 → 12 → 11 → 10 %. Politisch angekündigt (Koalitionsvertrag Frühjahr 2025), aber **ist § 23 KStG tatsächlich entsprechend geändert worden**? Wenn nur "geplant" und nicht enacted, sind alle Multi-Year-Steuerplanungs-Berechnungen falsch. **Höchste Verify-Priorität.**

### B.2 Sozialversicherungs-Rechengrößen 2026
- BBG KV/PV: 69.750 / 5.812,50 €/mo
- BBG RV/AV: 101.400 / 8.450 €/mo
- JAEG: 77.400 €/yr

Verify gegen Sozialversicherungs-Rechengrößenverordnung 2026 (publiziert ~Q4 2025 durch BMAS).

### B.3 PV-Sätze 2026 unverändert von 2025
3,6 % (mit Kind) / 4,2 % (kinderlos). Annahme: gleich wie 2025. Verify keine weitere Reform für 2026.

### B.4 KV-Zusatzbeitrag 2,9 % (rates-2026.json) für 2026
BMG-veröffentlicht jährlich. Verify.

### B.5 Insolvenzgeldumlage U3 0,15 % (rates-2026.json) für 2026
BMAS-festgesetzt jährlich. Verify.

### B.6 Sachbezugswert Mahlzeit 4,23 € (lohnabrechnung-skill line 467)
4,23 € entspricht 2024-Wert; 2025 = 4,40 €; 2026-Wert noch nicht in der Config.

### B.7 SolZ-Freigrenze 18.130 € / 36.260 € (lohnabrechnung-skill line 268)
18.130 € ist der 2024-Wert nach Inflationsausgleichsgesetz 2024. Mit JStG 2024/2025 weitere Anpassung. 2026-Wert wahrscheinlich höher.

### B.8 GewSt-Hebesätze 2026 (rates-2026.json + jahresabschluss-skill)
Berlin 410 / München 490 / Hamburg 470 / Frankfurt 460 — Hebesätze ändern sich Stadt-individuell. Verify aktuelle 2026-Werte.

### B.9 HGB-Taxonomie für GJ 2026 (ebilanz-skill + ebilanz-command)
Skill nennt 6.9, Command nennt 6.8. Standard-Veröffentlichungs-Rhythmus BMF: 6.8 (GJ 2024), 6.9 (GJ 2025). Für GJ 2026 erwartet man 6.10 oder 7.0. Verify die für GJ 2026 maßgebliche Taxonomie-Version durch das BMF.

### B.10 GoBD-Update vom 14.07.2025 (compliance-skill line 36)
Skill referenziert ein GoBD-Update mit diesem Datum. Bekannte historische Updates: 14.11.2014, 28.11.2019, 11.03.2024. Ob ein 14.07.2025-Update existiert, lässt sich aus den mir verfügbaren Quellen nicht bestätigen.

### B.11 Urlaubsrückstellungs-Konto 0968 (kontenrahmen.json + monatsabschluss-skill)
SKR03 0968 in der DATEV-aktuellen Veröffentlichung ist typisch **nicht** "Urlaubsverpflichtungen". Üblich: 0974 oder Sub-Konto von 0970. Verify gegen DATEV-SKR03-Stand 2026.

### B.12 SKR04 Urlaubsrückstellungs-Konto 3050 (kontenrahmen.json)
Analoge Frage in SKR04. Verify.

### B.13 KSt/GewSt-Aufwand-Konten 4300/4320 in SKR03 (jahresabschluss-skill Section 5.5)
SKR03 4xxx ist Klasse 4 "Betriebliche Aufwendungen". Steuern vom Einkommen (KSt/GewSt) sind in SKR03 traditionell in Klasse 2 ("Sonstige Erträge und Aufwendungen / neutrale"). Verify, ob 4300/4320 in der aktuellen DATEV-SKR03 für KSt/GewSt-Aufwand belegt sind oder ob es andere Konten sein sollten (z.B. 2200/2285).

### B.14 §13b-KZ-Codes — abstimmung-skill vs. ust-voranmeldung-skill widersprechen sich
- ust-voranmeldung: KZ 46 = BG für EU-Leistungen 19 %, KZ 47 = "Sonstige § 13b-Fälle"
- abstimmung: KZ 46 = EU-Dienstleistungen, KZ 73 = Lieferungen § 13b Abs. 2 Nr. 1/2/4-12, KZ 84 = Vorsteuer § 13b
Verify gegen aktuelles ELSTER-USt-1-A-Formular 2026, welche KZ welcher Sachverhalt ist.

### B.15 Konto-Bezeichnung "USt-Zahllast" auf 1780 vs. 1789 (kontenrahmen.json)
1780 in SKR03 ist tatsächlich "USt-Vorauszahlungen" (working account); Year-end "Zahllast" ist üblicherweise 1789. Soft-flag — Label und genaue Verwendung klären.

---

## C. Internal cross-references / contradictions

Wo zwei Plugin-Teile sich widersprechen, sieht die "richtige" Antwort so aus:

| Sachverhalt | Korrekte Quelle (im Plugin) | Inkorrekte Quelle(n) |
|---|---|---|
| § 264 Abs. 1 HGB Aufstellungsfrist | monatsabschluss-skill, commands/jahresabschluss, commands/monatsabschluss | **skills/jahresabschluss line 591-595 (vertauscht)** |
| § 149 Abs. 3 AO StB-Frist | ebilanz-skill (28.02. ✓) | monatsabschluss-skill, jahresabschluss-skill, compliance-skill (alle 31.07., veraltet) |
| Lohnbuchung mit AN-Anteil SV | lohnabrechnung-skill, buchungssatz-vorbereitung-skill | **buchungssatz-skill Section 5.3** |
| AG-Zuschuss bAV-Datum | lohnabrechnung-skill ("Neu 2019, Alt 2022") | buchungssatz-vorbereitung-skill ("seit 2019", verkürzt) |
| Aufbewahrungsfristen mit 2025-Split | compliance-skill, iks-pruefung-skill | rates-2026.json (Doppeleintrag), buchungssatz-vorbereitung-skill, ebilanz-skill, commands/compliance |
| § 13b KZ 46/47-Verwendung | (keine — beide Skills falsch oder ungenau) | abstimmung-skill und ust-voranmeldung-skill widersprechen sich |
| KSt-Senkungspfad 2028+ enacted? | (offen) | rates-2026.json + jahresabschluss-skill stellen es als Fakt dar — verify |
| Mindestlohn 2026 | lohnabrechnung-skill (13,90 €), rates-2026.json | commands/lohnabrechnung (12,82 €) |
| BBG-Werte 2026 | lohnabrechnung-skill, rates-2026.json | commands/lohnabrechnung (2024-Werte) |
| Minijob/Midijob-Grenze 2026 | lohnabrechnung-skill (603 €), rates-2026.json | commands/lohnabrechnung (556 €) |
| USt-VA-Schwelle | ust-voranmeldung-skill (9.000 €), rates-2026.json | commands/ust-voranmeldung (7.500 €) |
| Kleinunternehmer-Grenze | ust-voranmeldung-skill (25k/100k), rates-2026.json | commands/ust-voranmeldung (22k/50k) |
| HinSchG-Bußgeldrahmen | compliance-skill (20k/500k €) | commands/compliance (50k €, frei erfunden) |
| 1777 in SKR03 | (kein Skill direkt korrekt) | abstimmung-skill verwendet es falsch als "USt ig Lieferung" |
| HGB-Taxonomie für GJ 2026 | (offen — beide möglicherweise veraltet) | ebilanz-skill (6.9), commands/ebilanz (6.8) |

---

## D. Coverage gaps (informational — nicht falsch, sondern fehlend)

Was eine vollständige Referenz typischerweise auch enthalten würde:

### Rates / Schwellen
- GWG-Sofortabschreibung 250 € (§ 6 Abs. 2 EStG)
- Sammelposten/Pool 250-1.000 € (§ 6 Abs. 2a EStG) — kommt im monatsabschluss-skill vor, aber nicht in rates-2026
- Reisekostenpauschalen (Verpflegungsmehraufwand 14/28 € inland, Auslandspauschalen)
- Sachbezugswerte Unterkunft/Vollverpflegung monatlich
- Grundfreibetrag ESt 2026
- Eingangs-/Spitzen-/Reichensteuersatz ESt
- Bewirtungspauschalen 70 % (kommt vereinzelt vor, nicht zentralisiert)
- Lohnunterlagen-Aufbewahrungsfrist (typisch 6 Jahre, mit Sonderregeln für SV-Unterlagen)
- AfA-Tabellen-Verweis BMF
- SolZ-Freigrenze in rates-2026 (nur in Skill hardcoded)

### Konten (kontenrahmen.json)
- Reverse-Charge / innerg. Erwerb USt-Konten (1577/1787 SKR03)
- OSS-USt-Konten (OSS-Schwelle ist in rates-2026, aber Konten fehlen)
- Erhaltene / geleistete Anzahlungen
- KSt / GewSt / Soli Zahlungs- und Rückstellungs-Konten
- Skonto-Konten (Aufwand und Ertrag, je USt-Satz)
- SKR04 fehlt der Sammelkonto-Eintrag für Abziehbare Vorsteuer und USt-Zahllast (Asymmetrie zu SKR03)
- Trennung Löhne (4100/6000) vs. Gehälter (4120/6020) — derzeit unter einem Key gebündelt

### Inhaltliche Lücken
- Skonto bei Bezahlung
- Geldwerter Vorteil / Sachbezüge detailliert
- Anzahlungen geleistet/erhalten
- Innergemeinschaftliche Lieferung (Ausfuhr-Buchung)
- Privatentnahmen/-einlagen für PersGes/Einzelunternehmer
- Märzklausel-Hinweis (kommt in lohnabrechnung-skill vor, fehlt im command)
- Mehrere Beschäftigungsverhältnisse / StKl-VI-Logik
- Auslandstätigkeit / A1-Bescheinigung / DBA
- Schwerbehindertenabgabe § 154 SGB IX
- Künstlersozialabgabe
- LSt-Pauschalierung § 40 EStG
- Differenzbesteuerung § 25a UStG
- Land-/Forstwirt-Pauschalierung § 24 UStG

---

## E. Out-of-scope items für die Steuerberater-Prüfung

Dinge, die ich bewusst NICHT geprüft habe und die der Steuerberater zusätzlich abdecken sollte:

1. **Sektor-spezifische Vorschriften** — z.B. Reverse-Charge für Bauleistungen Edge Cases, Pflegeeinrichtungen, Banken, Versicherungen
2. **Aktuelle BMF-Schreiben und Verwaltungsanweisungen** — meine §-Citation-Verifikation deckt nur den Gesetzestext, nicht die Verwaltungsauffassung
3. **Aktuelle BFH-Rechtsprechung** — Änderungen der Auslegung sind nicht erfasst
4. **Konkrete Steuergestaltungs-Beispiele** — alle Berechnungen sind mathematisch korrekt, aber ob das gewählte Vorgehen empfehlenswert ist, beurteile ich nicht
5. **Spezifische SKR03/SKR04-Konto-Nummern** — wo ich "verify" schreibe, kann der Steuerberater gegen die DATEV-Stand-2026-Veröffentlichung prüfen
6. **eBilanz Taxonomie-IDs** — XBRL-Element-Namen müssen gegen die aktuelle BMF-Taxonomie-Veröffentlichung geprüft werden
7. **Tarifverträge und branchenspezifische Mindestlöhne**
8. **Korrekt-aktuelle Bearbeitungsdaten von Verordnungen** — alle Verordnungen, die ich als "2026" gegen die Config geprüft habe, sollten gegen die offiziellen Veröffentlichungen abgeglichen werden
9. **Bilanzanalyse-Aussagen** — Kennzahlen-Definitionen sind plausibel, aber Branchenkonventionen variieren

---

## F. Recommended remediation priorities

Falls du das Plugin sicherer machen möchtest (priorisiert):

### Priorität 1 — vor produktiver Nutzung
1. Alle hardcoded Rates in `commands/lohnabrechnung.md` und `commands/ust-voranmeldung.md` durch Verweise auf `config/rates-2026.json` ersetzen (Item A.1, A.2)
2. `commands/compliance.md` HinSchG-Bußgeld korrigieren auf 20.000 / 500.000 € (Item A.3)
3. `skills/buchungssatz/SKILL.md` Section 5.3 Lohnbuchung mit AN-SV-Anteil ergänzen (Item A.5)
4. `skills/jahresabschluss/SKILL.md` line 591-595 Aufstellungsfristen-Tabelle korrigieren (Item A.11)
5. `skills/buchungssatz-vorbereitung/SKILL.md` Pensionsrückstellung 10 → 15 Jahre (Item A.6), VL-Konten ersetzen (A.7), AfA-Sätze aktualisieren (A.8, A.9)

### Priorität 2 — vor Steuerberater-Übergabe
6. `commands/compliance.md` Aufbewahrungsfristen-Tabelle mit 2025-Split (Item A.4)
7. `skills/lohnabrechnung` § 3b EStG SV-Freiheit 25 € statt 50 € (Item A.10)
8. `skills/abstimmung` Konto-1777-Label korrigieren (Item A.12)
9. `skills/ust-voranmeldung` Existenzgründer-Pflicht-Aussetzung dokumentieren (Item A.13)
10. `config/rates-2026.json` Aufbewahrungsfristen-Doppeleintrag entkonflationieren (Item A.14)

### Priorität 3 — durch Steuerberater verifizieren lassen
11. Alle B-Items, vor allem KSt-Senkungspfad (B.1) und SV-Rechengrößen 2026 (B.2-B.5)

### Priorität 4 — coverage gaps schließen
12. Die fehlenden Rates und Konten ergänzen (Abschnitt D)

---

## G. Methodology notes (for traceability)

- Sequential read of all 23 content files via Claude Sonnet 4.6
- 11 skills reviewed individually (single-pass, building cross-reference ledger)
- 10 commands reviewed via 3 parallel subagents, then findings verified by re-reading each file directly
- 2 of the 3 subagents made specific errors (misreading file content) that were caught during verification — agent output is not reliable as a standalone deliverable
- Cross-reference ledger built progressively (see `xref-ledger.md` in same directory)
- No external sources accessed; all "verify" items genuinely need a Steuerberater or BMF-publication lookup

End of original report.

---

# Addendum — 2026-05-11 (later in same session)

## Methodology correction

After delivery of the original report, the user (correctly) pointed out that B-class items were over-cautiously deferred. They are answerable from publicly accessible legal text and ministerial publications via `WebFetch` / `WebSearch`. I had pre-framed "first pass" as not including outbound source verification, which was the wrong call — verifying a §-citation against the actual law is cheap and exactly what a first-pass should do to reduce noise.

All 10 B-items have now been resolved against:
- `gesetze-im-internet.de` (KSt, SGB XI, SvBezGrV 2026)
- `bundesgesundheitsministerium.de` (PV-Beitragssätze)
- `bundesfinanzministerium.de` (GoBD 2. Änderung vom 14.07.2025)
- `deutsche-rentenversicherung.de` (Minijob 2026)
- Standard fiscal-press references for current Sätze (TK, AOK, vdek, Haufe)

## B-item resolution

| # | Item | Original flag | Resolved answer | Plugin status |
|---|---|---|---|---|
| B.1 | KSt-Senkungspfad 2028-2032 | "verify whether enacted" | **Enacted**. § 23 Abs. 1 KStG aktueller Wortlaut listet die Stufen 15/14/13/12/11/10 % wörtlich. | ✓ Plugin correct |
| B.2 | SV-Rechengrößen 2026 | "verify against BMAS-VO" | BBG RV/AV 101.400/8.450 ✓; BBG KV/PV 69.750/5.812,50 ✓; JAEG 77.400 ✓ (alle aus SvBezGrV 2026) | ✓ Plugin correct |
| B.3 | PV-Sätze 2026 unverändert? | "verify no new reform" | 3,6 % allgemein + 0,6 % Kinderlosenzuschlag (BMG bestätigt; seit 1.1.2025; bis 2026 unverändert) + Sachsen AN 2,3 % / AG 1,3 % | ✓ Plugin correct |
| B.4 | KV-Zusatzbeitrag 2026 = 2,9 % | "verify BMG-Wert" | 2,9 % (BMG-Orientierungswert für 2026; +0,4 Pp vs. 2025) | ✓ Plugin correct |
| B.5 | U3 Insolvenzgeld 2026 = 0,15 % | "verify BMAS-Wert" | 0,15 % (gesetzlich festgeschrieben gemäß § 360 SGB III; keine Senkungs-VO für 2026 erlassen) | ✓ Plugin correct |
| B.6 | Sachbezugswert Mahlzeit "4,23 €" | "verify 2026-Wert" | **4,57 €** für 2026 (Mittag/Abend) / 2,37 € Frühstück (SvEV 2026, Bundesrat 19.12.2025) | ✗ **Plugin OUTDATED** — siehe Erweiterung Sektion A unten |
| B.7 | SolZ-Freigrenze "18.130 / 36.260" | "verify 2026-Werte" | **20.350 € Einzel / 40.700 € Zusammen** für 2026 | ✗ **Plugin OUTDATED** — siehe Erweiterung Sektion A unten |
| B.8 | GewSt-Hebesätze 2026 | "verify Stadt-Werte" | Berlin 410 / München 490 / Hamburg 470 / Frankfurt 460 (Stand 2026) | ✓ Plugin correct |
| B.9 | HGB-Taxonomie für GJ 2026 = 6.9? | "verify aktuelle Version" | **6.9 ist korrekt** (BMF-Schreiben vom 10.06.2025; Taxonomie 6.9 vom 01.04.2025; Pflichtanwendung Geschäftsjahre **ab 2026**). | ✓ ebilanz-**skill** correct (6.9); ebilanz-**command** outdated (sagt "6.8 oder aktuell") |
| B.10 | GoBD-Update 14.07.2025 | "verify Existenz" | **Existiert**. BMF-Schreiben vom 14.07.2025: "2. Änderung der GoBD" wegen E-Rechnungs-Anpassungen (Archivierung strukturierte Daten, Hybrid-Formate ZUGFeRD, Bon-Aufbewahrung) | ✓ compliance-skill correct |

**Score:** 7 von 10 B-Items resolved als "Plugin ist korrekt"; 2 als reale Errors gefunden; 1 mit Spaltung (Skill korrekt, Command veraltet).

## Promotion of 2 items from B-class to A-class (high-confidence errors)

### A.15 (new) — `skills/lohnabrechnung/SKILL.md` line 467 — Sachbezugswert Mahlzeit veraltet

Skill nennt "ca. 4,23 € Mittag" als Sachbezugswert. Tatsächlich:
- 2024: 4,23 € (Wert, den der Skill anscheinend übernommen hat)
- 2025: 4,40 €
- **2026: 4,57 €** (SvEV 2026, vom Bundesrat am 19.12.2025 beschlossen, gültig ab 1.1.2026)

Auch im Plugin nicht zentral abgelegt — der Wert sollte in `rates-2026.json` ergänzt werden statt im Skill hardcodiert zu sein. Frühstück 2026: 2,37 €; monatlich gesamt 345 € / Mittag-Monat 137 €.

### A.16 (new) — `skills/lohnabrechnung/SKILL.md` line 268 — SolZ-Freigrenze veraltet

Skill nennt 18.130 € (Einzel) / 36.260 € (Zusammen) als Freigrenze. Tatsächlich aktuelle Werte:
- 2024: 18.130 / 36.260 € (das, was der Skill verwendet)
- 2025: 19.950 / 39.900 €
- **2026: 20.350 / 40.700 €**

Wie bei A.15 ein hardcodierter Skill-Wert, der nicht für 2026 aktualisiert wurde. Sollte in `rates-2026.json` ergänzt werden.

## Knock-on updates to other sections

### Section A (high-confidence errors) total: 14 → 16
Added A.15 (Sachbezugswert) und A.16 (SolZ-Freigrenze).

### Section B (verify) total: 14 → 6
Resolved: B.1, B.2, B.3, B.4, B.5, B.6 (→ A.15), B.7 (→ A.16), B.8, B.9, B.10.
Still open as B-items (most still need Steuerberater confirmation against specific SKR03/SKR04-Belegungen of the current DATEV publication):
- B.11 Urlaubsrückstellungs-Konto 0968 SKR03 (Konto-Belegung in aktueller DATEV-SKR03)
- B.12 Urlaubsrückstellungs-Konto 3050 SKR04 (analog)
- B.13 KSt/GewSt-Aufwand-Konten 4300/4320 SKR03 (atypische Klasse-4-Verwendung)
- B.14 §13b-KZ-Codes — Inkonsistenz abstimmung-skill ↔ ust-voranmeldung-skill (gegen ELSTER-Formular 2026 verifizieren)
- B.15 USt-Zahllast-Konto 1780 vs. 1789 Label-Frage

### Section C (cross-references)
Aktualisierter Status:
- "KSt-Senkungspfad enacted?" — RESOLVED: ja, plugin correct
- "HGB-Taxonomie für GJ 2026" — RESOLVED: 6.9, skill correct, command outdated
- "GoBD-Update 14.07.2025" — RESOLVED: existiert, skill correct
- Neue Konflikte hinzuzufügen:
  - Sachbezugswert Mahlzeit: Plugin verwendet 4,23 € (2024-Wert) statt 4,57 € (2026)
  - SolZ-Freigrenze: Plugin verwendet 18.130/36.260 € (2024-Werte) statt 20.350/40.700 € (2026)

### Section F (remediation priorities)
Promote to Priority 1:
- Sachbezugswert Mahlzeit 4,23 → 4,57 € im lohnabrechnung-skill korrigieren (und in rates-2026 hinzufügen)
- SolZ-Freigrenze 18.130 → 20.350 € (Einzel) bzw. 36.260 → 40.700 € (Zusammen) im lohnabrechnung-skill korrigieren

Demote from Priority 3 (verify-with-Steuerberater) to "resolved, plugin correct" — saves the Steuerberater time:
- KSt-Senkungspfad
- BBG-Werte
- PV-Sätze 2026
- KV-Zusatzbeitrag 2026
- U3 2026
- GewSt-Hebesätze 2026
- HGB-Taxonomie 6.9 für GJ 2026
- GoBD-Update 14.07.2025

## What this means for the headline assessment

The original report framed many issues as "needs Steuerberater verification". After the resolution pass, the actual picture is **cleaner than I previously suggested**:

- The plugin authors got the **legal text and big-picture rates mostly right** for 2026 — KSt-Stufen, BBG, JAEG, PV-Sätze, KV-Zusatz, U3, GewSt-Hebesätze, HGB-Taxonomie-Version, GoBD-Aktualität sind alle korrekt.
- The **systematic problem is** the commands-vs-skills drift: commands are pre-2025, skills are current.
- The **specific hardcoded-in-skill values** that were not updated for 2026: Sachbezugswert Mahlzeit, SolZ-Freigrenze. Both should be in `rates-2026.json` rather than hardcoded inline.
- Plus the documented internal contradictions and the few accounting-logic errors (Lohnbuchung AN-SV, Pensionsrückstellungs-Abzinsung, AfA-Sätze, § 264 Aufstellungsfristen, § 3b SV-Freiheit).

**Net effect of this addendum:** the Steuerberater's to-do list shrunk meaningfully. The remaining open questions are now narrowly scoped to (a) verify specific SKR03/SKR04 account-number belegungen against current DATEV publication, (b) verify §13b KZ-codes against ELSTER form, and (c) sign off on the actual content edits we propose.

End of first addendum.

---

# Addendum 2 — 2026-05-11 (same session, DATEV account-number verification)

User pointed to DATEV's Hilfe-Center for SKR03 account-number authoritative source. The Hilfe-Center is JavaScript-rendered, so direct fetch returns only the page header. Instead I used WebSearch against `buchungssatz.de`, `haufe.de`, `rechnungswesen-info.de`, `sevdesk.de`, `faktorly.com`, and similar sources that quote the SKR03/SKR04 Kontenbezeichnungen directly. Findings below.

## Resolution of remaining B-class items

| # | Item | Resolved answer | Plugin status |
|---|---|---|---|
| B.11 | SKR03 0968 als Urlaubsrückstellung? | **WRONG**. SKR03 0968 ist **"Passive latente Steuern"** (per `buchungssatz.de`). Urlaubsrückstellungen sind in SKR03 auf **0961** zu buchen (per `haufe.de`). 0974 ist "Rückstellungen für Gewährleistungen" (Gewährleistungs-RST). | ✗ **Plugin REAL ERROR** — siehe A.17 unten |
| B.12 | SKR04 3050 als Urlaubsrückstellung? | Nicht direkt verifiziert in dieser Suche. Wahrscheinlich gleichermaßen falsch, da die SKR04-Belegung typischerweise im 3060er-Bereich liegt. Verify separately. | ⚠ verbleibt offen |
| B.13 | SKR03 KSt-Aufwand 4300 + GewSt-Aufwand 4320? | **Teilkorrekt**. GewSt-Vorauszahlung ist tatsächlich auf **4320** zu buchen ✓ (per `dasfinanzen.de`, `haufe.de`). KSt-Aufwand auf "4300" ist **WRONG** — KSt-Aufwand ist in SKR03 auf **2200** (Klasse 2 = neutrale Aufwendungen/Steuern vom Einkommen) (per `sevdesk.de`). Außerdem: jahresabschluss-skill nennt "0955 GewSt-Rückstellung" und "0956 KSt-Rückstellung" — tatsächlich ist **0956 = Gewerbesteuerrückstellung** (per `faktorly.com`); die plugin hat vermutlich die zwei Konten vertauscht. | ✗ **Plugin REAL ERRORS** — siehe A.18 + A.19 unten |
| B.14 | §13b KZ-Codes (Inkonsistenz abstimmung ↔ ust-voranmeldung) | Nicht via DATEV-Kontenrahmen-Suche verifizierbar; braucht aktuelles ELSTER-USt-1-A-Formular. | ⚠ verbleibt offen |
| B.15 | SKR03 1780 als "USt-Zahllast" oder "Vorauszahlungen"? | **CONFIRMED**. 1780 = "Umsatzsteuer-Vorauszahlungen/Erstattungen"; 1789 = "Umsatzsteuer laufendes Jahr" (= Year-end Zahllast). Plugin's kontenrahmen.json `umsatzsteuer_zahllast: 1780` ist semantisch off — label sollte `umsatzsteuer_vorauszahlungen` heißen, oder das Konto sollte 1789 sein. | ⚠ Label/Account-Mismatch — als Konsistenz-Issue ergänzt |

## Promotion to Section A (3 new high-confidence errors)

### A.17 (new) — `config/kontenrahmen.json` line 42 — SKR03 0968 ist NICHT Urlaubsrückstellung

Plugin definiert:
```json
"urlaubsrueckstellung": "0968"
```

In der aktuellen DATEV-SKR03-Belegung ist **0968 = "Passive latente Steuern"**, nicht Urlaubsrückstellung. Korrekt für Urlaubsverpflichtungen: **0961 "Urlaubsrückstellungen"**.

Knock-on effects:
- `skills/buchungssatz-vorbereitung/SKILL.md` Section 2.1 bucht Urlaubsrückstellung gegen 0968 → **falsche Buchung**
- `skills/monatsabschluss/SKILL.md` Section 3.2 und Konten-Referenztabelle nennt 0968 → falsch
- `skills/ebilanz/SKILL.md` Mapping-Tabelle nennt 0968 → falsch

**Fix:** In `config/kontenrahmen.json` 0968 → 0961 ändern, und propagieren in alle Skills, die das Konto referenzieren.

### A.18 (new) — `skills/jahresabschluss/SKILL.md` Section 5.5 — Steuerrückstellungs-Konten vertauscht

Plugin definiert:
```
SKR03 | 4320 Gewerbesteuer-Aufwand  | 0955 Gewerbesteuerrückstellung
SKR03 | 4300 KSt-Aufwand            | 0956 KSt-Rückstellung
```

Tatsächliche DATEV-Belegung (per `faktorly.com`, `rechnungswesen-info.de`):
- **0956 = Gewerbesteuerrückstellung** (nicht KSt-Rückstellung)
- KSt-Rückstellung ist eine andere Nummer (typisch 0954 oder 0959 — verify in DATEV-Originalveröffentlichung)
- 0955 ist Steuerrückstellungen-Sammelkonto

Plugin hat die Konten 0955 und 0956 zwischen GewSt-Rückstellung und KSt-Rückstellung vertauscht.

### A.19 (new) — `skills/jahresabschluss/SKILL.md` Section 5.5 — KSt-Aufwand falsches Konto

Plugin bucht KSt-Aufwand auf **4300** (SKR03). Klasse 4 ist "Betriebliche Aufwendungen". Tatsächlich:
- KSt-Aufwand in SKR03 ist auf **2200** (Klasse 2 = "Neutrale Aufwendungen und Erträge — Steuern vom Einkommen")
- 4300 in SKR03 ist standardmäßig anders belegt (häufig Wareneingang-Bereich oder spezifischer Aufwand — nicht KSt-Aufwand)

Die GewSt-Buchung auf **4320** dagegen ist eine etablierte Praxis und in Ordnung (auch wenn der "saubere" Posten ebenfalls in Klasse 2 wäre — die DATEV-Konvention erlaubt 4320 für Gewerbesteuer-Vorauszahlungen).

## Revision of earlier flag A (kontenrahmen.json SKR03 Klasse 2 label)

Ursprünglicher Flag: Plugin sagt "Abgrenzungskonten (Rückstellungen, ARAP/PRAP, latente Steuern)", korrekt sei "Sonstige Erträge und Aufwendungen / neutrale".

**Revidiert:** Die offizielle DATEV-Klassen-2-Bezeichnung lautet **"Neutrale Aufwendungen und Erträge — Abgrenzungskonten"** (per Ecovis-RTS). Beide Begriffe kommen vor. Die Plugin's Label "Abgrenzungskonten" ist **teilweise korrekt** (das Wort ist Teil des offiziellen Titels). Was **irreführend** bleibt: die parenthetische Aufzählung "Rückstellungen, ARAP/PRAP, latente Steuern" — diese Posten sind in Klasse 0, NICHT in Klasse 2. Klasse 2 enthält stattdessen Zinsen, Steuern vom Einkommen, außerordentliche und periodenfremde Posten.

**Empfehlung:** Plugin's Label aktualisieren auf: `"Neutrale Aufwendungen und Erträge / Abgrenzungskonten (Zinsen, Steuern vom Einkommen, außerordentliche/periodenfremde)"` — und die irreführende Aufzählung von Rückstellungen/ARAP/PRAP/latente Steuern entfernen.

## Confirmation of earlier flag (abstimmung 1777 als "USt ig Lieferung")

DATEV labelt 1777 tatsächlich als "Umsatzsteuer EG-Lieferungen" (per WebSearch). Das deckt sich mit dem Plugin-Label "USt ig Lieferung". Mein ursprünglicher Flag, dass es "USt aus i.G. Erwerb" heißen müsste, war **terminologisch zu streng**: DATEV verwendet beide Bezeichnungen (EG-Lieferung aus Erwerber-Perspektive bzw. EG-Erwerb je nach Quelle). Die Buchungslogik selbst ist im Plugin korrekt (1577 VSt + 1777 USt + Aufwand 3xxx an Verb. = Reverse-Charge für i.G. Erwerb).

**A.12 Flag downgraded:** das Label-Mapping ist OK; Aufmerksamkeit nur bei semantischer Konsistenz innerhalb des Skills (es sollte klar sein, dass dies die USt-Schuld des **Erwerbers** beim i.G. Erwerb ist, nicht eine USt auf eigene i.G. Lieferung).

## Updated totals

- High-confidence errors (Section A): 16 → **18** (A.17, A.18, A.19 added; A.12 downgraded but not removed entirely)
- Verify-needed (Section B): 6 → **2** (only B.12 SKR04 3050 und B.14 §13b KZ-Codes bleiben offen)

## Sources used in addendum 2

- [SKR03 0968 = Passive latente Steuern (buchungssatz.de)](https://www.buchungssatz.de/de_DE/konto/skr03/0968.html)
- [Urlaubsrückstellung auf SKR03 0961 (haufe.de)](https://www.haufe.de/finance/haufe-finance-office-premium/rueckstellung-urlaubsrueckstellung_idesk_PI20354_HI2924379.html)
- [SKR03 0974 = Gewährleistungs-Rückstellungen (buchungssatz.de)](https://www.buchungssatz.de/de/konto/skr03/0974.html)
- [SKR03 Klasse 2 Beschreibung (Ecovis RTS)](https://www.ecovis-rts.de/servicecenter/kontenrahmen/skr-03-klasse-2.html)
- [SKR03 1777/1780/1789 USt-Konten (buchhaltungsbutler.de)](https://wissen.buchhaltungsbutler.de/hc/de/articles/11408798861597-Salden-der-Umsatzsteuer-und-Vorsteuerkonten-vortragen)
- [SKR03 Körperschaftsteuer-Konto 2200 (sevdesk.de)](https://sevdesk.de/lexikon/koerperschaftssteuer/)
- [SKR03 GewSt-Rückstellung 0956, GewSt-Vorauszahlung 4320 (faktorly.com)](https://www.faktorly.com/rueckstellung-fuer-koerperschafts-und-gewerbesteuer/)
- [DATEV Kontenrahmenbeschreibung 2021 SKR03 (DATEV Hilfe-Center — JavaScript-rendered, nicht direkt fetchbar)](https://help-center.apps.datev.de/documents/0906300)
- [DATEV Kontenplan-Übersicht SKR03/SKR04 (datev.de)](https://www.datev.de/web/de/berufsgruppenuebergreifend/ratgeber/rechnungswesen/kontenplan-buchhaltung-mit-skr03-skr04)

End of addendum 2.

---

# Addendum 3 — 2026-05-11 (same session, authoritative DATEV PDF verification)

User provided two DATEV Hilfe-Center PDFs:
- `st65108547211_de.pdf` = SKR03-Kontenrahmen, **Gültig für 2026** (Art.-Nr. 11174 2026-01-01)
- `st65118491659_de.pdf` = SKR04-Kontenrahmen, **Gültig für 2026** (Art.-Nr. 11175 2026-01-01)

These are the authoritative source. I extracted text via poppler (`pdftotext -layout`) and grepped each requested account number directly. Findings change the picture for both SKR03 and SKR04 quite a bit.

## SKR03-Konten — authoritative DATEV verbatim

| Konto | DATEV-Bezeichnung (verbatim 2026) | Plugin-Verwendung | Status |
|---|---|---|---|
| 0955 | Steuerrückstellungen | Plugin (jahresabschluss-skill): "Gewerbesteuerrückstellung" | ✗ wrong |
| 0956 | Gewerbesteuerrückstellung nach... | Plugin (jahresabschluss-skill): "KSt-Rückstellung" | ✗ wrong (swapped with 0955) |
| 0961 | **Urlaubsrückstellungen** | nicht verwendet | (das wäre der korrekte Konto) |
| 0962 | Steuerrückstellung aus Steuerstundungen | nicht verwendet | |
| 0963 | **Körperschaftsteuerrückstellung** | nicht verwendet | (das wäre korrekt für KSt-Rückstellung) |
| 0968 | **Passive latente Steuern** | Plugin (kontenrahmen.json): "Urlaubsrückstellung" | ✗ wrong |
| 0974 | Rückstellungen für Gewährleistungen | nicht direkt verwendet | |
| 1776 | Umsatzsteuer 19 % | Plugin: "Umsatzsteuer 19 %" | ✓ |
| 1777 | Umsatzsteuer aus im Inland **steuerpflichtigen EU-Lieferungen** | Plugin (abstimmung-skill): "USt ig Lieferung" | ✓ matches DATEV label (Flag A.12 cancelled) |
| 1780 | Umsatzsteuer-Vorauszahlungen | Plugin: "USt-Zahllast" | ⚠ label off (semantisch "Vorauszahlungen", nicht "Zahllast") |
| 1789 | Umsatzsteuer laufendes Jahr | nicht direkt verwendet | (das wäre der korrekte Konto für Year-end-Zahllast) |
| 2200 | **Körperschaftsteuer** (Aufwand-Konto) | nicht direkt verwendet | (das wäre korrekt für KSt-Aufwand) |
| 2281 | Gewerbesteuernachzahlungen Vorjahre | nicht verwendet | |
| 2285 | Steuernachzahlungen Vorjahre | nicht verwendet | |
| 4170 | Vermögenswirksame Leistungen | Plugin (buchungssatz-vorber.): "Entgeltumwandlung Direktversicherung" | ✗ **konzeptionell wrong** (4170 IS VL but VL ≠ bAV-Direktversicherung — und beide sind verschiedene Tatbestände) |
| 4180 | **Bedienungsgelder** | (kein Plugin-Bezug — aber ich hatte 4180 als "Beiträge zur Direktversicherung" empfohlen → REVIDIERT: DATEV 4180 ist Bedienungsgelder, nicht bAV) |
| 4190 | **Aushilfslöhne** | Plugin (buchungssatz-vorber.): "Zuführung Pensionsrückstellung" | ✗ wrong (4190 ist Aushilfslöhne, kein Pensions-Konto) |
| 4194-4199 | Pauschale Steuern / Minijobs | nicht verwendet | |
| 4300 | **Nicht abziehbare Vorsteuer** | Plugin (jahresabschluss-skill 5.5): "KSt-Aufwand" | ✗ **wrong account class** (KSt-Aufwand ist 2200) |
| 4320 | Gewerbesteuer | Plugin (jahresabschluss-skill): "GewSt-Aufwand" | ✓ DATEV-konform |
| 4900 | Sonstige betriebliche Aufwendungen | Plugin (buchungssatz-vorber.): "Personalaufwand Urlaubsrückstellung" | ⚠ generisch verwendbar aber nicht spezifisch für Personal — eher unsauber, nicht falsch |

## SKR04-Konten — authoritative DATEV verbatim (mit dramatischen Plugin-Differenzen)

| Konto | DATEV-Bezeichnung (verbatim 2026) | Plugin-Verwendung | Status |
|---|---|---|---|
| 1200 | Forderungen aus Lieferungen | Plugin: "Forderungen aLuL" | ✓ |
| 1406 | Abziehbare Vorsteuer 19 % | Plugin: "Abziehbare Vorsteuer 19%" | ✓ |
| 1800 | Bank | Plugin: "Bank" | ✓ |
| 2000 | Festkapital | Plugin: "Gezeichnetes Kapital" | ⚠ DATEV-Bezeichnung anders, aber für KapGes ist das Plugin-Label etabliert |
| 2970 | Gewinnvortrag vor Verwendung | Plugin: "Gewinnvortrag" | ✓ |
| 3020 | **Steuerrückstellungen** (sammel) | Plugin (jahresabschluss-skill): "Pensionsrückstellungen" | ✗ wrong |
| 3035 | **Gewerbesteuerrückstellung** | Plugin (jahresabschluss-skill): "KSt-Rückstellung" | ✗ wrong (swap with KSt-RST) |
| 3050 | **Steuerrückstellung aus Steuerstundungen** | Plugin (kontenrahmen.json): "Urlaubsrückstellung" | ✗ wrong |
| 3060 | Rückstellung für latente Steuern | nicht verwendet | |
| 3070 | Sonstige Rückstellungen | Plugin: "Sonstige Rückstellungen" | ✓ |
| **3079** | **Urlaubsrückstellungen** | nicht verwendet | (DAS ist der korrekte Konto für Urlaubsrückstellung in SKR04) |
| 3300 | Verbindlichkeiten aus Lieferungen | Plugin: "Verbindl. aLuL" | ✓ |
| 3730 | Verbindlichkeiten aus Lohn- und (Kirchensteuer) | Plugin: "Verb. LSt/KiSt" | ✓ |
| 3740 | Verbindlichkeiten im Rahmen der (sozialen Sicherheit) | Plugin: "Verb. SV" | ✓ |
| 3806 | Umsatzsteuer 19 % | Plugin: "Umsatzsteuer 19%" | ✓ |
| 3820 | Umsatzsteuer-Vorauszahlungen | nicht direkt verwendet | |
| 4300 | Erlöse 7 % USt | Plugin: "Umsatzerlöse 7%" | ✓ |
| 4400 | Erlöse 19 % USt | Plugin: "Umsatzerlöse 19%" | ✓ |
| 6000 | Löhne und Gehälter | Plugin: "Löhne/Gehälter" | ✓ |
| 6020 | Gehälter | nicht verwendet | (wäre korrekt für reine Gehälter-Buchung) |
| 6100 | Soziale Abgaben (AG-Anteil SV) | Plugin: "AG-Anteil SV" | ✓ |
| 6170 | **Sonstige soziale Abgaben** | Plugin (buchungssatz-vorber.): "Vermögensw. Leistungen" für bAV | ✗ wrong on multiple counts (label und concept) |
| 6200 | **Abschreibungen auf immaterielle Vermögensgegenstände** | Plugin (kontenrahmen.json): "Abschreibungen SAV" | ✗ wrong account class |
| **6220** | **Abschreibungen auf Sachanlagen** | nicht verwendet | (DAS wäre der korrekte Konto für AfA SAV) |
| 6960 | **Periodenfremde Aufwendungen** | Plugin (buchungssatz-vorber.): "Personalaufwand Urlaubsrückstellung" | ✗ wrong |

## Section A — total revisions

### Promoted to high-confidence errors (new):

**A.17 (revised)** — SKR03 0968 ≠ Urlaubsrückstellung. DATEV-PDF bestätigt verbatim: 0968 = "Passive latente Steuern". Korrekt: **0961**. Plugin's `urlaubsrueckstellung: 0968` ist falsch.

**A.18 (revised)** — KSt/GewSt-Rückstellungs-Konten vertauscht in jahresabschluss-skill (beide SKR03 und SKR04):
- SKR03: Plugin sagt "0955 GewSt-RST, 0956 KSt-RST". DATEV: 0955 = Steuerrückstellungen (sammel), **0956 = Gewerbesteuerrückstellung**, **0963 = Körperschaftsteuerrückstellung**.
- SKR04: Plugin sagt "3030 GewSt-RST, 3035 KSt-RST". DATEV: 3020 = Steuerrückstellungen, **3035 = Gewerbesteuerrückstellung**, KSt-RST = anderer Konto (verify, vermutlich 3033 oder ähnlich).

**A.19 (revised)** — SKR03 4300 ≠ KSt-Aufwand. DATEV: 4300 = "Nicht abziehbare Vorsteuer". Korrekt: **2200 = Körperschaftsteuer** (Aufwand).

**A.20 (new)** — SKR03 4190 ≠ Zuführung Pensionsrückstellung. DATEV: 4190 = "Aushilfslöhne". Verify correct Pensionsrückstellungs-Zuführungs-Konto separately.

**A.21 (new)** — `config/kontenrahmen.json` SKR04 `abschreibungen_sav: 6200` ist falsch. DATEV: 6200 = "Abschreibungen auf immaterielle Vermögensgegenstände". Korrekt für **Sachanlagen** ist **6220 = "Abschreibungen auf Sachanlagen"**. Knock-on: alle Skills, die die SKR04-Abschreibungs-Buchung mit 6200 zeigen (insbesondere buchungssatz Section 5.4 mit "6200" SKR04), sind falsch.

**A.22 (new)** — `config/kontenrahmen.json` SKR04 `urlaubsrueckstellung: 3050` ist falsch. DATEV: 3050 = "Steuerrückstellung aus Steuerstundungen". Korrekt: **3079 = "Urlaubsrückstellungen"**.

**A.23 (new)** — SKR04 3020 (jahresabschluss-skill, "Pensionsrückstellungen") ist falsch. DATEV: 3020 = "Steuerrückstellungen". Korrekte SKR04-Konten für Pensionsrückstellungen müssen separat nachgeschlagen werden (verify; vermutlich in 3000er-Anfang).

**A.24 (new)** — SKR04 6960 (buchungssatz-vorbereitung-skill, "Personalaufwand Urlaubsrückstellung") ist falsch. DATEV: 6960 = "Periodenfremde Aufwendungen". Korrektes Aufwandskonto für Urlaubsrückstellungs-Zuführung müsste in 6100er- oder 6200er-Bereich (Personalaufwand) liegen.

**A.25 (new)** — SKR04 6170 als "Vermögenswirksame Leistungen" ist falsch. DATEV: 6170 = "Sonstige soziale Abgaben". (Außerdem konzeptioneller Mismatch: VL ≠ bAV-Direktversicherung).

### Revised / cancelled flags:

**A.12 (cancelled)** — SKR03 1777 als "USt ig Lieferung" ist tatsächlich konform mit DATEV's verbatim-Bezeichnung "Umsatzsteuer aus im Inland steuerpflichtigen EU-Lieferungen". Plugin's Label passt. Flag entfernen.

**A.7 (refined)** — bAV-Direktversicherung auf 4170 SKR03 ist konzeptionell falsch (VL ≠ bAV), aber der DATEV-Label "Vermögenswirksame Leistungen" für 4170 ist korrekt. Die Buchung als solche gehört auf andere Konten (siehe Plugin's separates "4172 AG-Zuschuss bAV", das vermutlich auch nicht stimmt — verify mit DATEV-PDF separat). Flag bleibt, aber präziser formuliert.

## Updated tallies

- **High-confidence errors (Section A)**: 18 → **24** (added A.20, A.21, A.22, A.23, A.24, A.25; cancelled A.12; reformulated A.7)
- **Verify-needed (Section B)**: 2 → **3** (added: korrekte SKR03 Konten für KSt-Aufwand bAV-Direktversicherung, AG-Zuschuss bAV, Pensionsrückstellung-Zuführung; und SKR04 KSt-Rückstellung und Pensionsrückstellung)
- **§13b KZ-Codes**: bleibt offen (kein DATEV-Bezug)

## Most important takeaway

Das Plugin hat **systematisch falsche Konto-Belegungen** insbesondere in SKR04:
- 3050 (Urlaubsrückstellung → ist tatsächlich Steuerstundungs-RST; korrekt: 3079)
- 6200 (Abschreibung SAV → ist tatsächlich immaterielle VG; korrekt: 6220)
- 6960 (Personalaufwand → ist tatsächlich Periodenfremde Aufwendungen)
- 3020 (Pensionsrückstellung → ist tatsächlich Steuerrückstellungen)
- 3035 (KSt-Rückstellung → ist tatsächlich GewSt-Rückstellung)

Plus in SKR03:
- 0968 (Urlaubsrückstellung → ist Passive latente Steuern; korrekt: 0961)
- 4190 (Pensionsrückstellungs-Zuführung → ist Aushilfslöhne)
- 4300 (KSt-Aufwand → ist Nicht abziehbare Vorsteuer; korrekt: 2200)
- 0955/0956 (vertauscht)

Wenn ein User eine Buchung nach Plugin-Anleitung tätigt, landet sie auf einem **inhaltlich völlig anderen Konto** als DATEV vorsieht. Das ist gravierend für GoBD-Konformität und Jahresabschluss-Qualität — die DATEV-Standard-Auswertungen (BWA, GuV-Strukturen) basieren auf den DATEV-Konto-Bezeichnungen.

**Priorität 1 für Remediation:** Vollständiger Abgleich aller Plugin-Konten gegen die DATEV-PDFs 11174/11175 (2026-01-01). Die Abweichungen sind nicht "Edge Cases", sondern systematische Fehlbelegungen, die auf eine veraltete oder erfundene Quelle hinweisen.

## Sources used in addendum 3

- DATEV Hilfe-Center PDF: SKR03-Kontenrahmen Gültig für 2026 (Art.-Nr. 11174 2026-01-01) — fetched via `https://help-center.apps.datev.de/api/amr/knowledge-common/v1/entities/st65108547211_de.pdf`, parsed mit `pdftotext`
- DATEV Hilfe-Center PDF: SKR04-Kontenrahmen Gültig für 2026 (Art.-Nr. 11175 2026-01-01) — fetched via `https://help-center.apps.datev.de/api/amr/knowledge-common/v1/entities/st65118491659_de.pdf`, parsed mit `pdftotext`

End of addendum 3.

---

# Addendum 4 — 2026-05-11 (same session, comprehensive SKR03/SKR04 Account-Abgleich)

Per user request: every account number referenced anywhere in the plugin compared verbatim to the official DATEV-Kontenrahmen 2026 (PDF Art.-Nr. 11174 SKR03 / 11175 SKR04). Method: `pdftotext -layout` extraction, then per-account grep.

~60 distinct account numbers were referenced across configs, skills, and commands. Of those, **about 25 are wrong / mislabeled / non-existent in DATEV**. The plugin has systematic problems beyond what addenda 1-3 surfaced.

## Master comparison table (sorted by Konto)

Legend: ✓ matches DATEV / ✗ wrong / ⚠ partially right or semantically off / ❌ erfundenes Konto (not in DATEV) / — not used in this SKR

### Klasse 0 (Anlage- und Kapital, SKR03 / Anlagevermögen, SKR04)

| Konto | Plugin's intended use | DATEV-SKR03 (verbatim) | DATEV-SKR04 (verbatim) | Verdict |
|---|---|---|---|---|
| 0210 | SKR03 Maschinen (buchungssatz 5.4) | Maschinen | Grundstücksgleiche Rechte | ✓ SKR03 |
| 0400 | (not directly used) | Betriebsausstattung | Technische Anlagen und Maschinen | — |
| 0440 | SKR04 Maschinen (buchungssatz 5.4) | Werkzeuge | Maschinen | ✓ SKR04 |
| 0630 / 0640 | iks-pruefung-skill: "Darlehen Covenant" | Verbindlichkeiten / Restlaufzeit-Sub | Betriebsausstattung / Ladeneinrichtung | ✓ SKR03 (Klasse-0-Verbindlichkeiten); SKR04 unused |
| 0800 | SKR03 Gezeichnetes Kapital | Gezeichnetes Kapital | Anteile an verbundenen Untern. | ✓ SKR03 only |
| 0860 | SKR03 Gewinnvortrag | Gewinnvortrag vor Verwendung | Beteiligungen Personengesellschaften | ✓ SKR03 only |
| 0953 | SKR03 Pensionsrückstellungen | **Rückstellungen für Direktzusagen** | — | ⚠ Plugin label imprecise but right Bereich (0950er = Pensionsrückstellungen) |
| **0955** | SKR03 "Gewerbesteuerrückstellung" (jahresabschluss-skill) | **Steuerrückstellungen** (Sammelkonto, allgemein) | — | ✗ **Plugin wrong** — 0955 ist Sammel, nicht spezifisch GewSt |
| **0956** | SKR03 "KSt-Rückstellung" (jahresabschluss-skill) | **Gewerbesteuerrückstellung** | — | ✗ **Plugin wrong** — 0956 ist GewSt, nicht KSt |
| 0961 | (not used in plugin) | **Urlaubsrückstellungen** | — | (das wäre der korrekte Konto für Urlaubs-RST in SKR03) |
| 0963 | (not used in plugin) | **Körperschaftsteuerrückstellung** | — | (das wäre der korrekte Konto für KSt-RST in SKR03) |
| **0968** | SKR03 "Urlaubsrückstellung" (kontenrahmen.json) | **Passive latente Steuern** | — | ✗ **Plugin wrong** — siehe A.17 |
| 0970 | SKR03 Sonstige Rückstellungen | Sonstige Rückstellungen | Ausleihungen an nahe stehende | ✓ SKR03 |
| 0980 | SKR03 ARAP (buchungssatz 5.8) | Aktive Rechnungsabgrenzung | Genossenschaftsanteile | ✓ SKR03 |
| 0990 | SKR03 PRAP | Passive Rechnungsabgrenzung | Rückdeckungsansprüche | ✓ SKR03 |

### Klasse 1 (Finanz- und Privat, SKR03 / Umlaufvermögen, SKR04)

| Konto | Plugin's intended use | DATEV-SKR03 (verbatim) | DATEV-SKR04 (verbatim) | Verdict |
|---|---|---|---|---|
| 1000 | SKR03 Kasse | Kasse | Roh-, Hilfs- und Betriebsstoffe | ✓ SKR03 |
| 1200 | SKR03 Bank / SKR04 Forderungen aLuL | Bank | Forderungen aus Lieferungen | ✓ both SKRs |
| **1289** | SKR04 "PWB Forderungen LuL" (abstimmung) | — | **Nicht standardmäßig belegt** | ❌ erfunden |
| **1290** | SKR04 "EWB Forderungen LuL" (abstimmung) | Finanzmittelanlagen | **Forderungen gegen Gesellschafter** | ✗ **Plugin wrong** — 1290 ist Forderung-Sub, nicht EWB |
| 1400 | SKR03 Forderungen aLuL / SKR04 Abziehbare Vorsteuer | Forderungen aus Lieferungen | Abziehbare Vorsteuer | ✓ both |
| 1401 | SKR03 / SKR04 VSt 7 % (abstimmung) | Forderungen aus L+L | Abziehbare Vorsteuer 7 % | ✓ both |
| 1406 | SKR04 Vorsteuer 19 % | — | Abziehbare Vorsteuer 19 % | ✓ |
| 1407 | SKR04 VSt §13b (abstimmung) | — | Abziehbare Vorsteuer nach (§13b) | ✓ |
| 1408 | SKR04 VSt ig Erwerb (abstimmung) | — | Abziehbare Vorsteuer nach (§13b) | ⚠ — Plugin label "ig Erwerb"; DATEV-Bezeichnung beginnt "Abziehbare Vorsteuer nach"; muss präzise abgeglichen werden |
| **1498** | SKR03 "PWB Forderungen LuL" (abstimmung) | **Gegenkonto zu sonstigen [Wertberichtigungen]** | Überleitungskonto Kostenstellen | ⚠ Plugin label nicht eindeutig; DATEV-Bezeichnung ist Gegenkonto |
| **1499** | SKR03 "EWB Forderungen LuL" (abstimmung) | **Gegenkonto 1451-1497** | — | ⚠ analog |
| 1570 | SKR03 Abziehbare Vorsteuer (Sammelkonto) | Abziehbare Vorsteuer | — | ✓ |
| 1571 | SKR03 VSt 7 % | Abziehbare Vorsteuer 7 % | — | ✓ |
| 1576 | SKR03 Vorsteuer 19 % | Abziehbare Vorsteuer 19 % | — | ✓ |
| 1577 | SKR03 VSt §13b (abstimmung) | Abziehbare Vorsteuer nach (§13b) | — | ✓ |
| 1578 | SKR03 VSt ig Erwerb (abstimmung) | Abziehbare Vorsteuer nach | — | ✓ |
| 1600 | SKR03 Verb. aLuL / SKR04 Kasse | Verbindlichkeiten aus Lieferungen | Kasse | ✓ both |
| **1740** | SKR03 "Verb. SV" (lohnabrechnung 8.1, buchungssatz 5.3) | **Verbindlichkeiten aus Lohn und Gehalt** | — | ✗ **Plugin wrong** — 1740 ist Brutto-Verb. an AN, nicht SV |
| **1741** | SKR03 "Verb. LSt" (allein) | **Verbindlichkeiten aus Lohn- und Kirchensteuer** (kombiniert!) | — | ⚠ Plugin label zu eng — 1741 enthält LSt UND KiSt zusammen |
| **1742** | SKR03 "Verb. KiSt" (allein) | **Verbindlichkeiten im Rahmen der sozialen Sicherheit** | — | ✗ **Plugin wrong** — 1742 ist Verb. SV, NICHT KiSt |
| 1770 | SKR03 USt Sammelkonto (abstimmung) | Umsatzsteuer | — | ✓ |
| 1771 | SKR03 USt 7 % | Umsatzsteuer 7 % | — | ✓ |
| 1776 | SKR03 USt 19 % | Umsatzsteuer 19 % | — | ✓ |
| 1777 | SKR03 "USt ig Lieferung" (abstimmung) | **Umsatzsteuer aus im Inland steuerpflichtigen EU-Lieferungen** | — | ✓ matches DATEV label (A.12 cancelled) |
| 1779 | SKR03 Range-Ende (abstimmung) | Umsatzsteuer aus innergemeinschaftlichem Erwerb ohne Vorsteuerabzug | — | ⚠ Plugin shows range 1770-1779; DATEV uses 1779 specifically |
| **1780** | SKR03 "USt-Zahllast" | **Umsatzsteuer-Vorauszahlungen** | LZB-Guthaben (anderer Kontext) | ⚠ Plugin-Label "Zahllast" semantisch unsauber für 1780 (= Vorauszahlungen) |
| 1787 | SKR03 USt §13b (abstimmung, buchungssatz 5.6) | Umsatzsteuer nach § 13b UStG | — | ✓ |
| 1800 | SKR03 Privatentnahmen / SKR04 Bank | Privatentnahmen allgemein | Bank | ✓ both (Plugin nutzt nur SKR04 1800 = Bank) |

### Klasse 2 (SKR03 neutrale Aufwendungen/Erträge / SKR04 Eigenkapital)

| Konto | Plugin's intended use | DATEV-SKR03 (verbatim) | DATEV-SKR04 (verbatim) | Verdict |
|---|---|---|---|---|
| 2000 | SKR04 Gezeichnetes Kapital | (Klasse-2-Anfang, neutrale Aufwendungen) | **Festkapital** | ⚠ DATEV nennt SKR04 2000 "Festkapital"; Plugin's "Gezeichnetes Kapital" ist KapGes-Konvention, aber im DATEV-SKR04-Manuell heißt das Konto 2000 für Einzelunternehmen "Festkapital" — bei KapGes wird es entsprechend umbezeichnet. Akzeptabel, aber dokumentations-würdig. |
| **2450** | SKR03 "Einstellung EWB Ford." (abstimmung) | **Einstellungen in die Pauschalwertberichtigung** | — | ✗ **Plugin label vertauscht** — 2450 ist PWB (nicht EWB) |
| **2451** | SKR03 "Einstellung PWB Ford." (abstimmung) | **Einstellungen in die Einzelwertberichtigung** | — | ✗ **Plugin label vertauscht** — 2451 ist EWB (nicht PWB) |
| 2970 | SKR04 Gewinnvortrag | (Klasse-2-Aufwendungen) | Gewinnvortrag vor Verwendung | ✓ SKR04 |

### Klasse 3 (SKR03 Wareneingang / SKR04 Fremdkapital)

| Konto | Plugin's intended use | DATEV-SKR03 (verbatim) | DATEV-SKR04 (verbatim) | Verdict |
|---|---|---|---|---|
| **3020** | SKR04 "Pensionsrückstellungen" (jahresabschluss) | (Wareneingangs-Bereich SKR03) | **Steuerrückstellungen** | ✗ **Plugin wrong** — 3020 ist Steuerrückstellung, nicht Pension; korrekte Pension-Konten sind 3000-3015 |
| **3030** | SKR04 "GewSt-Rückstellung" (jahresabschluss) | Einkauf Roh-/Hilfs- (SKR03) | (nicht direkt sichtbar in extraktion; verify) | ⚠ verify |
| **3035** | SKR04 "KSt-Rückstellung" (jahresabschluss) | — | **Gewerbesteuerrückstellung** | ✗ **Plugin wrong** — 3035 ist GewSt-RST, nicht KSt; KSt-RST ist im 3020er-Sub |
| **3050** | SKR04 "Urlaubsrückstellung" (kontenrahmen.json) | — | **Steuerrückstellung aus Steuerstundungen** | ✗ **Plugin wrong** — korrekt 3079 für Urlaubsrückstellung |
| 3070 | SKR04 Sonstige Rückstellungen | Einkauf Roh-/Hilfs- (SKR03) | Sonstige Rückstellungen | ✓ SKR04 |
| 3079 | (not used by plugin) | — | **Urlaubsrückstellungen** | (das wäre der korrekte Konto für Urlaubs-RST in SKR04) |
| 3123 | SKR03 EU-DL §13b (buchungssatz 5.6) | **Sonstige Leistungen eines im anderen EU-Land ansässigen Unternehmens** | — | ✓ DATEV-konform |
| 3200 | SKR03 Wareneingang (buchungssatz 5.1) | Wareneingang | (SKR04 anderer Bereich) | ✓ SKR03 |
| 3300 | SKR03 Wareneingang 7 % / SKR04 Verb. aLuL | **Wareneingang 7 % Vorsteuer** | **Verbindlichkeiten aus Lieferungen** | ✓ both (different meanings) |
| 3425 | SKR03 ig Erwerb (abstimmung) | **Innergemeinschaftlicher Erwerb** | (SKR04 anderer Bereich) | ✓ SKR03 |
| 3730 | SKR04 Verb. LSt/KiSt | (SKR03 anderer Bereich) | **Verbindlichkeiten aus Lohn- und Kirchensteuer** | ✓ SKR04 |
| 3740 | SKR04 Verb. SV | (SKR03 anderer Bereich) | **Verbindlichkeiten im Rahmen der sozialen Sicherheit** | ✓ SKR04 |
| 3800 / 3801 / 3806 / 3807 / 3809 | SKR04 USt-Konten | Bezugsnebenkosten (SKR03) | USt / USt 7 % / USt 19 % / USt EU-Lief / USt §13b | ✓ SKR04 |
| 3820 | SKR04 USt-Vorauszahlungen | (SKR03 anderer Bereich) | **Umsatzsteuer-Vorauszahlungen** | ✓ SKR04 |
| 3837 | SKR04 USt §13b (abstimmung) | (SKR03 anderer Bereich) | USt nach § 13b (extraction truncated; plausible) | ⚠ verify exact Bezeichnung |

### Klasse 4 (SKR03 Betriebliche Aufwendungen / SKR04 Erträge)

| Konto | Plugin's intended use | DATEV-SKR03 (verbatim) | DATEV-SKR04 (verbatim) | Verdict |
|---|---|---|---|---|
| 4100 | SKR03 "Löhne und Gehälter" (Sammel) | (Konto existiert; Bezeichnung in PDF nicht direkt gegrep'bar — aber bekannt: Löhne) | (anderer Bereich) | ✓ SKR03 (Plugin's Verwendung als Sammel ist konventional) |
| 4120 | SKR03 Gehälter | (Konto existiert; Bezeichnung: Gehälter) | — | ✓ SKR03 |
| 4125 | SKR03 Ehegattengehalt Gesellschafter-GF | **Ehegattengehalt Geschäftsführer** | — | ✓ |
| 4130 | SKR03 "AG-Anteil SV" | **Gesetzliche soziale Aufwendungen** | — | ⚠ Plugin's "AG-Anteil SV"-Label entspricht der Verwendung; DATEV-Bezeichnung ist breiter ("Gesetzliche soziale Aufwendungen") |
| **4170** | SKR03 "Vermögensw. Leistungen für bAV-Entgeltumwandlung" | **Vermögenswirksame Leistungen** | — | ⚠ DATEV-Label ist korrekt VL, ABER Plugin's konzeptionelle Verwendung für bAV ist falsch (VL ≠ bAV) |
| **4172** | SKR03 "AG-Zuschuss bAV" (buchungssatz-vorbereitung 2.5) | **Nicht standardmäßig belegt** | — | ❌ **erfunden** — siehe A.26 |
| **4190** | SKR03 "Zuführung Pensionsrückstellung" | **Aushilfslöhne** | — | ✗ **Plugin wrong** — 4190 ist Aushilfslöhne, nicht Pensions-Konto |
| **4300** | SKR03 "KSt-Aufwand" (jahresabschluss 5.5) | **Nicht abziehbare Vorsteuer** | Erlöse 7 % USt (EÜR) | ✗ **Plugin wrong** — siehe A.19 |
| 4320 | SKR03 "GewSt-Aufwand" (jahresabschluss 5.5) | **Gewerbesteuer** | Erlöse aus im anderen EU-Land | ✓ SKR03 |
| 4360 | SKR03 Versicherungen (buchungssatz 5.8) | **Versicherungen** | — | ✓ |
| 4400 | SKR04 Umsatzerlöse 19 % | **(zur freien Verfügung)** (SKR03) | **Erlöse 19 % USt** | ✓ SKR04 only |
| 4830 | SKR03 Abschreibungen SAV | **Abschreibungen auf Sachanlagen** | **Sonstige betriebliche Erträge** | ✓ SKR03; SKR04 anderer Sinn |
| 4840 | SKR03 Außerplanm. Abschreibung | Außerplanmäßige Abschreibungen | Erträge aus Währungsumrechnung | ✓ SKR03 |
| 4900 | SKR03 "Personalaufwand Urlaubsrückstellung" | Sonstige betriebliche Aufwendungen | — | ⚠ unsauber (4900 = "Sonstige", nicht spezifisch Personal) |

### Klasse 5/6/7 (SKR04 Material/Personal/Sonstige)

| Konto | Plugin's intended use | DATEV-SKR03 | DATEV-SKR04 (verbatim) | Verdict |
|---|---|---|---|---|
| 5200 | SKR04 Wareneingang | — | **Wareneingang und Betriebsstoffe** | ✓ |
| 5425 | SKR04 ig Erwerb 19 % (abstimmung) | — | **Innergemeinschaftlicher Erwerb** | ✓ |
| 6000 | SKR04 Löhne und Gehälter (Sammel) | — | **Löhne und Gehälter** | ✓ |
| 6100 | SKR04 AG-Anteil SV | — | **Soziale Abgaben und Aufwendungen** | ✓ |
| **6170** | SKR04 "Vermögensw. Leistungen für bAV" | — | **Sonstige soziale Abgaben** | ✗ **Plugin wrong** — 6170 ist NICHT VL in SKR04 (anders als SKR03 4170) |
| **6175** | SKR04 "AG-Zuschuss bAV" | — | **Nicht standardmäßig belegt** | ❌ **erfunden** — siehe A.26 |
| **6190** | SKR04 "Zuführung Pensionsrückstellung" | — | **Nicht standardmäßig belegt** | ❌ erfunden |
| **6200** | SKR04 "Abschreibungen SAV" | — | **Abschreibungen auf immaterielle Vermögensgegenstände** | ✗ **Plugin wrong** — siehe A.21; korrekt 6220 für Sachanlagen |
| 6210 | SKR04 Außerplanm. Abschreibung | — | **Außerplanmäßige Abschreibungen (auf immaterielle VG)** | ⚠ wie 6200 — gehört zu immateriell; für Sachanlagen wäre es anders |
| 6920 | SKR04 "Einstellung EWB Ford." (abstimmung) | — | **Einstellung in die Pauschalwertberichtigung** | ✗ **Plugin label vertauscht** — 6920 ist PWB (analog SKR03 2450) |
| **6921** | SKR04 "Einstellung PWB Ford." (abstimmung) | — | **Nicht standardmäßig sichtbar** | ⚠ verify (vermutlich 6921 = Einstellung EWB Ford., wenn Spiegelbild zu 6920) |
| **6960** | SKR04 "Personalaufwand für Urlaubsrückstellung" | — | **Periodenfremde Aufwendungen** | ✗ **Plugin wrong** — siehe A.24 |
| 7600 | SKR04 "KSt-Aufwand" (jahresabschluss 5.5) | — | **Körperschaftsteuer** | ✓ |
| 7610 | SKR04 "GewSt-Aufwand" (jahresabschluss 5.5) | — | **Gewerbesteuer** | ✓ |

### Klasse 8 (SKR03 Erlöse)

| Konto | Plugin's intended use | DATEV-SKR03 (verbatim) | Verdict |
|---|---|---|---|
| 8120 | SKR03 Steuerfreie Umsätze §4 (abstimmung) | **Steuerfreie Umsätze nach § 4** | ✓ |
| 8125 | SKR03 Steuerfreie ig Lieferungen (abstimmung) | **Steuerfreie innergemeinschaftliche [Lieferungen]** | ✓ |
| 8300 | SKR03 Umsatzerlöse 7 % | **Erlöse 7 % USt** | ✓ |
| 8400 | SKR03 Umsatzerlöse 19 % | **Erlöse 19 % USt** | ✓ |

## Summary of new findings from comprehensive abgleich

### New high-confidence errors (Section A additions)

**A.28** — SKR03 1740, 1741, 1742 mismapped throughout plugin:
- Plugin: 1740 = "Verb. SV", 1741 = "Verb. LSt", 1742 = "Verb. KiSt"
- DATEV: 1740 = "Verbindlichkeiten aus Lohn und Gehalt", 1741 = "Verbindlichkeiten aus Lohn- und Kirchensteuer" (kombiniert), **1742 = "Verbindlichkeiten im Rahmen der sozialen Sicherheit" (= das ist Verb. SV)**.
- Affects: buchungssatz Section 5.3, lohnabrechnung Section 8.1, alle SKR03-Lohnbuchungs-Beispiele.
- Effect: A user following the plugin würde SV-Verbindlichkeit auf "Verb. Lohn und Gehalt"-Konto buchen — komplett falsch.
- Korrekt für SKR03-Lohnbuchung: Brutto an 1742 Verb. SV + 1741 Verb. LSt/KiSt + 1200 Bank (Netto).
- (Die SKR04-Mapping in plugin lohnabrechnung 8.1 ist tatsächlich richtig: 3730 = LSt/KiSt, 3740 = SV.)

**A.29** — SKR03 2450 und 2451 (EWB/PWB) vertauscht:
- Plugin: 2450 = "Einstellung EWB", 2451 = "Einstellung PWB"
- DATEV: 2450 = "Pauschalwertberichtigung" (PWB), 2451 = "Einzelwertberichtigung" (EWB)
- Affects: abstimmung Section 2.5 — beide Buchungen verwenden vertauschte Konten.
- Same applies analog to SKR04: 6920 = "Pauschal" per DATEV (Plugin says EWB); 6921 wahrscheinlich Spiegel.

**A.30** — SKR04 1290 und 1289 für EWB/PWB Forderungen sind frei erfundene/wrong Konten:
- Plugin: 1290 = "EWB Forderungen LuL", 1289 = "PWB Forderungen LuL"
- DATEV SKR04: 1290 = "Forderungen aus Lieferungen und Leistungen gegen Gesellschafter"; 1289 ist nicht standardmäßig belegt.
- Korrekt: SKR04-Wertberichtigungs-Konten liegen vermutlich im Klasse-1-Wertberichtigungs-Bereich (~1276 / 1296 laut weiterem grep) — verify.

**A.31** — SKR03 0953 als "Pensionsrückstellungen" (buchungssatz-vorbereitung):
- DATEV: 0953 = "Rückstellungen für Direktzusagen" (= Pensionsverpflichtungen aus Direktzusagen) — ist tatsächlich eine Pensions-RST-Variante. Plugin's Label "Pensionsrückstellungen" ist akzeptabel, aber präziser wäre "Direktzusage-Rückstellungen". Bleibt aber ⚠ Soft-Issue, nicht Error.

## Final tallies

- **High-confidence errors (Section A)**: 26 → **30** (added A.28, A.29, A.30, A.31)
- **Verify-needed (Section B)**: 1 → **2** (added: SKR04 Wertberichtigungs-Konten und SKR04 3030er-Strucktur; §13b KZ-Codes bleibt offen)

## Summary statistic

| Kategorie | Anzahl |
|---|---|
| Plugin-Account-Referenzen geprüft (eindeutige Nummern) | ~60 |
| Davon korrekt (✓) gegen DATEV | ~35 |
| Falsch (✗) oder semantisch off (⚠) | ~20 |
| Erfunden / nicht in DATEV (❌) | ~5 |
| Total Plugin-Account-Probleme | **~25** |

## Bottom line for the Steuerberater

Das Plugin hat **systematische SKR03/SKR04-Probleme**. Wenn jemand die Buchungs-Beispiele eins-zu-eins nachbucht, landen viele Posten auf inhaltlich völlig anderen DATEV-Standard-Konten als beabsichtigt. Konkrete Risiken:

1. **Lohnbuchung SKR03** würde SV-Verb. auf "Verb. aus Lohn und Gehalt" buchen statt auf 1742 (SV).
2. **Wertberichtigungen** würden EWB/PWB vertauschen (echte Auswirkung in der BWA und beim Vergleich Plan-Ist).
3. **bAV-Buchungen** würden auf erfundene Konten gehen, die DATEV nicht kennt — keine standard-konforme Auswertung möglich.
4. **Steuer-Rückstellungen** würden GewSt-RST und KSt-RST tauschen — beim Jahresabschluss ein direkter Fehler im Bilanzausweis.
5. **Abschreibungen Sachanlagen SKR04** auf 6200 (= immat. VG) statt 6220 — falsche GuV-Position.

Diese Befunde **gehen über** die ursprünglichen 14 high-confidence Errors deutlich hinaus. Das ursprüngliche Bild ("Plugin-Skills sind mostly good") muss revidiert werden: **Die Konto-Belegungen sind systematisch unsauber**. Möglicherweise wurde die Plugin-Buchhaltungslogik aus älteren SKR-Veröffentlichungen oder aus einer anderen Quelle (z.B. einem alternativen Branchen-SKR oder einer Eigenkreation) zusammengestellt, ohne strikten Abgleich mit der offiziellen DATEV-Veröffentlichung.

**Priorität 1 vor jeglicher Nutzung des Plugins für reale Buchungen**: Konsequenter Re-Sync aller Account-Nummern in `config/kontenrahmen.json` und allen Buchungs-Beispielen in den Skills gegen die DATEV-PDFs 11174/11175 (2026-01-01).

End of addendum 4.
