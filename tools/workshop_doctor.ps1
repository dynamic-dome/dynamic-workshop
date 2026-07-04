param(
  [string]$WorkshopRoot = "$HOME/cc-workshop/dynamic-workshop"
)

$ErrorActionPreference = "Continue"

function Test-CommandVersion {
  param(
    [string]$Command,
    [string[]]$VersionArgs,
    [string]$Label
  )

  $cmd = Get-Command $Command -ErrorAction SilentlyContinue
  if (-not $cmd) {
    Write-Host "[FAIL] $Label not found on PATH"
    return $false
  }

  try {
    $output = & $cmd.Source @VersionArgs 2>$null
    Write-Host "[OK]   $Label -> $($output | Select-Object -First 1)"
    return $true
  } catch {
    Write-Host "[WARN] $Label found but version check failed: $($_.Exception.Message)"
    return $false
  }
}

Write-Host "Claude Code Workshop Doctor"
Write-Host "WorkshopRoot: $WorkshopRoot"
Write-Host ""

$ok = $true
$ok = (Test-CommandVersion -Command node -VersionArgs @("--version") -Label "Node.js") -and $ok
$ok = (Test-CommandVersion -Command git -VersionArgs @("--version") -Label "Git") -and $ok
$ok = (Test-CommandVersion -Command python -VersionArgs @("--version") -Label "Python") -and $ok
$ok = (Test-CommandVersion -Command claude -VersionArgs @("--version") -Label "Claude Code") -and $ok

if (Test-Path $WorkshopRoot) {
  Write-Host "[OK]   Workshop repo exists"
} else {
  Write-Host "[FAIL] Workshop repo missing: $WorkshopRoot"
  $ok = $false
}

$playground = Join-Path $WorkshopRoot "workshop-playground"
if (Test-Path $playground) {
  Push-Location $playground
  try {
    python -m pytest -q
    if ($LASTEXITCODE -eq 0) {
      Write-Host "[OK]   Playground tests pass"
    } else {
      Write-Host "[FAIL] Playground tests failed"
      $ok = $false
    }
  } finally {
    Pop-Location
  }
} else {
  Write-Host "[WARN] Playground folder missing; clone the workshop repo first"
}

$plugin = Join-Path $WorkshopRoot ".claude-plugin"
if (Test-Path $plugin) {
  Write-Host "[OK]   Workshop plugin directory exists: $plugin"
  Write-Host "       Launch with: claude --plugin-dir `"$plugin`""
} else {
  Write-Host "[WARN] Workshop plugin directory missing"
}

if ($ok) {
  Write-Host ""
  Write-Host "READY: core workshop setup looks usable."
  exit 0
}

Write-Host ""
Write-Host "NOT READY: fix the FAIL lines above, then rerun this script."
exit 1
