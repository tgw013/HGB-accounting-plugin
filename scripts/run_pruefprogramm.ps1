<#
.SYNOPSIS
    Helper to validate a generated EXTF CSV against DATEV's official Prüfprogramm.

.DESCRIPTION
    PRD §16 requires that every release generates a representative CSV which
    passes the DATEV-Format-Prüfprogramm. The Prüfprogramm itself is a
    Windows-native GUI application (PE subsystem = Windows GUI; no CLI mode)
    distributed by DATEV under their own license — it CANNOT be redistributed
    via this public repo. The maintainer downloads it once from
    developer.datev.de (free DATEV-Entwickler login), extracts the zip, and
    points this script at the EXE.

    What this script does:
      1. Confirms the Prüfprogramm EXE is reachable
      2. Generates a representative CSV via scripts/generate_extf.py from a
         chosen fixture JSON (or uses one you provide)
      3. Launches the Prüfprogramm pre-loaded with the CSV path as argv[1]
         (most GUI apps accept a file argument and open it on start; if this
         does NOT pre-open the file, click "Datei → Öffnen" and select the
         CSV path printed below)
      4. Prints a checklist for the manual GUI walkthrough

    Why no full automation: the Prüfprogramm's PE subsystem is "Windows GUI"
    (not "Console"), so there's no stdout/stderr stream to parse and no useful
    exit code. CI integration via Windows-runner is tracked as v2.2.0 work in
    PRD §14.1.

.PARAMETER PruefprogrammExe
    Path to DatevFormatPruefProgramm.exe. Required (no default — depends on
    where the maintainer extracted the DATEV zip).

.PARAMETER InputJson
    Path to a JSON file in the input contract documented in
    skills/datev-export/SKILL.md §5. Optional — if omitted, runs against the
    EU-§13b reference fixture in tests/fixtures (if present).

.PARAMETER OutDir
    Where to write the generated CSV + .report.md. Defaults to %TEMP%\extf-validation.

.EXAMPLE
    .\scripts\run_pruefprogramm.ps1 -PruefprogrammExe "C:\tools\DatevFormatPruefprogramm\DatevFormatPruefProgramm.exe"

.EXAMPLE
    .\scripts\run_pruefprogramm.ps1 `
      -PruefprogrammExe "C:\tools\DatevFormatPruefprogramm\DatevFormatPruefProgramm.exe" `
      -InputJson .\tests\fixtures\eu_13b\input.json `
      -OutDir C:\Temp\my-validation
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$PruefprogrammExe,

    [Parameter(Mandatory=$false)]
    [string]$InputJson,

    [Parameter(Mandatory=$false)]
    [string]$OutDir = (Join-Path $env:TEMP "extf-validation")
)

$ErrorActionPreference = "Stop"

# Sanity: Prüfprogramm reachable?
if (-not (Test-Path $PruefprogrammExe)) {
    Write-Error "Prüfprogramm not found at: $PruefprogrammExe"
    Write-Host ""
    Write-Host "To get it:"
    Write-Host "  1. Log in at https://developer.datev.de/ (free DATEV-Entwickler account)"
    Write-Host "  2. Download 'DATEV-Format-Prüfprogramm' from the Tools section"
    Write-Host "  3. Extract the zip somewhere persistent (do NOT commit to the repo)"
    Write-Host "  4. Re-run this script with -PruefprogrammExe pointing at the extracted EXE"
    exit 1
}

# Repo root (script lives in <repo>/scripts/)
$RepoRoot = Split-Path -Parent $PSScriptRoot

# Default fixture if none provided
if (-not $InputJson) {
    $InputJson = Join-Path $RepoRoot "tests\fixtures\eu_13b\input.json"
}
if (-not (Test-Path $InputJson)) {
    Write-Error "Input JSON not found at: $InputJson"
    Write-Host "Pass -InputJson <path> with a JSON that matches the schema in skills/datev-export/SKILL.md §5"
    exit 1
}

# Prepare output dir
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$CsvPath = Join-Path $OutDir "EXTF_pruefprogramm_test.csv"
$ReportPath = "$CsvPath.report.md"

# Step 1: generate the CSV via the deterministic serializer
$Generator = Join-Path $RepoRoot "scripts\generate_extf.py"
Write-Host "[1/3] Generating CSV via $Generator..."
python $Generator --input $InputJson --output $CsvPath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Serializer failed (exit $LASTEXITCODE)"
    exit $LASTEXITCODE
}
Write-Host "       CSV    : $CsvPath"
Write-Host "       Report : $ReportPath"

# Step 2: launch Prüfprogramm with the CSV as argument
Write-Host ""
Write-Host "[2/3] Launching Prüfprogramm GUI..."
Write-Host "       EXE: $PruefprogrammExe"
Write-Host "       Will attempt to pre-load: $CsvPath"
Write-Host ""
Start-Process -FilePath $PruefprogrammExe -ArgumentList "`"$CsvPath`""

# Step 3: human checklist
Write-Host "[3/3] Manual GUI walkthrough:"
Write-Host ""
Write-Host "  a) If the CSV did NOT auto-open: 'Datei → Öffnen' and select:"
Write-Host "     $CsvPath"
Write-Host "  b) Choose Format = 'Buchungsstapel' if not auto-detected"
Write-Host "  c) Click 'Prüfen' (or equivalent)"
Write-Host "  d) Expected result: 'keine Fehler' / 'keine Warnungen'"
Write-Host "  e) Screenshot the result + paste into PR #1 description"
Write-Host ""
Write-Host "If the Prüfprogramm reports any error or warning:"
Write-Host "  - Note the field number (#1-125) + the message"
Write-Host "  - File an issue or comment on PR #1; the maintainer will adjust"
Write-Host "    scripts/generate_extf.py and/or config/shared/datev-extf-fields.json"
Write-Host "    to comply, then re-run this script"
