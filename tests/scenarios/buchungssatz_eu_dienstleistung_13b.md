# Szenario: EU-Dienstleistung mit § 13b UStG (Reverse Charge)

**Skill(s):** buchungssatz, ust-voranmeldung
**Schwierigkeit:** mittel
**Quelle:** konstruiert (typischer Software-Abo-Fall)

## Input

Rechnung Acme Cloud Ltd. (IE-Lieferant, gültige USt-IdNr. IE9999999X) vom 03.05.2026 über SaaS-Abo Mai 2026:
- Nettobetrag: 1.500,00 €
- USt: 0 € (Lieferant weist Reverse Charge aus: "VAT to be paid by the recipient — Article 196 of Council Directive 2006/112/EC")
- Mandant: GmbH (DE), SKR04, valide DE-USt-IdNr., voll vorsteuerabzugsberechtigt
- Bezahlung per SEPA am 10.05.2026

## Erwarteter Output

```
Buchung 1 (Rechnungs-Eingang 03.05.2026 — § 13b Abs. 1 UStG)
6840 EDV-/Softwarekosten            Soll   1.500,00 €
1407 Abziehbare Vorsteuer § 13b     Soll     285,00 €
3837 USt § 13b 19%                                Haben    285,00 €
3300 Verb. aus L+L                                Haben  1.500,00 €

Buchung 2 (Bezahlung 10.05.2026)
3300 Verb. aus L+L                  Soll   1.500,00 €
1800 Bank                                         Haben  1.500,00 €
```

USt-VA 05/2026:
- KZ **46** (BG § 13b Abs. 1, Z. 30): 1.500,00 €
- KZ **47** (Steuer § 13b Abs. 1, Z. 30):   285,00 €
- KZ **67** (Vorsteuer aus § 13b, Z. 41):  -285,00 €

Saldo aus § 13b: 0 € (voller VSt-Abzug)

## Begründung

- **§ 13b Abs. 1 UStG**: Sonstige Leistung nach § 3a Abs. 2 UStG (B2B-Grundregel: Empfänger-Ort) eines im übrigen Gemeinschaftsgebiet ansässigen Unternehmers → Empfänger schuldet USt
- USt-Schuld 19% × 1.500 € = 285 € auf Konto **3837** (SKR04)
- Korrespondierender Vorsteuer-Abzug auf **1407** nach § 15 Abs. 1 S. 1 Nr. 4 UStG
- Konto **6840** für SaaS-/EDV-Aufwand (alternativ 6815 wenn als allgemeine Bürokosten klassifiziert)
- KZ-Codes 46/47/67 nach BMF-Vordruckmuster USt 1 A 2026 Zeile 30 + Zeile 41

## Stolperfallen

- **USt-IdNr.-Prüfung Pflicht** vor Buchung: qualifizierte Bestätigung über BZSt (BOP) abrufen — sonst Risiko, dass kein § 13b vorliegt
- Bei **nicht-vorsteuerabzugsberechtigtem** Mandant (z.B. Heilberufler, Wohnungsvermieter): KZ 67-Abzug ENTFÄLLT → 285 € Saldo-Belastung
- **Lieferort-Prüfung**: bei B2C oder bei Sonstigen Leistungen § 3a Abs. 3 (z.B. Grundstücksleistungen, kulturelle Leistungen) gilt § 13b NICHT — andere Buchung
- **Zusammenfassende Meldung** § 18a UStG: § 13b-Eingangsleistung selbst nicht meldepflichtig; ig-Erwerbe + ig-Lieferungen schon
- Wenn Lieferant **keine USt-IdNr.** ausweist oder Reverse Charge nicht erkennbar: nachfragen, ggf. anders behandeln
