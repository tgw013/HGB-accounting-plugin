---
name: buchung-grundlagen
description: Vorbereitung von Buchungssätzen für den Monats- bzw. Jahresabschluss unter HGB — Rechnungsabgrenzungen (§ 250 HGB) und typische Rückstellungen (§ 249 HGB). Anwenden bei Monats-/Jahresabschluss, ausstehenden Eingangsrechnungen, Urlaubs-/Steuer-/Pensions-/Garantierückstellungen, ARAP/PRAP. Inspiriert vom Anthropic `journal-entry-prep`, adaptiert an HGB/DATEV (SKR03/SKR04) und Hinweisen zum Steuerbilanz-Delta und der DATEV-Praxis.
---

> ⚠ **Hinweis:** Dieser Skill ist als automatisiertes Hilfsmittel konzipiert auf Basis öffentlicher, verifizierter Quellen und soll beim Workflow zur Erstellung von Buchungssätzen unterstützen. **Er ist kein Ersatz für eine Steuerberatung.** Alle Buchungssätze sind vor der Buchung von einer dafür qualifizierten Person zu prüfen.

# Buchung-Grundlagen — Abschlussbuchungen HGB

**Typ:** `knowledge` · **Pendant:** `anthropics/knowledge-work-plugins/finance/journal-entry-prep` (HGB-adaptiert) · **Gilt für:** GmbH, UG, KapG · **Config:** `config/{active_year}/`

---

## 1. Zweck

Stellt Best Practices, häufige Buchungssituationen, Grundlagenwissen und Überprüfungs-Workflow bereit für alle Workflow-Skills (`buchungssatz`, `monatsabschluss`, `jahresabschluss`, `ust-voranmeldung`, `abstimmung`, `wiederkehrende-buchungen`): **welche Abgrenzungen und Rückstellungen sind wann zu bilden, wie wird gebucht, was unterscheidet Handels- von Steuerbilanz, und wo passiert das in DATEV.**

Der Schwerpunkt liegt auf den Buchungen, die in der laufenden Buchführung *nicht* aus einem Beleg fallen, sondern durch periodengerechte Abgrenzung entstehen — der typische Bestand an Abschlussbuchungen einer mittelständischen GmbH/UG.

Dieser Skill beschreibt die **Vorgänge** (analog `journal-entry-prep`): Soll/Haben-Muster, Bewertung, Steuerbilanz-Delta, DATEV-Praxis. Den **konkreten Buchungssatz mit Beträgen** erzeugt der Skill `buchungssatz` (analog `journal-entry`) — er liest die hier beschriebenen Muster und gibt einen prüffähigen Vorschlag plus maschinellen Handoff für `datev-export` aus. Wer den Buchungsvorschlag für einen *einzelnen Beleg* sucht: → Skill `buchungssatz`. Wer den vollständigen Monats-/Jahresabschluss-Workflow sucht: → Skills `monatsabschluss` / `jahresabschluss`. Doppik-Grundlagen, GoBD-Detail und Belegpflicht: → Anhang dieses Skills (Abschnitt 8) bzw. Skill `gobd-konformitaet`.

## 2. Wann unterjährig, wann zum Jahresabschluss?

Anders als im US-Modell (monatlicher Close mit Auto-Reversal-Accruals) ist die deutsche KMU-Praxis überwiegend **jährlich** — der Monats-BWA ist meist vorläufig, der harte Cut liegt am Jahresabschluss. Faustregel:

| Buchungstyp                                | Unterjährig (monatlich/quartal) | Nur Jahresabschluss | DATEV-Praxis                                              |
| ------------------------------------------ | ------------------------------- | ------------------- | --------------------------------------------------------- |
| ARAP / PRAP für laufende Verträge          | **Empfohlen** (wiederkehrend)   | —                   | Wiederkehrende Buchung in DATEV (Auflösung 1/12 pro Monat) |
| AfA (lineare / degressive Abschreibung)    | **Empfohlen** (monatlich)       | —                   | Anlagenbuchführung DATEV, automatischer Stapel             |
| Steuerrückstellungen (KSt/GewSt)           | Vereinfachte Schätzung möglich  | **Pflicht**         | Manuell durch StB im Abschluss-Stapel                      |
| Urlaubsrückstellung                        | Selten (große KMU)              | **Pflicht**         | Externe Berechnung (HR/Excel) → Stapel-Import oder manuell |
| Rückstellung ausstehende Eingangsrechnungen | Bei Monats-/Quartals-BWA sinnvoll | **Pflicht** | Manuell in DATEV, oft mit Auto-Reversal nächster Monat     |
| Tantieme / Bonus                           | Anteilig (z.B. 1/12)            | **Pflicht** (Endabrechnung) | Manuell                                              |
| Garantierückstellung                       | Pauschal monatlich denkbar      | **Pflicht**         | Manuell, häufig pauschal aus Umsatz × Erfahrungssatz       |
| Pensionsrückstellung                       | —                               | **Pflicht (jährlich)** | Aktuar-Gutachten → Buchungsstapel-Import                |
| Drohverlustrückstellung                    | —                               | **Pflicht (HGB)**, Steuerverbot | Einzelfallbewertung StB, manuell                  |
| Jahresabschluss-/Prüfungskosten            | —                               | **Pflicht**         | Manuell, oft Pauschalbetrag aus Vorjahres-StB-Honorar      |

**Drei DATEV-Wege für Abschlussbuchungen:**

1. **In DATEV, manuell** — Erfassen | Belege buchen → Buchungsstapel "Abschluss YYYY-MM". Standardweg für einfache RAP und Standard-Rückstellungen. Siehe Skill `buchungssatz`.
2. **In DATEV, wiederkehrende Buchung** — Erfassen | Wiederkehrende Buchungen | Erfassen. Sinnvoll bei wiederkehrender ARAP-Auflösung (Versicherung, Software-Lizenzen, Leasing-Vorauszahlung). Siehe Skill `wiederkehrende-buchungen`.
3. **Extern berechnet → Import via DATEV-Buchungsstapel (EXTF-CSV)** — Erfassen | Stapelverarbeitung → Importieren. Standard für Pensionsrückstellung aus Aktuar-Software, Urlaubsrückstellung aus HR-System, und für Drittsoftware (sevdesk, BuchhaltungsButler etc.). Siehe Skill `datev-export`.

**StB-Kanzlei-Pattern (häufigste KMU-Konstellation):** Mandant bucht laufende Geschäftsvorfälle in DATEV Unternehmen online. Zum Jahresabschluss übernimmt die StB-Kanzlei den Bestand in DATEV Kanzlei-Rechnungswesen, bucht die Abschlussbuchungen als eigenen Stapel ("Prüferbuchungen" / "Abschlussbuchungen"), gibt den finalisierten Stand zurück, festschreibt nach GoBD.

## 3. Rechnungsabgrenzungsposten (§ 250 HGB)

**Konzept:** RAP gleichen *bereits erfolgte Zahlungen* periodengerecht aus, deren Aufwand/Ertrag in eine andere Periode gehört. Nicht zu verwechseln mit Rückstellungen (= ungewisse zukünftige Verpflichtungen, ohne Zahlung).

### 3.1 Aktive Rechnungsabgrenzung (ARAP) — § 250 Abs. 1 HGB

**Anwendung:** Vor Bilanzstichtag bezahlt, Aufwand gehört in spätere Periode.

**Typische Fälle:** Jahresversicherung (z.B. 01.07.–30.06.), KFZ-Steuer für 12 Monate im Voraus, Wartungsverträge, Software-Lizenzen jährlich, Miete im Voraus, Domain-/Hosting-Gebühren, Beiträge zu IHK/Berufsverbänden.

**Buchungsmuster (SKR04):**
- *Bildung am Stichtag:* Soll **1900** Aktive Rechnungsabgrenzung an Haben Aufwandskonto (z.B. **6400** Versicherungen) — in Höhe des auf die Folgeperiode entfallenden Anteils.
- *Auflösung in der Folgeperiode (zeitanteilig, ggf. monatlich 1/12):* Soll Aufwandskonto an Haben **1900** Aktive Rechnungsabgrenzung.
- → Konkreten Satz mit Beträgen erzeugt Skill `buchungssatz`.

**Bewertung:** Zeitanteilig linear. Nur sicher bestimmbare Zahlungen — bei unsicherem Betrag ggf. Rückstellung statt RAP.

**Steuerbilanz-Delta:** Identisch — § 5 Abs. 5 Satz 1 Nr. 1 EStG übernimmt § 250 HGB. **Bagatellgrenze ab 2022:** Der **Gesetzgeber** hat mit dem JStG 2022 in § 5 Abs. 5 Satz 2 EStG ein Wahlrecht eingeführt, auf den ARAP-Ansatz zu verzichten, wenn die jeweilige Ausgabe die GWG-Grenze nach § 6 Abs. 2 EStG (derzeit 800 €) nicht übersteigt. Hintergrund war das BFH-Urteil vom 16.03.2021 (X R 34/19), das gerade *gegen* eine ungeschriebene Wesentlichkeitsgrenze entschieden hatte — der Gesetzgeber hat darauf mit dem Wahlrecht reagiert. HGB-rechtlich gilt § 250 ohne Bagatellgrenze, in der Praxis wird Wesentlichkeit nach § 264 Abs. 2 HGB analog angewandt.

**DATEV-Praxis:** Klassischer Fall für wiederkehrende Buchungen. Alternativ direkt gegen ARAP-Konto buchen und monatlich 1/12 auflösen. Skill `wiederkehrende-buchungen` zeigt das DATEV-Format Kategorie 65.

### 3.2 Passive Rechnungsabgrenzung (PRAP) — § 250 Abs. 2 HGB

**Anwendung:** Vor Bilanzstichtag erhalten, Ertrag gehört in spätere Periode.

**Typische Fälle:** Vorausbezahlte Mieten (Vermieter-Sicht), Wartungsverträge bei IT-Dienstleistern, vorausbezahlte Beratungspauschalen, mehrjährige Lizenzeinnahmen.

**Buchungsmuster (SKR04):**
- *Bei Zahlungseingang:* Soll **1800** Bank an Haben Erlöskonto (z.B. **4400** Erlöse 19 % USt) für den laufenden Anteil **und** an Haben **3900** Passive Rechnungsabgrenzung für den auf die Folgeperiode entfallenden Anteil. (USt-Behandlung je Soll-/Istversteuerung — siehe Skill `ust-voranmeldung`.)
- *Auflösung in der Folgeperiode:* Soll **3900** Passive Rechnungsabgrenzung an Haben Erlöskonto (z.B. **4400**).
- → Konkreten Satz mit Beträgen erzeugt Skill `buchungssatz`.

**Steuerbilanz-Delta:** Identisch (§ 5 Abs. 5 Satz 1 Nr. 2 EStG). USt-rechtlich ist entscheidend, ob Soll- oder Istversteuerung (§ 13 vs. § 20 UStG) — PRAP ändert die USt-Schuld nicht, sondern nur den Ertragsausweis.

**DATEV-Praxis:** Wie ARAP — wiederkehrende Buchung sinnvoll bei wiederkehrenden Sachverhalten, sonst manuell.

## 4. Rückstellungen (§ 249 HGB) — der Schwerpunkt

**Konzept:** Rückstellungen erfassen *ungewisse Verbindlichkeiten* gegenüber Dritten oder drohende Verluste — Ursache liegt in der abgelaufenen Periode, Höhe und/oder Fälligkeit unsicher. Klar abgrenzbar von:

- **Verbindlichkeiten** (sicher dem Grund und der Höhe nach) — gehören auf Konto 3300 ff.
- **RAP** (Zahlung bereits erfolgt) — siehe Abschnitt 3
- **Eventualverbindlichkeiten** (geringe Wahrscheinlichkeit) — nur Anhangangabe § 285 Nr. 27 HGB

**§ 249 HGB-Pflichtkatalog (handelsrechtlich zwingend):**

1. Ungewisse Verbindlichkeiten
2. Drohende Verluste aus schwebenden Geschäften
3. Unterlassene Instandhaltung (Nachholung innerhalb 3 Monate des Folgejahres)
4. Gewährleistungen ohne rechtliche Verpflichtung (Kulanz)

**Bewertung (§ 253 Abs. 1 + 2 HGB):**

- Höhe = nach vernünftiger kaufmännischer Beurteilung notwendiger Erfüllungsbetrag
- **Abzinsung handelsrechtlich:** Restlaufzeit > 1 Jahr → Marktzins entsprechend Restlaufzeit (Bundesbank 10-Jahres-Durchschnitt nach § 253 Abs. 2 HGB; siehe `config/{active_year}/rates.json`)
- Bei Pensionsrückstellungen pauschale 15-Jahres-Restlaufzeit zulässig

**Allgemeines Buchungsmuster:** *Bildung:* Soll Aufwandskonto an Haben Rückstellungskonto. *Inanspruchnahme:* Soll Rückstellung an Haben Bank/Verbindlichkeit. *Überdotierungs-Auflösung:* Soll Rückstellung an Haben sonstige betriebliche / periodenfremde Erträge. Konkrete Sätze → Skill `buchungssatz` (Abschnitt 6 zeigt die Auflösungs-Varianten).

### 4.1 Steuerrückstellungen (KSt, GewSt, USt-Nachzahlungen)

**Anwendung:** Zum Bilanzstichtag entstandene, aber noch nicht veranlagte Ertragsteuern (KSt 15 % + SolZ 5,5 % auf KSt + GewSt Hebesatz × Messzahl 3,5 %) sowie noch nicht beglichene USt-Schulden.

**Bewertung:** Berechnung auf vorläufigem Jahresergebnis. Bei GewSt-Rückstellung **Schachtelrechnung**: GewSt mindert ihre eigene Bemessungsgrundlage nicht (§ 4 Abs. 5b EStG), aber das HGB-Ergebnis vor Steuern wird durch die GewSt-Rückstellung gemindert.

**Buchungsmuster (SKR04):** Soll **7600** Körperschaftsteuer / **7610** Gewerbesteuer (sowie SolZ-Aufwand) an Haben **3040** Körperschaftsteuerrückstellung / **3035** Gewerbesteuerrückstellung. Mehrere Soll-Konten gegen mehrere Haben-Konten → Splittbuchung. → Skill `buchungssatz`.

**Steuerbilanz-Delta:** GewSt-Rückstellung ist in Handelsbilanz Aufwand, in Steuerbilanz aufgrund § 4 Abs. 5b EStG **kein Betriebsausgabenabzug** — die Bildung der Rückstellung selbst ist steuerlich zulässig, aber der Aufwand ist außerbilanziell hinzuzurechnen.

**DATEV-Praxis:** **Immer manuell durch StB im Jahresabschluss-Stapel.** Vorerfassung im Monats-BWA nur als grobe Schätzung sinnvoll (z.B. Erwartungswert KSt-Quote × kumuliertes Ergebnis); reale Bewertung braucht Steuererklärungs-Daten.

### 4.2 Urlaubsrückstellung

**Anwendung:** Am Bilanzstichtag noch nicht genommener Urlaub der Arbeitnehmer. Pflicht nach § 249 Abs. 1 Satz 1 HGB.

**Bewertung:** Pro Mitarbeiter: Resturlaubstage × Tagessatz Brutto-Personalkosten. Tagessatz = (Jahresgehalt + Arbeitgeber-SV-Anteile) / Arbeitstage. Tarifliche Sonderzahlungen, Urlaubsgeld und SV-Beiträge sind einzubeziehen (IDW HFA 5.7).

**Buchungsmuster (SKR04):** Soll Personalaufwand (**6072** Aufwand Urlaubsrückstellung; alternativ **6020** Gehälter + **6100** soziale Abgaben für den AG-SV-Anteil) an Haben **3079** Urlaubsrückstellungen. → Skill `buchungssatz`.

**Steuerbilanz-Delta:** Grundsätzlich identisch in den einbezogenen Bestandteilen (R 6.11 EStR — auch Arbeitgeber-Anteile zur SV und lohnabhängige Nebenkosten gehören dazu, abweichend von verbreiteter Falschdarstellung in Praxisliteratur). **Zwei echte Unterschiede:**
- **Stichtagsprinzip** (§ 6 Abs. 1 Nr. 3a Buchst. f EStG): in der Steuerbilanz dürfen künftige Lohnsteigerungen *nicht* berücksichtigt werden — Bewertung mit den Verhältnissen am Bilanzstichtag. HGB-Erfüllungsbetrag bezieht erwartete Steigerungen ein (§ 253 Abs. 1 Satz 2 HGB).
- **Maßgebliche Arbeitstage**: steuerlich nur reguläre Arbeitstage abzüglich Wochenenden und Feiertage (ohne Urlaubs- und Krankheitstage); HGB-Praxis tendiert ebenfalls dazu, die genaue Anzahl ist aber Wahlrecht.

**Praxis:** Zwei separate Berechnungen sinnvoll, vor allem bei steigenden Tarifen / Lohnerhöhungen über den Bilanzstichtag hinaus.

**DATEV-Praxis:** Berechnung extern (HR-System oder Excel-Tool je Mitarbeiter), Buchungssatz manuell oder via Stapel-Import. Auto-Reversal nicht üblich — Inanspruchnahme erfolgt durch tatsächliche Urlaubsnahme über laufende Personalbuchungen.

### 4.3 Rückstellung für Jahresabschluss- und Prüfungskosten

**Anwendung:** Verpflichtung zur Aufstellung des Jahresabschlusses, Steuererklärungen, ggf. Abschlussprüfung — entsteht mit Ablauf des Geschäftsjahres, Rechnungen kommen erst Monate später.

**Bewertung:** Honorarrechnung des Steuerberaters/WP aus Vorjahr als Anhalt, korrigiert um bekannte Änderungen (Umsatzwachstum, neue Sachverhalte, ggf. Wirtschaftsprüferpflicht nach § 316 i.V.m. § 267 HGB). Pauschalansatz bei kleinen GmbHs üblich.

**Buchungsmuster (SKR04):** Soll **6825** Abschluss- und Prüfungskosten / **6827** Steuerberatungskosten an Haben **3070** Sonstige Rückstellungen. → Skill `buchungssatz`.

**Steuerbilanz-Delta:** Vollständig identisch — diese Rückstellung ist ein steuerlicher "Klassiker" ohne Korrektur (H 5.7 (3) EStH "Jahresabschlusskosten").

**DATEV-Praxis:** Manuell im Abschluss-Stapel, einmal jährlich. Auflösung mit Eingang der StB-Rechnung im Folgejahr.

### 4.4 Rückstellung für ausstehende Eingangsrechnungen

**Anwendung:** Lieferung/Leistung im alten Jahr erbracht, Rechnung am Bilanzstichtag noch nicht eingegangen. Klassisch: Energie-Nachzahlungen, Strom/Gas/Wasser, Telefon-/Internet-Abschlussrechnungen, Berufsverbandbeiträge, externe Dienstleister (Marketing, IT, Reinigung).

**Bewertung:** Schätzung nach vernünftiger kaufmännischer Beurteilung (§ 253 Abs. 1 HGB). Datenquellen: offene Bestellungen mit erfolgter Wareneingangsmeldung, Verträge mit erbrachter Leistung ohne Rechnung, historische Run-Rate (Strom/Gas), Mitarbeiter-Reisekostenanträge ohne Beleg.

**Buchungsmuster (SKR04):** Soll Aufwandskonto (z.B. **6605** Strom/Gas oder das passende Sachkonto) an Haben **3070** Sonstige Rückstellungen. Bei klar bezifferbarer Verbindlichkeit ggf. statt Rückstellung "Sonstige Verbindlichkeit" — Grenzfall. → Skill `buchungssatz`.

**Steuerbilanz-Delta:** Identisch, sofern bewertungsfähig nach vernünftiger Schätzung. **Achtung Abzinsung:** Bei Restlaufzeit > 12 Monate ist die Rückstellung in der Steuerbilanz nach § 6 Abs. 1 Nr. 3a Buchst. e EStG mit **5,5 %** abzuzinsen; in der Handelsbilanz mit dem Bundesbank-Marktzins (§ 253 Abs. 2 HGB). Bei kurzfristigen Eingangsrechnungen-Rückstellungen (< 12 Monate) **keine Abzinsung** in beiden Bilanzen.

**DATEV-Praxis:** Standardfall für Monats- und Jahresabschluss. Bei Monatsabschlüssen häufig mit Auto-Reversal-Logik geführt (Rückstellung wird im Folgemonat aufgelöst und bei tatsächlichem Rechnungseingang neu beurteilt) — DATEV unterstützt das nicht automatisch, daher manuell als zwei Stapel.

### 4.5 Tantieme- und Bonusrückstellung

**Anwendung:** Vertraglich vereinbarte erfolgsabhängige Vergütungen für Geschäftsführer (Tantieme) oder Mitarbeiter (Bonus), die im alten Jahr verdient, aber erst im Folgejahr ausgezahlt werden.

**Bewertung:** Nach Vertragsformel (z.B. x % vom Jahresüberschuss vor Tantieme — **iterativ rechnen!**). Bei GF-Tantieme von Gesellschafter-GF Vorsicht: § 8 Abs. 3 KStG i.V.m. H 8.5 / H 8.8 KStH — Begrenzung auf max. 50 % des Jahresüberschusses vor Tantieme und max. 25 % der Gesamtbezüge, sonst vGA-Risiko.

**Buchungsmuster (SKR04):**
- *GF-Tantieme:* Soll **6027** Aufwendungen für Vergütung Gesellschafter-GF (+ **6100** soziale Abgaben) an Haben **3074** Rückstellungen für Personalkosten (Tantieme).
- *Mitarbeiter-Bonus:* Soll **6020** Gehälter (+ **6100** soziale Abgaben) an Haben **3070** Sonstige Rückstellungen.
- → Skill `buchungssatz`.

**Steuerbilanz-Delta:** Identisch in der Bewertung, **aber** bei Gesellschafter-GF-Tantieme verschärfte vGA-Prüfung (§ 8 Abs. 3 KStG):
- Klare schriftliche Vereinbarung **vor** Beginn des Geschäftsjahres, in dem die Tantieme verdient wird (bei beherrschendem Gesellschafter zivilrechtlich wirksamer Gesellschafterbeschluss erforderlich)
- Angemessenheit Gesamtbezüge nach **H 8.5 KStH "Angemessenheit der Gesamtbezüge"** und **H 8.8 KStH "Tantiemen"** (gestützt auf BFH-Rechtsprechung)
- Faustregeln: Tantieme max. **25 % der Gesamtbezüge** (= 75/25-Verhältnis Festgehalt/variabel), Bemessungsgrundlage höchstens **50 % des handelsrechtlichen Jahresüberschusses vor Tantieme**
- Bei Überschreitung: gewinnerhöhende vGA mit Nachzahlung KSt/SolZ/GewSt + Kapitalertragsteuer beim Gesellschafter

**DATEV-Praxis:** Manuell, einmal jährlich im Jahresabschluss. Inanspruchnahme über die Lohnabrechnung des Auszahlungsmonats.

### 4.6 Garantie- / Gewährleistungsrückstellung

**Anwendung:** Gesetzliche Gewährleistung (§§ 437, 634 BGB) und/oder vertragliche Garantieversprechen — am Stichtag ungewisse, aus dem alten Jahr stammende Verpflichtung zur Nachbesserung.

**Bewertung:** Zwei Wege je Erfahrungsbasis:

- **Pauschal:** Umsatz × historischer Garantie-Aufwandsquote (z.B. 0,5 % des garantierelevanten Umsatzes)
- **Einzelfall:** Bekannte konkrete Reklamationsfälle mit Schätzung pro Fall

**Buchungsmuster (SKR04):** Soll **6510** Garantiekosten an Haben **3070** Sonstige Rückstellungen. → Skill `buchungssatz`.

**Steuerbilanz-Delta:** Pauschale Garantierückstellung steuerlich zulässig, aber **Erfahrungswerte über mindestens 3 Jahre belegen** (BFH-Urteil vom 30.01.2002, I R 71/00). Kulanzrückstellungen (ohne rechtliche Verpflichtung) sind handelsrechtlich nach § 249 Abs. 1 Satz 2 Nr. 2 HGB zulässig — steuerlich nur, wenn faktischer Leistungszwang besteht und Inanspruchnahme wahrscheinlich.

**DATEV-Praxis:** Pauschalmethode lässt sich gut als wiederkehrende monatliche Anpassung führen (umsatzproportional), Einzelfälle manuell. Bei materieller Größenordnung Bewertungsmethodik dokumentieren (GoBD-Verfahrensdokumentation).

### 4.7 Pensionsrückstellung

**Anwendung:** Erteilte Pensionszusagen an Geschäftsführer oder Mitarbeiter (Direktzusage). Bei mittelbaren Zusagen über Unterstützungskasse/Pensionskasse meist keine Bilanzpassivierung (§ 246 Abs. 2 Satz 2 HGB + § 6a EStG).

**Bewertung — handelsrechtlich (§ 253 Abs. 1 Satz 2 i.V.m. Abs. 2 HGB):**

- Erfüllungsbetrag inkl. künftiger Trend-Annahmen (Lohn/Gehalt, Renten, Fluktuation, Sterblichkeit nach Heubeck-Richttafeln)
- **Abzinsung:** Marktzins, 10-Jahres-Durchschnitt nach Restlaufzeit (Bundesbank veröffentlicht monatlich, siehe `config/{active_year}/rates.json`); pauschale 15-Jahres-Restlaufzeit zulässig (§ 253 Abs. 2 Satz 2 HGB)
- Unterschiedsbetrag aus 10- vs. 7-Jahres-Durchschnittszins ausschüttungsgesperrt (§ 253 Abs. 6 HGB)

**Bewertung — steuerrechtlich (§ 6a EStG):**

- Teilwertverfahren mit festem Rechnungszins **6 %**
- Strikte Formvoraussetzungen: schriftliche Pensionszusage, eindeutige Höhe, kein Vorbehalt der Minderung außer in engen Grenzen

**Buchungsmuster (SKR04):** Soll **6140** Aufwendungen für Altersversorgung (bei Gesellschafter-GF **6149**) an Haben **3010** Rückstellungen für Direktzusagen. → Skill `buchungssatz`.

**Steuerbilanz-Delta:** **Strukturell unterschiedlich** — fast immer zwei separate Aktuar-Gutachten (HGB-Wert und StB-Wert), Differenz führt zu **passiven latenten Steuern** (§ 274 HGB; bei kleinen KapG Wahlrecht § 274a Nr. 5 HGB). Verschärfung Eigenkapital durch HGB-Marktzins-Schwankungen erkennbar.

**DATEV-Praxis:** Niemals manuell schätzen. **Standardweg:** Aktuar-Software (z.B. Heubeck, longial) berechnet HGB- und StB-Wert, Bilanzwerte und Aufwand werden als Buchungsstapel-CSV in DATEV importiert. Jährlich einmal, regelmäßig durch StB orchestriert.

### 4.8 Rückstellung für unterlassene Instandhaltung

**Anwendung:** Im alten Jahr **unterlassene** Instandhaltungsarbeit (Reparatur, Wartung), die im Folgejahr **innerhalb 3 Monaten** nachgeholt wird (§ 249 Abs. 1 Satz 2 Nr. 1 HGB). Strikte Frist!

**Bewertung:** Voraussichtliche Aufwendungen für die Nachholung. Bei Nachholung später als 3 Monate, aber innerhalb 12 Monaten → **Wahlrecht** § 249 Abs. 1 Satz 2 Nr. 1 Halbsatz 2 HGB (Wahlrecht, kein Müssen). Spätere Nachholung → keine Rückstellung.

**Buchungsmuster (SKR04):** Soll **6470** Instandhaltung betrieblicher Räume an Haben **3070** Sonstige Rückstellungen. → Skill `buchungssatz`.

**Steuerbilanz-Delta:** **Verschärft** — nur Pflicht-Rückstellung bei 3-Monats-Nachholung (R 5.7 Abs. 11 EStR). Das HGB-Wahlrecht für die 3–12-Monats-Spanne **gilt steuerlich nicht** → bei Inanspruchnahme des Wahlrechts entsteht eine Differenz und ggf. aktive latente Steuern.

**DATEV-Praxis:** Manuell, einmal jährlich. Inanspruchnahme mit tatsächlicher Reparaturrechnung. Bei fehlender Nachholung innerhalb 3 Monaten: **Auflösung Pflicht** (Aufwandsumkehr in laufender Periode).

### 4.9 Drohverlustrückstellung — HGB-Pflicht, **Steuerverbot**

**Anwendung:** Schwebendes Geschäft (Vertrag, bei dem Leistung und Gegenleistung noch nicht vollständig erbracht sind), bei dem mit überwiegender Wahrscheinlichkeit ein Verlust droht (Leistungsverpflichtung wertmäßig > erwartete Gegenleistung). Klassische Fälle: ungünstige Lieferverträge mit Fixpreisen bei gestiegenen Materialkosten, Mietverträge für nicht genutzte Räume (Leerstand), Beschäftigungsverpflichtungen bei Auftragsrückgang.

**Bewertung:** Erwarteter Verlust nach vernünftiger kaufmännischer Beurteilung.

**Buchungsmuster (SKR04):** Soll **6960** Periodenfremde / sonstige Aufwendungen an Haben **3092** Rückstellung für drohende Verluste aus schwebenden Geschäften (Konto gegen Mandanten-Kontenrahmen prüfen). → Skill `buchungssatz`.

**Steuerbilanz-Delta — kritisch:** **Bildung in Steuerbilanz verboten** (§ 5 Abs. 4a EStG). HGB-Aufwand ist außerbilanziell zu korrigieren → führt regelmäßig zu **aktiven latenten Steuern** (§ 274 HGB; Wahlrecht für kleine KapG § 274a Nr. 5 HGB). **Praxis:** Vor Bildung **immer StB konsultieren** — Abgrenzung zu zulässigen Rückstellungen für ungewisse Verbindlichkeiten ist heikel.

**DATEV-Praxis:** Manuell, ausschließlich im Jahresabschluss-Stapel, dokumentierte Einzelfallbewertung. Übergabe an StB via Skill `steuerberater-handoff` empfohlen.

### 4.10 Künstlersozialabgabe (KSK) — die vergessene Rückstellung

**Anwendung:** Jedes Unternehmen, das **regelmäßig** Aufträge an selbstständige Künstler oder Publizisten vergibt (Designer, Texter/Copywriter, Webdesigner, Fotografen, Journalisten, Übersetzer, Musiker, Illustratoren), ist nach **§ 24 KSVG** abgabepflichtig. Klassischer Trigger: Marketingagentur extern, Logo-Design extern, Websitetexte extern, Pressemitteilungen extern, Unternehmensvideo extern.

**Zwei Tatbestände unterscheiden:**
- **Typische Verwerter** (§ 24 Abs. 1 Satz 1 KSVG — z.B. Verlage, Presseagenturen, Theater, Galerien, Werbeagenturen): abgabepflichtig **ohne Bagatellgrenze**
- **Eigenwerber-Generalklausel** (§ 24 Abs. 1 Satz 2 + Abs. 2 KSVG — Unternehmen, die für Zwecke der eigenen Öffentlichkeitsarbeit oder Werbung künstlerische/publizistische Leistungen einkaufen): abgabepflichtig erst oberhalb der **Bagatellgrenze**: 450 € bis 2024, **700 € ab 2025**, **1.000 € ab 2026** (jeweils Summe der Honorare im Kalenderjahr)

Häufigster Fehler in der Praxis: **wird über Jahre vergessen**, fällt erst bei KSK-Betriebsprüfung auf (typischer Prüfungszeitraum 5 Jahre rückwirkend → erhebliche Nachzahlungen + Säumniszuschläge).

**Bewertung:**
- **Abgabesatz 2026: 4,9 %** auf alle Netto-Honorare an die o.g. Personengruppen (BMAS Künstlersozialabgabe-Verordnung 2026; Historie: 5,0 % 2024+2025, 4,2 % 2022+2023 — aktuelle Werte in `config/{active_year}/rates.json`)
- **Bemessungsgrundlage:** Honorar inkl. Auslagen und Nebenkosten, **ohne** USt und ohne nachgewiesene Reisekosten
- **Meldepflicht:** jährlich bis **31.03. des Folgejahres** an die KSK
- **Zahlung:** monatliche Vorauszahlungen + Jahresausgleich; bei nicht gemeldeten Vorjahren Nachzahlung-Rückstellung

**Buchungsmuster (SKR04):**
- *Laufende Abgabe:* Soll **6135** Künstlersozialabgabe (alt. **6855** sonstige betriebliche Aufwendungen) an Haben **3740** Verbindlichkeiten Künstlersozialkasse.
- *Rückstellung am Bilanzstichtag* für noch nicht gemeldete Honorare (oder bekannte Nachzahlung aus laufender KSK-Prüfung): Soll **6135** Künstlersozialabgabe an Haben **3070** Sonstige Rückstellungen.
- → Skill `buchungssatz`.

**Steuerbilanz-Delta:** Identisch — KSK-Abgabe ist abzugsfähige Betriebsausgabe, Rückstellung steuerlich gleichermaßen geboten (ungewisse Verbindlichkeit § 249 Abs. 1 HGB / § 5 Abs. 1 EStG).

**DATEV-Praxis:** Bei sauberer laufender Erfassung **wiederkehrende monatliche Buchung** der Vorauszahlung sinnvoll. Jahresausgleich + ggf. Nachzahlungsrückstellung manuell im Jahresabschluss-Stapel. **Tipp für die Belegerfassung:** jede Eingangsrechnung von Kreativen mit USt-pflichtigem Einzelunternehmer-Status (kein KSK-Risiko) vs. selbstständigem Künstler/Publizist markieren — Skill `buchungssatz` kann hier mit Lieferanten-Klassifikation unterstützen.

**Verwandte Pflichten:** Aufzeichnungspflicht aller KSK-relevanten Honorare über 5 Jahre (§ 28 KSVG). Bei Verstoß Bußgeld bis 50.000 € (§ 36 KSVG). Klare Verfahrensdokumentation einrichten — siehe Skill `gobd-konformitaet`.

## 5. Konsolidierte Übersicht: HGB vs. Steuerbilanz

| Rückstellungstyp                       | HGB                             | Steuerbilanz                                                      | Latente Steuern             |
| -------------------------------------- | ------------------------------- | ----------------------------------------------------------------- | --------------------------- |
| Steuerrückstellungen (KSt/GewSt/USt)   | Pflicht                         | Pflicht; GewSt-Aufwand außerbilanziell hinzurechnen (§ 4 Abs. 5b EStG) | Keine direkt              |
| Urlaubsrückstellung                    | Erfüllungsbetrag inkl. künftiger Lohnsteigerungen | Stichtagswert ohne künftige Lohnsteigerungen (§ 6 Abs. 1 Nr. 3a Buchst. f EStG); AG-Anteile einbezogen (R 6.11 EStR) | Mögliche aktive LSt |
| Jahresabschluss-/Prüfungskosten        | Pflicht                         | Pflicht — identisch                                               | Keine                       |
| Ausstehende Eingangsrechnungen         | Pflicht                         | Pflicht, Abzinsung 5,5 % bei Restlaufzeit > 1 Jahr (§ 6 EStG)     | Mögliche aktive LSt         |
| Tantieme/Bonus (Mitarbeiter)           | Pflicht                         | Pflicht — identisch                                               | Keine                       |
| Tantieme (Gesellschafter-GF)           | Pflicht                         | Vorab-Vereinbarung Pflicht; Angemessenheit nach H 8.5/H 8.8 KStH (max. 25 % der Gesamtbezüge, max. 50 % JÜ vor Tantieme) | vGA-Risiko statt LSt |
| Garantie / Gewährleistung              | Pflicht (pauschal + Einzelfall) | Pauschal nur mit 3-Jahres-Erfahrungswerten (BFH I R 71/00)        | Mögliche aktive LSt         |
| Kulanzrückstellung                     | Pflicht (§ 249 I 2 Nr. 2 HGB)   | Nur bei faktischem Leistungszwang                                 | Mögliche aktive LSt         |
| Pensionsrückstellung                   | Marktzins-Abzinsung (10-J-Ø)    | Fester Rechnungszins 6 % (§ 6a EStG)                              | **Praktisch immer LSt**     |
| Unterlassene Instandhaltung (≤ 3 Mon.) | Pflicht                         | Pflicht — identisch                                               | Keine                       |
| Unterlassene Instandhaltung (3–12 Mon.) | Wahlrecht                       | **Verbot** (R 5.7 Abs. 11 EStR)                                   | Aktive LSt bei Inanspruchnahme Wahlrecht |
| Drohverlust aus schwebenden Geschäften | Pflicht                         | **Verbot** (§ 5 Abs. 4a EStG)                                     | **Immer aktive LSt**        |
| Künstlersozialabgabe (KSK)             | Rückstellung für ungewisse Verbindlichkeiten (§ 249 Abs. 1 HGB) — abgabepflichtig nach § 24 KSVG | Identisch — abzugsfähige Betriebsausgabe | Keine |
| Aufwandsrückstellung (eigen)           | Verbot seit BilMoG              | Verbot                                                            | —                           |

Allgemeine **Abzinsung** Rückstellungen mit Restlaufzeit > 12 Monate:

- HGB § 253 Abs. 2: Bundesbank-Marktzins entsprechend Restlaufzeit, 10-Jahres-Durchschnitt; bei Pensionsrückstellungen pauschal 15 Jahre Restlaufzeit zulässig
- Steuerbilanz: 5,5 % allgemein (§ 6 Abs. 1 Nr. 3a Buchst. e EStG), 6 % nur für Pensionsrückstellungen (§ 6a EStG)

**Latente Steuern:** Bei mittelgroßen/großen KapG Pflicht (§ 274 HGB), bei kleinen KapG Wahlrecht (§ 274a Nr. 5 HGB). Die HGB-/Steuerbilanz-Differenzen aus obigen Zeilen sind die häufigsten Ursachen.

## 6. Auflösung von Rückstellungen

Drei Auflösungsanlässe, drei Buchungsmuster (konkrete Sätze → Skill `buchungssatz`):

- **6.1 Inanspruchnahme** (tatsächliche Zahlung passt zur Rückstellung): Soll Rückstellung (z.B. **3070**) an Haben **1800** Bank.
- **6.2 Übermäßige Dotierung** (Rückstellung war zu hoch — ertragswirksame Auflösung): Soll Rückstellung (z.B. **3070**) an Haben Konto "Erträge aus der Auflösung von Rückstellungen" (periodenfremder Ertrag; SKR04 z.B. 4830/4930 je Mandanten-Praxis — gegen Kontenrahmen prüfen).
- **6.3 Unterdotierung** (Zahlung höher als Rückstellung — Differenz als Aufwand): Soll Rückstellung (z.B. **3070**) + Soll **6960** periodenfremde Aufwendungen an Haben **1800** Bank.

**Stetigkeit:** Auflösungsmethodik und Bewertungsmethode pro Rückstellungstyp **stetig** über Jahre (§ 252 Abs. 1 Nr. 6 HGB) — Methodenwechsel begründungspflichtig im Anhang (§ 284 Abs. 2 Nr. 3 HGB).

## 7. Häufige Fehler

1. **Verwechslung Rückstellung ↔ Verbindlichkeit:** Rechnung liegt vor und ist sicher → Verbindlichkeit (3300 ff.), nicht Rückstellung. Faustregel: Liegt eine Rechnung vor? → Verbindlichkeit.
2. **Verwechslung Rückstellung ↔ RAP:** Geld bereits geflossen → RAP. Geld noch nicht geflossen + ungewisse Verpflichtung → Rückstellung.
3. **Steuerbilanz-Verbote übersehen** (Drohverlust, Aufwandsrückstellung) → Korrektur außerhalb der Steuerbilanz vergessen.
4. **GewSt-Hinzurechnung** nach § 4 Abs. 5b EStG vergessen — GewSt mindert die KSt-Bemessungsgrundlage nicht.
5. **Pensionsrückstellung mit HGB-Wert in Steuerbilanz** übernommen — § 6a EStG strikt einhalten, zwei Gutachten Pflicht.
6. **Urlaubsrückstellung** ohne SV-Beiträge — handelsrechtlich AG-Anteile mit einbeziehen.
7. **Tantieme an Gesellschafter-GF** ohne wirksame Vorab-Vereinbarung → vGA mit Nachzahlungsrisiko.
8. **Auto-Reversal nicht eingerichtet** bei kurzfristigen Rückstellungen (ausstehende Eingangsrechnungen) → Doppelbuchung in laufender Periode.
9. **Bagatellgrenze ARAP** nicht beachtet — Gesetzgeber-Wahlrecht (JStG 2022, § 5 Abs. 5 Satz 2 EStG) bei ≤ 800 €; vor 2022 kein Wahlrecht (BFH X R 34/19).
10. **Drohverlustrückstellung gebildet** ohne dokumentierte Bewertungsgrundlage → IKS-Risiko, latente-Steuer-Risiko.
11. **Auflösungserträge** auf Erlöskonto statt periodenfremdem Ertragskonto gebucht — verfälscht operatives Ergebnis.
12. **Stetigkeit gebrochen** ohne Anhangangabe — bei nächster Betriebsprüfung Diskussion zur Bewertungsmethode.

## 8. Belegpflicht, Bewertungsstetigkeit, Festschreibung (GoBD)

Auch Rückstellungs- und Abgrenzungsbuchungen sind GoBD-pflichtig:

- **Belegfunktion** (GoBD Tz. 61 ff.): Eigenbeleg mit Berechnungsschema (z.B. Excel-Sheet "Urlaubsrückstellung YYYY"), Begründung, Datum, Ersteller, Genehmigung
- **Festschreibung** nach Buchung im laufenden Stapel — siehe Skill `gobd-konformitaet`
- **Bewertungsstetigkeit** (§ 252 Abs. 1 Nr. 6 HGB) — gleiche Methode wie Vorjahr; Wechsel ist im Anhang zu erläutern (§ 284 Abs. 2 Nr. 3 HGB)
- **Aufbewahrung** Berechnungsunterlagen 10 Jahre / 8 Jahre für ab 01.01.2025 entstandene Buchungsbelege (Viertes Bürokratieentlastungsgesetz, § 147 Abs. 3 AO)

**Mindestangaben pro Abschlussbuchung:**

1. Buchungstext: Sachverhalt + Periode (z.B. "Urlaubsrückstellung 12/YYYY")
2. Berechnungsgrundlage: Verweis auf Eigenbeleg/Excel-Sheet (Dateiname, Speicherort, Versions-Hash)
3. §-Grundlage (HGB / EStG / EStR)
4. Periodenzuordnung
5. Ersteller + Datum
6. Genehmigung (bei Materialitätsschwelle — typisch ab 5.000 €)
7. Auflösungsmechanik (Auto-Reversal ja/nein + Datum)

### 8.1 Rechnungspflichtangaben (§ 14 UStG) — Grundlage jeder Eingangsrechnungs-Buchung

Auch wenn dieser Skill den Schwerpunkt auf Abschlussbuchungen legt: Jede Rückstellung für *ausstehende Eingangsrechnungen* (Abschnitt 4.4) wird beim tatsächlichen Rechnungseingang gegen eine konkrete Eingangsrechnung aufgelöst — diese Rechnung muss die Pflichtangaben enthalten, sonst **Vorsteuerabzug gefährdet** und Buchung formell mangelhaft.

**Pflichtangaben Vollrechnung (§ 14 Abs. 4 UStG):**

1. Name und vollständige Anschrift Rechnungssteller + Empfänger
2. Steuer-Nr. **oder** USt-IdNr. des Rechnungsstellers
3. Ausstellungsdatum
4. Fortlaufende, einmalige Rechnungsnummer
5. Menge und handelsübliche Bezeichnung der Lieferung / Art und Umfang der Leistung
6. Zeitpunkt (oder Zeitraum) der Lieferung / Leistung
7. Nettoentgelt, nach Steuersätzen und Steuerbefreiungen aufgeschlüsselt
8. Anzuwendender Steuersatz **und** Steuerbetrag — oder Hinweis auf Steuerbefreiung / Reverse Charge (§ 13b UStG) / Kleinunternehmer (§ 19 UStG)
9. Bei Aufbewahrungsfrist-relevanten Sonderfällen ggf. Hinweis "Aufbewahrungspflicht des Leistungsempfängers" (B2C Bauleistungen § 14b UStG)

**Kleinbetragsrechnung (§ 33 UStDV) bis 250 € brutto:**
Vereinfachte Pflichten — Name/Anschrift Rechnungssteller, Ausstellungsdatum, Menge/Art Leistung, Brutto + Steuersatz (oder Hinweis Steuerbefreiung). Rechnungsnummer und Empfänger-Angaben entfallen.

**E-Rechnung B2B-Pflicht** (seit 01.01.2025, Übergangsfristen):
- Empfang strukturierter E-Rechnungen (XRechnung / ZUGFeRD ≥ 2.0.1) bereits seit 01.01.2025 Pflicht für jedes Unternehmen
- Ausstellung: Übergangsfristen je nach Vorjahresumsatz, vollständige Pflicht spätestens **01.01.2028**
- PDF-Rechnungen sind ab 2025 *keine* E-Rechnungen im Sinne des § 14 UStG mehr und gelten als "sonstige Rechnung" → Übergangsfristen-relevant

**Praxisrelevanz für diesen Skill:** Beim Auflösen einer Rückstellung für ausstehende Eingangsrechnung gegen die eingetroffene Rechnung *immer* die Pflichtangaben prüfen. Bei fehlenden Pflichtangaben: Rechnung zurück an Rechnungssteller, Rückstellung **nicht** auflösen, sondern stehen lassen bis korrigierte Rechnung vorliegt. Detail-Workflow für laufende Belegbuchung: → Skill `buchungssatz`.

## 9. SKR03 vs. SKR04 — Kurzhinweis

Dieser Skill nutzt durchgehend **SKR04** (DATEV-Standard für KapG-Neueinrichtungen, näher an HGB-Bilanzgliederung § 266/§ 275). SKR03-Mandanten: Konto-Mapping in `config/{active_year}/kontenrahmen.json`. Beispiele für die wichtigsten Rückstellungs-/RAP-Konten:

| SKR04 | SKR03 | Bezeichnung                                  |
| ----- | ----- | -------------------------------------------- |
| 1900  | 980   | Aktive Rechnungsabgrenzung                   |
| 3900  | 990   | Passive Rechnungsabgrenzung                  |
| 3010  | 950   | Rückstellungen für Direktzusagen (Pensionsrückstellungen) |
| 3035  | 956   | Gewerbesteuerrückstellung                    |
| 3040  | 957   | Körperschaftsteuerrückstellung               |
| 3070  | 970   | Sonstige Rückstellungen                      |
| 3079  | 961   | Urlaubsrückstellungen                        |
| 3092  | 953   | Drohverlustrückstellung                      |

Wechsel zwischen SKR03/04 ist möglich, aber aufwändig. Bestand entscheidet meistens. Neueinrichtung KapG → SKR04 empfohlen. Konkrete Konto-Auswahl je Vorgang → Skill `buchungssatz` (Vorgang-Katalog).

## 10. Übergabe an Steuerberater

Für komplexe oder strittige Rückstellungen (Drohverlust, vGA-relevante Tantieme, Pension) Skill `steuerberater-handoff` nutzen. Der Handoff-Bogen sollte enthalten:

- Sachverhalt
- Eigener Bewertungsvorschlag mit Berechnung
- §-Grundlagen HGB + Steuerbilanz
- Steuerbilanz-Delta-Hinweis
- Belege (Verträge, Gutachten, Vorjahres-Werte)
- Konkrete offene Fragen

## 11. Quellen

- HGB §§ 246, 249, 250, 252, 253, 266, 274, 274a, 275, 284, 285 — gesetze-im-internet.de/hgb/
- EStG § 5 Abs. 4a (Drohverlustverbot), § 5 Abs. 5 (RAP-Definition), § 6 Abs. 1 Nr. 3a (Abzinsung 5,5 %), § 6a (Pensionsrückstellung 6 %), § 4 Abs. 5b (GewSt-Abzugsverbot)
- KStG § 8 Abs. 3 (vGA bei Gesellschafter-GF-Tantieme)
- UStG § 14, § 14a (Rechnungspflichtangaben), § 14b (Aufbewahrung), UStDV § 33 (Kleinbetragsrechnung)
- KSVG §§ 24, 25, 28, 36 (Künstlersozialabgabe Verwerter/Eigenwerber, Aufzeichnung, Bußgeld); BMAS Künstlersozialabgabe-Verordnung 2026 (Abgabesatz 4,9 %)
- AO §§ 145–147 (Aufbewahrung, GoBD-Datenzugriff)
- EStR/EStH: R 5.7 (Rückstellungen allgemein), R 6.11 (Urlaubsrückstellung)
- KStR/KStH: H 8.5 KStH (Angemessenheit Gesamtbezüge), H 8.8 KStH (Tantiemen, vGA-Faustregeln)
- BMF GoBD vom 28.11.2019
- BFH-Urteile: I R 71/00 (Pauschalrückstellungen Garantie, 30.01.2002), X R 34/19 (BFH gegen ungeschriebene ARAP-Wesentlichkeitsgrenze, 16.03.2021 — Gesetzgeber-Reaktion JStG 2022 mit § 5 Abs. 5 Satz 2 EStG)
- IDW HFA 5.7 (Urlaubsrückstellung Bewertung)
- BVerfG-Beschluss vom 28.07.2023 (2 BvL 22/17) — Richtervorlage des FG Köln zur Verfassungsmäßigkeit des starren 6-%-Rechnungszinses nach § 6a EStG **als unzulässig zurückgewiesen** (keine inhaltliche Bestätigung; Frage materiell offen)
- DATEV Hilfe-Center: Wiederkehrende Buchungen (apps.datev.de/help-center/documents/9211468, 9211472)
- DATEV Format EXTF-CSV (developer.datev.de — Buchungsstapel)
- DATEV SKR04 Art.-Nr. 11175 Stand 2026-01-01
- Bundesbank Abzinsungszinssätze nach § 253 Abs. 2 HGB (monatliche Veröffentlichung)
- `config/{active_year}/rates.json` (HGB-Abzinsungszinssätze, GWG-Grenze, GewSt-Hebesatz)
- `config/{active_year}/kontenrahmen.json` (SKR03/04-Konto-Definitionen)

## 12. Verwandte Skills

- `buchungssatz` — erzeugt den konkreten Buchungssatz (Beträge + Soll/Haben + §-Begründung) zu den hier beschriebenen Vorgängen, plus JSON-Handoff für `datev-export`
- `wiederkehrende-buchungen` — DATEV-Stapel für ARAP-Auflösung u.ä.
- `datev-export` — EXTF-CSV-Stapel für externe Berechnungen (Pension, Urlaub aus HR)
- `monatsabschluss` — Workflow inkl. dieser Buchungen als Teil-Checkliste
- `jahresabschluss` — Workflow Jahresabschluss-Stapel (StB-Übergabe-Pattern)
- `abstimmung` — Konten-Abstimmung Rückstellungs- und RAP-Konten
- `gobd-konformitaet` — Festschreibung, Verfahrensdokumentation, Z1/Z2/Z3
- `steuerberater-handoff` — Strukturierte Übergabe komplexer Sachverhalte
- `ebilanz` — Taxonomie-Mapping der RAP-/Rückstellungs-Positionen
