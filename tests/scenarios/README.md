# Test-Szenarien

Realistische Geschäftsvorfälle als Markdown-Triplets: **Input → Erwarteter Output → Begründung**.

Zweck: Regression bei Skill-Refactors, Onboarding für neue Beitragende, Diskussions-Grundlage mit StB.

## Struktur

Jedes Szenario ist eine eigene Markdown-Datei nach Schema `<skill>_<kurzname>.md` oder `<topic>_<kurzname>.md` für Querschnitts-Szenarien.

```markdown
# Szenario: <Titel>

**Skill(s):** buchungssatz, ust-voranmeldung
**Schwierigkeit:** einfach / mittel / komplex
**Quelle:** echtes Beispiel anonymisiert / konstruiert

## Input
<Sachverhalt, Beträge, Kontext>

## Erwarteter Output
<Buchungs-Vorschlag, KZ-Mapping, etc.>

## Begründung
<§-Verweise, Konto-Wahl-Logik, ggf. Alternativen>

## Stolperfallen
<Was geht oft schief, was muss geprüft werden>
```

## Aktuelle Szenarien

- [buchungssatz_buerobedarf.md](buchungssatz_buerobedarf.md) — einfach
- [buchungssatz_eu_dienstleistung_13b.md](buchungssatz_eu_dienstleistung_13b.md) — mittel
- [lohnabrechnung_gf_gehalt.md](lohnabrechnung_gf_gehalt.md) — mittel
- [monatsabschluss_urlaubsrueckstellung.md](monatsabschluss_urlaubsrueckstellung.md) — mittel

## Diese Sammlung erweitern

Beim Hinzufügen:
1. Echten Sachverhalt anonymisieren (Namen, Beträge ggf. skalieren)
2. Quellen-Verweise gegen aktuelle Rechtslage prüfen
3. Mindestens 1 Stolperfalle dokumentieren
4. In dieser Liste verlinken

## Out of Scope

- Vollständige automatisierte Test-Suite (kein CI-Runner)
- Konkrete Mandanten-Daten (Datenschutz)
