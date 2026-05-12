---
name: jahresabschluss
description: Erstellung von Bilanz (§266 HGB), GuV (§275 HGB), Anhang und Steuerpositionen fuer GmbH/UG.
---

> ⚠ **Hinweis:** Automatisiertes Hilfsmittel auf Basis öffentlich verifizierter Quellen (DATEV-SKR03/04 2026 Art.-Nr. 11174/11175, HGB/EStG/UStG/KStG/SGB Stand 2026-05, BMF-Schreiben). **Ersetzt keine Steuerberatung.** Output ist Vorschlag — vor produktiver Buchung Konten und §-Verweise stichprobenartig prüfen, bei rechtlicher Unsicherheit Steuerberater/Wirtschaftsprüfer konsultieren.

# Jahresabschluss

**Typ:** `workflow` (workflow / knowledge / methodology)
**Anthropic-Pendant:** `financial-statements`
**Geltungsbereich:** GmbH, UG (siehe `config/shared/entity-types.json` für vollständige Scoping-Definition)
**Config:** `config/{active_year}/` (Default: 2026)

---

## 1. Zweck

(TODO: Was tut diese Skill konkret? In 2-3 Saetzen.)

## 2. Eingaben

(TODO: Welche Informationen muss der User liefern?)

## 3. Workflow / Vorgehen

(TODO: Schritt-fuer-Schritt was Claude tun soll, mit Verweisen auf Config-Files.)

## 4. Output-Format

(TODO: Wie sieht das Ergebnis aus? Welche Bestandteile?)

## 5. Validierung

(TODO: Welche automatischen Pruefungen erfolgen?)

## 6. Quellen

- `config/{active_year}/rates.json`
- `config/{active_year}/kontenrahmen.json`
- (weitere §-/Quellen-Verweise je Skill)

## 7. Verwandte Skills

- (siehe `buchung-grundlagen` fuer Hintergrundwissen)
- (cross-references)

---

**Status:** SKELETON — Inhalt wird in Phase 4 der v2.0-Migration befuellt. Verifizierte v1.1.0-Quelle: `git show main:skills/<entsprechender-name>/SKILL.md`
