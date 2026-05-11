---
description: "Lohnabrechnung prüfen — SV-Beiträge, LSt, bAV, Umlagen."
---

# /lohnabrechnung

Berechnet und prueft die Lohnabrechnung (Gehaltsabrechnung) mit allen Sozialversicherungs- und Steuerabzuegen.

## Referenzierter Skill

- `lohnabrechnung`

## Workflow

1. **Mitarbeiterdaten erfassen** — Sammle die erforderlichen Stamm- und Bewegungsdaten:
   - Name, Steuer-ID, Steuerklasse (I–VI)
   - Konfession (Kirchensteuer: 8 % oder 9 % je nach Bundesland)
   - Bruttogehalt (monatlich)
   - Kinderfreibetraege
   - Sozialversicherungsstatus (pflichtversichert, privat versichert, Minijob)
   - Sonderzahlungen (Weihnachtsgeld, Urlaubsgeld, Boni)

2. **Mindestlohn pruefen** — Stelle sicher, dass der gesetzliche Mindestlohn eingehalten wird:
   - Aktueller Mindestlohn 2026: **13,90 EUR/Stunde** (ab 2027: 14,60 EUR/Std.)
   - Berechnung: Bruttogehalt / Arbeitsstunden >= Mindestlohn
   - Bei Unterschreitung: Warnung ausgeben (Bussgeld bis 500.000 EUR nach § 21 MiLoG)
   - Branchenmindestloehne beachten (z.B. Bau, Pflege, Elektro)
   - Alle Werte aus `config/rates-2026.json` → `mindestlohn`

3. **Sozialversicherungsbeitraege berechnen** — Berechne die SV-Beitraege (AN- und AG-Anteil):

   | Versicherung | Gesamtbeitrag | AN-Anteil | AG-Anteil | BBG 2026 (einheitlich) |
   |-------------|---------------|-----------|-----------|-----------------|
   | Krankenversicherung | 14,6 % + 2,9 % Zusatzbeitrag (Durchschnitt) = 17,5 % | 8,75 % | 8,75 % | 5.812,50 EUR/Monat |
   | Pflegeversicherung | 3,6 % (kinderlos: +0,6 % = 4,2 %) | 1,8 %* | 1,8 % | 5.812,50 EUR/Monat |
   | Rentenversicherung | 18,6 % | 9,3 % | 9,3 % | 8.450,00 EUR/Monat |
   | Arbeitslosenversicherung | 2,6 % | 1,3 % | 1,3 % | 8.450,00 EUR/Monat |

   *Pflegeversicherung: Zuschlag fuer Kinderlose ab 23. Lebensjahr (+0,6 % nur AN); Abschlaege -0,25 Pp je Kind ab 2.-5. Kind. **Sachsen-Sonderregel:** AN 2,3 % / AG 1,3 %.
   Beitragsbemessungsgrenzen (BBG) jaehrlich aktualisieren. Alle Werte aus `config/rates-2026.json`.

4. **Lohnsteuer berechnen** — Ermittle die Lohnsteuer anhand:
   - Steuerklasse und Freibetraege
   - Lohnsteuertarif (progressiv nach §32a EStG)
   - Solidaritaetszuschlag (5,5 % auf LSt, Freigrenze beachten)
   - Kirchensteuer (8 % oder 9 % auf LSt)

5. **Betriebliche Altersvorsorge (bAV) anwenden** — Falls vorhanden:
   - Entgeltumwandlung steuerfrei nach §3 Nr. 63 EStG: bis **676 EUR/Monat (8 % BBG-RV; 8.112 €/Jahr in 2026)**
   - SV-Freiheit nach § 1 SvEV: bis **338 EUR/Monat (4 % BBG-RV; 4.056 €/Jahr in 2026)**
   - AG-Zuschuss: mindestens **15 %** des umgewandelten Entgelts (§1a Abs. 1a BetrAVG; Neuverträge seit 2019, Altverträge seit 01.01.2022)
   - Aufwand auf **SKR03 4165 / SKR04 6140** "Aufwendungen für Altersversorgung"
   - Auswirkung auf Brutto und Netto berechnen

6. **Nettolohn berechnen** — Erstelle die vollstaendige Abrechnung:
   ```
   ══════════════════════════════════════════
   Lohnabrechnung — [Monat/Jahr]
   Mitarbeiter: [Name]
   Steuerklasse: [X] | Kinder: [X]
   ══════════════════════════════════════════

   Bruttogehalt                    x.xxx,xx EUR
   + Sonderzahlungen                 xxx,xx EUR
   ──────────────────────────────────────────
   = Gesamtbrutto                  x.xxx,xx EUR
   - Entgeltumwandlung (bAV)       -xxx,xx EUR
   ──────────────────────────────────────────
   = SV-pflichtiges Brutto         x.xxx,xx EUR
   = Steuer-Brutto                 x.xxx,xx EUR

   Abzuege Arbeitnehmer:
     Krankenversicherung             -xxx,xx EUR
     Pflegeversicherung               -xx,xx EUR
     Rentenversicherung              -xxx,xx EUR
     Arbeitslosenversicherung         -xx,xx EUR
     Lohnsteuer                      -xxx,xx EUR
     Solidaritaetszuschlag             -x,xx EUR
     Kirchensteuer                    -xx,xx EUR
   ──────────────────────────────────────────
   = Nettolohn                     x.xxx,xx EUR

   Arbeitgeberkosten:
     AG-Anteil SV                    xxx,xx EUR
     AG-Zuschuss bAV                  xx,xx EUR
     Umlagen (U1/U2/Insolvenzgeld)    xx,xx EUR
   ──────────────────────────────────────────
   = Gesamtkosten AG               x.xxx,xx EUR
   ══════════════════════════════════════════
   ```

7. **Gehaltszettel generieren** — Praesentiere die Abrechnung im uebersichtlichen Format zur Pruefung. Weise auf Besonderheiten hin (z.B. Einmalzahlungen, Freibetraege, Grenzueberschreitungen).

## Erwartete Eingaben

- Mitarbeiterstammdaten (Name, Steuerklasse, Kinderfreibetraege, SV-Status)
- Bruttogehalt und ggf. Sonderzahlungen
- bAV-Vereinbarung (falls vorhanden)
- Bundesland (fuer Kirchensteuersatz)
- Arbeitsstunden (fuer Mindestlohnpruefung)

## Erwartete Ausgaben

- Vollstaendige Lohnabrechnung (Brutto-Netto)
- Aufschluesselung aller SV-Beitraege (AN + AG)
- Lohnsteuer, SolZ, KiSt
- Arbeitgebergesamtkosten
- Mindestlohnpruefung

## Hinweise

- Beitragssaetze und Beitragsbemessungsgrenzen aendern sich jaehrlich — stets aktuellen Stand pruefen (alle Werte zentral in `config/rates-2026.json`).
- **Minijob-Grenze 2026: 603 EUR/Monat** (Formel: Mindestlohn × 130 Std. / 3 = 13,90 × 130/3 = 602,33 ≈ 603) — bei Unterschreitung gelten Sonderregeln.
- **Midijob (Uebergangsbereich) 2026: 603,01–2.000 EUR/Monat** — reduzierte AN-Beitraege.
- Einmalzahlungen (Weihnachtsgeld, Boni) unterliegen der Maerz- bzw. Jahreslohnsteuertabelle. **Maerzklausel** (§ 23a SGB IV): Einmalzahlungen 01.01.-31.03. werden dem Vorjahr zugeordnet, wenn Beschaeftigungsverhaeltnis im Vorjahr bestand.
- Lohnsteueranmeldung: monatlich (>5.000 EUR LSt/Jahr), quartalsweise (1.080–5.000 EUR), jaehrlich (<1.080 EUR) — § 41a Abs. 2 EStG (Grenzen aktualisiert per Wachstumschancengesetz).
