# Germany — Finance & Accounting Plugin (Internal Vendored Copy)

This repository is an **internal vendored copy** of the open-source
[`mlobo2012/Germany-SMB-Finance-Accounting-Plugin`](https://github.com/mlobo2012/Germany-SMB-Finance-Accounting-Plugin),
prepared for use inside our company.

## Status

| | |
|---|---|
| **Source** | `mlobo2012/Germany-SMB-Finance-Accounting-Plugin` on GitHub |
| **Pinned commit** | `787d81cbb78f227767a415cb64c911b1ad8acbb0` (2026-03-28) |
| **Upstream tag** | `v1.0.3` (note: pinned commit is 2 commits ahead — see PROVENANCE.md) |
| **License** | Apache 2.0 + Commons Clause (free for internal business use; no commercial resale) |
| **Security review** | ✅ Completed — see [SECURITY_REVIEW.md](./SECURITY_REVIEW.md) |
| **Content / accounting review** | ⏳ **Required before production use** — see [RECOMMENDATIONS.md](./RECOMMENDATIONS.md) |
| **Auto-configured connectors** | 🔧 **Pruned to zero** — see `.mcp.json` (original kept as `.mcp.json.original`) |

## What this plugin is

An 11-skill, 10-slash-command Claude plugin that produces structured German
accounting and tax-preparation outputs (Buchungssätze, Abstimmungen,
Jahresabschluss nach §§266/275 HGB, USt-Voranmeldung, eBilanz, Lohnabrechnung,
IKS-Prüfung nach IDW PS 261, GoBD/HinSchG/DCGK compliance checks,
Abweichungsanalysen, Monatsabschluss, EÜR).

It is a **draft generator for review by a qualified professional** —
it does not replace a Steuerberater or Wirtschaftsprüfer.

## Repository contents

```
.
├── .claude-plugin/plugin.json    # Plugin manifest (germany-accounting v1.0.3)
├── .mcp.json                     # PRUNED — empty servers list (deploy-ready)
├── .mcp.json.original            # Original upstream MCP config, for reference
├── CONNECTORS.md                 # Author's notes on recommended integrations
├── LICENSE                       # Apache 2.0 + Commons Clause
├── README.md                     # Author's original README (preserved unchanged)
├── commands/                     # 10 slash-command definitions
├── config/                       # kontenrahmen.json (SKR03/SKR04), rates-2026.json
├── skills/                       # 11 SKILL.md files (the actual content)
│
├── PROVENANCE.md                 # ← Where this came from, exact hashes
├── SECURITY_REVIEW.md            # ← What we checked and what we found
├── RECOMMENDATIONS.md            # ← What needs to happen before deployment
└── SHA256SUMS                    # Cryptographic manifest of every file
```

## How to use

1. **Read the three review documents** (`PROVENANCE.md`, `SECURITY_REVIEW.md`,
   `RECOMMENDATIONS.md`) in full before considering a deployment.
2. **Do not deploy until the content / accounting review is complete.** The
   security review is done; the accounting review is not. The plugin's outputs
   must be validated against actual current German law and standards by a
   qualified person (Steuerberater / Wirtschaftsprüfer / accounting controller).
3. **Verify integrity** before each install: `sha256sum -c SHA256SUMS` should
   report all files as `OK`.
4. **Maintain rate tables annually.** `config/rates-2026.json` will need to be
   updated each January when the new Sozialversicherungsrechengrößen take
   effect. See RECOMMENDATIONS.md for the maintenance checklist.

## Updates from upstream

We do **not** auto-pull from upstream. If a new upstream version ships and we
want to consider adopting it:

1. Diff the new upstream against `787d81cbb78f227767a415cb64c911b1ad8acbb0`
2. Re-run the security review on any added or changed files
3. Re-run the content review on any changed German content
4. Update `PROVENANCE.md` with the new pinned commit and tag
5. Regenerate `SHA256SUMS`
