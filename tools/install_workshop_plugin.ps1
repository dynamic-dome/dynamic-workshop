param(
  [string]$InstallRoot = "$HOME/cc-workshop",
  [string]$RepoUrl = "https://github.com/dynamic-dome/dynamic-workshop.git"
)

$ErrorActionPreference = "Stop"

function Invoke-Git {
  param([string[]]$Arguments)

  & git @Arguments
  if ($LASTEXITCODE -ne 0) {
    throw "git command failed (exit $LASTEXITCODE): git $($Arguments -join ' ')"
  }
}

function Assert-GitCheckout {
  param([string]$Path)

  $inside = & git -C $Path rev-parse --is-inside-work-tree 2>$null
  if (($LASTEXITCODE -ne 0) -or ($inside -ne "true")) {
    throw "Existing destination is not a Git checkout: $Path"
  }

  $topLevel = & git -C $Path rev-parse --show-toplevel 2>$null
  if ($LASTEXITCODE -ne 0) {
    throw "Could not determine Git checkout root: $Path"
  }

  $expected = [IO.Path]::GetFullPath($Path).TrimEnd([char[]]@('\', '/'))
  $actual = [IO.Path]::GetFullPath(($topLevel | Select-Object -Last 1)).TrimEnd([char[]]@('\', '/'))
  if ($actual -ne $expected) {
    throw "Existing destination is not the Git checkout root: $Path"
  }
}

function Assert-PluginManifest {
  param([string]$PluginPath)

  $manifestPath = Join-Path $PluginPath "plugin.json"
  if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "Plugin manifest not found after checkout update: $manifestPath"
  }

  try {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
  } catch {
    throw "Plugin manifest is not valid JSON: $manifestPath"
  }

  if (-not $manifest.name) {
    throw "Plugin manifest is missing required field 'name': $manifestPath"
  }
}

$repoDir = Join-Path $InstallRoot "dynamic-workshop"
$pluginDir = Join-Path $repoDir ".claude-plugin"

New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null

if (-not (Test-Path -LiteralPath $repoDir)) {
  Invoke-Git @("ls-remote", $RepoUrl, "HEAD")
  Invoke-Git @("clone", $RepoUrl, $repoDir)
} else {
  if (-not (Test-Path -LiteralPath $repoDir -PathType Container)) {
    throw "Existing destination is not a directory: $repoDir"
  }

  Assert-GitCheckout $repoDir
  $dirty = & git -C $repoDir status --porcelain --untracked-files=normal
  if ($LASTEXITCODE -ne 0) {
    throw "Could not inspect Git checkout state: $repoDir"
  }
  if ($dirty) {
    throw "Existing Git checkout is dirty; commit, stash, or remove local changes before updating: $repoDir"
  }

  Invoke-Git @("-C", $repoDir, "pull", "--ff-only")
}

Assert-GitCheckout $repoDir
Assert-PluginManifest $pluginDir

Write-Host "Workshop plugin source is ready:"
Write-Host $pluginDir
Write-Host ""
Write-Host "Start Claude Code with the local plugin enabled:"
Write-Host "claude --plugin-dir `"$pluginDir`""
