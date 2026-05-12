# Szenario: Büromaterial-Einkauf Inland

**Skill(s):** buchungssatz
**Schwierigkeit:** einfach
**Quelle:** konstruiert

## Input

Rechnung Office Discount AG (DE-Lieferant) vom 12.05.2026 über Büromaterial:
- Netto: 84,03 €
- USt 19%: 15,97 €
- Brutto: 100,00 €
- Bezahlung per Banküberweisung am 14.05.2026
- Mandant: GmbH, SKR04, SOLL-Versteuerung

## Erwarteter Output

```
Buchung 1 (Rechnungs-Eingang 12.05.2026)
6815 Bürobedarf           Soll   84,03 €
1406 Abziehbare Vorsteuer Soll   15,97 €
3300 Verb. aus L+L                       Haben  100,00 €

Buchung 2 (Bezahlung 14.05.2026)
3300 Verb. aus L+L         Soll  100,00 €
1800 Bank                                Haben  100,00 €
```

## Begründung

- Konto **6815** "Bürobedarf" (SKR04) für Sofort-Aufwand (kein Anlagegut)
- **1406** Vorsteuer 19% — abzugsberechtigt nach § 15 Abs. 1 S. 1 Nr. 1 UStG
- **3300** Kreditoren-Sammelkonto — bei Personenkonto eines Kreditors auf 70xxx oder konkretes Kreditorenkonto buchen
- **1800** Bank — bei Bezahlung
- USt-Tatbestand: § 12 Abs. 1 UStG (Regelsatz 19%)

## Stolperfallen

- Wenn Office Discount nicht in EU oder Schweiz sitzt: anderer Sachverhalt (Drittland-Import, EUSt)
- Wenn Netto > 800 € + Charakter Anlagegut (z.B. Stuhl, Drucker): GwG-Prüfung — Aktivierung statt Aufwand (§ 6 Abs. 2 EStG)
- Wenn Kleinbetragsrechnung ≤ 250 € brutto (§ 33 UStDV): vereinfachte Pflichten, aber gleiche Buchung
