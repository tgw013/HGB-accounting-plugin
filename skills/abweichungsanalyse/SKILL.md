---
name: abweichungsanalyse
description: Plan-Ist-Vergleich + Forecast — Erlös-/Kosten-Abweichungs-Zerlegung (Preis/Menge/Mix), BWA-Kommentierung, Forecast-Aktualisierung.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# Abweichungsanalyse

**Typ:** `workflow`
**Anthropic-Pendant:** `variance-analysis`
**Geltungsbereich:** GmbH, UG
**Config:** `config/{active_year}/kontenrahmen.json`
**Knowledge-Base:** `buchung-grundlagen`

---

## 1. Zweck

Vergleicht Ist-Werte gegen Plan, Vorjahr oder Forecast; zerlegt Abweichungen in Preis-/Mengen-/Mix-Effekte; kommentiert BWA; aktualisiert Forecast. Klassisches Controlling-Werkzeug — keine HGB-Pflicht, aber Pflicht-Tool für CFO/COO-Steuerung.

## 2. Eingaben

- Periode (Monat, YTD, Quartal, Jahr)
- Ist-Werte (Saldenliste, Buchhaltungsexport)
- Vergleichsbasis: Plan, Forecast, Vorjahres-Periode, oder Kombination
- Vergleichs-Tiefe: Top-Level (Erlös, EBIT, EBITDA), nach Sparte/Produkt, nach Konto-Klasse
- (Optional) Stamm-Daten für Mengen-/Preis-Decomposition (Stück, ASP)

## 3. Workflow

### 3.1 Basis-Aufbereitung
- Vergleichsperioden auf gleiche Definition normieren (z.B. YTD vs YTD, gleiche Bilanzierungs-Wahlrechte)
- Einmal-Effekte trennen (z.B. Veräußerungsgewinne, Restrukturierungs-Aufwand)
- Währungsbereinigung (sofern relevant)

### 3.2 Vergleichs-Berechnung
- Absolut + Prozent
- Vorzeichen vereinheitlichen (Aufwand positiv kommunizieren)

### 3.3 Decomposition (Erlös)
**Preis-Effekt:** (ASP_ist − ASP_plan) × Menge_ist
**Mengen-Effekt:** (Menge_ist − Menge_plan) × ASP_plan
**Mix-Effekt:** Restdifferenz / aggregierte Produkt-Verschiebung

### 3.4 Decomposition (Kosten)
- **Variabel** (Material, var. Personal, Energie) → mengen-proportional, ggf. Preis-Effekt
- **Fix** (Mieten, Versicherungen, Abschreibungen) → Vergleich vs. Plan-Annahme
- **Personalkosten**: Stellenbesetzung × Durchschnittsgehalt, ggf. Tarifsteigerung

### 3.5 BWA-Kommentierung
- 3–5 Top-Treiber für Gesamt-Abweichung priorisieren
- Trend (verschlechternd / verbessernd / stabil)
- Handlungs-Empfehlung (z.B. Preis-Anhebung, Lieferantenwechsel, MA-Kapazität)

### 3.6 Forecast-Update
- Restjahres-Forecast unter Berücksichtigung aktueller YTD-Performance
- Sensitivitäten (Best / Base / Worst)
- Liquiditäts-Implikation grob

## 4. Output-Format

```
**Abweichungsanalyse 01-04/2026 YTD vs. Plan** (GmbH)

GuV-Position           | Plan YTD | Ist YTD | Δ €     | Δ %   | Kommentar
Umsatzerlöse           | 220.000  | 234.500 | +14.500 | +6,6% | Preis +8k, Menge +6,5k
Materialaufwand        | -88.000  | -98.000 |  -10.000| +11%  | Stahlpreis +12% (Index)
Personalaufwand        | -52.000  | -54.000 |  -2.000 | +3,8% | Tarif-Anpassung
sonst. betr. Aufwand   | -28.000  | -27.500 |    +500 | -1,8% |
EBITDA                 |  52.000  |  55.000 |  +3.000 | +5,8% |
Abschreibungen         |  -8.000  |  -8.000 |       0 |     - |
EBIT                   |  44.000  |  47.000 |  +3.000 | +6,8% |

TOP-TREIBER
1. Materialkosten: ungeplant +10k — Stahlpreis-Index +12% YoY → Preisweitergabe an Kunden prüfen
2. Umsatz Preis-Effekt +8k — Listenpreisanpassung 02/2026 trägt
3. Personal: Tarif-Plan-Annahme +2% vs. Real +3,5%

FORECAST UPDATE
- Restjahr Material: +25k zu Plan (annualisiert)
- Kompensierbar durch +3% Preisanhebung Q3 → EBIT-Punktlandung
- Worst Case (keine Anhebung): EBIT -22k vs. Plan
```

## 5. Validierung

- Plan + Δ = Ist (rechnerische Konsistenz)
- Aufwands-Vorzeichen einheitlich
- Sonder-Effekte ausgewiesen
- Vergleichsperioden definitorisch identisch

## 6. Quellen

- HGB § 275 (GuV-Struktur)
- Controlling-Standardliteratur (nicht-rechtlich, Methode)
- `config/2026/kontenrahmen.json`

## 7. Verwandte Skills

- `monatsabschluss` — liefert die Ist-Salden
- `abstimmung` — vorgelagert
- `steuerberater-handoff` — Abweichungsbericht ist Anlage zur StB-Übergabe
