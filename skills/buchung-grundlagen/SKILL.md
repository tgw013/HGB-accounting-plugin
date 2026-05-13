---
name: buchung-grundlagen
description: Doppik-Grundlagen, GoB/GoBD, Belegpflicht, Aufbewahrungsfristen, SKR03/SKR04-Auswahl. Hintergrundwissen für alle Workflow-Skills.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# Buchung Grundlagen

**Typ:** `knowledge`
**Anthropic-Pendant:** `journal-entry-prep` (Knowledge-Anteil) (siehe [anthropics/knowledge-work-plugins/finance](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance))
 GmbH, UG
**Config:** `config/{active_year}/`

---

## 1. Zweck

Liefert das Hintergrundwissen, das alle Workflow-Skills (`buchungssatz`, `monatsabschluss`, `jahresabschluss`, `ust-voranmeldung`) gemeinsam brauchen: Doppelte Buchführung, GoB/GoBD, Belegpflicht, Konto-Klassen, SKR-Wahl, Aufbewahrung. Wird nicht direkt aufgerufen — Workflows zitieren daraus.

## 2. Doppelte Buchführung (Doppik) — Grundlagen

- **Bilanzgleichung**: Aktiva = Eigenkapital + Fremdkapital
- **Jeder Geschäftsvorfall → mindestens zwei Konten**: Soll an Haben, betragsgleich
- **Bestandskonten** (Bilanz) vs. **Erfolgskonten** (GuV)
- **Aktivkonten**: Zugang im Soll, Abgang im Haben
- **Passivkonten**: spiegelbildlich
- **Aufwand**: zehrt Eigenkapital (Soll mehrt Aufwand)
- **Ertrag**: mehrt Eigenkapital (Haben mehrt Ertrag)

**Saldenmechanik kapitalgesellschaft (GmbH/UG):**
GuV-Saldo (Jahresergebnis) → Eigenkapital. Bei UG zusätzlich Rücklagenpflicht nach § 5a Abs. 3 GmbHG (25% des Jahresüberschusses bis Stammkapital 25.000 € erreicht).

## 3. GoB / GoBD

**Grundsätze ordnungsmäßiger Buchführung** (§§ 238, 239, 257 HGB i.V.m. § 145 ff. AO) und **GoBD** (BMF-Schreiben 28.11.2019):

- **Vollständigkeit** — kein Geschäftsvorfall unbelegt
- **Richtigkeit** — sachliche und rechnerische Korrektheit
- **Zeitgerecht** — laufende Geschäftsvorfälle möglichst zeitnah, Kasse täglich (§ 146 Abs. 1 AO)
- **Ordnung** — systematische Erfassung, klare Belegfolge
- **Unveränderbarkeit** — keine nachträglichen Änderungen ohne Nachvollziehbarkeit ("Festschreibung")
- **Belegfunktion** — "keine Buchung ohne Beleg"
- **Datenzugriff** — Z1 (unmittelbar), Z2 (mittelbar), Z3 (Datenträgerüberlassung) nach § 147 Abs. 6 AO
- **Verfahrensdokumentation** — Pflicht, siehe Skill `gobd-konformitaet`

## 4. Beleg

**Belegpflicht** (§ 257 HGB, GoBD Tz. 61 ff.):
- Eingangsbeleg (Rechnungen, Quittungen, Verträge) oder
- Eigenbeleg (Nachweis mit ausreichender Begründung — Notlösung, nicht Regel)

**Pflichtangaben Rechnung** (§ 14 UStG):
- Name + Anschrift Rechnungssteller + Empfänger
- Steuer-Nr. oder USt-IdNr. Rechnungssteller
- Ausstellungsdatum, fortlaufende Rechnungs-Nr.
- Menge / Art Lieferung / Leistung
- Zeitpunkt Lieferung / Leistung
- Nettobetrag, USt-Satz, USt-Betrag (oder Hinweis auf Steuerbefreiung / § 13b UStG)
- Bei Kleinbetragsrechnung bis 250 € (§ 33 UStDV): vereinfachte Pflichten

**E-Rechnung** (B2B-Pflicht ab 01.01.2025, Übergangsfristen bis 2027/2028 nach Umsatzgröße): strukturiertes Format (XRechnung, ZUGFeRD ab 2.0.1).

## 5. SKR03 vs. SKR04

| Kriterium | SKR03 | SKR04 |
|---|---|---|
| Gliederungsprinzip | **Prozessgliederung** (Geschäftsablauf) | **Abschlussgliederung** (Bilanz-/GuV-Struktur § 266/§ 275 HGB) |
| Klassen 0-9 | nach Prozess (Einkauf, Verkauf, Aufwand, Ertrag) | nach Bilanzposten (Anlage-, Umlaufvermögen, EK, FK, Erlöse, Aufwand) |
| Verbreitung | DATEV-Default historisch, weit verbreitet KMU | Empfohlen DATEV-Standard für Neueinrichtungen, näher an HGB-Bilanzstruktur |
| Beispiel: Erlöse 19% | 8400 | 4400 |
| Beispiel: Bank | 1200 | 1800 |

**Wahl:** Wechsel ist möglich, aber Aufwand. Mandanten-Bestand entscheidet meistens. Neueinrichtung GmbH/UG → SKR04 empfohlen (HGB-näher).

**Konto-Lookups:** alle in `config/{active_year}/kontenrahmen.json`. Workflow-Skills lesen dort, nicht hier.

## 6. Aufbewahrungsfristen (§ 147 AO, § 257 HGB)

**Änderung durch das Vierte Bürokratieentlastungsgesetz** (Stand 2026-05):

| Belegart | Bis 31.12.2024 entstanden | Ab 01.01.2025 entstanden |
|---|---|---|
| **Buchungsbelege** (Rechnungen, Kassenbons, Kontoauszüge) | **10 Jahre** | **8 Jahre** |
| **Handels- und Geschäftsbriefe** | 6 Jahre | 6 Jahre |
| **Jahresabschlüsse, Inventare, Buchungsjournale** | 10 Jahre | 10 Jahre |
| **Lohnkonten** (§ 41 EStG) | 6 Jahre nach Ablauf KJ | 6 Jahre nach Ablauf KJ |

Fristbeginn: Ende des Kalenderjahres, in dem letzter Eintrag / Ausstellung erfolgte. **Bei laufender Betriebsprüfung oder offenen Steuerfestsetzungen: Frist gehemmt.**

## 7. SoLL / HaBen — Merkhilfen

- **S**oll an **H**aben: **S** kommt vor **H** im Alphabet, **S**oll wird also zuerst genannt
- **Aktiv-Konten**: Zugänge **Soll**, Abgänge **Haben**
- **Passiv-Konten**: Zugänge **Haben**, Abgänge **Soll**
- **Aufwand** (zehrt EK): **Soll**
- **Ertrag** (mehrt EK): **Haben**
- **Vorsteuer** (USt-Forderung gegen Finanzamt): **Soll** beim Einkauf
- **USt** (Verbindlichkeit gegen Finanzamt): **Haben** beim Verkauf

## 8. Quellen

- HGB §§ 238, 239, 257, 266, 275 — gesetze-im-internet.de/hgb/
- AO §§ 145–147 — gesetze-im-internet.de/ao_1977/
- GoBD BMF-Schreiben 28.11.2019 — bundesfinanzministerium.de
- UStG § 14 (Rechnungspflichtangaben) — gesetze-im-internet.de/ustg_1980/
- UStDV § 33 (Kleinbetragsrechnungen)
- GmbHG § 5a (UG-Rücklagenpflicht)
- DATEV SKR03 Art.-Nr. 11174, SKR04 Art.-Nr. 11175 (jeweils Stand 2026-01-01)
- `config/{active_year}/rates.json` (Aufbewahrungsfristen, Sätze)
- `config/{active_year}/kontenrahmen.json` (Konto-Definitionen)

## 9. Verwandte Skills

- `buchungssatz` — Workflow: nutzt diese Grundlagen für konkreten Buchungsvorschlag
- `gobd-konformitaet` — Vertieft GoBD-Anforderungen für Verfahrensdokumentation
- `monatsabschluss`, `jahresabschluss` — Workflows mit gleicher Wissensbasis
