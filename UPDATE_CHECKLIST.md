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

## 9. Release

- [ ] `plugin.json` Version bumpen
- [ ] Tag `v{neue_version}` setzen
- [ ] Release Notes aus CHANGELOG generieren

---

**Wichtig:** Nicht das neue Jahr in `active-year.json` aktivieren, solange auch nur ein Punkt offen ist. Lieber Übergangsphase im alten Jahr bleiben.
