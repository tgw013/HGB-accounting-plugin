# germany-accounting (HGB-Plugin für Claude)

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

**Status:** `v2.0.0` — produktive Linie auf `main`. 14 Skills + 14 Commands befüllt, 128 Konten gegen DATEV-PDFs 2025+2026 verifiziert. Output bleibt **Vorschlag** — vor produktiver Buchung mit Steuerberater/Wirtschaftsprüfer abgleichen. Vorherige Stände bleiben als Tags erreichbar (`v1.1.0`, `v2.0.0-alpha`).

---

## Was ist das?

Ein Claude-Plugin für **deutsche Finanzbuchhaltung nach HGB** mit Fokus auf:

- **DATEV-Anwender** (SKR03 / SKR04, Buchungsstapel-CSV)
- **GmbH und UG** (haftungsbeschränkt) — bewusst eng gefasst
- **Workflow-Unterstützung**: Buchungssätze, Monats-/Jahresabschluss, USt-Voranmeldung, Lohnabrechnung, eBilanz-Vorbereitung, GoBD-Konformität, IKS-Prüfung
- **Steuerberater-Handoff**: Strukturierte Übergabe statt Eigenversand an ELSTER/Bundesanzeiger

Inspiriert vom offiziellen [Anthropic Finance Plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance) (US-fokussiert: Journal-Entry-Prep, Reconciliation, Close-Management, Variance-Analysis, SOX-Testing) — eigenständig auf deutsche Rechtslage portiert (HGB, DATEV-SKR03/04, BMF-Vordruckmuster, IDW PS 261 statt SOX).

## Quick Overview (English)

`germany-accounting` is a Claude plugin providing German bookkeeping (HGB) workflows: SKR03/SKR04 chart of accounts, VAT pre-registrations (USt-VA), monthly/annual closings, payroll, and GoBD/IKS compliance support — scoped to GmbH and UG (limited-liability) entities. Inspired by Anthropic's official finance skill (US-focused), independently built for German law (HGB, EStG, UStG, KStG, SGB, stand 2026-05). Output is a draft — review with a `Steuerberater` (tax advisor) before productive use.

---

## Installation

**In Claude Code** — innerhalb einer aktiven Session zwei Slash-Commands:

```
/plugin marketplace add tgw013/HGB-accounting-plugin-internal
/plugin install germany-accounting@hgb-accounting
```

Das war's. Skills + Commands stehen sofort zur Verfügung; `germany-accounting` ist in `/plugin` als installiert sichtbar.

**Voraussetzungen:** Claude Code installiert (`npm install -g @anthropic-ai/claude-code`, Node 18+). Bei privatem Repo zusätzlich `gh auth login` für GitHub-Zugriff.

**In Claude Cowork** (Desktop-Variante): Plugin-Marketplace ist offiziell ein Claude-Code-Feature. Ob Cowork die in Claude Code installierten Plugins automatisch übernimmt, ist offiziell **nicht dokumentiert**. Bei Bedarf testen und Rückmeldung über `/feedback` in Cowork erbitten.

**Lokale Entwicklung / Test ohne Marketplace:** `claude --plugin-dir ./HGB-accounting-plugin-internal` aus dem Eltern-Ordner des Klons startet Claude Code mit dem Plugin direkt geladen.

Quelle Plugin-Mechanik: [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins.md), [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces.md).

## Verfügbare Skills (v2.0-alpha)

| Skill | Typ | Zweck |
|---|---|---|
| `buchung-grundlagen` | knowledge | Doppik-Grundlagen, GoBD, SKR-Auswahl |
| `buchungssatz` | workflow | Beleg → Buchungsvorschlag |
| `monatsabschluss` | workflow | Monatliche Abschluss-Checkliste |
| `ust-voranmeldung` | workflow | USt-VA-Vorbereitung (BMF USt 1 A 2026) |
| `lohnabrechnung` | workflow | Lohnabrechnung GmbH-Geschäftsführer + Mitarbeiter |
| `jahresabschluss` | workflow | HGB-Jahresabschluss (Aufstellung) |
| `ebilanz` | workflow | eBilanz-Datenpaket-Vorbereitung |
| `abstimmung` | workflow | Konten-Abstimmung (Bank, OP, EWB/PWB) |
| `abweichungsanalyse` | workflow | Plan-Ist-Vergleich, Forecast |
| `gobd-konformitaet` | knowledge | GoBD-Anforderungen, Verfahrensdokumentation |
| `iks-pruefung` | methodology | IKS nach IDW PS 261 (5 COSO-Komponenten) |
| `hinschg-meldewesen` | knowledge | HinSchG-Anforderungen ab 50 MA |
| `datev-export` | workflow | DATEV-Buchungsstapel-CSV erzeugen |
| `steuerberater-handoff` | workflow | Übergabepaket für StB / WP |

## Geltungsbereich

- **In Scope:** GmbH, UG (haftungsbeschränkt)
- **Out of Scope (architektonisch erweiterbar):** AG, KGaA, GmbH & Co. KG, OHG, KG, eGbR/GbR, Einzelunternehmen, Vereine, Stiftungen

Details: [`config/shared/entity-types.json`](config/shared/entity-types.json) und [`docs/SCOPE.md`](docs/SCOPE.md).

## Mehrjahres-Config

`config/{year}/` enthält jahres-spezifische Werte (Sätze, Kontenrahmen, Fristen, KZ-Codes).
Aktuell verifiziert: **2026**. Pointer in `config/active-year.json`.

## Output-Formate

- **Markdown** (Buchungsvorschläge, Begründungen, Quellen-Verweise)
- **DATEV-Buchungsstapel-CSV** (importfähig in DATEV-Software)
- **Excel-Tabellen** (Abstimmungs- und Analyse-Output)
- **Steuerberater-Handoff-Brief** (strukturierte Übergabe)

**Nicht enthalten:** Direkte ELSTER-Übermittlung, XBRL/eBilanz-Direktversand. Diese Verantwortung bleibt beim Anwender / StB.

## Quellen

Vollständige Liste verifizierter Primärquellen: [`docs/SOURCES.md`](docs/SOURCES.md).

## Lizenz

Apache License 2.0 — siehe [`LICENSE`](LICENSE).

## Beiträge

Siehe [`CONTRIBUTING.md`](CONTRIBUTING.md). Beiträge willkommen — insbesondere Verifikation gegen aktuelle Rechtslage, Erweiterungen für weitere Rechtsformen.

## Verwandte Projekte

- [Anthropic Finance Plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/finance) — US-Pendant (Journal-Entry-Prep, Reconciliation, Close-Management, Variance-Analysis, SOX-Testing, Audit-Support, Financial-Statements)
- DATEV-MCP-Server (geplant): `datev_finrobotics` (Read-only EXTF), `datev_badrix` (Read+Write)
