# Provenance

## Source

| Field | Value |
|---|---|
| Upstream repository | https://github.com/mlobo2012/Germany-SMB-Finance-Accounting-Plugin |
| Upstream author | AI Heroes (https://www.ai-heroes.co), GitHub user `mlobo2012` |
| License | Apache 2.0 + Commons Clause |
| Vendored on | 2026-05-08 |

## Pinned version

**This repository is pinned to commit `787d81cbb78f227767a415cb64c911b1ad8acbb0`**
(committed 2026-03-28 10:38:05 UTC), which is `main` HEAD as of the vendoring date.

This commit is **2 commits ahead of the v1.0.3 release tag** (`16eea24`):

```
787d81c  Fix Cowork upload: clean plugin.json, remove marketplace.json,
         fix .mcp.json (remove empty URLs)
d2ab10d  fix: Lizenz-Referenz im README, marketplace.json korrigiert
16eea24  Germany — Finance & Accounting Plugin v1.0.3      ← v1.0.3 tag
```

## Why we pinned to `main` HEAD instead of the v1.0.3 tag

The v1.0.3-tagged release contains a `.mcp.json` with several empty-URL
placeholder entries (DATEV, Lexware, Personio, ELSTER, HBCI-FinTS,
Unternehmensregister), which prevents the plugin from uploading successfully
into Claude Cowork. The post-tag fix (`787d81c`) is required for the plugin to
install at all. We therefore pin to the post-tag commit.

The trade-off this introduces:

- **Pro:** the plugin actually works with current Cowork.
- **Con:** the post-tag commit also replaced the German-flavoured connector
  stubs (DATEV, Lexware, ELSTER, etc.) with seven generic workspace connectors
  (Slack, Box, Egnyte, Atlassian, MS365, Gmail, GCal). These are not relevant
  to HGB accounting, which is why our deployed `.mcp.json` removes them all
  (see RECOMMENDATIONS.md, item 1).

## File integrity

`SHA256SUMS` records the SHA-256 hash of every file as captured from upstream.
Run `sha256sum -c SHA256SUMS` at any time to verify that nothing has drifted.

The two files that diverge from upstream by design are:

- `.mcp.json` — pruned by us; original kept as `.mcp.json.original`
- (We add `INTERNAL_README.md`, `PROVENANCE.md`, `SECURITY_REVIEW.md`,
  `RECOMMENDATIONS.md`, and `SHA256SUMS` as new files; these are not part of
  the upstream and are not in the integrity manifest.)

## Author trust signals

| Signal | Value | Notes |
|---|---|---|
| GitHub stars (upstream, at time of vendoring) | 0 | No community review |
| GitHub forks | 0 | No community review |
| Watchers | 0 | No community review |
| Contributors | 1 (`mlobo2012`) | Single-author repo |
| Total commits on main | 3 | Very young project |
| Commit signing | None | Future updates not cryptographically attestable |
| Public author identity | "AI Heroes" company website verified | Real entity, not anonymous |
| Disclaimer present | Yes — explicitly states "no replacement for Steuerberater / Wirtschaftsprüfer" | Honest framing |

The trust signals are weak from a community-review standpoint but **not
suspicious**. The plugin is what it claims to be (see SECURITY_REVIEW.md).
The remaining gap is content-correctness, not authenticity.

---

## v2.0 rewrite audit (added 2026-05-17, for public-launch readiness)

### What changed between upstream `787d81c` and v2.0 HEAD

Substantial rewrite. Diff summary from `git diff 787d81c..HEAD -- skills/ commands/ config/`:

```
44 files changed, 2347 insertions(+), 5636 deletions(-)
```

- **Net negative line count** (-3,289 lines): every upstream skill was significantly trimmed and restructured under the new Knowledge/Workflow separation pattern.
- **Deleted entirely:** `skills/buchungssatz-vorbereitung/`, `skills/compliance/` (upstream-only, replaced by new architecture).
- **Added from scratch (zero upstream lineage):** `skills/buchung-grundlagen/`, `skills/datev-export/`, `skills/gobd-konformitaet/`, `skills/hinschg-meldewesen/`, `skills/steuerberater-handoff/`.
- **Substantively rewritten:** every other skill file (lohnabrechnung, jahresabschluss, monatsabschluss, ust-voranmeldung, abstimmung, ebilanz, iks-pruefung, abweichungsanalyse, buchungssatz) — most lost 50–80% of upstream content and was replaced with HGB-2026-verified content backed by primary-source citations.
- **Config layer rebuilt:** original single `config/kontenrahmen.json` replaced by `config/{2025,2026}/` multi-year structure with 128 konten verified against DATEV PDFs Art.-Nr. 11174/11175 via structure-aware extractor (`scripts/extract_datev_pdf.py`).

### Apache 2.0 + Commons Clause inheritance

Upstream was licensed under Apache 2.0 with an appended Commons Clause restricting commercial sale. v2 LICENSE drops the Commons Clause and is pure Apache 2.0.

**Reasoning for the drop:**

1. The substantive content in v2 is overwhelmingly new work: 5 wholly new skills, full rebuild of the config layer, and net-negative line counts in surviving skills indicate the rewrite is not a thin derivative.
2. The factual content most likely to have survived from upstream (HGB §-references, DATEV konto numbers, KZ-codes from BMF Vordruckmuster) is not copyrightable — these are statutory and administrative facts, not creative expression.
3. Any residual prose patterns from upstream that may survive are de minimis relative to v2's volume and have been re-cast in service of the new Knowledge/Workflow architecture.

**Honest caveat:** Commons Clause is a non-standard rider and its enforceability against substantial rewrites is contested. If you are planning a commercial product based on this repo and want absolute clarity, contact upstream (`mlobo2012` / AI Heroes) for a written waiver, or re-add the Commons Clause to your own distribution. The Apache 2.0 license terms are otherwise straightforward.

### Upstream attribution

LICENSE file's footer retains the lineage acknowledgment to AI Heroes / Marco Lobo. README and CHANGELOG also document the inspiration. This satisfies Apache 2.0 §4(c) attribution.
