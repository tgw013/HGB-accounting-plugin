# IT Security Review

**Subject:** Germany-SMB-Finance-Accounting-Plugin
**Pinned commit:** `787d81cbb78f227767a415cb64c911b1ad8acbb0` (2026-03-28)
**Review date:** 2026-05-08
**Verdict:** ✅ **Cleared on technical security.** ⚠️ Operational hardening required (see RECOMMENDATIONS.md).
**Scope of this review:** IT-security review only. **Content / accounting correctness is NOT in scope and must be reviewed separately by a qualified professional before production use.**

---

## Threat model

The plugin will be deployed in a real company environment with potential access
to sensitive client data, DATEV credentials (once an MCP server is added),
and production accounting systems. The threat model considers:

1. **Prompt injection** in skill files — instructions that could redirect Claude
   away from the user's intent (data exfiltration, unauthorised actions).
2. **Hidden Unicode** — invisible characters used to smuggle instructions past
   human reviewers (zero-width chars, bidi overrides, Unicode tag chars).
3. **Code execution** — install-time scripts, runtime scripts, or shell hooks.
4. **Supply chain** — `pip install`, `npm install`, `curl | bash` patterns.
5. **Outbound network calls** — exfiltration channels, command-and-control.
6. **MCP server configuration** — auto-configured connectors, suspicious URLs.
7. **Credential / filesystem access** — references to `.ssh`, `.aws`, browser
   cookies, password files, environment variables.
8. **Provenance integrity** — does the plugin match its claimed upstream?

---

## What was checked

### 1. File-type inventory — ✅ Pass

The plugin contains 30 files, all of them text/JSON. There are zero binaries,
zero executables, zero scripts (no `.py`, `.sh`, `.js`, `.exe`, no `scripts/`
directory), no install hooks, no `requirements.txt`, no `package.json`. **The
plugin contains no executable code.** This single fact eliminates the entire
category of supply-chain and malware risk: there is nothing to run.

### 2. Hidden Unicode scan — ✅ Pass

Every byte of every file was scanned for the dangerous Unicode ranges:

| Range | Description |
|---|---|
| U+200B–U+200F | Zero-width chars, RLM/LRM marks |
| U+202A–U+202E | Bidirectional override chars (classic injection vector) |
| U+2060–U+206F | Word joiner, invisible operators |
| U+FEFF | BOM in non-leading position |
| U+E0000–U+E007F | Unicode tag chars (modern invisible-text injection) |
| U+180E | Mongolian vowel separator |

**Result: zero matches across all 30 files.**

### 3. Prompt-injection pattern scan — ✅ Pass

Grep across all markdown for German + English injection patterns:

- "ignore previous", "disregard", "forget everything"
- "system prompt", "you are now", "new instructions"
- "do anything", "jailbreak", "exfiltrate"
- "im hintergrund", "verschweige", "heimlich" (German equivalents)
- "without telling the user", "tell nobody"
- "send the data", "upload to", "webhook"
- exec/eval/subprocess, base64 decode, curl/wget/PowerShell

**Result: zero matches.**

### 4. Filesystem-access pattern scan — ✅ Pass

Grep for references to sensitive paths:

- `.ssh`, `.aws`, `~/.config`, `/etc/`, `/root/`
- credential filenames, browser cookie stores
- DATEV/ELSTER token paths

**Result: zero matches.**

### 5. URL inventory — ✅ Pass with operational caveat

Eleven unique URLs across the entire plugin, all legitimate:

| URL | Purpose | Verdict |
|---|---|---|
| `https://mcp.slack.com/mcp` | Official Slack MCP | Legitimate |
| `https://mcp.box.com` | Official Box MCP | Legitimate |
| `https://mcp-server.egnyte.com/mcp` | Official Egnyte MCP | Legitimate |
| `https://mcp.atlassian.com/v1/mcp` | Official Atlassian MCP | Legitimate |
| `https://microsoft365.mcp.claude.com/mcp` | Anthropic-managed MS365 MCP | Legitimate |
| `https://gcal.mcp.claude.com/mcp` | Anthropic-managed Google Calendar MCP | Legitimate |
| `https://gmail.mcp.claude.com/mcp` | Anthropic-managed Gmail MCP | Legitimate |
| `https://github.com/anthropics/knowledge-work-plugins/tree/main/finance` | Source of upstream fork | Documentation reference |
| `https://github.com/mlobo2012/Germany-SMB-Finance-Accounting-Plugin/releases` | Author's release page | Documentation reference |
| `https://www.ai-heroes.co` | Author website | Documentation reference |
| `https://www.ai-heroes.co/contact` | Author contact | Documentation reference |

No IP addresses, no shorteners, no obscure third-party domains, no paste sites,
no Telegram/Discord/webhook URLs. **All seven MCP server URLs are legitimate
official endpoints.**

The operational caveat: the plugin auto-configures all seven MCP servers, none
of which are necessary for HGB accounting workflows. See RECOMMENDATIONS.md
item 1 — we have already pruned `.mcp.json` to remove all of them in our
deployed copy.

### 6. SKILL.md content review — ✅ Pass

All 11 SKILL.md files (5,812 lines total) and 10 command files were sampled
or read in full. Every file is reference content (German accounting / tax
procedures, with §-references to HGB, EStG, UStG, GoBD, IDW PS standards) plus
ASCII workflow templates. **No imperative instructions to Claude that would
cause it to take actions outside the conversation.** The instructions to
Claude are scoped to: process user-supplied data, ask clarifying questions,
present results, validate Soll = Haben, flag for review.

### 7. Frontmatter review — ✅ Pass (with quality note)

YAML frontmatter in all 11 SKILL.md files is benign metadata only (skill name,
description, language, version, dependencies, tags). No instructions hidden in
metadata.

**Quality note (not security):** the plugin uses a custom frontmatter schema
(`skill`, `type`, `language`, `version`, `dependencies`, `config`, `tags`)
that does not match the standard Claude Skills schema (`name`, `description`,
`argument-hint`). Cowork likely silently ignores the unknown fields. The
practical implication is that the declared `dependencies:` field probably has
no functional effect — it documents intent but doesn't actually load the
referenced skill. Worth being aware of when reviewing skill content.

### 8. Provenance / fork-integrity check — ✅ Pass

The plugin claims to be a fork of `anthropics/knowledge-work-plugins/finance`.
A structural diff against the upstream confirms this:

- Upstream is also pure markdown + JSON (no scripts) — same architecture.
- 7 of 11 skills in the German plugin map directly to upstream skills
  (journal-entry → buchungssatz, reconciliation → abstimmung, etc.).
- 4 skills are net-new and Germany-specific (USt-Voranmeldung, eBilanz,
  Lohnabrechnung, Compliance). All four were reviewed and contain no novel
  instruction patterns vs. the ported skills.
- The German fork **adds** a `commands/` directory and a `config/` directory
  not present in upstream. Both contain only markdown / JSON data. Reviewed
  and clean.
- 1 upstream skill (sox-testing) was correctly **dropped** (US-specific).

The fork is what it claims to be: a content localisation, not a behaviour
modification.

---

## What was NOT checked (out of scope)

- **Content / accounting correctness.** Whether the §-references are accurate,
  whether the rate values in `config/rates-2026.json` reflect actual current
  law, whether the calculation schemes match BMF guidance — out of scope here,
  required before deployment. See RECOMMENDATIONS.md item 2.
- **Runtime behaviour.** This is a static review. We did not load the plugin
  into a live Claude environment and observe what tool calls it triggers.
  Given the absence of executable code and the absence of any instruction
  patterns that would trigger external actions, we expect runtime behaviour to
  match the static content. But this is an inference, not an observation.
- **Future versions.** This review applies only to commit
  `787d81cbb78f227767a415cb64c911b1ad8acbb0`. Any future update from upstream
  must be re-reviewed before adoption.
- **Third-party MCP servers** (DATEV, Lexware, sevDesk, etc.). The plugin does
  not bundle or auto-install any. If we later add a community-built MCP
  server for our accounting system, **that server requires its own full
  security review** — a separate, larger exercise than this one (because
  those servers run real code and hold API tokens).

---

## Verdict

**The plugin is technically safe to install.** It cannot run code, cannot
phone home, cannot read sensitive data on its own. Its risk profile is
identical to that of a markdown handbook a colleague might email you — the
content might be wrong, but the file format itself cannot harm you.

**Operational hardening still required** before deploying near production
data — see RECOMMENDATIONS.md for the four-step pre-deployment checklist
(MCP pruning, content review, version pinning, annual rate-table maintenance).
