# germany-accounting

Ein Finanz- und Buchhaltungs-Plugin für **Cowork** (Anthropic's agentische Desktop-App) — funktioniert auch in **Claude Code**. Auf deutsche Rechtslage portiert: HGB, DATEV-SKR03/04, USt-Voranmeldung, Lohn, GoBD/IKS, eBilanz-Vorbereitung. Geltungsbereich GmbH + UG.

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2025+2026, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Vordruckmuster). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung mit Steuerberater/Wirtschaftsprüfer abgleichen.

**Status:** `v2.0.0` auf `main`. 14 Skills + 14 Commands, 128 Konten gegen DATEV-PDFs 2025+2026 verifiziert. Vorgänger-Tags: `v1.1.0`, `v2.0.0-alpha`.

---

## Quick Overview (English)

A finance and accounting plugin for German GmbH/UG entities — HGB-compliant journal entries with SKR03/SKR04, VAT pre-registration, payroll, monthly/annual close, and GoBD/IKS compliance. Primarily designed for Cowork; also works in Claude Code. Inspired by Anthropic's [finance plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance) (US-focused), independently ported to German law. Output is a draft — review with a `Steuerberater` (German tax advisor) before productive use.

---

## Installation

### Cowork (empfohlen für Nicht-Entwickler)

Cowork installiert Plugins über **ZIP-Upload** (kein Slash-Command-Marketplace wie Claude Code).

1. **Lade die fertige ZIP** von der [Releases-Seite](https://github.com/tgw013/HGB-accounting-plugin-internal/releases) herunter — `germany-accounting-vX.Y.Z.zip` (Asset der jeweiligen Release).
2. In Cowork: Plugin-Bereich öffnen → neues Plugin hinzufügen → ZIP hochladen.
3. Skills + Commands stehen sofort zur Verfügung.

> ⚠ **Nicht** GitHub's grünen "Code → Download ZIP" Button benutzen — dort liegt alles in einem Wrapper-Ordner `HGB-accounting-plugin-internal-main/`, was Cowork nicht versteht. Immer die Release-ZIP nutzen.
>
> **Falls eine Release-ZIP fehlt** (zwischen Releases): GitHub-ZIP entpacken, in den entpackten Ordner gehen, dort `.claude-plugin`, `commands`, `skills`, `config`, `.mcp.json` etc. markieren und neu zippen (Windows: Rechtsklick → "In ZIP-Datei komprimieren"). Diese neue ZIP in Cowork hochladen.

### Claude Code (für Entwickler)

Innerhalb einer aktiven Claude-Code-Session:

```
/plugin marketplace add tgw013/HGB-accounting-plugin-internal
/plugin install germany-accounting@hgb-accounting
```

Oder als Shell-Shortcut (analog zu Anthropic's Finance-Plugin-README):

```bash
claude plugins add tgw013/HGB-accounting-plugin-internal
```

**Voraussetzungen:** Claude Code (`npm install -g @anthropic-ai/claude-code`, Node 18+). Bei privatem Repo zusätzlich `gh auth login`.

**Lokale Entwicklung:** `claude --plugin-dir ./HGB-accounting-plugin-internal` lädt das Plugin direkt aus einem Klon ohne Marketplace.

Doku-Quellen: [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins.md), [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md).

---

## Skills (14)

Skills stellen Hintergrundwissen und Workflow-Logik bereit. Claude wählt sie automatisch passend zur Aufgabe; Zugriff erfolgt über die Slash-Commands oder über natürliche Aufforderungen ("Erstelle Buchungssatz für …").

| Skill | Typ | Anthropic-Pendant | Zweck |
|---|---|---|---|
| `buchung-grundlagen` | knowledge | `journal-entry-prep` (Knowledge) | Doppik, GoBD, SKR-Auswahl, Aufbewahrungsfristen, §-Verweis-Disziplin |
| `buchungssatz` | workflow | `journal-entry-prep` + `journal-entry` | Beleg → Buchungsvorschlag (SKR03/04, USt-Tatbestand, §-Begründung) |
| `monatsabschluss` | workflow | `close-management` | Monats-Closing-Checkliste, Abgrenzungen, USt-VA-Vorbereitung |
| `ust-voranmeldung` | workflow | — (DE-spezifisch) | KZ-Mapping nach BMF-Vordruckmuster USt 1 A, ELSTER-fähige Aufstellung |
| `lohnabrechnung` | workflow | — (DE-spezifisch) | Brutto-Netto, SV, LSt, bAV §3 Nr.63, Minijob/Midijob, Verbuchung |
| `jahresabschluss` | workflow | `close-management` + `financial-statements` | HGB-Aufstellung (Bilanz §266, GuV §275, Anhang §284-288) |
| `ebilanz` | workflow | `financial-statements` (sinngemäß) | Datenpaket-Vorbereitung für ERiC/DATEV (kein Direktversand) |
| `abstimmung` | workflow | `reconciliation` | Bank, Kasse, OP-Debitoren/-Kreditoren, USt, Intercompany, EWB/PWB |
| `abweichungsanalyse` | workflow | `variance-analysis` | Plan-Ist-Decomposition (Preis/Menge/Mix), BWA-Kommentierung, Forecast |
| `gobd-konformitaet` | knowledge | — (DE-spezifisch) | BMF-GoBD 28.11.2019: Festschreibung, Z1/Z2/Z3, Verfahrensdokumentation |
| `iks-pruefung` | methodology | `sox-testing` + `audit-support` | IKS nach IDW PS 261 / 5 COSO-Komponenten (ersetzt SOX in DE) |
| `hinschg-meldewesen` | knowledge | — (DE-spezifisch) | HinSchG-Pflichten ab 50 MA, Meldestelle, Fristen, Bußgeldrahmen |
| `datev-export` | workflow | — (DACH-spezifisch) | DATEV-Buchungsstapel-CSV (EXTF-Format) für direkten Import |
| `steuerberater-handoff` | workflow | — (DACH-spezifisch) | Strukturiertes Übergabe-Paket (Sachverhalt + Vorschlag + § + Belege) |

## Slash-Commands (14)

Jeder Skill hat einen gleichnamigen Slash-Command zum direkten Aufruf:

`/buchung-grundlagen` · `/buchungssatz` · `/monatsabschluss` · `/ust-voranmeldung` · `/lohnabrechnung` · `/jahresabschluss` · `/ebilanz` · `/abstimmung` · `/abweichungsanalyse` · `/gobd-konformitaet` · `/iks-pruefung` · `/hinschg-meldewesen` · `/datev-export` · `/steuerberater-handoff`

---

## Beispiel-Workflows

### Monatsabschluss April

```
/monatsabschluss
  → Saldenliste 04/2026 hochladen
  → Bank-Auszüge aller Konten (PDF/CSV)
  → OP-Listen Debitoren + Kreditoren

Plugin liefert:
  - Closing-Checkliste (was ist OK, was ist offen)
  - Vorgeschlagene Nachbuchungen (Abgrenzungen, RST-Anpassungen)
  - BWA-Kommentar

Anschluss:
/ust-voranmeldung 04/2026   → KZ-Aufstellung + Zahllast/Erstattung
/datev-export               → Buchungsstapel-CSV der Vorschläge
/steuerberater-handoff      → Übergabe-Brief an StB
```

### Einzel-Buchungssatz mit § 13b

```
/buchungssatz
  → "Rechnung Acme Cloud Ltd. (IE), 1.500 € netto, SaaS Mai 2026"

Plugin erkennt § 13b Abs. 1 UStG, baut Buchung mit
SKR04 6840/3837/1407/3300, schlägt KZ 46/47/67 in USt-VA vor,
begründet mit §-Verweis.
```

### Jahresabschluss-Vorbereitung

```
/jahresabschluss
  → Saldenliste GJ vor Umbuchungen
  → Inventur-Liste
  → Anlagengitter
  → AfA-Lauf-Ergebnis

Plugin liefert:
  - Größenklasse-Bestimmung (§ 267 HGB)
  - Bilanz § 266 + GuV § 275 (Markdown + Excel)
  - Anhang-Gerüst (§§ 284-288)
  - Steuerrückstellungs-Berechnung (KSt + GewSt + Solz)

/ebilanz   → Datenpaket-Vorbereitung
/steuerberater-handoff   → Übergabe an StB für ELSTER/Bundesanzeiger
```

### IKS-Selbstbewertung vor Prüfung

```
/iks-pruefung
  → Prozess-Beschreibungen, Berechtigungskonzept, bestehende Kontrollen

Plugin liefert:
  - Reife-Score je COSO-Komponente
  - Lücken-Liste mit Priorität
  - Maßnahmen-Backlog mit Frist + Verantwortlichem
```

---

## Wo kommen die Daten her?

Anthropic's Pendant verbindet sich via MCP an ERP / Data-Warehouse / BI-Tools. **Bei uns sind MCP-Integrationen Stand v2.0.0 noch geplant** (siehe `.mcp.json`). Bis dahin liefert der Anwender die Daten manuell — Claude kann sie aus mehreren Formaten lesen:

| Daten-Typ | Quelle | Format | Wie übergeben |
|---|---|---|---|
| **Belege** | Eingangs-/Ausgangs-Rechnungen | PDF, Foto (JPG/PNG), oder Text-Paste | Direkt in die Konversation hochladen oder einfügen |
| **Saldenliste** | DATEV Unternehmen online / DATEV Rechnungswesen / Lexware | Excel-Export (XLSX), CSV, PDF | Hochladen |
| **Bankauszüge** | Online-Banking | PDF, CSV, MT940 | Hochladen |
| **OP-Listen** | DATEV-OPOS-Auswertung / Lexware | Excel, CSV, PDF | Hochladen |
| **Lohnjournal** | DATEV LODAS / DATEV Lohn und Gehalt / Lexware Lohn / Personio | Excel, CSV, PDF | Hochladen |
| **Anlagengitter** | DATEV Anlagenverwaltung | Excel, PDF | Hochladen |
| **Plan/Budget** | Excel-Planung intern | Excel, CSV, Text-Tabelle | Hochladen oder einfügen |
| **MA-Stammdaten** | HR-System | CSV / strukturierte Liste | Einfügen oder Skill-Frage beantworten |
| **Vertragsdaten** | Verträge (Miete, Versicherung, bAV, GF-Anstellungsvertrag) | PDF, Text | Hochladen + kurze Zusammenfassung des Sachverhalts |

**Praxis-Tipp:** Daten **lokal** halten — Cowork läuft auf deinem Rechner. Keine Cloud-Synchronisation der Belege ohne ausdrückliche Freigabe; DSGVO-Pflichten bleiben beim Anwender.

**Geplante MCP-Integrationen** (in `.mcp.json` als `evaluating`):
- `datev_finrobotics` (Read-only EXTF-Import aus DATEV-Exporten)
- `datev_badrix` (Read + Write inkl. EXTF-Export für DATEV-Import)
- `bank_hbci` (HBCI/FinTS Bank-API)
- `elster` (XML-Vorbereitung — kein Direktversand)

---

## Vergleich: germany-accounting (DE/HGB) vs. Anthropic Finance Plugin (US/GAAP)

**Architektur**: identisch — Knowledge/Workflow-Trennung, source-fidelity-Disziplin, Markdown + CSV + Excel als Output.
**Inhalt**: portiert auf DE-Rechtslage. Wo US-spezifisch (z.B. SOX), durch das deutsche Äquivalent (IDW PS 261) ersetzt. Plus DACH-spezifische Skills (USt-VA, Lohn, GoBD, DATEV-Export, StB-Handoff).

### Skills

| Anthropic Finance (US-GAAP) | germany-accounting (HGB) | Status |
|---|---|---|
| `journal-entry-prep` | `buchung-grundlagen` (Knowledge) | übernommen |
| `journal-entry` | `buchungssatz` (Workflow) | übernommen + DE-USt-Tatbestände + SKR03/04 |
| `reconciliation` | `abstimmung` | übernommen + EWB/PWB-Logik nach HGB |
| `financial-statements` | `jahresabschluss` + `ebilanz` | aufgeteilt: HGB-Aufstellung + eBilanz-Datenpaket |
| `variance-analysis` | `abweichungsanalyse` | übernommen, gleiche Methodik |
| `close-management` | `monatsabschluss` + `jahresabschluss` | aufgeteilt nach Periode |
| `sox-testing` | `iks-pruefung` | SOX 404 ersetzt durch IDW PS 261 / COSO |
| `audit-support` | teilweise in `iks-pruefung`, `gobd-konformitaet` | aufgeteilt |
| — | `ust-voranmeldung` | **DE-neu** — keine US-Entsprechung (Bund-Sales-Tax dezentral) |
| — | `lohnabrechnung` | **DE-neu** — US-Payroll grundsätzlich anders |
| — | `gobd-konformitaet` | **DE-neu** — BMF-spezifisches Verwaltungsrecht |
| — | `hinschg-meldewesen` | **DE-neu** — EU-Whistleblower-Richtlinie + HinSchG |
| — | `datev-export` | **DACH-neu** — DATEV-EXTF-Standard |
| — | `steuerberater-handoff` | **DACH-neu** — StB-System hat keine US-Entsprechung |

### Slash-Commands

| Anthropic | germany-accounting | Hinweis |
|---|---|---|
| `/journal-entry` | `/buchungssatz` | Output formatär identisch (Soll/Haben + §) |
| `/reconciliation` | `/abstimmung` | Output formatär identisch |
| `/income-statement` | (im `/jahresabschluss`-Output enthalten) | GuV ist Teil der Bilanz/GuV-Aufstellung |
| `/variance-analysis` | `/abweichungsanalyse` | Identische Decomposition-Logik |
| `/sox-testing` | `/iks-pruefung` | IDW-PS-261-Framework statt SOX-Walkthroughs |
| — | 9 weitere DE-Commands | siehe Skills-Tabelle oben |

---

## Geltungsbereich

- **In Scope:** GmbH, UG (haftungsbeschränkt)
- **Out of Scope (architektonisch erweiterbar):** AG, KGaA, GmbH & Co. KG, OHG, KG, eGbR/GbR, Einzelunternehmen, Vereine, Stiftungen

Details: [`config/shared/entity-types.json`](config/shared/entity-types.json), [`docs/SCOPE.md`](docs/SCOPE.md).

## Mehrjahres-Config

`config/{year}/` enthält jahres-spezifische Werte (Sätze, BBG, Mindestlohn, Kontenrahmen-Wording, Fristen, USt-VA-KZ-Codes). Aktuell verifiziert: **2025 + 2026**. Stub: 2027. Pointer in `config/active-year.json`.

## Output-Formate

- **Markdown** — Buchungsvorschläge, Begründungen, Quellen-Verweise (Default)
- **DATEV-Buchungsstapel-CSV** (EXTF) — importfähig in DATEV-Software
- **Excel-Tabellen** — Abstimmungen, Analysen, Bilanz/GuV
- **Steuerberater-Handoff-Brief** — strukturiert für StB-Übergabe

**Nicht enthalten:** direkter ELSTER-Versand, Bundesanzeiger-Offenlegung, eBilanz-XBRL-Übermittlung — bleibt bei Anwender / StB.

## Quellen

[`docs/SOURCES.md`](docs/SOURCES.md) — alle Primärquellen (HGB/EStG/UStG/etc. auf gesetze-im-internet.de, DATEV-PDFs, BMF-Schreiben, SGB, IDW).

## Lizenz

Apache License 2.0 — siehe [`LICENSE`](LICENSE). Lineage-Hinweis im LICENSE-Footer, vollständige Provenienz in [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## Beiträge

[`CONTRIBUTING.md`](CONTRIBUTING.md). Insbesondere willkommen: Verifikation gegen aktuelle Rechtslage, Erweiterungen für weitere Rechtsformen, MCP-Server-Anbindung an DATEV.

## Verwandte Projekte

- [Anthropic Finance Plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance) — US-Pendant
- [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) — Anthropic's Meta-Marketplace (enthält Finance, Sales, weitere)
- DATEV-MCP-Server (geplant, in `.mcp.json` als `evaluating`): `datev_finrobotics`, `datev_badrix`
