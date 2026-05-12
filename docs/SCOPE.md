# Geltungsbereich (Scope)

## In Scope (verifiziert, produktiv vorgesehen)

| Rechtsform | Begründung |
|---|---|
| **GmbH** | Häufigste Kapitalgesellschaft KMU, klares HGB-Regelwerk (§ 264 ff.), KStG-pflichtig, eindeutige DATEV-Praxis |
| **UG (haftungsbeschränkt)** | Sonderform der GmbH, identische Buchhaltungslogik, Rücklagenpflicht § 5a Abs. 3 GmbHG ergänzt |

## Out of Scope (architektonisch erweiterbar)

| Rechtsform | Warum nicht jetzt |
|---|---|
| **AG / SE** | Kommt selten bei KMU; ergänzende Pflichten (Aufsichtsrat, Vergütungsbericht, Corporate-Governance-Kodex) erfordern separates Knowledge-Modul |
| **KGaA** | Sehr selten; Mischform-Komplexität |
| **GmbH & Co. KG** | Mischrechtsform-Logik (Kapges + Persges-Steuerung), gesonderte Ergebnisverteilung, Sonderbilanzen — eigene Skill-Familie nötig |
| **OHG / KG** | Personengesellschafts-Spezifika (§ 5 EStG-Gewinnermittlung, Sondervergütungen § 15 Abs. 1 Nr. 2 EStG, Ergänzungsbilanzen) |
| **eGbR / GbR (mit MoPeG)** | § 264a HGB-Anwendbarkeit auf eingetragene GbR ist Stand 2026-05 **offen** — siehe [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md). Bewusst nicht im Default-Scope. |
| **Einzelunternehmen / Freiberufler** | EÜR-Logik statt Bilanz; eigenständige Skill-Familie |
| **Vereine / Stiftungen / gGmbH** | Gemeinnützigkeitsrecht (§§ 51 ff. AO), Mittelverwendungsrechnung, Sphärentheorie — eigene Komplexität |

## Erweiterungs-Mechanik

Wer eine Rechtsform ergänzen möchte:

1. `config/shared/entity-types.json`: Eintrag von `out_of_scope_extensible` → `in_scope` ändern
2. Pro betroffenem Skill `Geltungsbereich:`-Zeile im Frontmatter erweitern
3. Rechtsform-spezifische Sektion im Skill ergänzen (oder neuen Skill anlegen)
4. Test-Szenario in `tests/scenarios/` hinzufügen
5. PR mit Verifikations-Diff (siehe `CONTRIBUTING.md`)

## Funktional in Scope

- Laufende Buchhaltung (Buchungssatz-Vorschläge SKR03/04)
- Monatsabschluss (Kontenabstimmung, Abgrenzungen)
- USt-Voranmeldung Vorbereitung (BMF-Formular USt 1 A)
- Lohnabrechnung (Geschäftsführer-Gehalt, Mitarbeiter, Minijob, Midijob)
- Jahresabschluss-Aufstellung (Bilanz, GuV, Anhang nach HGB)
- eBilanz-Datenpaket-Vorbereitung
- Konten-Abstimmung (Bank, OP-Debitoren/Kreditoren, EWB/PWB)
- Abweichungsanalyse / Plan-Ist-Vergleich
- GoBD-Konformitäts-Prüfung
- IKS-Bewertung nach IDW PS 261
- HinSchG-Pflichten (ab 50 MA)
- DATEV-Buchungsstapel-CSV-Export
- Steuerberater-Handoff-Brief

## Funktional out of Scope

- **Direkter ELSTER-Versand** — Verantwortung bleibt beim Anwender / StB
- **Direkte Bundesanzeiger-Offenlegung** — gleicher Grund
- **Direkter eBilanz-XBRL-Versand** — Datenpaket-Vorbereitung ja, Übermittlung nein
- **Steuerberatung im Sinne des StBerG** — Plugin liefert Vorschläge, keine Beratung
- **Wirtschaftsprüferische Bestätigung** — keine Prüfungs-Aussage
- **Rechtsberatung** — keine Aussagen zu Vertragsgestaltung, Gesellschaftsrecht über das HGB-Buchführungs-Maß hinaus
- **Steuerberechnung mit Bindungswirkung** — Berechnungs-Hilfen ja, finale Steuerbescheide nein
