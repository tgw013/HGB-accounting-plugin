# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/) · Versionierung: [SemVer](https://semver.org/)

## [2.3.0] - 2026-05-23

### Added
- **Automatikkonten-Schutz** (PRD §14.2). Plugin lehnt vor dem CSV-Export Buchungen ab, in denen ein AM- oder AV-Automatikkonto mit einem nicht-leeren BU-Schlüssel verwendet wird (außer BU `"0040"` Aufhebung der Automatik). Fängt DATEV-Importfehler **REW00305** vorab ab.
- `config/shared/datev-automatik-konten.json` — auto-generated Automatik-Set für SKR03 + SKR04 (163 + 163 Konten, AM- und AV-Prefix der DATEV-Programmverbindung). DATEV-copyright-safe (nur Konto-Nummern, keine Bezeichnungen).
- `scripts/generate_automatik_konten.py` — generiert die obige JSON-Datei aus den `.skr0[34]-clean.tsv`-Extraktionen. Re-run-fähig bei jedem DATEV-PDF-Jahresupdate.
- **Multi-Formatkategorie-Routing-Seam** in `scripts/generate_extf.py`. v2.3 unterstützt nur `formatkategorie=21` (Buchungsstapel); Wiederkehrende (65) kommt in v2.5, Debitoren/Kreditoren (16) in v2.7. Klare Fehlermeldung bei nicht-unterstützten Kategorien.
- `scripts/extract_datev_pdf.py` (v5): erfasst jetzt zusätzlich den Programmverbindungs-Prefix (AM/AV/S/F/R/...). Output-TSV hat neue 4. Spalte `pv_prefix`.

### Changed
- `skills/datev-export/SKILL.md`: neue §11.1 "Automatikkonten-Schutz" mit Beispiel-Fehlermeldung.
- Sidecar `.report.md` listet jetzt ob Automatikkonten verwendet wurden (auch ohne BU-Clash, zur Audit-Sichtbarkeit).
- Test-Suite: 62 → 69 Tests (7 neue für Automatik-Check + Routing-Seam). Coverage stabil bei 92 %.

### Notes
- v2.3 ist die kleinste der vier geplanten Folge-Releases (PRD §14). Nächste: v2.5.0 (Wiederkehrende Buchungen), v2.6.0 (KOST-Splitt), v2.7.0 (Debitoren/Kreditoren).
- "S"-Prefix-Konten (Sammelkonten wie Debitoren-Sammel 1200, Vorsteuer-Sammel 1406) sind **bewusst NICHT** als Automatik geflagged — sie folgen anderen Regeln (z.B. direkte Buchung auf Sammelkonto generell unzulässig, aber das ist nicht REW00305).
- Wenn `config/shared/datev-automatik-konten.json` fehlt: Plugin läuft weiter, der Automatik-Check ist dann no-op (soft-degrade). Vorteil: Backward-compat für ältere Setups.

## [2.1.0] - 2026-05-22

### Added
- `scripts/generate_extf.py`: deterministic Python serializer for DATEV-EXTF-Buchungsstapel Formatversion 13
- `config/shared/datev-extf-fields.json`: declarative 31-header + 125-data field inventory per Formatversion, source-tagged to developer.datev.de
- `tests/test_extf_serializer.py`: round-trip, determinism, validation, portal-inconsistency, and synthetic-fixture tests (60 tests, 92% line coverage on the serializer)
- Sidecar `.report.md` output alongside every generated CSV (SHA-256, saldo check, account validation, portal-inconsistency deviations applied, Formatversion targeted)
- Support for Generalumkehr (field #118) via optional `generalumkehr: true` in input JSON Buchungen
- Documented interpretation rules for four [PORTAL-INCONSISTENT] cases (Skontosperre, BVV-Position, Generalumkehr, Header Formatversion)

### Changed
- `skills/datev-export/SKILL.md`: new §6.5 "Implementation" section documenting Bash invocation pattern; new §12 "Determinism guarantee"
- EXTF generation is now deterministic: previously Claude generated CSV inline, now `datev-export` skill delegates to `scripts/generate_extf.py`
- Buchungsstapel default target version is now Formatversion 13 (introduced by DATEV February 2024 per portal Changelog)

### Notes
- Formatversionen 10/11/12 backward-compatibility is planned for v2.4.0, only if a Sealogy-specific Steuerberater requires it
- DATEV-Format-Prüfprogramm CI integration (PRD §14.1 / v2.2.0) **deferred indefinitely**. Three unresolvable design blockers: (a) DATEV-Lizenz makes EXE redistribution legally fuzzy, (b) GitHub-Actions secrets capped at 64 KB vs. 314 KB EXE, (c) GUI-subsystem EXE has no parseable exit code. For a solo-maintainer project, manual run via `scripts/run_pruefprogramm.ps1` as a release-gate (see `UPDATE_CHECKLIST.md` §9) provides the same protection at zero infrastructure cost. Re-evaluation trigger: first external contributor PR that touches `scripts/generate_extf.py`.
- No new pip dependencies; Python 3.10+ stdlib only
- Anlagenverwaltung-internal logic and DATEV LODAS are explicitly NOT addressable via this serializer (they are not part of DATEV-Format)

## [2.0.1] — 2026-05-17 — Public-launch readiness

Pre-public-release audit. No functional skill/command changes — purely repo hygiene.

### Removed
- `docs/INTERNAL_README.md` (explicitly internal framing)
- `docs/ISSUES_LOG.md` (empty template)
- `.mcp.json` `see_also` references to private `-internal` MCP repos

### Moved
- 5 v1.x historical artifacts → `docs/archive/` (with archive README explaining context)

### Changed
- `docs/SECURITY_REVIEW.md`: historical-reference banner; clarifies v2.0 rewrite was not re-audited at the file level
- `docs/PROVENANCE.md`: added "v2.0 rewrite audit" section with diff stats (-3,289 net lines vs upstream) + Commons Clause / Apache 2.0 reasoning
- `skills/steuerberater-handoff/SKILL.md`: example name placeholder genericised
- All repo URL refs updated `HGB-accounting-plugin-internal` → `HGB-accounting-plugin` (repo renamed)
- Git history scrubbed: personal/work emails replaced with GitHub noreply across all 35 commits

### Added
- `SECURITY.md` (vulnerability disclosure via GitHub Security Advisory)
- `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1)
- `.github/ISSUE_TEMPLATE/bug-report.md` + `accounting-correction.md`
- `.github/PULL_REQUEST_TEMPLATE.md` with verification-diff requirement

### Verified
- gitleaks: clean (35 commits, ~733 KB)
- trufflehog: clean (0 verified, 0 unverified secrets)

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
