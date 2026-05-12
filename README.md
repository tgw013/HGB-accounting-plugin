# germany-accounting (HGB-Plugin für Claude)

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

**Status:** `v2.0.0-alpha` — Skeleton-Phase. Inhalt der Skills wird in Phase 4 der v2.0-Migration befüllt. Für produktive Verwendung den Stand `v1.1.0` (Branch `main`) nutzen.

---

## Was ist das?

Ein Claude-Plugin für **deutsche Finanzbuchhaltung nach HGB** mit Fokus auf:

- **DATEV-Anwender** (SKR03 / SKR04, Buchungsstapel-CSV)
- **GmbH und UG** (haftungsbeschränkt) — bewusst eng gefasst
- **Workflow-Unterstützung**: Buchungssätze, Monats-/Jahresabschluss, USt-Voranmeldung, Lohnabrechnung, eBilanz-Vorbereitung, GoBD-Konformität, IKS-Prüfung
- **Steuerberater-Handoff**: Strukturierte Übergabe statt Eigenversand an ELSTER/Bundesanzeiger

Inspiriert von der offiziellen [Anthropic Finance Skill](https://github.com/anthropics/skills) (US-fokussiert), eigenständig auf deutsche Rechtslage portiert.

## Quick Overview (English)

`germany-accounting` is a Claude plugin providing German bookkeeping (HGB) workflows: SKR03/SKR04 chart of accounts, VAT pre-registrations (USt-VA), monthly/annual closings, payroll, and GoBD/IKS compliance support — scoped to GmbH and UG (limited-liability) entities. Inspired by Anthropic's official finance skill (US-focused), independently built for German law (HGB, EStG, UStG, KStG, SGB, stand 2026-05). Output is a draft — review with a `Steuerberater` (tax advisor) before productive use.

---

## Installation

```bash
# Plugin in Claude Code lokal registrieren (Repo-Pfad anpassen)
claude plugin add ./path/to/HGB-accounting-plugin-internal
```

`plugin.json` deklariert Name `germany-accounting`. Skills werden automatisch geladen, Slash-Commands stehen unter `/<command-name>` zur Verfügung.

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

- [Anthropic Finance Skill](https://github.com/anthropics/skills) — US-Pendant, Inspiration für v2.0-Struktur
- DATEV-MCP-Server (geplant): `datev_finrobotics` (Read-only EXTF), `datev_badrix` (Read+Write)
