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

function Test-WorkshopRepository {
  param([string]$Path)

  if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
    Write-Host "[FAIL] Workshop repo missing: $Path"
    return $false
  }

  $inside = & git -C $Path rev-parse --is-inside-work-tree 2>$null
  if (($LASTEXITCODE -ne 0) -or ($inside -ne "true")) {
    Write-Host "[FAIL] Workshop path is not a Git checkout: $Path"
    return $false
  }

  $topLevel = & git -C $Path rev-parse --show-toplevel 2>$null
  if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Cannot determine workshop Git root: $Path"
    return $false
  }

  $expected = [IO.Path]::GetFullPath($Path).TrimEnd([char[]]@('\', '/'))
  $actual = [IO.Path]::GetFullPath(($topLevel | Select-Object -Last 1)).TrimEnd([char[]]@('\', '/'))
  if ($actual -ne $expected) {
    Write-Host "[FAIL] Workshop path is not the Git checkout root: $Path"
    return $false
  }

  Write-Host "[OK]   Workshop Git checkout is valid"
  return $true
}

function Test-PluginManifest {
  param([string]$PluginPath)

  $manifestPath = Join-Path $PluginPath "plugin.json"
  if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    Write-Host "[FAIL] Workshop plugin manifest missing: $manifestPath"
    return $false
  }

  try {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
  } catch {
    Write-Host "[FAIL] Workshop plugin manifest is invalid JSON: $manifestPath"
    return $false
  }

  if ($manifest.name -ne "dynamic-workshop") {
    Write-Host "[FAIL] Workshop plugin manifest name must be 'dynamic-workshop': $manifestPath"
    return $false
  }

  Write-Host "[OK]   Workshop plugin identity is valid: $manifestPath"
  # --plugin-dir takes the plugin root, the parent of .claude-plugin
  Write-Host "       Launch with: claude --plugin-dir `"$(Split-Path -Parent $PluginPath)`""
  return $true
}

Write-Host "Claude Code Workshop Doctor"
Write-Host "WorkshopRoot: $WorkshopRoot"
Write-Host ""

$ok = $true
$ok = (Test-CommandVersion -Command node -VersionArgs @("--version") -Label "Node.js") -and $ok
$ok = (Test-CommandVersion -Command git -VersionArgs @("--version") -Label "Git") -and $ok
$ok = (Test-CommandVersion -Command python -VersionArgs @("--version") -Label "Python") -and $ok
$ok = (Test-CommandVersion -Command claude -VersionArgs @("--version") -Label "Claude Code") -and $ok
$ok = (Test-WorkshopRepository -Path $WorkshopRoot) -and $ok

$playground = Join-Path $WorkshopRoot "workshop-playground"
if (Test-Path -LiteralPath $playground -PathType Container) {
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
  Write-Host "[FAIL] Playground folder missing: $playground"
  $ok = $false
}

$plugin = Join-Path $WorkshopRoot ".claude-plugin"
$ok = (Test-PluginManifest -PluginPath $plugin) -and $ok

if ($ok) {
  Write-Host ""
  Write-Host "READY: core workshop setup looks usable."
  exit 0
}

Write-Host ""
Write-Host "NOT READY: fix the FAIL lines above, then rerun this script."
exit 1
