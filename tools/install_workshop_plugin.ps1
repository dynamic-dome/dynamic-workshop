param(
  [string]$InstallRoot = "$HOME/cc-workshop",
  [string]$RepoUrl = "https://github.com/dynamic-dome/dynamic-workshop.git"
)

$ErrorActionPreference = "Stop"

$repoDir = Join-Path $InstallRoot "dynamic-workshop"
$pluginDir = Join-Path $repoDir ".claude-plugin"

New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null

if (-not (Test-Path $repoDir)) {
  git ls-remote $RepoUrl HEAD | Out-Null
  git clone $RepoUrl $repoDir
} else {
  Push-Location $repoDir
  try {
    git fetch --all --prune
  } finally {
    Pop-Location
  }
}

if (-not (Test-Path $pluginDir)) {
  throw "Plugin directory not found after clone: $pluginDir"
}

Write-Host "Workshop plugin source is ready:"
Write-Host $pluginDir
Write-Host ""
Write-Host "Start Claude Code with the local plugin enabled:"
Write-Host "claude --plugin-dir `"$pluginDir`""

