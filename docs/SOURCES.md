# Primärquellen

Alle Werte und Konto-Verweise in diesem Plugin sind gegen die folgenden Primärquellen verifiziert. Sekundärliteratur (Lehrbücher, Beraterportale) wird nicht als Belegquelle anerkannt.

## Gesetze (Stand 2026-05)

| Bereich | Quelle | URL |
|---|---|---|
| Handelsrecht | HGB | https://www.gesetze-im-internet.de/hgb/ |
| Einkommensteuer | EStG | https://www.gesetze-im-internet.de/estg/ |
| Umsatzsteuer | UStG | https://www.gesetze-im-internet.de/ustg_1980/ |
| Umsatzsteuer-DV | UStDV | https://www.gesetze-im-internet.de/ustdv_1980/ |
| Körperschaftsteuer | KStG | https://www.gesetze-im-internet.de/kstg_1977/ |
| Gewerbesteuer | GewStG | https://www.gesetze-im-internet.de/gewstg/ |
| Abgabenordnung | AO | https://www.gesetze-im-internet.de/ao_1977/ |
| Solidaritätszuschlag | SolzG | https://www.gesetze-im-internet.de/solzg_1995/ |
| Sozialversicherung Allg. | SGB IV | https://www.gesetze-im-internet.de/sgb_4/ |
| Krankenversicherung | SGB V | https://www.gesetze-im-internet.de/sgb_5/ |
| Rentenversicherung | SGB VI | https://www.gesetze-im-internet.de/sgb_6/ |
| Arbeitslosenversicherung | SGB III | https://www.gesetze-im-internet.de/sgb_3/ |
| Pflegeversicherung | SGB XI | https://www.gesetze-im-internet.de/sgb_11/ |
| Unfallversicherung | SGB VII | https://www.gesetze-im-internet.de/sgb_7/ |
| Betriebliche Altersvorsorge | BetrAVG | https://www.gesetze-im-internet.de/betravg/ |
| Whistleblower-Schutz | HinSchG | https://www.gesetze-im-internet.de/hinschg/ |
| GmbH-Recht | GmbHG | https://www.gesetze-im-internet.de/gmbhg/ |
| Mindestlohn | MiLoG | https://www.gesetze-im-internet.de/milog/ |
| Personengesellschaftsrecht | BGB (§§ 705 ff., MoPeG ab 2024) | https://www.gesetze-im-internet.de/bgb/ |

## DATEV-Kontenrahmen

| Rahmen | Art.-Nr. | Stand | Bezug |
|---|---|---|---|
| **SKR03** (Prozessgliederungsprinzip) | 11174 | 2026-01-01 | DATEV-Shop / Help Center: https://help-center.apps.datev.de/documents/0907817 |
| **SKR04** (Abschlussgliederungsprinzip) | 11175 | 2026-01-01 | DATEV-Shop / Help Center |

Anwender müssen die PDFs separat beschaffen (Urheberrecht). Plugin enthält nur verifizierte Konto-Nummern + Bezeichnungen als Verweis.

## BMF-Vordruckmuster und -Schreiben

| Dokument | Stand | URL |
|---|---|---|
| Vordruckmuster USt 1 A 2026 (USt-Voranmeldung) | BMF-Schreiben 29.12.2025, GZ III C 3 - S 7344/00040/008/034 | https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/2025-12-29-vordruckmuster-USt-voranmeldung-2026.pdf |
| Vordruckmuster USt-Jahreserklärung 2026 | BMF-Schreiben 29.12.2025 | https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/2025-12-29-muster-USt-erklaerung-2026.pdf |
| Verpflegungspauschalen In-/Ausland 2026 | BMF jährlich | bundesfinanzministerium.de |
| GoBD | BMF-Schreiben 28.11.2019 (idgF) | https://www.bundesfinanzministerium.de/ |

## Sozialversicherungs-Rechengrößen

| Quelle | URL |
|---|---|
| Sozialversicherungs-Rechengrößenverordnung 2026 | BGBl. — bgbl.de |
| BBG GKV/PV | GKV-Spitzenverband: https://www.gkv-spitzenverband.de/ |
| Beitragssätze KV (Zusatzbeitrag durchschnittlich) | BMG / GKV |
| Mindestlohn | Mindestlohnkommission: https://www.mindestlohn-kommission.de/ |

## Prüfungsstandards (für IKS-Skill)

| Standard | Quelle |
|---|---|
| IDW PS 261 (Feststellung und Beurteilung von Fehlerrisiken) | IDW Verlag |
| IDW PS 720 (Bericht über die Erweiterung der Abschlussprüfung) | IDW Verlag |

## Geplante MCP-Quellen

| Server | Repo | Zweck |
|---|---|---|
| datev_finrobotics | https://github.com/ppronobis/datev-mcp-server | EXTF-Read |
| datev_badrix | https://github.com/BadRix90/datev-mcp | EXTF-Read+Write |

Siehe `docs/CONNECTORS.md` für Security-Evaluierung.

## Verifikations-Diskipplin

- Jede §-Angabe muss auf eine der oben genannten URLs zurückführbar sein
- DATEV-Konto-Nummern müssen Seitenverweis auf das jeweilige Jahres-PDF haben (in PR-Diskussionen, nicht im Code)
- BMF-KZ-Codes müssen Zeilen-Nummern aus dem konkreten Vordruckmuster-PDF haben
- Bei Zweifel: aktuelle Fassung von gesetze-im-internet.de zieht — Druckwerke nicht
