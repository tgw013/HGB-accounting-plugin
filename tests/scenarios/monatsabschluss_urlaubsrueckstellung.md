# Szenario: Urlaubsrückstellung-Hochrechnung im Monatsabschluss

**Skill(s):** monatsabschluss, abstimmung
**Schwierigkeit:** mittel
**Quelle:** konstruiert

## Input

Monatsabschluss 04/2026 einer GmbH (SKR04), 8 MA:
- Jahres-Bruttolöhne (geschätzt aus Plan): 480.000 €
- Urlaubsanspruch durchschnittlich: 28 Tage / 220 Arbeitstage pro Jahr ≈ 12,7%
- Resturlaubs-Saldo per 30.04.2026 (aus HR-System): durchschnittlich 18 Tage / MA = 144 Tage gesamt
- Vorjahres-Endbestand 3079 (Urlaubsrückstellungen): 15.300 €

## Erwarteter Output

```
Berechnung Urlaubsrückstellungs-Bedarf 30.04.2026:

Tagesbruttolohn (Durchschnitt) = 480.000 / (8 MA × 220 AT) = 272,73 €/Tag
Soziallasten + Lohnnebenkosten-Faktor ≈ 22% → Vollkosten/Tag = 332,73 €
Rückstellungs-Bedarf = 144 Tage × 332,73 € = 47.913 €

(Konservative Schätzung; tatsächliche RST i.d.R. linear hochgerechnet
zwischen Vorjahr und JA — hier Stichtagsbetrachtung 30.04.)

Aktueller Saldo 3079:            15.300 €
Soll-Saldo 30.04.2026:           47.913 €
Anpassung Soll:                  32.613 €

Buchung:
6072 Aufwendungen für Urlaubsrückstellung    Soll   32.613,00 €
3079 Urlaubsrückstellungen                              Haben   32.613,00 €
```

## Begründung

- **§ 249 Abs. 1 HGB** verpflichtet zur Rückstellung für ungewisse Verbindlichkeiten — Urlaubsanspruch des MA ist erfüllbar gemäß BUrlG, daher rückstellungspflichtig
- **§ 253 Abs. 1 HGB**: Bewertung nach vernünftiger kaufmännischer Beurteilung
- **Konto 3079** (Urlaubsrückstellungen, SKR04) — verifiziert gegen DATEV SKR04 PDF 11175
- **Konto 6072** (Aufwand Urlaubsrückstellung, SKR04 — Personalaufwand sonstige Rückstellungs-Zuführung; alternativ direkt auf 6020 Gehälter, je Praxis)
- Bei MA-Wechsel im Jahr: anteilige Korrektur erforderlich
- Hochrechnung im Monat ist Schätzung — finale Bewertung im Jahresabschluss mit tatsächlichem HR-Bestand
- **Steuerlich** (E-Bilanz): Bewertung folgt § 5 Abs. 1 EStG (Maßgeblichkeit) plus § 6 EStG-Spezialia (keine Sonder-Abschläge wie HGB)

## Stolperfallen

- **Tageslohn-Definition**: brutto oder netto? Praxis: Bruttogehalt + AG-SV (Vollkosten-Ansatz). Reine Brutto-Hochrechnung wäre Unterbewertung
- **Soziallasten-Faktor**: ca. 20–24% je nach AG-SV-Beitragssatz und Pflicht-Umlagen (U1, U2, Insolvenzgeldumlage, BG)
- **Anwartschaften aus dem Vorjahr**: bei Übertrag Urlaub muss alter Tageslohn zugrunde gelegt werden — strenge Praxis. Vereinfacht: aktueller Lohn
- **Steuerlich** Urlaubsrückstellung anerkannt (kein Drohverlust-Verbot greift hier); bei Pensionsrückstellungen wäre § 6a EStG einschlägig
- **Achtung Konto-Verwechslung SKR03**: dort **0961** für Urlaubs-RST, NICHT 0951 (das wäre Saldierungskonto Aktive Latente Steuern bei GmbH); 0956 ist GewSt-RST
- **Tantieme-Rückstellung GF** separat (i.d.R. eigenes Konto): nicht in Urlaubs-RST einrechnen
