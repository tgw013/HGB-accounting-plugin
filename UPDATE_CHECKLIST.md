# Jährliche Update-Checkliste

Diese Checkliste durchgehen vor jeder neuen Jahres-Release (z.B. v2.x.0 für VZ 2027).

## 1. Neuen Jahres-Ordner anlegen

- [ ] `config/{neues_jahr}/README.md` aus Stub befüllen
- [ ] `config/active-year.json` auf neues Jahr setzen (erst nach vollständiger Verifikation!)

## 2. Sätze und Werte (`config/{jahr}/rates.json`)

- [ ] **Umsatzsteuer**: Normal- (19%) / ermäßigt (7%) — Änderung sehr unwahrscheinlich, aber prüfen
- [ ] **Mindestlohn**: Quelle BMAS, Mindestlohnkommission-Beschluss
- [ ] **BBG Renten-/Arbeitslosenversicherung West/Ost** (oder einheitlich ab 2025): Sozialversicherungs-Rechengrößenverordnung
- [ ] **BBG GKV/PV**: GKV-Spitzenverband-Veröffentlichung
- [ ] **Pflegeversicherungssatz** + Zuschlag für Kinderlose, Abschläge je Kind: SGB XI § 55
- [ ] **Solidaritätszuschlag-Freigrenze**: BMF / Solidaritätszuschlaggesetz
- [ ] **Grundfreibetrag / Tarifeckwerte**: EStG § 32a
- [ ] **Sachbezugswerte** (Verpflegung, Unterkunft): Sozialversicherungsentgeltverordnung
- [ ] **Verpflegungspauschalen In-/Ausland**: BMF-Schreiben jährlich
- [ ] **kFz-Pauschale / 1%-Regelung**: keine Jahresanpassung üblich, aber prüfen
- [ ] **Aufbewahrungsfristen**: § 147 AO — letzte Änderung 2025 (von 10 auf 8 Jahre für ab 01.01.2025)
- [ ] **Kleinunternehmer-Grenzen**: § 19 UStG (aktuell 25k Vorjahr / 100k laufend, ab 2025)

## 3. Kontenrahmen (`config/{jahr}/kontenrahmen.json`)

- [ ] Aktuelles DATEV-PDF SKR03 (Art.-Nr. 11174) für das Jahr beschaffen
- [ ] Aktuelles DATEV-PDF SKR04 (Art.-Nr. 11175) für das Jahr beschaffen
- [ ] Diff gegen Vorjahr — neue/geänderte/entfallene Konten markieren
- [ ] Bei strukturellen Änderungen: alle Skills auf betroffene Konten-Referenzen grep'en

## 4. USt-VA KZ-Codes (`config/{jahr}/kz-codes-ust-va.json`)

- [ ] BMF-Vordruckmuster USt 1 A für das neue Jahr (BMF-Schreiben Ende Dezember Vorjahr)
- [ ] KZ-Code-Tabelle 1:1 abgleichen
- [ ] Zeilen-Nummern im Formular abgleichen (verschieben sich oft)

## 5. Fristen-Kalender (`config/{jahr}/fristen.json`)

- [ ] Steuererklärungsfristen-Verlängerungen (häufig per Sondergesetz, z.B. Corona-Verlängerungen, "Viertes Corona-Steuerhilfegesetz", Wachstumschancengesetz)
- [ ] § 149 AO-Fristen prüfen
- [ ] Vorauszahlungstermine GewSt/KSt unverändert? (§ 19 GewStG / § 37 EStG i.V.m. § 31 KStG)

## 6. Cross-Skill-Verifikation

- [ ] Alle Skills auf `2026` / `Stand 2026` / `VZ 2026` grep'en und Bezüge aktualisieren
- [ ] Disclaimer-Block in jedem Skill auf aktuelles Jahr setzen
- [ ] Beispiele in Skills durchprüfen: Sätze noch korrekt?

## 7. Doku

- [ ] `CHANGELOG.md` Eintrag mit Jahres-Update
- [ ] `docs/SOURCES.md`: neue PDF-Versionsnummern eintragen
- [ ] `README.md`-Tabelle aktuell?

## 8. Tests (sobald `tests/scenarios/` befüllt)

- [ ] Szenarien gegen neue Sätze re-rechnen
- [ ] Erwartete Outputs auf neues Jahr anpassen

## 9. EXTF-Format-Validierung (Pflicht bei jeder Release, die `scripts/generate_extf.py`, `config/shared/datev-extf-fields.json` oder `tests/fixtures/` berührt)

DATEV-Format-Prüfprogramm-Lauf gegen alle Test-Fixtures. Erwartetes Ergebnis: **`Headermeldungen: 0, Datensatzmeldungen: 0`** pro Fixture.

- [ ] Prüfprogramm lokal installiert (von [developer.datev.de](https://developer.datev.de/) → Tools, kostenloser DATEV-Entwickler-Account; Repo enthält die EXE wegen DATEV-Lizenz NICHT)
- [ ] Für jede Datei in `tests/fixtures/*/input.json`: `scripts/run_pruefprogramm.ps1 -PruefprogrammExe <pfad> -InputJson <fixture>` ausführen
- [ ] In jedem Prüfprogramm-Fenster: Header-Tab + Datensätze-Tab + Bericht-Tab visuell auf 0 Meldungen prüfen
- [ ] Bei Befund: Fehler an `scripts/generate_extf.py` oder `config/shared/datev-extf-fields.json` reproduzieren, fixen, neuen Regression-Test in `tests/test_extf_serializer.py::TestPruefprogrammMeldung110` ergänzen
- [ ] Erst nach grünem Lauf aller Fixtures: nächster Schritt (§10 Release)

**Begründung:** der Prüfprogramm-Lauf ist die einzige Validierung, die *spec-exakt* gegen DATEV's eigenen Validator prüft. Tests im Plugin sind notwendig, aber nicht hinreichend. Beispiel-Bug, der nur per Prüfprogramm gefunden wurde: 23 Text-Felder emittierten `;;` statt `";";` für leere Werte → Prüfprogramm Meldung 110 (323× warnings). Fix in v2.1.0 Commit `1eb9c2f`.

**Warum kein CI (Stand v2.1.0):** EXE-Redistribution unter DATEV-Lizenz problematisch + GitHub-Secret-Cap 64 KB vs. 314 KB EXE + GUI-Subsystem ohne parsbaren Exit-Code. Re-evaluation, sobald erste externe PR `scripts/generate_extf.py` berührt. Bis dahin: manuell als Release-Gate via dieser Checkliste.

## 10. Release

- [ ] `plugin.json` + `marketplace.json` Version bumpen
- [ ] `CHANGELOG.md` `[neue_version]` Eintrag
- [ ] Tag `v{neue_version}` setzen
- [ ] Release-ZIP bauen + `gh release create` mit Asset
- [ ] Release Notes aus CHANGELOG generieren

---

**Wichtig:** Nicht das neue Jahr in `active-year.json` aktivieren, solange auch nur ein Punkt offen ist. Lieber Übergangsphase im alten Jahr bleiben.
