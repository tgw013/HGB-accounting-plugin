# Scripts

Hilfs-Skripte für Wartung und Verifikation. Nicht zur Laufzeit des Plugins notwendig.

## `extract_datev_pdf.py`

**Zweck:** Extrahiert Konto-Nummern + -Bezeichnungen aus den offiziellen DATEV-Kontenrahmen-PDFs (SKR03 Art.-Nr. 11174, SKR04 Art.-Nr. 11175) in eine TSV-Datei zur Verifikation.

**Warum nicht `pdftotext`?** Die DATEV-PDFs haben pro Seite zwei Spalten. `pdftotext -layout` schreibt diese Spalten nebeneinander auf dieselbe Zeile — Grep-Treffer können Bezeichnungen aus der falschen Spalte erwischen. Zusätzlich nutzen die PDFs eine Konvention, bei der mehrere konsekutive Konten denselben Bezeichnungs-Stamm haben:

```
1248 Pauschalwertberichtigung auf
     Forderungen
     – Restlaufzeit bis 1 Jahr
1249 – Restlaufzeit größer 1 Jahr
```

Beide Konten meinen "Pauschalwertberichtigung auf Forderungen – Restlaufzeit ...".
Ein naives Extraktions-Skript würde 1249 fälschlicherweise nur als
"– Restlaufzeit größer 1 Jahr" speichern.

**Funktion des Skripts:**
1. Trennt jede Seite spaltenweise über die x-Koordinaten der Wörter
2. Liest erst die linke, dann die rechte Spalte
3. Fasst gewickelte Mehrzeilen-Bezeichnungen zusammen
4. Erkennt Dash-Continuation-Bezeichnungen und ergänzt den Stamm-Label

**Nutzung:**
```bash
pip install pdfplumber
python scripts/extract_datev_pdf.py PFAD/ZU/SKR04.pdf .skr04-clean.tsv
python scripts/extract_datev_pdf.py PFAD/ZU/SKR03.pdf .skr03-clean.tsv
```

Die Output-TSVs sind `gitignore`d — DATEV-PDF-Inhalte sind urheberrechtlich geschützt, keine Versionskontrolle.

**Bekannte Grenzen:**
- Einige Konten mit umfangreicher Layout-Eigenheit (z.B. 1246/1247 mit eingerückten Sub-Strukturen) werden nicht sauber extrahiert
- Wenige Konten mit Hyperkerning (Zeichenabstand) werden ggf. mit Leerzeichen zwischen Buchstaben extrahiert
- Etwa 20 von ~1.000 Konten pro Rahmen haben Edge-Cases — bei Zweifel Original-PDF konsultieren

**Verwendung im Wartungsprozess:** Vor jeder Jahres-Release neu erzeugen und gegen `config/{jahr}/kontenrahmen.json` diff'en, um Konto-Renamings / -Streichungen / -Neuanlagen zu erkennen. Siehe `UPDATE_CHECKLIST.md`.
