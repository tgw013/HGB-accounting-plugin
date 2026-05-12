# Szenario: GmbH-Geschäftsführer-Gehalt mit bAV-Entgeltumwandlung

**Skill(s):** lohnabrechnung, buchungssatz
**Schwierigkeit:** mittel
**Quelle:** konstruiert

## Input

GmbH-Alleingesellschafter-Geschäftsführer (beherrschend, SV-frei):
- Bruttogehalt: 8.000 € monatlich
- Steuerklasse III, 1 Kind, ev. Konfession
- bAV-Entgeltumwandlung 250 € monatlich (Direktversicherung)
- AG-Pflichtzuschuss 15% nach § 1a BetrAVG = 37,50 € (zusätzlich)
- 1%-Regelung Firmenwagen: BLP 50.000 € → 500 €/Monat geldwerter Vorteil
- Mandant: GmbH, SKR04

## Erwarteter Output (Brutto-Netto, vereinfacht)

```
Bruttogehalt                         8.000,00 €
+ Sachbezug 1%-Regelung Kfz            500,00 €
─────────────────────────────────────────────
Brutto vor Entgeltumwandlung         8.500,00 €
- bAV-Entgeltumwandlung               -250,00 €
─────────────────────────────────────────────
Steuerpflichtiges Brutto             8.250,00 €

LSt (StKl III, indiv. ELStAM-Tabelle, ca.)    -1.610,00 €
KiSt (~9%)                                       -145,00 €
SolZ                                                0,00 €  (unter Freigrenze StKl III i.d.R.)
SV-AN-Anteile (beherrschender GF: ENTFÄLLT)         0,00 €

Netto (vor Sachbezug-Abzug)                     6.495,00 €
- Sachbezug Kfz (bereits versteuert, kein Cash-Outflow) -500,00 €
─────────────────────────────────────────────
Netto-Auszahlung                                5.995,00 €
```

Buchungen (SKR04, vereinfacht als Sammelbuchung):

```
6027 Geschäftsführer-Gehalt           Soll   8.000,00 €
6020 Geldwerter Vorteil Kfz           Soll     500,00 €   (Aufwand-neutral, ggf. via 4949 Privatentnahme verbucht — je Praxis)
6140 Aufwand bAV                      Soll     287,50 €   (250 € EU + 37,50 € AG-Zuschuss)

3730 Verb. LSt                                    Haben  1.610,00 €
3730 Verb. KiSt                                   Haben    145,00 €
3550 Verb. bAV-Versorgungswerk                    Haben    287,50 €
1800 Bank (Netto-Auszahlung)                      Haben  5.995,00 €
4949 Privatentnahme/Sachbez. Kfz                  Haben    500,00 €  (oder als Korrektur-Konto je Mandanten-Praxis)

Σ Soll = Σ Haben
```

## Begründung

- **6027** SKR04 — eigenes GF-Konto (statt 6020 Gehälter MA) für trennscharfes Reporting
- **6140** bAV-Aufwand für sowohl Entgeltumwandlung als auch 15%-AG-Zuschuss (§ 1a Abs. 1a BetrAVG)
- **Steuerfreiheit Entgeltumwandlung**: § 3 Nr. 63 EStG — bis 8% BBG RV-West (2026 grob ca. 7.700 €/Jahr = 642 €/Monat) steuerfrei; SV-frei bis 4% (§ 1 SvEV) — 250 € liegt darunter
- **SV-Freiheit beherrschender GF**: i.d.R. wenn ≥ 50% Anteile oder Sperrminorität — Statusprüfung Clearingstelle § 7a SGB IV einmalig durchgeführt
- **1%-Regelung Kfz**: § 6 Abs. 1 Nr. 4 S. 2 EStG — geldwerter Vorteil + Fahrten Wohnung-Arbeit ggf. zusätzlich (0,03%/km)
- **SolZ** unter Freigrenze 20.350 € Jahres-LSt bei StKl III i.d.R. nicht angefallen (Achtung: Reform 2021 — bei hoher Jahres-LSt fällt SolZ wieder an)

## Stolperfallen

- **Status-Prüfung GF**: nicht jeder GF ist SV-frei — Clearingstelle-Bescheid einholen, Praxis-Standard
- **Tantieme** separat — als sonstiger Bezug, ggf. progressive LSt nach Fünftelregelung § 34 EStG
- **Kfz Privatnutzung**: Fahrtenbuch-Methode (oft günstiger bei wenig privater Nutzung) prüfen
- **Solz reform 2021**: ≤ 20.350 €/40.700 € Jahres-LSt = befreit; über Milderungszone bis ca. 33.000 € reduziert; darüber voller Satz 5,5%
- **Verdeckte Gewinnausschüttung**: GF-Gehalt im Fremdvergleich angemessen? (BFH-Rechtsprechung) — sonst vGA-Risiko
- **bAV-Versorgungszusage**: rechtliche Gestaltung (Direktversicherung / Pensionskasse / Pensionszusage) hat steuerliche Folgen — vor Vertragsabschluss StB
- **Pensionszusage GF** würde Rückstellung nach § 6a EStG erfordern — ganz anderer Sachverhalt
