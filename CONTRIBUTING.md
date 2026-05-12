# Contributing

Beiträge willkommen. Dieses Plugin lebt davon, dass Anwender mit StB-Hintergrund oder DATEV-Erfahrung Quellen-Verweise verifizieren und Verbesserungen vorschlagen.

## Bevor du einen PR öffnest

1. **Quellen-Treue**: Jede §-Angabe, jeder Konto-Nummer-Vorschlag und jeder KZ-Code muss gegen eine **Primärquelle** prüfbar sein:
   - HGB/EStG/UStG/KStG/SGB → `gesetze-im-internet.de`
   - DATEV-Kontenrahmen → DATEV-PDF Art.-Nr. 11174 (SKR03) / 11175 (SKR04)
   - USt-VA KZ-Codes → BMF-Vordruckmuster USt 1 A des betroffenen Jahres
   - BMF-Schreiben → bundesfinanzministerium.de
   - Sozialversicherung → BMAS / DRV / GKV-Spitzenverband
2. **Stand-Angabe** in der Änderung: "verifiziert gegen X vom YYYY-MM-DD".
3. **Multi-Jahres-Korrektheit**: Wenn ein Wert jahres-abhängig ist (Sätze, BBG, Mindestlohn), Änderung in `config/{year}/`, nicht hardcoded in Skill.
4. **Disclaimer-Diktat respektieren**: Der `⚠ Hinweis`-Block am Skill-Anfang bleibt — kein Output ohne Vorbehalt.

## Geltungsbereich

Default-Scope ist GmbH + UG (siehe [docs/SCOPE.md](docs/SCOPE.md)). PRs, die andere Rechtsformen ergänzen, sind willkommen, müssen aber:

- Skill-Frontmatter mit `Geltungsbereich:` erweitern
- `config/shared/entity-types.json` entsprechend pflegen
- Rechtsformspezifische Besonderheiten dokumentieren (z.B. § 264a HGB-Anwendbarkeit auf eGbR ist noch offen — siehe [docs/OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md))

## Verifikations-Diff

Bei Änderungen an Konten-Nummern oder KZ-Codes: vorher/nachher-Tabelle im PR-Body. Beispiel:

| Konto | v_alt | v_neu | Quelle |
|---|---|---|---|
| 4165 | bAV (falsch) | bAV §3 Nr. 63 EStG | DATEV SKR03 PDF 2026, S. 47 |

## Tests

`tests/scenarios/` enthält (perspektivisch) realistische Buchungs-Szenarien. Neue Skills sollten mindestens 1-2 Szenarien mitliefern.

## Code of Conduct

Respektvoll. Konstruktiv. Annahme: Beitragende handeln in guter Absicht.

## Lizenz für Beiträge

Mit dem Einreichen eines PR stimmst du zu, dass dein Beitrag unter Apache-2.0 lizenziert wird (Inbound = Outbound).
