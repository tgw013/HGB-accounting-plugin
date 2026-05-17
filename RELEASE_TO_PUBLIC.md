# Release-to-Public Checklist

Stand: 2026-05-17. Status: alle nicht-destruktiven Audit-Punkte aus dem Plan sind erledigt und in `main` committet (siehe Commit-Historie). Es bleiben **5 Aktionen, die du manuell ausführen musst**, bevor das Repo öffentlich gehen kann.

## Verbleibende Aktionen (in dieser Reihenfolge)

### 1. Repo umbenennen (GitHub Web-UI oder gh CLI)

```bash
gh repo rename HGB-accounting-plugin --yes
git remote set-url origin https://github.com/tgw013/HGB-accounting-plugin.git
git remote -v   # verify
```

GitHub leitet die alte URL automatisch weiter — keine Link-Brüche extern. Aber: Klone, die jemand mit der alten URL hat, müssen die Remote-URL aktualisieren.

### 2. Personal-Email-Scrub (destruktive History-Umschreibung)

```bash
bash scripts/scrub-personal-emails.sh
```

Das Skript zeigt vor Ausführung was es ändert und fragt nach Bestätigung. Es ersetzt in **allen Commits**:
- `[REDACTED]` → `169305885+tgw013@users.noreply.github.com`
- `[REDACTED]` → `169305885+tgw013@users.noreply.github.com`
- Author-Name "Till Weidemüller" → "tgw013"

Marco Lobo's Upstream-Commits bleiben unverändert (sind bereits noreply).

### 3. Force-Push (nach Scrub)

```bash
git push --force-with-lease origin main
git push --force --tags origin
```

Force-Push ist hier OK weil keine externen Mit-Entwickler existieren.

### 4. Vorhandene GitHub-Releases prüfen + ggf. neu erstellen

```bash
gh release view v2.0.0 --json author,tagName
gh release view v2.0.0-alpha --json author,tagName
```

Falls der Release-Author eine personal Email zeigt → löschen + neu erstellen:

```bash
gh release delete v2.0.0 --yes
gh release create v2.0.0 germany-accounting-v2.0.0.zip \
  --title "v2.0.0 — Knowledge/Workflow split, multi-year config, GmbH+UG scope" \
  --notes-file CHANGELOG.md
# Analog für v2.0.0-alpha falls relevant — oder einfach Tag rausnehmen, die Phase ist abgeschlossen
```

### 5. GitHub Account-Einstellungen (verhindert künftige Leaks)

In https://github.com/settings/emails:
- [x] **Keep my email addresses private** aktivieren
- [x] **Block command line pushes that expose my personal email address** aktivieren

In https://github.com/tgw013/HGB-accounting-plugin/settings:
- About → Description: "HGB-Buchhaltungs-Plugin für Claude — DATEV SKR03/04, GmbH+UG, GoBD-konform. Inspiriert vom Anthropic Finance Plugin."
- Topics: `claude`, `claude-plugin`, `claude-cowork`, `accounting`, `bookkeeping`, `germany`, `hgb`, `datev`, `skr03`, `skr04`, `gobd`, `german-tax`
- Features: Issues **on**, Discussions **on**, Wiki **off**, Projects **off**
- Security → Private vulnerability reporting → **enable** (so dass `SECURITY.md`'s Verweis funktioniert)

### 6. Visibility flip (letzter Schritt)

In https://github.com/tgw013/HGB-accounting-plugin/settings:
- Danger Zone → Change visibility → **Public**
- Bestätige in Incognito-Tab dass das Repo lädt + README rendert + Install-Commands stimmen

---

## Post-Flip-Verifikation

```bash
# (in einer Inkognito-Shell ohne gh-Auth)
git clone https://github.com/tgw013/HGB-accounting-plugin.git /tmp/verify-public
cd /tmp/verify-public
git log --all --format='%ae %ce' | sort -u
# Erwartete Ausgabe: NUR noreply-Adressen
```

```bash
# Smoke-test ZIP-Install in Cowork
# (eine andere ZIP von Releases-Page downloaden, in Cowork uploaden, prüfen dass 14 Skills auftauchen)
```

---

## Was wurde im Voraus erledigt (für deine Übersicht)

- ✅ `docs/INTERNAL_README.md` gelöscht
- ✅ `docs/SECURITY_REVIEW.md` mit Historical-Banner versehen (klar als v1.x-Artefakt markiert)
- ✅ `docs/PROVENANCE.md` ergänzt mit "v2.0 rewrite audit" + Commons-Clause-Begründung
- ✅ `.mcp.json` — beide `see_also`-Lines zu `-internal` Repos entfernt
- ✅ Historische v1-Dokumente in `docs/archive/` verschoben (5 Files + Archive-README)
- ✅ `docs/ISSUES_LOG.md` entfernt (leere Vorlage)
- ✅ Name "T. Weidemüller" aus `skills/steuerberater-handoff/SKILL.md` Beispiel entfernt
- ✅ `SECURITY.md` erstellt (verweist auf GitHub Security Advisory, nicht personal email)
- ✅ `CODE_OF_CONDUCT.md` erstellt (Contributor Covenant 2.1)
- ✅ `.github/ISSUE_TEMPLATE/` mit zwei Templates (bug-report, accounting-correction)
- ✅ `.github/PULL_REQUEST_TEMPLATE.md` mit Verifikations-Diff-Sektion
- ✅ `scripts/scrub-personal-emails.sh` (für Aktion 2 oben)
- ✅ Lokale git config auf noreply-Email umgestellt — alle künftigen Commits sind sauber
- ✅ Diese Datei (`RELEASE_TO_PUBLIC.md`)

## Was bewusst NICHT gemacht wurde

- ❌ Repo-Rename auf GitHub — bedarf deiner Bestätigung (Aktion 1)
- ❌ History-Scrub — destruktiv, du musst entscheiden (Aktion 2)
- ❌ Force-Push — Folge aus Scrub (Aktion 3)
- ❌ Visibility-Flip — letzter Schritt, deine Hand am Hebel (Aktion 6)

Wenn alle 6 Aktionen erledigt sind, kann diese Datei (`RELEASE_TO_PUBLIC.md`) gelöscht werden — sie ist nur als Übergangs-Checkliste gedacht.
