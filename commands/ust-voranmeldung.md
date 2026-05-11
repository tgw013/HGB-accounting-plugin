---
description: "USt-Voranmeldung vorbereiten (monatlich/vierteljährlich) für ELSTER."
---

# /ust-voranmeldung

Erstellt die Umsatzsteuer-Voranmeldung (USt-VA) fuer die elektronische Uebermittlung via ELSTER.

## Referenzierter Skill

- `ust-voranmeldung`

## Workflow

1. **Voranmeldungszeitraum bestimmen** — Klaere (Schwellen ab 2025 gemaess Wachstumschancengesetz):
   - Monatliche oder quartalsweise Abgabe (abhaengig von Vorjahres-Zahllast)
   - Vorjahres-Zahllast > **9.000 EUR**: monatlich
   - Vorjahres-Zahllast **2.001–9.000 EUR**: quartalsweise
   - Vorjahres-Zahllast **<= 2.000 EUR**: Befreiung moeglich (nur Jahreserklaerung)
   - Dauerfristverlaengerung vorhanden? (1 Monat Aufschub; bei monatlicher Abgabe 1/11 Sondervorauszahlung)
   - Existenzgruender: keine Sonder-Pflicht zur monatlichen VA mehr (Aussetzung BEG III bis VZ 2026)

2. **Kleinunternehmerregelung pruefen** — Pruefe §19 UStG (ab 2025 Wachstumschancengesetz):
   - Vorjahresumsatz **<= 25.000 EUR** und laufendes Jahr voraussichtlich **<= 100.000 EUR**
   - Bei Ueberschreitung der 100.000-EUR-Grenze im laufenden Jahr: **ab dem ueberschreitenden Umsatz** sofortige Pflicht zur Regelbesteuerung
   - Falls Kleinunternehmer: keine USt-VA erforderlich, entsprechenden Hinweis geben
   - Falls Option zur Regelbesteuerung: normal fortfahren (5-Jahres-Bindung gemaess §19 Abs. 2 UStG)

3. **Umsatzsteuer- und Vorsteuer-Daten erfassen** — Sammle:
   - Steuerpflichtige Umsaetze (19 %, 7 %)
   - Steuerfreie Umsaetze (§4 UStG)
   - Innergemeinschaftliche Lieferungen (§4 Nr. 1b UStG)
   - Innergemeinschaftliche Erwerbe (§1a UStG)
   - Reverse-Charge-Umsaetze (§13b UStG)
   - Vorsteuer aus Eingangsrechnungen
   - Vorsteuer aus innergemeinschaftlichem Erwerb
   - Vorsteuer nach §13b UStG

4. **Zahllast berechnen** —
   ```
   Umsatzsteuer (Ausgangsrechnungen)       xxx.xxx,xx EUR
   + USt auf ig. Erwerbe                     x.xxx,xx EUR
   + USt nach §13b                           x.xxx,xx EUR
   ─────────────────────────────────────────────────────
   = Summe USt                             xxx.xxx,xx EUR
   - Vorsteuer (Eingangsrechnungen)         xx.xxx,xx EUR
   - VSt auf ig. Erwerbe                     x.xxx,xx EUR
   - VSt nach §13b                           x.xxx,xx EUR
   ─────────────────────────────────────────────────────
   = Zahllast (positiv) / Erstattung (negativ)   x.xxx,xx EUR
   ```

5. **Auf Kennzahlen (KZ) mappen** — Ordne die Betraege den ELSTER-Kennzahlen zu:

   | KZ | Bezeichnung | Bemessungsgrundlage | Steuer |
   |----|-------------|---------------------|--------|
   | 81 | Stpfl. Umsaetze 19 % | KZ 81 | KZ — |
   | 86 | Stpfl. Umsaetze 7 % | KZ 86 | KZ — |
   | 41 | ig. Lieferungen | KZ 41 | — |
   | 89 | ig. Erwerbe 19 % | KZ 89 | KZ — |
   | 46 | Leistungen §13b | KZ 46 | KZ 47 |
   | 66 | Vorsteuer | — | KZ 66 |
   | 61 | VSt ig. Erwerbe | — | KZ 61 |
   | 67 | VSt §13b | — | KZ 67 |
   | 83 | Zahllast/Erstattung | — | KZ 83 |

6. **ELSTER-Daten vorbereiten** — Erstelle eine uebersichtliche Zuordnung aller Werte zu KZ-Feldern, bereit fuer die Eingabe in ELSTER oder Uebergabe an die Steuerberatung.

7. **Zur Abgabe praesentieren** — Zeige die vollstaendige USt-VA mit allen Positionen und pruefe:
   - Stimmt KZ 83 mit der berechneten Zahllast ueberein?
   - Sind alle innergemeinschaftlichen Umsaetze korrekt erfasst?
   - Ist die Frist eingehalten?

## Erwartete Eingaben

- Voranmeldungszeitraum (Monat/Quartal + Jahr)
- Umsatzdaten (steuerpflichtig, steuerfrei, ig. Lieferungen)
- Vorsteuerdaten (Eingangsrechnungen, ig. Erwerbe, §13b)
- Steuernummer, USt-IdNr.

## Erwartete Ausgaben

- Vollstaendige USt-VA mit allen KZ-Feldern
- Berechnung der Zahllast / Erstattung
- ELSTER-faehige Datenzuordnung
- Fristenhinweis

## Hinweise

- Abgabefrist: 10. des Folgemonats (mit Dauerfristverlaengerung: 10. des uebernachsten Monats).
- Sondervorauszahlung bei Dauerfristverlaengerung: 1/11 der Vorjahres-Zahllast.
- Zusammenfassende Meldung (ZM) bei ig. Lieferungen separat pruefen.
- USt-Betraege werden mit Cent-Genauigkeit erfasst und an ELSTER uebermittelt; Rundungs-Differenzen aus Buchhaltung vs. Voranmeldung dürfen 1,00 EUR (Rundungstoleranz) nicht uebersteigen.
