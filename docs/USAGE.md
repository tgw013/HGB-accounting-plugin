# USAGE — Praktische Nutzung des HGB-Accounting Plugins

## Was dieses Plugin tut

11 Skills + 10 Commands für die deutsche Finanzbuchhaltung nach HGB/GoBD:
- **buchungssatz** + **buchungssatz-vorbereitung** — Buchungssätze nach HGB-Logik
- **ust-voranmeldung** — Umsatzsteuer-Voranmeldung Vorbereitung (USt 1 A 2026)
- **lohnabrechnung** — Vollständige Lohn-/Gehaltsabrechnung mit SV + LSt + bAV
- **monatsabschluss** + **jahresabschluss** + **ebilanz** — Periodenabschlüsse + XBRL-Übermittlung
- **abstimmung** — Konten-/USt-Abstimmung mit EWB/PWB
- **abweichungsanalyse** — Plan-Ist-Vergleich nach IDW PS 250
- **compliance** + **iks-pruefung** — GoBD, HinSchG, DCGK, IDW PS 261

Alle Konto-Nummern und Rate-Werte sind gegen die DATEV-Standardkontenrahmen 2026 (Art.-Nr. 11174 SKR03 / 11175 SKR04) und die aktuelle Gesetzgebung (HGB/EStG/UStG/KStG/SGB Stand 2026-05) verifiziert.

---

## Was dieses Plugin NICHT tut

- **Ersetzt keinen Steuerberater oder Wirtschaftsprüfer.** Output ist immer ein Vorschlag, keine Freigabe.
- **Keine ELSTER-Übermittlung.** Die Skills bereiten die Daten vor; die tatsächliche Übermittlung erfolgt über ELSTER / DATEV / dein Buchhaltungssystem.
- **Keine Echtzeit-Daten.** Konto-Salden, OP-Listen, Bankauszüge müssen aus deiner Buchhaltung kommen.
- **Keine Rechtsberatung.** Bei unklaren Rechtsfragen → Steuerberater.

---

## Installation

### Claude Code (CLI)

```bash
# In deinem Projekt-Repo:
cd <projekt>
git clone https://github.com/tgw013/HGB-accounting-plugin.git .claude/plugins/germany-accounting

# Oder via Claude Code's Plugin-Marketplace (wenn dort gelistet)
claude plugin install germany-accounting
```

### Claude Desktop

Plugin via Cowork-Plugin-Upload installieren (siehe Claude-Dokumentation).

### Lokal testen (ohne Installation)

Das Repo direkt klonen und Claude Code mit `--plugin-dir` darauf zeigen lassen, oder Skills manuell ins `.claude/skills/`-Verzeichnis kopieren.

---

## Erste Schritte

### Beispiel-Anfragen

| Was du sagst | Welcher Skill greift |
|---|---|
| "Stelle einen Buchungssatz für die Lieferanten-Rechnung über 2.380 € brutto" | `buchungssatz` |
| "Prüfe die USt-Voranmeldung für März 2026" | `ust-voranmeldung` |
| "Berechne die Lohnabrechnung für ein Bruttogehalt von 4.500 €" | `lohnabrechnung` |
| "Mache den Monatsabschluss für Februar 2026" | `monatsabschluss` |
| "Reconciliere die Bank-Konten zum 31.03.2026" | `abstimmung` |
| "Bereite die eBilanz für GJ 2026 vor" | `ebilanz` |

Alternativ via Slash-Commands:
```
/buchungssatz
/ust-voranmeldung
/lohnabrechnung
...
```

### Was Claude tut, wenn ein Skill greift

1. Liest die SKILL.md des relevanten Skills (inkl. Disclaimer-Hinweis)
2. Lädt `config/rates-2026.json` und `config/kontenrahmen.json` aus dem Plugin
3. Fragt dich nach den fehlenden Eingaben (z. B. Brutto, Anzahl AN, Geschäftsjahr)
4. Erstellt den Buchungssatz / die Berechnung / die Auswertung
5. Verweist auf die §-Grundlagen und die verwendeten DATEV-Konten
6. Bei kritischen Stellen: Hinweis auf Steuerberater-Konsultation

---

## Sicheres Arbeiten in der Praxis — "Validate-as-you-go"

Da du das Plugin in der Praxis nutzen willst, ohne vorab eine teure Komplett-Prüfung zu bezahlen, ist das Vorgehen:

### 1. Beim ersten Mal: Spot-Check gegen DATEV

Wenn Claude einen Konto-Vorschlag macht, prüfe stichprobenartig:
- **SKR03/SKR04 Konto-Nummer** gegen die DATEV-PDF (oder DATEV-Hilfe-Center)
- **§-Verweise** gegen [gesetze-im-internet.de](https://www.gesetze-im-internet.de) — Wortlaut der zitierten Paragraphen prüfen
- **Beträge** nachrechnen (z. B. AG-SV-Beiträge, Vorsteuer-Berechnung)

### 2. Bei jeder ersten Anwendung eines Skill-Typs: Steuerberater-Briefing

Für die ersten 1-3 echten Anwendungen jeder Skill:
- Output mit Steuerberater besprechen
- "Hier ist der vorgeschlagene Buchungssatz / die vorgeschlagene Voranmeldung. Bitte verifizieren."
- Steuerberater-Korrekturen in `ISSUES_LOG.md` notieren (siehe unten)

### 3. Bei Routine-Anwendungen: Konsistenz-Check

Wenn du den Skill in der Praxis 5+ Mal mit ähnlichen Sachverhalten benutzt hast und die Outputs konsistent gegen Steuerberater-Reviews bestätigt sind: Steuerberater-Konsultation nur noch bei **Abweichungen** vom Routinemuster.

### 4. Bei kritischen Sachverhalten: Immer Steuerberater

Pflicht-Konsultation bei:
- **GbR / eGbR** (siehe OPEN_QUESTIONS.md #1 — § 264a HGB-Frage)
- **Sektor-spezifischen Sachverhalten** (Bau, Pflege, Banken, Versicherungen)
- **Konzernrechnungslegung** und Konsolidierung
- **Erstmaliger Anwendung** einer neuen Vorschrift (z. B. neues BMF-Schreiben)
- **Steuerprüfungen** und Betriebsprüfungen
- **Gerichtsverfahren** (Finanzgericht, Steuerstreit)

### 5. Issue-Logging für Lerneffekte

Wenn dir oder dem Steuerberater eine Abweichung / ein Fehler im Plugin-Output auffällt:

1. Eintrag in `ISSUES_LOG.md` machen (Datum, Sachverhalt, falscher Output, korrekte Antwort)
2. Falls kontenrahmen.json oder rates-2026.json betroffen: PR mit Korrektur
3. Falls Skill-Logik betroffen: Issue im GitHub-Repo

---

## Quellen und Authoritative Referenzen

Wenn du selbst etwas verifizieren möchtest:

| Quelle | URL |
|---|---|
| DATEV-Hilfe-Center SKR03 2026 | https://help-center.apps.datev.de/api/amr/knowledge-common/v1/entities/st65108547211_de.pdf |
| DATEV-Hilfe-Center SKR04 2026 | https://help-center.apps.datev.de/api/amr/knowledge-common/v1/entities/st65118491659_de.pdf |
| BMF Vordruckmuster USt 1 A 2026 | https://www.bundesfinanzministerium.de/.../2025-12-29-vordruckmuster-USt-voranmeldung-2026.pdf |
| BMF Muster USt-Erklärung 2026 | https://www.bundesfinanzministerium.de/.../2025-12-29-muster-USt-erklaerung-2026.pdf |
| Gesetze (HGB, EStG, UStG, KStG, SGB, AO etc.) | https://www.gesetze-im-internet.de |
| Sozialversicherungs-Rechengrößen 2026 | https://www.gesetze-im-internet.de/svbezgrv_2026/ |
| BMG Pflegeversicherung | https://www.bundesgesundheitsministerium.de/themen/pflege/online-ratgeber-pflege/die-pflegeversicherung/finanzierung |

---

## Bei Problemen

- **Plugin lädt nicht:** Frontmatter prüfen (`name:` Feld muss vorhanden sein). `plugin.json` validieren.
- **Konto-Vorschlag wirkt falsch:** Mit DATEV-PDF abgleichen, in `OPEN_QUESTIONS.md` nachsehen, ggf. `ISSUES_LOG.md` ergänzen
- **§-Verweis veraltet:** gesetze-im-internet.de prüfen, ggf. Issue/PR
- **Plugin-Update wegen Jahreswechsel:** Siehe OPEN_QUESTIONS.md #3 — rates-2026 → rates-2027

---

## Iterative Verbesserung

Dieses Plugin ist als Living Document gedacht. Bei jeder Praxis-Anwendung:
1. Notiere, was geklappt hat
2. Notiere, was Steuerberater korrigiert hat
3. Aktualisiere das Plugin entsprechend

Die volle Audit-Historie ist in `ACCOUNTING_REVIEW_FIRST_PASS.md` (4 Addenda mit allen ursprünglichen Befunden) und `CHANGES_APPLIED.md` (Liste aller bisherigen Korrekturen) dokumentiert.

End of USAGE.md
