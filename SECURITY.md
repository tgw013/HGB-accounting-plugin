# Security Policy

## Reporting a vulnerability

**Please do not file public GitHub issues for security vulnerabilities.**

Report security issues privately via **GitHub Security Advisories**:
1. Navigate to the repository's **Security** tab
2. Click **Report a vulnerability**
3. Fill in the form — describe the issue, reproduction steps, and impact

Alternatively, mention `@tgw013` in a private channel.

## Response expectations

- Acknowledgement: within 7 days
- Triage + assessment: within 14 days
- Fix or mitigation: timeline depends on severity, communicated after triage

## Scope

In scope:
- This plugin's skills, commands, scripts, and config files
- The DATEV-PDF extractor (`scripts/extract_datev_pdf.py`)
- Any future MCP server integrations declared in `.mcp.json`

Out of scope:
- Vulnerabilities in Claude Code / Claude Cowork themselves — report to Anthropic
- Vulnerabilities in DATEV software or third-party MCP servers — report to their respective maintainers
- Issues that require local-machine compromise to exploit (those are general OS hygiene)

## What counts as a security issue here

- Hardcoded secrets or credentials in the repo or git history
- Skill instructions that exfiltrate user data, contact unexpected hosts, or execute arbitrary commands
- Prompt-injection vectors in skill or command files
- Supply-chain risks in declared dependencies
- Privacy leaks (PII / personal email / personal data in scenarios or commits)

## What does NOT count as a security issue

- Accounting-correctness errors (HGB §-misinterpretation, wrong konto, KZ-code typo) — these go in regular Issues with the `accounting-correction` template
- Outdated rates (e.g., new Mindestlohn value not yet in `config/{year}/rates.json`) — regular issue
- Disagreements about which Steuerberater-tooling is best — discussion forum
