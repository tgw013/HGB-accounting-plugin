# Bekannte offene Fragen — Stand 2026-05

Dieses Plugin wurde gegen die DATEV-Kontenrahmen 2026 (Art.-Nr. 11174/11175), das aktuelle HGB/EStG/UStG/KStG/SGB sowie BMF-Schreiben mit Stand 2026-05 abgeglichen. Die folgenden Punkte sind dabei **bewusst offen geblieben** und erfordern fachjuristische / steuerberaterliche Klärung im Einzelfall.

---

## 1. § 264a HGB & eingetragene GbR (eGbR) — Bilanzierungspflicht

**Status:** ungeklärt (Stand 2026-05)

**Sachverhalt:** Seit Inkrafttreten des **MoPeG** (Gesetz zur Modernisierung des Personengesellschaftsrechts, 01.01.2024) gibt es die eingetragene GbR (eGbR) als rechtsfähige, im Gesellschaftsregister eingetragene Variante der GbR. Die Frage:

> **Gilt § 264a HGB (verschärfte Bilanzierungs-/Offenlegungspflichten für OHG/KG ohne natürliche Person als Vollhafter) analog für eGbR, deren Gesellschafter ausschließlich Kapitalgesellschaften sind?**

**Pro Analogie:**
- Der Schutzzweck (Schutz vor Bilanzlücken bei reiner Kapitalgesellschafts-Struktur) gilt gleichermaßen für die eGbR
- Mit der Eintragung im Gesellschaftsregister hat die eGbR eine Publizität, die mit OHG/KG vergleichbar ist

**Contra Wortlaut:**
- § 264a HGB nennt explizit nur **offene Handelsgesellschaften und Kommanditgesellschaften**
- Das MoPeG hat keine entsprechende Anpassung in § 264a HGB vorgenommen, obwohl Gelegenheit bestand
- Eine planwidrige Regelungslücke (Voraussetzung für Analogie) ist daher umstritten

**Quellenlage:**
- Keine eindeutige BGH-Rechtsprechung
- Kein BMF-Schreiben zur Klarstellung
- Großteil der Kommentarliteratur (Beck'scher Bilanzkommentar, ADS) tendiert zu **Contra Analogie**
- Einzelne Stimmen (insbesondere IDW-Positionen, manche bilanzrechtliche Aufsätze) tendieren zu **Pro Analogie**

**Plugin-Verhalten:**
Wenn ein Sachverhalt mit eGbR vorliegt und alle Vollhafter Kapitalgesellschaften sind, **muss** die `jahresabschluss`-Skill auf diese offene Frage hinweisen und die Konsultation eines Steuerberaters / Wirtschaftsprüfers anstoßen. **Keine automatisierte Empfehlung möglich.**

**Was bei Klärung zu tun ist:**
- Wenn BGH oder BMF Klarstellung schaffen → diese OPEN_QUESTIONS.md aktualisieren
- jahresabschluss-Skill Section 7.1 (GbR-Besonderheiten) entsprechend anpassen
- Eintrag in CHANGES_APPLIED.md mit Quelle

**Praktische Empfehlung (zwischenzeitlich):**
- Bei eGbR mit ausschließlich Kapitalgesellschaftern: defensiv die strengeren §-264a-HGB-Vorgaben anwenden (Bilanz, GuV, Anhang, Offenlegung) — gegen die Risiko-Seite hin
- ABER: Mit Steuerberater abstimmen, ob eine Position auf "Wortlaut" rechtssicher vertretbar ist (z. B. wenn Offenlegung aus Wettbewerbsgründen vermieden werden soll)

---

## 2. §13b-KZ-Codes — Vollständige Mapping-Tabelle (Wartungs-Item)

**Status:** für 2026 verifiziert; jährliche Aktualisierung nötig

Das BMF gibt jährlich neue Vordruckmuster für USt 1 A heraus. Die KZ-Codes wurden für **2026 verifiziert** gegen das BMF-Vordruckmuster vom 29.12.2025. Bei Wechsel auf 2027/2028 ist die Mapping-Tabelle in `skills/ust-voranmeldung/SKILL.md` Section 3.1 + `skills/abstimmung/SKILL.md` Section 4.6 zu überprüfen.

---

## 3. Rate-Updates für Folgejahre

**Status:** für 2026 verifiziert; jährliche Aktualisierung nötig

Folgende Werte ändern sich erfahrungsgemäß jährlich und sind in `config/rates-2026.json` hinterlegt:

- Mindestlohn (jährliche Anpassung)
- BBG KV/PV und RV/AV (jährlich per Sozialversicherungs-Rechengrößenverordnung)
- JAEG (jährlich)
- Minijob-/Midijob-Grenzen (folgen Mindestlohn)
- Durchschnittlicher KV-Zusatzbeitrag (BMG-Veröffentlichung)
- Insolvenzgeldumlage U3 (BMAS)
- Sachbezugswerte (SvEV)
- SolZ-Freigrenze
- Gewerbesteuer-Hebesätze (Stadt-spezifisch)
- KSt-Senkungspfad (gesetzlich festgeschrieben bis 2032 — keine jährliche Aktualisierung nötig)

Vor jedem Jahreswechsel: `config/rates-2026.json` durch `config/rates-2027.json` ersetzen und alle Skills-Quellverweise aktualisieren.

---

## 4. Sektor-/Branchen-spezifische Sachverhalte

**Status:** außerhalb des Plugin-Umfangs

Das Plugin deckt **allgemeine deutsche Buchhaltung** ab. Folgende Bereiche sind **explizit nicht** enthalten und benötigen Steuerberater-/Sektor-spezifische Beratung:

- Bauleistungen-Reverse-Charge Edge Cases (§ 13b Abs. 2 Nr. 4 UStG)
- Differenzbesteuerung § 25a UStG (Gebrauchtwaren)
- Land-/Forstwirt-Durchschnittssatzbesteuerung § 24 UStG
- Bank-/Versicherungs-Sonderregelungen (RechKredV, RechVersV)
- Krankenhaus-/Pflegeeinrichtungs-Spezialregelungen
- Konzernrechnungslegung (HGB / IFRS)
- Tax Compliance Management Systems (TCMS) nach IDW PS 980
- Verrechnungspreisdokumentation § 90 Abs. 3 AO

---

## 5. Konkrete Steuergestaltungs-Entscheidungen

**Status:** außerhalb des Plugin-Umfangs

Das Plugin kann **arithmetisch und kontentechnisch** Vorschläge machen, aber **keine** Empfehlung zu strategischen Steuerentscheidungen, etwa:

- Wahl SKR03 vs. SKR04
- Wahl GKV vs. UKV in der GuV
- Wahl Bilanzierungsmethoden bei Wahlrechten (z. B. Verbrauchsfolge, FIFO/LIFO)
- bAV-Durchführungsweg (Direktversicherung, Pensionskasse, Pensionsfonds, Direktzusage, Unterstützungskasse)
- Wahl Voll- vs. Teilversteuerung bei Kleinunternehmer (§ 19 UStG)
- Optionsrechte zum Verzicht auf Steuerbefreiung (§ 9 UStG)
- IFRS-Anwendung statt HGB für Konzern-Reporting

Solche Entscheidungen erfordern **immer** Steuerberater-Konsultation mit Blick auf die spezifische Unternehmenssituation.

---

## 6. eBilanz-Taxonomie-Versionen für Folgejahre

**Status:** HGB-Taxonomie 6.9 für GJ 2026 (verifiziert via BMF-Schreiben 10.06.2025)

BMF veröffentlicht jährlich neue Taxonomien. Für GJ 2027 ist die nachfolgende Version (vermutlich 6.10 oder 7.0) zu erwarten — Plugin-Aktualisierung beim Jahreswechsel.

---

## Wie diese Liste gepflegt wird

- Bei jeder Klärung einer offenen Frage: Eintrag entfernen, korrespondierender CHANGES_APPLIED-Eintrag schreiben
- Bei neuen offenen Fragen in der Praxis: Eintrag hier hinzufügen mit Datum
- Jahresübergreifend prüfen: gibt es neue BGH/BFH/BMF-Klarstellungen, die Themen schließen?

End of OPEN_QUESTIONS.md
