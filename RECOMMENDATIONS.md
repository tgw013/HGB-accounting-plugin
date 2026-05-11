# Pre-Deployment Recommendations

The IT-security review (see [SECURITY_REVIEW.md](./SECURITY_REVIEW.md)) is
complete. The plugin is technically safe to install. However, **four steps must
happen before this is used near production data**.

---

## 1. ✅ MCP connectors pruned (already done)

**Status:** Done — `.mcp.json` in this repository has been pruned to an empty
`mcpServers: {}` map. The original upstream config is preserved as
`.mcp.json.original` for reference.

**Why:** The upstream plugin auto-configures seven workspace connectors
(Slack, Box, Egnyte, Atlassian, Microsoft 365, Gmail, Google Calendar) that
have no relevance to HGB accounting. Each one represents a potential OAuth
prompt and a potential context-attack surface. Removing them is a defence-in-depth
measure — they cannot read data without OAuth authorisation, but their
presence in the config makes accidental authorisation easier than it should be.

**If you later need to add a connector** (e.g., a DATEV or Lexware MCP server),
add it to `.mcp.json` deliberately, after that specific connector has passed
its own security review. **Community-built MCP servers run real code and hold
your API tokens — they are a much higher-risk category than this skill plugin
itself, and require a more rigorous review than what we did here.**

---

## 2. ⏳ Content / accounting review (REQUIRED, NOT YET DONE)

**Status:** **Not started. This is the gating item before production use.**

The IT-security review confirms the plugin contains no malicious code or
prompt injection. It does **not** confirm that the German accounting content
is correct, current, or applicable to your specific business circumstances.

A qualified person (Steuerberater, Wirtschaftsprüfer, or senior accounting
controller with current German qualifications) must review at minimum:

- **`config/rates-2026.json`** — verify every rate, threshold, and limit
  against actual current law (Sozialversicherungsrechengrößen-Verordnung
  2026, BMF rate publications, Beitragssatzverordnung). Pay specific
  attention to: Beitragsbemessungsgrenzen (KV/PV vs. RV/AV, Ost/West),
  Mindestlohn, Künstlersozialkasse abgabe, Insolvenzgeldumlage U3,
  Pflegeversicherung Kinderlosenzuschlag and Sachsen sonderregel,
  Solidaritätszuschlag thresholds, Kirchensteuer rates per Bundesland.
- **`config/kontenrahmen.json`** — verify SKR03 / SKR04 mappings are correct
  and current.
- **All 11 SKILL.md files** — verify the §-references are accurate and that
  the workflow logic matches actual procedure (especially: USt-Voranmeldung
  ELSTER process, eBilanz XBRL taxonomy version, Lohnabrechnung calculation
  order, Jahresabschluss §266/§275 HGB structure for the relevant size class,
  IKS-Prüfung mapping to IDW PS 261 latest revision).
- **GoBD-relevant procedures** — confirm the documentation/retention guidance
  in the compliance skill matches your firm's actual GoBD-Verfahrensdokumentation.

A reasonable approach: take three real, anonymised cases from recent client
work, run them through the plugin, and have a Steuerberater compare the
output line-by-line to the correct answer. Document any discrepancies.

**Do not deploy to anyone with access to live client data until this review
is complete and gaps are documented.**

---

## 3. 🔒 Version pinning (already done)

**Status:** Done — pinned to commit `787d81cbb78f227767a415cb64c911b1ad8acbb0`,
SHA-256 manifest in `SHA256SUMS`.

**Verify integrity at any time:**

```bash
sha256sum -c SHA256SUMS
```

All files should report `OK`. If any report `FAILED`, do not install — investigate.

**Do not auto-update.** If the upstream author publishes a new version, treat
it as a candidate for a new review cycle (re-run the IT-security review on
any added/changed files, re-run the content review on any changed German
content), not as a drop-in replacement.

---

## 4. 📅 Annual rate-table maintenance (NEW responsibility)

**Status:** Process not yet established. **Owner needed.**

`config/rates-2026.json` contains rate values that change every January
(Sozialversicherungsrechengrößen, Mindestlohn, Beitragssätze, etc.). The
upstream author may or may not publish a 2027 update. We cannot rely on it.

**Recommended process:**

- Designate an owner (suggest: head of payroll or senior Steuerberater).
- Add a calendar reminder for **mid-November each year** to begin the update
  for the following year.
- The owner reviews the new Sozialversicherungsrechengrößen-Verordnung,
  Beitragssatzverordnung, and BMF rate publications when they are released.
- The owner produces an updated `config/rates-NNNN.json` for the new year.
- The new file goes through the same review cycle: IT-security check
  (file-type and content-pattern scans), content review (Steuerberater
  sign-off on the rate values).
- Update `SHA256SUMS` after any change.
- Document the change in this repository's commit history.

Without this process, the plugin will progressively become wrong over time
in ways that may not be obvious until someone receives a tax-office query.

---

## Summary checklist before any production use

- [x] MCP connectors pruned in `.mcp.json`
- [x] Version pinned, integrity manifest generated
- [ ] **Content / accounting review by qualified professional** ← **gating**
- [ ] Annual rate-table maintenance owner assigned
- [ ] Three test cases run end-to-end with Steuerberater sign-off
- [ ] Documentation updated to reflect any content gaps found in the review
