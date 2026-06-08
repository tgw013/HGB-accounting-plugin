---
description: Beleg ODER Abschluss-/Abgrenzungsvorgang (RAP § 250, Rückstellungen § 249, Auflösungen) in Buchungsvorschlag umwandeln (SKR03/SKR04, USt-Behandlung, §-Begründung) — mit JSON-Handoff für datev-export. DATEV-konform.
argument-hint: <Sachverhalt oder Beleg> [| beleg|rückstellung|arap|prap|auflösung] [SKR03|SKR04]
---

Aktiviere die `buchungssatz`-Skill und arbeite den Sachverhalt durch.

**Geltungsbereich:** GmbH, UG. Bei anderen Rechtsformen Hinweis geben und Steuerberater-Konsultation empfehlen.

Der Skill erkennt Einzelbeleg vs. Abschlussbuchung automatisch; bei Mehrdeutigkeit genau eine Rückfrage stellen (Rechnung vorhanden? → Verbindlichkeit/Beleg, sonst Rückstellung). Standardmäßig den lesbaren Buchungsvorschlag UND den strukturierten JSON-Handoff (Section 9) ausgeben.

Falls kein konkreter Sachverhalt mitgegeben wurde, erfrage die Eingaben (siehe Section 2/3 des Skills).

Bei Unsicherheit: Disclaimer aus dem Skill-Header zitieren und Steuerberater empfehlen.
