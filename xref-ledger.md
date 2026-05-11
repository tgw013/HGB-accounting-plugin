# Cross-Reference Ledger — HGB Plugin

Working document for the accounting-content first-pass review.
Section A is the "canonical" side (what the configs define). Section B is
filled in as each skill / command is reviewed (what they reference).
Section C lists §-citations to verify in the cross-check pass.

---

## A. Canonical values defined by the configs

### A.1 — Rates (from `config/rates-2026.json`)

| ID / key | Value | Source path |
|---|---|---|
| Mindestlohn 2026 | 13.90 €/h | `mindestlohn.stundensatz_2026` |
| Mindestlohn 2027 | 14.60 €/h | `mindestlohn.stundensatz_ab_2027` |
| Vollzeit-Brutto 40h | 2,410 € | `mindestlohn.vollzeit_40h_brutto_monatlich` (rounded; exact = 2,408.67) |
| Minijob-Grenze | 603 €/mo | `beitragsbemessungsgrenzen.geringfuegigkeitsgrenze_monatlich` |
| Midijob-Obergrenze | 2,000 € | `beitragsbemessungsgrenzen.uebergangsbereich_bis` |
| BBG KV/PV | 69,750 / yr (5,812.50 / mo) | `beitragsbemessungsgrenzen.kv_pv_*` |
| BBG RV/AV | 101,400 / yr (8,450 / mo) | `beitragsbemessungsgrenzen.rv_av_*` |
| JAEG (PKV-Wechsel) | 77,400 / yr | `beitragsbemessungsgrenzen.versicherungspflichtgrenze_jaehrlich` |
| KV gesamt (allg. + Zusatz) | 17.5 % (8.75 / 8.75) | `sozialversicherung.krankenversicherung.*` |
| RV | 18.6 % (9.3 / 9.3) | `sozialversicherung.rentenversicherung.*` |
| AV | 2.6 % (1.3 / 1.3) | `sozialversicherung.arbeitslosenversicherung.*` |
| PV mit Kind | 3.6 % (1.8 / 1.8; Sachsen AG 1.3) | `sozialversicherung.pflegeversicherung.*` |
| PV kinderlos | 4.2 % (Zuschlag 0.6) | `sozialversicherung.pflegeversicherung.*` |
| PV-Abschläge | -0.25 pro Kind ab 2. (max 4) | `sozialversicherung.pflegeversicherung.abschlag_*` |
| U1 (typisch) | 1.0 – 3.5 % (bei ≤30 MA) | `umlagen.u1_*` |
| U2 (typisch) | 0.44 % | `umlagen.u2_typisch` |
| U3 Insolvenz | 0.15 % | `umlagen.insolvenzgeldumlage_u3` |
| bAV SV-frei | 4 % BBG-RV = 4,056 € | `betriebliche_altersvorsorge.entgeltumwandlung_max_sv_frei_2026` |
| bAV steuerfrei | 8 % BBG-RV = 8,112 € | `betriebliche_altersvorsorge.steuerfreier_hoechstbetrag_2026` |
| bAV AG-Zuschuss Pflicht | 15 % | `betriebliche_altersvorsorge.arbeitgeber_zuschuss_pflicht_prozent` |
| USt Normalsatz | 19 % | `umsatzsteuer.normalsatz` |
| USt ermäßigt | 7 % | `umsatzsteuer.ermaessigter_satz` |
| USt VA monatlich ab | > 9,000 € Vorjahr | `umsatzsteuer.voranmeldung_schwelle_monatlich` |
| USt VA viertelj. ab | 2,001 – 9,000 € Vorjahr | `umsatzsteuer.voranmeldung_schwelle_vierteljaehrlich_min` |
| USt Befreiung jährlich | ≤ 2,000 € Vorjahr | `umsatzsteuer.befreiung_schwelle` |
| Kleinunternehmer Vorjahr | 25,000 € | `umsatzsteuer.kleinunternehmer_grenze_vorjahr` |
| Kleinunternehmer laufend | 100,000 € | `umsatzsteuer.kleinunternehmer_grenze_laufend` |
| OSS-Schwelle | 10,000 € | `umsatzsteuer.oss_schwelle` |
| ZM Schwelle (Waren, viertelj.) | 50,000 € | `umsatzsteuer.zm_schwelle_vierteljaehrlich` |
| KSt 2025–2027 | 15 % | `koerperschaftsteuer.steuersatz_2025_2027` |
| KSt 2028–2032+ (?) | 14→10 % | `koerperschaftsteuer.steuersatz_2028..ab_2032` **(verify: enacted?)** |
| Soli auf KSt | 5.5 % (effektiv 0.825 %) | `koerperschaftsteuer.solidaritaetszuschlag_*` |
| KSt-Vorauszahlung | 10.03/06/09/12 | `koerperschaftsteuer.vorauszahlung_termine` |
| GewSt Messzahl | 3.5 % | `gewerbesteuer.steuermesszahl` |
| GewSt Mindesthebesatz | 200 % | `gewerbesteuer.mindest_hebesatz` |
| GewSt Hebesätze (Ref) | BE 410 / M 490 / HH 470 / F 460 | `gewerbesteuer.hebesaetze_referenz.*` |
| GewSt-Vorauszahlung | 15.02/05/08/11 | `gewerbesteuer.vorauszahlung_termine` |
| GewSt Freibetrag PersGes | 24,500 € | `gewerbesteuer.freibetrag_personengesellschaften` |
| Urlaubsanspruch (6-Tage-W.) | 24 Werktage | `urlaub.minimum_werktage_6_tage_woche` |
| Urlaubsanspruch (5-Tage-W.) | 20 Arbeitstage | `urlaub.minimum_arbeitstage_5_tage_woche` |
| HGB Kleinst-KapGes | BS ≤ 450k / UE ≤ 900k / AN ≤ 10 | `hgb_groessenklassen.kleinst` |
| HGB Klein-KapGes | BS ≤ 7.5M / UE ≤ 15M / AN ≤ 50 | `hgb_groessenklassen.klein` |
| HGB Mittelgroß | BS ≤ 25M / UE ≤ 50M / AN ≤ 250 | `hgb_groessenklassen.mittelgross` |
| Aufbewahrung JA/Bilanzen | 10 Jahre | `aufbewahrungsfristen.jahresabschluesse_buchungsbelege` **(label conflates two categories)** |
| Aufbewahrung Buchungsbelege | 8 Jahre (ab 2025) | `aufbewahrungsfristen.buchungsbelege_ab_2025` |
| Aufbewahrung Handelsbriefe | 6 Jahre | `aufbewahrungsfristen.handelsbriefe` |

### A.2 — Account numbers (from `config/kontenrahmen.json`)

#### SKR03

| Bezeichnung | Konto | Klasse |
|---|---|---|
| Kasse | 1000 | 1 (Finanz- und Privatkonten) |
| Bank | 1200 | 1 |
| Forderungen aLuL | 1400 | 1 |
| Abziehbare Vorsteuer (Sammel) | 1570 | 1 |
| Abziehbare Vorsteuer 19 % | 1576 | 1 |
| Verbindlichkeiten aLuL | 1600 | 1 |
| Umsatzsteuer 19 % | 1776 | 1 |
| Umsatzsteuer-Zahllast/Vorauszahlung | 1780 | 1 |
| Löhne und Gehälter (sammel) | 4100 | 4 (Betriebliche Aufwendungen) |
| AG-Anteil zur Sozialversicherung | 4130 | 4 |
| Abschreibungen auf Sachanlagen | 4830 | 4 |
| Umsatzerlöse 7 % USt | 8300 | 8 (Erlöskonten) |
| Umsatzerlöse 19 % USt | 8400 | 8 |
| Gezeichnetes Kapital | 0800 | 0 (Anlage- und Kapitalkonten) |
| Gewinnvortrag (vor Verwendung) | 0860 | 0 |
| Urlaubsrückstellung | 0968 | 0 **(verify: 0968 is typically NOT Urlaubsverpflichtungen in SKR03)** |
| Sonstige Rückstellungen | 0970 | 0 |
| Debitoren-Range | 10000–69999 (5-stellig) | — |
| Kreditoren-Range | 70000–99999 (5-stellig) | — |

#### SKR04

| Bezeichnung | Konto | Klasse |
|---|---|---|
| Forderungen aLuL | 1200 | 1 (Umlaufvermögen) |
| Abziehbare Vorsteuer 19 % | 1406 | 1 |
| Kasse | 1600 | 1 |
| Bank | 1800 | 1 |
| Gezeichnetes Kapital | 2000 | 2 (Eigenkapital) |
| Gewinnvortrag (vor Verwendung) | 2970 | 2 |
| Urlaubsrückstellung | 3050 | 3 (Fremdkapital) **(verify)** |
| Sonstige Rückstellungen | 3070 | 3 |
| Verbindlichkeiten aLuL | 3300 | 3 |
| Umsatzsteuer 19 % | 3806 | 3 |
| Umsatzerlöse 7 % USt | 4300 | 4 (Betriebliche Erträge) |
| Umsatzerlöse 19 % USt | 4400 | 4 |
| Löhne und Gehälter (sammel) | 6000 | 6 (Betriebliche Aufw. — Personal etc.) |
| AG-Anteil zur Sozialversicherung | 6100 | 6 |
| Abschreibungen auf Sachanlagen | 6200 | 6 |
| Debitoren-Range | 10000–69999 (5-stellig) | — |
| Kreditoren-Range | 70000–99999 (5-stellig) | — |

---

## B. References (filled in as skills / commands are reviewed)

> Format per file: list of {account-numbers, rate-keys, other-skill-deps, §-citations} referenced.
> An xref check at the end resolves each against Section A and §-Catalog (Section C).

### skills/buchungssatz/SKILL.md
- Cites § / norms: § 252 HGB (impliziert), § 13b UStG, § 4 UStG, § 4b UStG, § 19 UStG, GoB
- Uses SKR03 accounts: 0210, 0980, 1200, 1400, 1576, 1577, 1600, 1740, 1741, 1776, 1780, 1787, 3123, 4100, 4130, 4360, 4830, 8400
- Uses SKR04 accounts: 0440, 1200, 1406, 1800, 3300, 3730, 3740, 3806, 4400, 5200, 6000, 6100, 6200
- Uses rates: 19% (normal), 7% (ermäßigt), 25.000 € Kleinunternehmer-Vorjahr
- Depends on: buchungssatz-vorbereitung
- DATEV export claims: UTF-8 (verify), Semikolon, TTMM, Komma-Dezimal, S/H, Buchungstext max 60 Z. (but input says 120 Z. — internal contradiction)

### skills/buchungssatz-vorbereitung/SKILL.md
- Cites § / norms: § 238 HGB, § 249 Abs.1 HGB, § 252 Abs.1 Nr.4 HGB, § 253 Abs.2 S.2 HGB, § 253 Abs.3 HGB, § 253 Abs.3 S.4 HGB, § 253 Abs.4 HGB, § 257 Abs.4 HGB, § 266 HGB, § 275 HGB, § 446 BGB, § 4 Abs.3 EStG, § 6 Abs.2 EStG (implizit GWG), § 7 Abs.1 EStG, § 7 Abs.1 S.3 EStG, § 7 Abs.1 S.6 EStG, § 7 Abs.2 EStG, § 7g Abs.5 EStG, § 11 EStG, § 3 Nr.63 EStG, § 18 EStG, § 141 AO, § 241a HGB, § 1a BetrAVG, § 1a Abs.1a BetrAVG, § 1 Abs.1 Nr.9 SvEV, § 3 BUrlG, DRS 35
- Uses SKR03 accounts: 0953, 0968, 0970, 1200, 1740, 4100 (impliziert), 4130, 4170, 4172, 4190, 4830, 4840, 4900
- Uses SKR04 accounts: 1800, 3020, 3050, 3070, 3740, 6100, 6170, 6175, 6190, 6200, 6210, 6960
- Uses rates: KV/RV/AV/PV AG-Anteile, Sachsen-Sonderregel, BBG KV/PV/RV/AV/JAEG/Minijob/Midijob, U1/U2/U3, bAV 4%/8% BBG-RV (4.056/8.112 €), 15 % AG-Zuschuss-Pflicht, Mindesturlaub 24/20, 800.000 € / 80.000 € § 141 AO Schwellen, 800 € GWG (§6 Abs.2 EStG)
- Cross-skill: buchungssatz (consumed)

### skills/ust-voranmeldung/SKILL.md
- Cites § / norms: § 18 Abs. 2 UStG (S. 1/2/3/4), §§ 46–48 UStDV, § 47 UStDV (SVZ), § 19 Abs. 1+2 UStG, § 4 Nr. 1b UStG, § 6a UStG (impliziert), § 17a UStDV, § 13b Abs. 1, Abs. 2 Nr. 4/8/10 UStG, § 1a UStG, § 14 UStG, § 20 UStG, § 240 AO, § 152 AO, § 108 Abs. 3 AO, § 11 Abs. 2 EStG
- KZ-Codes used: 41, 46, 47, 61, 66, 67, 81, 83, 86, 89, 39
- Uses SKR03 accounts: 1570, 1576, 1776, 1780, 8300, 8400
- Uses SKR04 accounts: 1406, 3806, 4300, 4400
- Uses rates: 19 % / 7 %, Schwellen 9.000 / 2.001 / 2.000 €, KU 25.000 / 100.000 €, OSS 10.000 €, ZM 50.000 €
- Forms: USt 1 A (VA), USt 1 H (Dauerfristverlängerung)

### skills/lohnabrechnung/SKILL.md
- Cites § / norms: § 38b EStG, § 39e EStG, § 41a EStG, § 41b EStG, § 3b EStG, § 3 Nr. 15 EStG, § 8 Abs. 2 S. 11 EStG, § 40 Abs. 2 Nr. 3 EStG (impliziert), § 1a BetrAVG, § 21 MiLoG, § 23a SGB IV, § 23 SGB IV (impliziert), § 154 SGB IX (nicht behandelt aber relevant), § 1 Abs. 1 Nr. 1 SvEV (impliziert für SV-Freiheit), § 108 Abs. 3 AO
- Uses SKR03 accounts: 1200, 1740, 1741, 1742, 4100, 4130
- Uses SKR04 accounts: 1800, 3730, 3740, 6000, 6100
- Uses rates: KV/RV/AV/PV (vollständige Sätze inkl. Sachsen + Kinderabschläge), Mindestlohn 13,90 / 14,60, Minijob 603 €, Midijob 603,01–2.000 €, Minijob-Pauschalen (KV 13 % / RV 15 % / LSt 2 %), Umlagen, bAV 4 % / 8 % BBG-RV, KiSt 8 % / 9 %, SolZ 5,5 %, LSt-Anmelde-Schwellen 5.000 / 1.080 €, Sachbezugswert Mahlzeit "ca. 4,23 €" (verify), SolZ-Freigrenze 18.130 / 36.260 (verify), Steuerklassen I–VI
- Cross-skill conflict: Section 8.2 Lohnbuchung shows Verb. SV = 1.903,50 € (AG + AN) — KORREKT; widerspricht buchungssatz Section 5.3 wo nur AG gebucht wird (951,75) und AN-SV im Netto fehlt
- Cross-skill consistency: AG-Zuschuss bAV "Neuverträge 2019, Altverträge 2022" — korrekt; buchungssatz-vorbereitung verkürzt fälschlich auf "seit 2019"

### skills/abstimmung/SKILL.md
- Cites § / norms: § 13b UStG, § 15 UStG, § 18 UStG, § 152 AO, § 233a AO (0,15 %/Mon. ✓), § 238 HGB, § 239 HGB, § 370 AO, § 378 AO
- KZ-Codes: 81, 86, 35, 36, 66, 89, 46, 73, 84 (some inconsistent with ust-voranmeldung)
- Uses SKR03 accounts: 1200, 1400, 1498, 1499, 1570, 1571, 1576, 1577, 1578, 1600, 1770, 1771, 1776, 1777, 1780, 1787, 2450, 2451, 8300, 8400, 8120, 8125, 3425
- Uses SKR04 accounts: 1200, 1289, 1290, 1400, 1401, 1406, 1407, 1408, 1800, 3300, 3800, 3801, 3806, 3807, 3820, 3837, 4300, 4400, 4120, 4125, 5425, 6920, 6921
- Toleranzen: USt-Verprobung 1,00 € / 0,01 %; Bank/Deb/Kred/IC 0,00 €

### skills/abweichungsanalyse/SKILL.md
- Cites § / norms: IDW PS 250, IDW PS 240 (Performance Materiality implizit), ISA 450 (Clearly Trivial implizit), HGB-Größenklassen, IDW (Controlling-Standards)
- Uses SKR03 accounts: 3xxx, 4100, 4830, 8300, 8400
- Uses SKR04 accounts: 4300, 4400, 5xxx, 6000, 6200
- Uses rates: KSt 15 % + Soli 0,825 % → effektiv 15,825 %; GewSt 3,5 % Messzahl; HGB-Größenklassen für Berichtsskalierung
- Wesentlichkeitsschwellen: EBT 3-5 %, Umsatz 0,5-1,0 %, Bilanzsumme 1-2 %, EK 2-5 %; Performance 50-75 %; Clearly Trivial 5 %
- Eskalationsschwellen: < 8 T€ / 8-120 T€ / 120-500 T€ / > 500 T€ / > 50 % EBT

### skills/compliance/SKILL.md
- Cites § / norms: §§ 145-147 AO, §§ 238, 239, 257 HGB, § 257 Abs. 4 HGB (alt + n.F.), § 14b UStG, § 41 EStG, § 91 Abs. 2 AktG, § 161 AktG, § 80 BetrVG, § 17 HinSchG, § 11 HinSchG, § 40 HinSchG, HinSchG 31.05.2023 / EU-RL 2019/1937, DCGK 28.04.2022, § 161 AktG, GoBD BMF-Schreiben 28.11.2019 + Update 14.07.2025 (verify), § 264 Abs. 1 HGB, § 325 HGB, § 5b EStG, § 149 Abs. 3 AO, § 18a UStG (ZM 25. FM), § 19 GewStG, § 31 KStG, § 41a Abs. 1 EStG, § 23 Abs. 1 SGB IV, § 28a SGB IV, § 146 Abs. 1 AO, § 162 AO, DSGVO Art. 5, 28, 30, 35
- E-Rechnung-Pflicht: 01.01.2025 Empfangspflicht, 01.01.2027 Versandpflicht > 800 T€ Vorjahresumsatz ✓
- Aufbewahrungsfristen-Darstellung KORREKT mit Trennung 10 J. Altbelege / 8 J. ab 2025 — besser als rates-2026
- Uses SKR03 accounts: 1576, 1776, 1780, 4100, 4130, 0970
- Uses SKR04 accounts: 1406, 3806, 6000, 6100, 3070

### skills/iks-pruefung/SKILL.md
- Cites § / norms: § 289 Abs. 4 HGB, § 315 Abs. 4 HGB, § 91 Abs. 2 AktG, § 107 Abs. 3 S. 2 AktG, § 43 GmbHG, § 161 AktG, § 14 UStG, IDW PS 261 (n.F.), IDW PS 530, ISA 265, ISA 530, COSO (impliziert), DCGK 28.04.2022
- Uses SKR03 accounts: 0xxx, 0630, 0640, 1200, 1400, 1576, 1600, 1776, 3xxx, 4100, 4130, 4830, 8300, 8400
- IKS-Komponenten: COSO/IDW PS 261 fünf Komponenten ✓
- Mängel-Hierarchie: Mangel / Bedeutsamer Mangel / Wesentliche Schwäche (ISA 265) ✓
- Cross-skill: referenziert compliance, monatsabschluss, lohnabrechnung Werte

### skills/monatsabschluss/SKILL.md
- Cites § / norms: § 240 HGB, § 249 HGB, § 250 HGB, § 253 HGB, § 264 Abs. 1 HGB, § 267 HGB, § 267a HGB, § 274 HGB, § 316 HGB, § 325 HGB, § 264a HGB, § 175 AktG, § 18 UStG, § 19 GewStG, § 31 KStG, § 41a EStG, § 4 UStG, § 13b UStG, § 6 Abs. 2 EStG (GWG 800 €), § 6 Abs. 2a EStG (Pool 250-1.000), § 5b EStG, § 149 Abs. 2 + Abs. 3 AO, § 141 AO, § 108 Abs. 3 AO, § 46 UStDV, IDW PS 450
- Uses SKR03 accounts: 1000, 1200, 1400, 1576, 1600, 1776, 1780, 4100, 4130, 4830, 0968, 0970
- Uses SKR04 accounts: 1600, 1800, 1200, 1406, 3300, 3806, 6000, 6100, 6200, 3050, 3070
- Internal §264-Frist (line 236): "6 Mon. kleine" ✓ — aber widerspricht jahresabschluss line 593
- StB-Frist (line 245): "31.07. übernächstes Jahr" — FALSCH (richtige Frist 28.02.)

### skills/jahresabschluss/SKILL.md
- Cites § / norms: § 241a HGB, §§ 246-274a HGB, § 252 HGB (alle 6 Grundsätze), § 264 Abs. 1 HGB, § 266 HGB (Bilanz), § 267 HGB / § 267a HGB, § 268 Abs. 8 HGB, § 274 HGB, § 274a HGB, § 275 Abs. 2 + Abs. 3 HGB, § 264a HGB (MoPeG), § 4 Abs. 3 EStG, § 6 EStG, § 7 EStG, § 7g EStG, § 11 EStG, § 18 EStG, § 23 KStG, § 35 EStG, § 2 GewStG, § 7 GewStG, § 11 Abs. 1 Nr. 1 GewStG (Freibetrag 24.500), § 15 Abs. 3 Nr. 1 EStG (Abfärbetheorie), § 141 AO, § 149 Abs. 2 + 3 AO, § 709 BGB n.F., § 6a EStG, § 5 Abs. 4a EStG, § 5b EStG, MoPeG, BilMoG
- Uses SKR03 accounts: 0800, 0860, 0955, 0956, 4300 (KSt-Aufwand), 4320 (GewSt-Aufwand)
- Uses SKR04 accounts: 2000, 2970, 3030, 3035, 7600, 7610
- KSt-Stufen-Berechnung 2025-2032 alle math konsistent ✓
- GewSt-Hebesatz-Berechnungen alle math konsistent ✓
- §264-Frist (line 593): "3 Mon. kleine, 6 Mon. große/mittelgr." — VERTAUSCHT, FALSCH
- StB-Frist (line 595): "31.07. Zweitfolgejahr" — FALSCH (richtige Frist 28.02.)

### skills/ebilanz/SKILL.md
- Cites § / norms: § 5b EStG, § 4 Abs. 1 EStG, § 5 EStG, § 5a EStG, § 4 Abs. 3 EStG (EÜR ausgeschlossen), § 141 AO, § 267 HGB, § 6 EStG, § 4 Abs. 5 EStG, § 7g EStG
- HGB-Taxonomie 6.9 für GJ 2026 — VERIFY (möglicherweise veraltet; aktuelle Versionen 6.8 für 2024, 6.9 für 2025; 2026 wahrscheinlich 6.10 oder 7.0)
- StB-Frist (line 247): "28.02.2028" ✓ KORREKT (widerspricht monatsabschluss + jahresabschluss + compliance)
- Aufbewahrungsfristen-Tabelle line 350-352 wiederholt den inkonsistenten Doppeleintrag aus rates-2026
- SKR03/SKR04 → Taxonomie-Mapping konsistent mit kontenrahmen.json
- Unverdichtete Kontennachweise ab FJ 2025 ✓
- XBRL 2.1 + Dimensions 1.0 ✓

### commands/*.md (10 files)

**Systemic finding**: Command files are noticeably more outdated than the paired skills. Multiple commands use pre-Wachstumschancengesetz / pre-Bürokratieentlastungsgesetz-IV (= pre-2025) values labeled as "2026". Pattern suggests commands were drafted earlier than skills and not refreshed.

#### commands/lohnabrechnung.md — **SEVERELY OUTDATED, multiple high-confidence errors**
- Line 24: Mindestlohn "12,82 €/Std" — **WRONG**, that's 2025; 2026 = 13,90 €
- Line 33-36: BBG-Tabelle alle 2024-Werte:
  - KV/PV "5.175 €/Mon" → 2026 = 5.812,50 €
  - RV/AV "7.550 €/Mon" → 2026 = 8.450 €
- Line 34: PV "3,4 %" → 2026 = 3,6 %
- Line 48-49: bAV-Grenze "302 €/Mon" → 2026 = 338 € (SV-frei) bzw. 676 € (Steuer-frei)
- Line 111-112: Minijob "556 €/Mon" → 2026 = 603 €; Midijob "556,01–2.000" → 603,01–2.000
- Line 31-36: KV-Zusatzbeitrag-Rate fehlt komplett (nur "Zusatzbeitrag" generisch)
- Märzklausel-Hinweis fehlt
- AG-Zuschuss bAV-Datum nicht differenziert (Neuverträge vs. Altverträge)

#### commands/ust-voranmeldung.md — **SEVERELY OUTDATED, pre-Wachstumschancengesetz Schwellen**
- Line 17-19: Schwellen "7.500 / 1.000 €" → seit 2025 "9.000 / 2.000 €" (Wachstumschancengesetz)
- Line 23: Kleinunternehmer "22.000 / 50.000 €" → seit 2025 "25.000 / 100.000 €" (Wachstumschancengesetz)
- Line 59: KZ 46/47-Tabelle bündelt zwei Felder ohne Differenzierung
- Line 91: Rundungs-Verweis "§20 Satz 1 UStG i.V.m. §1 Abs. 1 Satz 1 KStG analog" — **nonsensical citation**, §20 UStG ist Istversteuerung, hat nichts mit Rundung zu tun

#### commands/compliance.md — outdated Aufbewahrungsfristen + falsches HinSchG-Bußgeld
- Line 44: "Buchungsbelege 10 Jahre" — **propagiert den alten Wert ohne 2025-Split** (Skill und Config wissen es korrekt: 8 J. ab 2025)
- Line 47: "Rechnungen 10 Jahre §14b UStG" — gleiche Problematik (8 J. ab 2025)
- Line 92: "HinSchG ... Bußgeldrahmen bis 50.000 EUR" — **WRONG**. Tatsächlich: 20.000 € für mangelhafte Meldestelle, **500.000 €** für Behinderung / Repressalien / Vertraulichkeitsbruch (§ 40 HinSchG). Die 50.000-€-Zahl entspricht keinem realen Bußgeldsatz.
- Line 36: "Ab 250 MA: erweiterte Anforderungen" — verwechselt Inkrafttretens-Stichtag (02.07.2023 vs. 17.12.2023) mit "erweiterten Anforderungen"; die Anforderungen sind gleich, nur das Datum unterschiedlich

#### commands/ebilanz.md — Taxonomie veraltet, sloppy XBRL-Beispiel
- Line 21: "Kerntaxonomie (6.8 oder aktuell)" — 6.8 ist GJ 2024; Skill sagt 6.9 für GJ 2026 (Skill möglicherweise auch veraltet — siehe Round 6)
- Line 30-32: XBRL-Mapping-Beispiel: 1200 Forderungen und 1800 Bank beide auf `bs.ass.currAss.worksEquip` gemappt — **wrong/illustrative-only IDs** (worksEquip = Werksausstattung passt weder zu Forderungen noch zu Bank)
- Line 87: "28./29. Februar des übernächsten Jahres" — die "/29." berücksichtigt Schaltjahre, ist aber unpräzise (gesetzliche Frist ist 28.02.; verschiebt sich nur via §108 AO bei Wochenende/Feiertag)

#### commands/iks-pruefung.md — mischt IDW-PS-261-Komponenten und operative Bereiche
- Line 20: "9 Kontrollbereiche bewerten ... nach IDW PS 261" — **konzeptionell falsch**: IDW PS 261 hat **5 Komponenten** (Kontrollumfeld, Risikobeurteilung, Kontrollaktivitäten, Information/Kommunikation, Überwachung). Items 6-9 (IT, Einkauf, Zahlungsverkehr, Personalwesen) sind operative Audit-Schwerpunkte, NICHT IDW-PS-261-Komponenten. Das Command-File suggeriert irreführend die Zugehörigkeit zu IDW PS 261.
- Skill macht die Trennung sauber (5 Komponenten getrennt von 9 operativen Bereichen)

#### commands/jahresabschluss.md — **korrekt, widerspricht aber dem fehlerhaften Skill**
- Line 63: "3 Monate (große KapGes), 6 Monate (kleine KapGes)" — **KORREKT** gemäß § 264 Abs. 1 HGB
- Damit wird das Command der "richtige" Side im Cross-Skill-Konflikt — das paired SKILL (jahresabschluss line 591-595) hat es vertauscht
- (Agent 2 hatte das Command fälschlich als "reversed" eingestuft; Agent hat den Sachverhalt verwirrt)

#### commands/buchungssatz.md, commands/abstimmung.md, commands/abweichungsanalyse.md, commands/monatsabschluss.md
- Diese 4 Commands sind im Wesentlichen schlanke Workflow-Wrapper ohne substanzielle Inhalte über die Skills hinaus
- Keine high-confidence Fehler gefunden
- monatsabschluss line 263 (cross-ref von Agent): 6-Monats-Frist für "kleine KapGes" — korrekt

---

## C. §-Citations to verify (filled in from skills / commands)

| § | Plugin's claim | Verified? |
|---|---|---|
| (pending) | | |

---

## D. Issues collected during per-file pass

### From `config/rates-2026.json`
- **Inconsistent grouping** — `aufbewahrungsfristen.jahresabschluesse_buchungsbelege: 10` conflates JA/Bilanzen (still 10 J.) with Buchungsbelege (8 J. seit 2025).
- **Rounding nit** — `vollzeit_40h_brutto_monatlich: 2410` is rounded; exact 13.90 × 40 × 52 / 12 = 2,408.67.
- **Verify** — KSt-Senkungspfad 2028→2032 (14→10 %): enacted in §23 KStG, or political plan?
- **Verify** — Sozialversicherungs-Rechengrößen 2026 (BBG KV/PV 69,750; BBG RV/AV 101,400; JAEG 77,400) against published Rechengrößen-VO 2026.
- **Verify** — Pflegeversicherung 2026 (3.6 / 4.2) — unchanged from 2025?
- **Verify** — Insolvenzgeldumlage U3 (0.15 %) for 2026.
- **Verify** — Durchschnittlicher KV-Zusatzbeitrag (2.9 %) for 2026.
- **Verify** — GewSt-Hebesätze (BE 410 / M 490 / HH 470 / F 460) for 2026.
- **Coverage gaps** — Reisekosten / Sachbezugswerte / GWG-Grenzen / Sammelposten / AfA-Tabellen / Lohnsteuer-Eckwerte / Grundfreibetrag / Bewirtungspauschalen / Lohnunterlagen-Aufbewahrungsfrist.

### From `config/kontenrahmen.json`
- **High-confidence error: SKR03 Klasse 2 label wrong.** File says "Abgrenzungskonten (Rückstellungen, ARAP/PRAP, latente Steuern)". Actual SKR03 Klasse 2 is **"Sonstige Erträge und Aufwendungen / neutrale Aufwendungen und Erträge"** (Zinsen, Steuern v. Einkommen, außerordentliche, periodenfremde). Rückstellungen, ARAP/PRAP, latente Steuern are in **Klasse 0** in SKR03. Could mislead a Buchungssatz-skill into wrong klasse-based logic.
- **Asymmetry SKR03 vs SKR04 häufige_konten.** SKR03 lists 4 USt-accounts (Vorsteuer 19, USt 19, Sammelkonto Vorsteuer, USt-Zahllast); SKR04 lists only 2 (Vorsteuer 19, USt 19). SKR04 should also include the analogs of `abziehbare_vorsteuer` (Sammel) and `umsatzsteuer_zahllast` (in SKR04: 1400 und 3820 üblich).
- **Likely-wrong account: Urlaubsrückstellung.** SKR03 says 0968, SKR04 says 3050. Standard SKR03 has Urlaubsverpflichtungen typically as 0974 (or sub-account of 0970); SKR04 analog 3060/3070-Bereich. Verify against current DATEV-SKR03/SKR04-Veröffentlichung.
- **Label imprecise: `umsatzsteuer_zahllast: 1780`.** In SKR03, 1780 is "Umsatzsteuer-Vorauszahlungen" (working account for VA); the year-end Zahllast is usually 1789. Label and account number are mismatched in intent.
- **Lumping issue: `loehne_gehaelter`.** Single key pointing to one account (4100 SKR03 / 6000 SKR04) conflates Löhne (Stundenlöhner) and Gehälter (Angestellte), which are two distinct DATEV accounts. A Lohnabrechnung-skill consuming this key will misbook one group. Should split into `loehne` (4100/6000) and `gehaelter` (4120/6020).
- **Coverage gaps in häufige_konten:**
  - Reverse-Charge / innerg. Erwerb USt-Konten (SKR03: 1577 / 1787; SKR04: analog)
  - OSS-USt-Konten (rates-2026 erwähnt OSS-Schwelle)
  - Erhaltene / Geleistete Anzahlungen
  - KSt / GewSt / Soli Zahlungs- und Rückstellungs-Konten (rates-2026 gibt diese Sätze vor)
  - Skonto-Konten (Aufwand und Ertrag, je nach USt-Satz)
  - Privatentnahmen/-einlagen (nur falls Plugin auch PersGes/EU abdeckt — bisher KapGes-Fokus erkennbar)
