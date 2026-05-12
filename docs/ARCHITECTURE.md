# Architektur (v2.0)

## Designprinzipien

1. **Knowledge ≠ Workflow.** Inspiriert von Anthropic's Original-Finance-Skill: Hintergrundwissen ist eine eigene Skill-Klasse, Workflows greifen darauf zu — keine Vermischung.
2. **Quellen-Treue.** Jeder Konto-Vorschlag, jeder KZ-Code, jede Frist hat einen Verweis auf eine Primärquelle. Sekundärliteratur ist Hilfsmaterial, keine Belegquelle.
3. **Mehrjahres-Kompatibilität.** Alles Jahres-abhängige liegt in `config/{jahr}/`. Skills referenzieren `{active_year}`, nie hardcoded 2026.
4. **Disclaimer als Diktat.** Kein produktiver Output ohne `⚠ Hinweis`-Block. Plugin ist Hilfsmittel, nicht StB-Ersatz.
5. **Enger Geltungsbereich, breiter Bauplan.** Default GmbH+UG, aber Struktur erlaubt Erweiterung ohne Re-Architektur.

## Verzeichnisstruktur

```
.claude-plugin/plugin.json     Plugin-Manifest (Name, Version, Author, Apache-2.0)
.mcp.json                      MCP-Server-Konfiguration (z.Z. leer; planned_integrations dokumentiert)
LICENSE                        Apache 2.0
README.md                      Einstiegspunkt für Anwender
CONTRIBUTING.md                Beitrags-Regeln
CHANGELOG.md                   Versions-Historie
UPDATE_CHECKLIST.md            Jährliche Update-Routine

config/
  active-year.json             Pointer auf aktives VZ
  shared/
    formats.json               Output-Format-Definitionen (DATEV-CSV, Excel, Handoff-Brief)
    entity-types.json          Rechtsformen-Scoping (in_scope vs out_of_scope_extensible)
  2025/README.md               (Stub — bei Bedarf befüllen)
  2026/
    rates.json                 Sätze, BBG, Pauschalen, Freigrenzen
    kontenrahmen.json          SKR03 (63) + SKR04 (69) verifiziert gegen DATEV
    kz-codes-ust-va.json       Verbatim BMF USt 1 A 2026
    fristen.json               Konsolidierter Fristen-Kalender
  2027/README.md               (Stub)

docs/
  ACCOUNTING_REVIEW_FIRST_PASS.md  v1-Audit-Journey
  CHANGES_APPLIED.md               v1-Per-File-Diff
  xref-ledger.md                   v1-Cross-Reference (PRE-FIX-Snapshot)
  USAGE.md                         Nutzungs-Hinweise
  OPEN_QUESTIONS.md                Offene Rechtsfragen (z.B. § 264a HGB / eGbR)
  ISSUES_LOG.md                    Bekannte Issues
  INTERNAL_README.md               Interne Notizen
  PROVENANCE.md                    Herkunft des Forks
  SECURITY_REVIEW.md               IT-Security-Review
  CONNECTORS.md                    MCP-Connector-Evaluierung
  RECOMMENDATIONS.md               Empfehlungen
  ARCHITECTURE.md                  (diese Datei)
  SCOPE.md                         Geltungsbereich-Details
  SOURCES.md                       Primärquellen-Liste

skills/
  buchung-grundlagen/    knowledge — Doppik, GoBD, SKR-Auswahl
  buchungssatz/          workflow  — Beleg → Buchungsvorschlag
  monatsabschluss/       workflow
  ust-voranmeldung/      workflow
  lohnabrechnung/        workflow
  jahresabschluss/       workflow
  ebilanz/               workflow
  abstimmung/            workflow
  abweichungsanalyse/    workflow
  gobd-konformitaet/     knowledge
  iks-pruefung/          methodology
  hinschg-meldewesen/    knowledge
  datev-export/          workflow
  steuerberater-handoff/ workflow

commands/                Slash-Command-Stubs (1:1 zu Skills wo passend)
tests/scenarios/         Realistische Buchungs-Szenarien (P8)
```

## Skill-Klassen

- **knowledge** — Erklärt Sachverhalt, liefert Hintergrundwissen, keine Output-Erzeugung. Beispiele: `buchung-grundlagen`, `gobd-konformitaet`, `hinschg-meldewesen`.
- **workflow** — Nimmt Input, produziert konkretes Artefakt (Buchungssatz, CSV, Brief). Beispiele: `buchungssatz`, `datev-export`, `monatsabschluss`.
- **methodology** — Strukturiertes Vorgehen, oft iterativ, Output ist Prüfungs-/Analyse-Bericht. Beispiel: `iks-pruefung`.

## Datenfluss

```
User-Input ──► Workflow-Skill ──► nutzt Knowledge-Skill ──► liest config/{active_year}/
                    │
                    ├──► Output Markdown (default)
                    ├──► Output DATEV-CSV (über datev-export)
                    ├──► Output Excel (über shared/formats.json-Definition)
                    └──► Output StB-Handoff-Brief (über steuerberater-handoff)
```

## Konfig-Auflösung

Skills referenzieren Werte als `config/{active_year}/<file>.json`. Default-Jahr in `config/active-year.json`. Wechsel des aktiven Jahres ist ein bewusster Schritt, nicht automatisch (siehe `UPDATE_CHECKLIST.md`).

## MCP-Integration (geplant)

`.mcp.json` ist Platzhalter. Planned:
- `datev_finrobotics` (Read-only EXTF-Import) — Phase 1
- `datev_badrix` (Read+Write, EXTF-Export für DATEV-Import) — Phase 2, mit OS-Sandbox
- `bank_hbci` — HBCI/FinTS für Bank-Ingestion — Phase 3
- `elster` — XML-Vorbereitung (kein Direktversand!) — Phase 4

Siehe `docs/CONNECTORS.md` für Security-Evaluierung der Kandidaten.

## Test-Strategie (P8, ausstehend)

`tests/scenarios/` enthält realistische Geschäftsvorfälle als Markdown-Triplet: Input, erwarteter Buchungsvorschlag, Begründung mit §-Verweisen. Manuelle Regression bei jedem Skill-Refactor.
