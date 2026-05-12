# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/) · Versionierung: [SemVer](https://semver.org/)

## [2.0.0] — 2026-05-12

Merged from `v2-redesign` branch. Drops `-alpha` suffix; promoted to `main`
without further structural change (alpha-tag was conservative naming for the
in-development branch).

Plus: LICENSE copyright updated to current author (tgw013); upstream lineage
acknowledgment moved to `docs/PROVENANCE.md` per Apache-2.0 attribution guidance.

## [2.0.0-alpha] — 2026-05-12 (Branch `v2-redesign`, superseded by 2.0.0)

### Added
- **Multi-Jahres-Config-Struktur**: `config/{2025,2026,2027}/` mit `active-year.json`-Pointer
- **Shared Config**: `config/shared/{entity-types,formats}.json` für rechtsformübergreifende Definitionen
- **Verbatim BMF-Quellen**: `config/2026/kz-codes-ust-va.json` (USt 1 A 2026), `fristen.json` (konsolidierter Frist-Kalender)
- **Neue Skills (Skeleton)**: `buchung-grundlagen`, `datev-export`, `gobd-konformitaet`, `hinschg-meldewesen`, `steuerberater-handoff`
- **Doku-Set**: README (DE+EN-Overview), CONTRIBUTING, ARCHITECTURE, SCOPE, SOURCES, UPDATE_CHECKLIST

### Changed
- **Restrukturierung**: Top-Level v1-Audit-Artefakte → `docs/`
- **plugin.json**: `v2.0.0-alpha`, Apache-2.0 (Commons Clause entfernt), Autor `tgw013`
- **Geltungsbereich**: Bewusst eng auf GmbH + UG (architektonisch erweiterbar — siehe `docs/SCOPE.md`)
- **Skill-Aufteilung**: Knowledge/Workflow-Trennung als Designprinzip (Inspiration: Anthropic Original)
- **`compliance`-Skill**: aufgeteilt in `gobd-konformitaet`, `iks-pruefung`, `hinschg-meldewesen`
- **`buchungssatz-vorbereitung`**: umbenannt zu `buchungssatz`

### Removed
- Commons Clause aus LICENSE (jetzt reines Apache-2.0)

---

## [1.1.0] — 2026-05 (Branch `main`)

### Praxis-Readiness
- Frontmatter-Normalisierung über alle Skills/Commands
- Runtime-Disclaimer-Block in allen Skills (`⚠ Hinweis`)
- Prominenter GbR/MoPeG-Warnhinweis (offen: § 264a HGB-Anwendbarkeit auf eGbR)
- Doku-Pflege: `USAGE.md`, `OPEN_QUESTIONS.md`, `ISSUES_LOG.md`

### DATEV-2026 Re-Sync
- 16 Files gefixt nach systematischem Abgleich gegen DATEV SKR03/04 PDFs Art.-Nr. 11174/11175
- ~25 fehlerhafte Konto-Referenzen korrigiert (u.a. 0961, 0963, 0956, 4165, 4167; SKR04: 3079, 3040, 3035, 6140, 6147, 6923)
- bAV-Konten verifiziert: SKR03 4165/4167, SKR04 6140/6147 (§3 Nr. 63 EStG)
- EWB/PWB-Konten verifiziert: SKR04 1246/1247 (EWB), 1248/1249 (PWB), 6920 (PWB Einstellung), 6923 (EWB Einstellung)
- USt-VA KZ-Codes 2026 gegen BMF-Vordruckmuster USt 1 A 2026 verifiziert

### Documentation
- `ACCOUNTING_REVIEW_FIRST_PASS.md` mit 4 Addenda (Verify-Journey)
- `CHANGES_APPLIED.md` mit Per-File-Diff-Tabelle
- `xref-ledger.md` als PRE-FIX-Snapshot getaggt

---

## [1.0.0] — 2026-04

- Initial Internal Fork, IT-Security-Review abgeschlossen
- Erste SKR03/04-Kontenrahmen-Integration, KZ-Code-Mapping
