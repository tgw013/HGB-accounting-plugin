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

**Wie funktioniert es im Detail (v4):**

1. **PyMuPDF (`fitz`)** statt `pdftotext` — liefert pro Span: Bounding-Box, Font-Name (Bold-Detection), und Unicode-Text inkl. korrekter Umlaute.
2. **Konto-Anchor-Detection:** Spans, deren Text mit optionalem Programmverbindungs-Präfix (F/S/R/KU/AM/…) + 4-Digit-Konto-Nummer beginnt, werden als Anker erkannt.
3. **Pro-Seite Spalten-Detektion:** Die kleinste x0 aller Konto-Anker in der linken Seitenhälfte = LHS-Konto-x; analog RHS. Die rechte Grenze der LHS-Konto-Sub-Spalte = Mittelpunkt zwischen LHS- und RHS-Konto-x (verhindert RHS-Bilanzposten-Bleed-in).
4. **Wrap-Continuation:** Spans ohne Konto-Anker, die innerhalb der Konto-Sub-Spalte liegen, werden an den vorherigen Anker angehängt.
5. **Heading-Detection:** Fette Spans ohne Konto-Anker, die bei x ≈ Wrap-Indent UND nach einer vertikalen Lücke (> 4.5pt zum vorherigen Wrap) erscheinen → Section-Heading wie "Finanzanlagen". Brechen die Wrap-Kette ohne selbst Konto zu werden.
6. **Footer-Filter:** Spans mit `top > page_height - 25` (Art.-Nr./Datum-Footer) werden ignoriert.
7. **Range-Marker-Filter:** Spans wie `-69` (Programmverbindungs-Range) werden ignoriert.
8. **Hyphenation-Smart-Join:** Wort-Bindestriche werden kontextabhängig zusammengefügt — vor `und/oder/auf/im/...` bleibt der Bindestrich (`"Betriebs- und Geschäftsausstattung"`); sonst wird zusammengezogen (`"Altersversor- gung"` → `"Altersversorgung"`).
9. **Dash-Continuation-Resolution:** Folge-Konten mit `"– …"` erben den Stamm-Label des vorherigen, gesplittet an `\s+[-–]\s+`. Behebt 1248/1249-Konvention.

**Bekannte Grenzen:**
- Bei extrem dichten Layouts (Bilanzposten-Box-Labels in 3-Spalten-Wirrwarr) können vereinzelt Bezeichnungen leicht abweichend extrahiert werden
- Bei Zweifel das Original-PDF konsultieren — der Cross-Check über `scripts/generate_verification_sheet.py` zeigt v2-Bezeichnung neben PDF-Bezeichnung

## `generate_verification_sheet.py`

Erzeugt `konten-verification.tsv` (gitignored) — Side-by-Side Vergleich der ~129 Konten aus `config/2026/kontenrahmen.json` gegen die frisch extrahierten PDF-Bezeichnungen. Spalten:

```
konto | rahmen | bold | v2_bezeichnung_paraphrased | pdf_bezeichnung_extracted
```

Voraussetzung: `.skr03-clean.tsv` und `.skr04-clean.tsv` wurden vorher erzeugt.

**Wartungsprozess:** Vor jeder Jahres-Release neu erzeugen und gegen `config/{jahr}/kontenrahmen.json` diff'en, um Konto-Renamings / -Streichungen / -Neuanlagen zu erkennen. Siehe `UPDATE_CHECKLIST.md`.
