Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$Python = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

& $Python -m compileall -q src app tests
& $Python -m unittest discover -s tests
& $Python -m llmops_governance.cli run-gate
& $Python -m llmops_governance.cli compare-models

