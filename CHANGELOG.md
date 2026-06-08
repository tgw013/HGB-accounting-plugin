# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/) · Versionierung: [SemVer](https://semver.org/)

## [2.7.2] - 2026-06-08

### Fixed
- **Serializer-Aufruf pfad-robust** in `datev-export` (§ 6.5) und `wiederkehrende-buchungen`: bisher wurde `generate_extf.py` per relativem `scripts/...`-Pfad aufgerufen, der nur aufgeht, wenn das Arbeitsverzeichnis zufällig der Plugin-Root ist (i. d. R. nicht der Fall). Jetzt wird der Plugin-Root explizit aufgelöst (`${CLAUDE_PLUGIN_ROOT}` in Claude Code bzw. absoluter Plugin-Ordner in Cowork) und das Script über absoluten Pfad aufgerufen. Das Script ist self-locating (Config über `__file__`), läuft also von jedem Arbeitsverzeichnis.

### Notes
- Reine Instruktions-/Doku-Härtung; Serializer-Code unverändert. Hintergrund: `${CLAUDE_PLUGIN_ROOT}` expandiert in SKILL.md nicht zuverlässig (claude-code Issue #9354), daher zusätzlich explizite Lokalisierungs-Anweisung an das Modell.

## [2.7.1] - 2026-06-08

### Fixed
- **Release-Bundle:** `scripts/generate_extf.py` wird jetzt in der Cowork-Release-ZIP mitgeliefert. `datev-export` ruft den Serializer zur Laufzeit (deterministische, 125-Feld-validierte EXTF-CSV); fehlte er im Bundle (so bei v2.1.0–v2.7.0), fiel Cowork auf inline-CSV-Generierung zurück. Das Script ist Python-3.10-stdlib-only und findet seine Config (`config/shared/datev-extf-fields.json` + `datev-automatik-konten.json`) selbst über `__file__` — beides ist bereits im Bundle. README-Zip-Anleitung + `UPDATE_CHECKLIST.md` entsprechend ergänzt.

### Notes
- Reine Packaging-Korrektur; Plugin-Code unverändert ggü. v2.7.0. Patch-Release, weil das v2.7.0-Release-Asset wegen GitHub-Immutability nicht nachträglich ersetzbar war.

## [2.7.0] - 2026-06-08

### Added
- **`bwa-kommentierung`** — neuer Skill (deutsches Pendant zu Anthropic `financial-statements`, Kommentierungs-Teil). Erzeugt aus einer DATEV-BWA (Form 01/04/05) eine kanonische GuV-Markdown-Tabelle, Kennzahlen-Übersicht (Margen-Kaskade, Cash-Conversion), Tabelle materieller Abweichungen mit Treiber-Hypothesen und Folgefragen; delegiert die Tiefen-Decomposition (Preis/Menge/Mix) an `abweichungsanalyse`. Inkl. Referenz-Material (§ 266/§ 275 HGB, DATEV-BWA-Formen, Cashflow E-DRS 28/DRS 21). + `commands/bwa-kommentierung.md`. Frontmatter als echter YAML-Block.
- **`buchungssatz`** zweiter Output: strukturierter **JSON-Handoff** (`{ "skr", "buchungen": [...] }`) neben dem lesbaren Buchungsvorschlag — von `datev-export`/`scripts/generate_extf.py` ohne Transformation in die EXTF-CSV überführbar. Plus Vorgang-Katalog (Abschlussbuchungen SKR04) und 3 durchgerechnete Beispiele (ARAP-Bildung, Urlaubsrückstellung-Splitt, § 13b Reverse Charge).
- `skills/datev-export/SKILL.md` § 2.1 — kanonisches Eingabe-Schema (beidseitiger Vertrag mit `buchungssatz`): Feld-Keys, `skr`→Sachkontenrahmen-Mapping, `__`-Felder werden verworfen, § 13b-Zwei-Zeilen-Fall.

### Changed
- **`buchungssatz`** deckt jetzt Einzelbelege **und** Abschluss-/Abgrenzungsvorgänge ab (RAP § 250, Rückstellungen § 249, Auflösungen) — deutsches `journal-entry`-Pendant zu `journal-entry-prep`. Modus-Routing erkennt Beleg vs. Abschlussbuchung automatisch.
- **`buchung-grundlagen`** auf `journal-entry-prep`-Stil umgestellt: beschreibt die Abschlussbuchungs-Vorgänge als konzeptionelle Soll/Haben-Muster (Bewertung, HGB-vs-Steuerbilanz, DATEV-Praxis). Die ausgerechneten Beispiel-Buchungssätze entfernt (Entdoppelung gegen `buchungssatz`). Description, Command und README-Zeile angepasst.
- README: 16 Skills / 16 Commands; Mapping-Tabellen ergänzt (`bwa-kommentierung` ← `financial-statements`; `wiederkehrende-buchungen` ergänzt).

### Fixed
- **EXTF-Saldo-Invariante** (`scripts/generate_extf.py` `validate_saldo`): Eine vollständige Zeile mit `konto` **und** `gegenkonto` ist in sich ausgeglichen (Konto = Soll-Seite, Gegenkonto = Haben-Seite) und benötigt keine separate Gegenbuchung; `gegenkonto` darf bei echten Splittsatz-Teilzeilen leer sein. Eine normale Einzelbuchung läuft jetzt durch — **ohne** künstliche Spiegelzeile, die beim Mandanten-Import doppelt buchen würde. Fixtures `eu_13b`/`automatik_erloese`/`kost_splitt_miete` import-korrigiert (Spiegelzeilen entfernt).
- Test-Suite: 87 → 88 Tests; angepasst an die neue Saldo-Semantik (leeres Gegenkonto für Unbalanced-Test, Zeilenanzahl `kost_splitt`-Fixture, neuer Einzelbuchungs-Test).

### Notes
- Debitoren/Kreditoren (Formatkategorie 16), in v2.5/v2.6 für v2.7 vorgemerkt, ist auf eine spätere Release verschoben.
- Der EXTF-Saldo-Fix ist `[REASONED]` (Korrektur der Plugin-internen Balance-Prüfung), kein Portal-Pattern. Output-CSV bleibt 100 % Buchungsstapel-konform. DATEV-Prüfprogramm (`scripts/run_pruefprogramm.ps1`) nach der `eu_13b`-Fixture-Änderung erneut gegenprüfen (benötigt DATEV-Tool + Windows).

## [2.6.0] - 2026-05-23

### Added
- **KOST-Splitt** (PRD §14.5) — eine Buchung kann jetzt über mehrere Kostenstellen verteilt werden via `kost_allocations`-Array im Input-JSON. Der Serializer expandiert eine Quell-Buchung in N flache Buchungen mit proportionalem Umsatz, gemeinsamen `konto`/`gegenkonto`/`belegfeld_1`/`buchungstext` und je eigener `kost1`/`kost2`/`kost_menge`. Use-Case: 1000 € Miete aufgeteilt 40 % Vertrieb / 30 % Verwaltung / 30 % F&E in einer Eingabe statt drei copy-paste-Buchungen.
- `scripts/generate_extf.py`:
  - `expand_kost_allocations(buchungen) → (expanded, audit)` — Expansion vor Saldo- und Automatik-Check, validiert `Σ anteil_prozent == 100,00` exakt, rechnet jede Allocation via `Decimal` + `ROUND_HALF_EVEN`, verteilt Rundungs-Residual auf die letzte Allocation für cent-exakte Summe.
  - `_format_splitt_audit_block()` — neue Sidecar-Report-Sektion `## KOST-Splittbuchungen (v2.6)` mit Quell-Buchung + Allocations-Breakdown (Anteil %, Cent-Betrag pro Kostenstelle).
  - Backwards-kompatibel: Buchungen ohne `kost_allocations` (flache `kost1`/`kost2`/`kost_menge`-Felder) bleiben unverändert.
- `tests/fixtures/kost_splitt_miete/input.json` — Miete 04/2026 1000 € auf VERTRIEB/VERWALTUNG/FundE (40/30/30) gesplittet plus balancing H-Buchung gegen Kreditor.
- `tests/test_extf_serializer.py` `TestKostSplitt` — 6 neue Tests: 2-way 50/50, 3-way 33,33/33,33/33,34 mit Residual-auf-Letzter, anteil-Sum ≠ 100 wird abgelehnt, Saldo-Check stimmt nach Expansion gegen die H-Seite, Flat-KOST-Backwards-Compat, synthetische Fixture round-trip.

### Changed
- `skills/datev-export/SKILL.md` — neue §6.7 "KOST-Splitt mit `kost_allocations`" mit Input-Schema-Beispiel + Rundungs-Semantik.
- Test-Suite: 81 → 87 Tests (+6). Coverage stabil ≥ 90 %.

### Notes
- v2.6 ist explizit `[REASONED]` (Input-Schema-Design-Entscheidung), nicht `[PORTAL]` — DATEV publiziert kein Multi-Allocation-Pattern. Die Output-CSV bleibt 100 % Buchungsstapel-konform (jede expandierte Allocation ist eine ordentliche Buchungsstapel-Zeile mit KOST1/KOST2/Umsatz).
- Saldo-Check läuft NACH Expansion: die N expandierten S-Zeilen summieren cent-exakt zur Original-Umsatz und balancieren weiterhin gegen die H-Seite.
- Nächste geplante Release per PRD §14: v2.7.0 (Debitoren/Kreditoren — recommended deferred bis konkreter Use-Case bestätigt).

## [2.5.0] - 2026-05-23

### Added
- **Wiederkehrende Buchungen** (PRD §14.4) — Formatkategorie 65, Formatversion 4. Serien-Definition für monatlich/quartalsweise wiederkehrende Buchungen (Beitragsüberträge, Bestandsprovisionen, Miete, etc.). Typische Anwendungsfälle: monatliche Bestandsprovisionen + quartalsweise Beitragsüberträge.
- `config/shared/datev-extf-fields.json` Section `wiederkehrende_buchungen.4` — 101 Felder verbatim aus developer.datev.de Portal (Cross-Reference: `Format_Wiederkehrende Buchungen.xml` im DATEV-Prüfprogramm). Plus 3 Portal-Inkonsistenz-Interpretationsregeln dokumentiert (Felder #4 Soll/Haben, #81 Zeitintervallart, #97 Generalumkehr — alle Character-Class-zu-Alternation).
- `scripts/generate_extf.py`:
  - Formatkategorie-Routing erweitert: `{21, 65}` unterstützt; `16` (Debitoren/Kreditoren) kommt in v2.7
  - `_make_wiederkehrend_field_handlers()` (101 Handler) + `build_data_row_wk()` + `build_column_header_row_wk()` parallel zu den Buchungsstapel-Varianten
  - Spezielle Formatter: `_format_belegfeld_wk` (strikter als Buchungsstapel — verbietet `& * +`), `_format_zeitintervallart` (Portal-Typo-Interpretation), `_format_beginndatum_wk` (TTMMJJJJ quoted), `_format_endetyp` (1/2/3)
  - WK-spezifisch: kein Saldo-Check (WK ist Serien-Spec, nicht balanced Stapel); auto-Normalisierung von Formatname + Formatversion via `FORMATKATEGORIE_META`-Lookup wenn nicht explizit angegeben
- `skills/wiederkehrende-buchungen/SKILL.md` + `commands/wiederkehrende-buchungen.md` — neue Skill + Command für den WK-Workflow, inkl. expliziter Unterscheidung zu Buchungsstapel
- `tests/fixtures/wiederkehrend_premium_accrual/input.json` — Monats-Beitragsübertrag + Quartalsbeitrag (fiktiver Broker, SKR04)
- `tests/test_extf_serializer.py` `TestWiederkehrendeBuchungen` — 11 neue Tests: Header-Felder (Kat 65, Formatname, Version 4), Row-Counts (31+101+N), Row-2-Overrides, Zeitintervallart-Alternation, Endetyp 1-3, Ordnungszahl Wochentag 1-5, Belegfeld-1 WK-Regex (verbietet `& * +`), Belegfeld-2 max 12 Zeichen, Beginndatum TTMMJJJJ quoted, kein Saldo-Check, synthetische Fixture round-trip

### Changed
- `skills/datev-export/SKILL.md` — Cross-Reference zu neuem `wiederkehrende-buchungen`-Skill
- Test-Suite: 70 → 81 Tests (+11). Coverage stabil bei 91 % (Ziel ≥90%).

### Notes
- **v2.4.0 wurde übersprungen** — Formatversionen 10/11/12 Buchungsstapel-Backwards-Compat ist per PRD §14.3 konditional auf Steuerberater-DATEV-Rechnungswesen-Version; kein Signal, dass das benötigt wird.
- Multi-Format-Routing-Seam aus v2.3 zahlt sich hier aus: kein Refactor des Buchungsstapel-Codes notwendig, nur parallele Handler-Liste + Dispatcher.
- Belegfeld-1 in WK ist strikter als in Buchungsstapel (`& * +` verboten) — wichtig wenn Belegfeld-1 zwischen Buchungsstapel und WK kopiert wird. Validator weist mit klarer Meldung darauf hin.
- Nächste geplante Releases per PRD §14: v2.6.0 (KOST-Splitt), v2.7.0 (Debitoren/Kreditoren — recommended deferred bis konkreter Use-Case bestätigt).

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
- Formatversionen 10/11/12 backward-compatibility is planned for v2.4.0, only if a Mandanten-spezifischer Steuerberater requires it
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
