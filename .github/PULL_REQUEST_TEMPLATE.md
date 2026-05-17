<!--
Danke für deinen Beitrag! Bitte fülle die relevanten Sektionen aus.
Pflichtfelder sind mit (Pflicht) markiert.
-->

## Art der Änderung (Pflicht)

- [ ] Bug-Fix (Plugin verhält sich nicht wie dokumentiert)
- [ ] Accounting-Korrektur (Konto / KZ / § / Frist / Wert)
- [ ] Neuer Skill / Command (Erweiterung)
- [ ] Doku-Verbesserung
- [ ] Refactor (kein funktionaler Effekt)
- [ ] Tests / Szenarien
- [ ] Anderes: ...

## Beschreibung (Pflicht)

Was ändert sich und warum?

## Verifikations-Diff (Pflicht bei Accounting-Korrekturen)

Bei jeder Änderung an Konto-Nummern, KZ-Codes, §-Verweisen oder Werten:

| Datei | Feld | v_alt | v_neu | Primärquelle |
|---|---|---|---|---|
| `config/2026/kontenrahmen.json` | SKR04 → 1247 → bezeichnung | "..." | "..." | DATEV SKR04 PDF 2026, S. NN |

Siehe `CONTRIBUTING.md` für Quellen-Treue-Regeln. Primärquelle ist Pflicht — keine Sekundärliteratur, keine Beraterportale, kein Lehrbuch.

## Geltungsbereich (Pflicht)

[ ] In Scope: GmbH, UG
[ ] Erweitert Scope auf: ...  → habe `config/shared/entity-types.json` + Skill-Frontmatter aktualisiert
[ ] Out of Scope, nur dokumentiert (kein Code-Effekt)

## Tests / Szenarien

[ ] Bestehende Szenarien in `tests/scenarios/` laufen unverändert durch
[ ] Neues Szenario hinzugefügt: `tests/scenarios/...md`
[ ] Manuell verprobt mit Claude (welches Modell, welcher Input): ...
[ ] Nicht testbar (z.B. reine Doku-Änderung)

## Disclaimer-Block

[ ] Der `⚠ Hinweis:`-Block am Skill-Anfang bleibt unverändert (oder wurde nur sprachlich verbessert, ohne den Vorbehalt zu verwässern)

## Personenbezogene Daten

[ ] Keine personenbezogenen Daten (Namen, Mandantendaten, reale Beträge aus konkreten Fällen) in Code, Tests oder Beispielen
