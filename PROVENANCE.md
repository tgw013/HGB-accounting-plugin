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
