---
name: hinschg-meldewesen
description: HinSchG-Pflichten (ab 50 MA) — interne Meldestelle, Fristen, Hinweisgeber-Schutz, Bußgeldrahmen, IKS-Verzahnung.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (HinSchG vom 31.05.2023, Stand 2026-05). **Ersetzt keine Rechtsberatung.** Konkrete Implementierung des Meldekanals und arbeitsrechtliche Konsequenzen mit Datenschutzbeauftragten + Arbeitsrecht-Anwalt abstimmen.

# HinSchG-Meldewesen

**Typ:** `knowledge`
**Anthropic-Pendant:** (kein direktes Pendant)
**Geltungsbereich:** GmbH, UG **ab 50 MA** (Schwellwert HinSchG)
**Config:** —
**Knowledge-Base:** —

---

## 1. Zweck

Erklärt die Pflichten nach dem **Hinweisgeberschutzgesetz** (HinSchG, in Kraft seit 02.07.2023). Plugin ist Knowledge — die tatsächliche Einrichtung eines Meldekanals erfolgt nicht hier; Skill verknüpft mit `iks-pruefung` als Kontroll-Komponente.

## 2. Anwendungsbereich

- **Ab 50 Beschäftigte**: Pflicht zur Einrichtung einer internen Meldestelle (§ 12 HinSchG)
- 50–249 Beschäftigte: gemeinsame Meldestelle mit anderen Unternehmen / Konzern möglich
- < 50 Beschäftigte: keine Pflicht, aber freiwillige Einrichtung erlaubt und empfohlen
- Auch externe Meldestellen beim Bund (BfJ) und Ländern bestehen — Hinweisgeber kann zwischen intern + extern frei wählen (§ 7 HinSchG)

## 3. Materieller Schutzbereich

Geschützte Meldungen betreffen **Verstöße im beruflichen Kontext** (§ 2 HinSchG), u.a.:
- Strafbewehrte Verstöße (Korruption, Betrug, Untreue)
- Bußgeldbewehrte Verstöße (sofern Schutz von Leben, Gesundheit, Rechten)
- Verstöße gegen EU-Recht in definierten Bereichen (Geldwäsche, Datenschutz, Verbraucherschutz, Lebensmittel, Produktsicherheit, Vergabe, Finanzdienstleistungen)
- Verstöße gegen Vorschriften zur Bekämpfung von Steuerhinterziehung bei Körperschaften

## 4. Anforderungen an die interne Meldestelle (§ 13 ff. HinSchG)

- **Eingangsbestätigung** an Hinweisgeber: innerhalb **7 Tagen**
- **Rückmeldung** zu Folgemaßnahmen: spätestens nach **3 Monaten**
- **Vertraulichkeit** der Identität des Hinweisgebers (und ggf. Dritter)
- **Unabhängigkeit** der zuständigen Person (keine Interessenkonflikte)
- **Schriftliche/mündliche** Meldungen ermöglichen, auf Wunsch Treffen
- **Dokumentation** der Meldung (Aufbewahrung 3 Jahre nach Abschluss, § 11 HinSchG)
- **Datenschutzkonforme Verarbeitung** (DSGVO; Datenschutz-Folgenabschätzung empfohlen)

## 5. Schutz des Hinweisgebers (§ 33 ff. HinSchG)

- Verbot von Repressalien (Kündigung, Versetzung, Mobbing, Diskriminierung)
- **Beweislastumkehr**: Repressalie bei zeitlichem Zusammenhang mit Meldung — Arbeitgeber muss Gegenteil beweisen (§ 36)
- Schadensersatzanspruch bei Repressalie (§ 37)

## 6. Bußgelder (§ 40 HinSchG)

| Verstoß | Rahmen |
|---|---|
| Behinderung der Meldung / Repressalie | bis **50.000 €** |
| Verletzung Vertraulichkeitsgebot | bis 50.000 € |
| Keine Einrichtung Meldestelle (ab 50 MA) | bis **20.000 €** |
| Vorsatz / Fahrlässigkeit weiterer Pflichten | bis 10.000 € |

## 7. Implementierungs-Optionen (zur Orientierung)

- **In-House**: Bestellung einer "beauftragten Person" (Compliance, HR, Externe)
- **Externer Ombudsmann** (z.B. spezialisierte Anwaltskanzlei)
- **Software-Lösung** (digitale Plattform mit Anonymisierungs-Option)
- **Konzernlösung** (gemeinsame Meldestelle mehrerer verbundener Unternehmen)

## 8. Verzahnung mit IKS

Whistleblower-Kanal ist Teil der Komponente **"Information + Kommunikation"** im IDW PS 261 / COSO. Skill `iks-pruefung` referenziert.

## 9. Quellen

- HinSchG vom 31.05.2023 (in Kraft 02.07.2023) — gesetze-im-internet.de/hinschg/
- EU-Whistleblower-Richtlinie 2019/1937
- BfJ-Informationen zu externer Meldestelle: bundesjustizamt.de
- DSGVO Art. 6, Art. 35 (DSFA)

## 10. Verwandte Skills

- `iks-pruefung` — Whistleblower-Kanal als Kontroll-Element
- (alle Workflow-Skills nur indirekt, kein Buchungs-Berührungspunkt)
