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

function ConvertTo-RepositoryIdentity {
  param([string]$Url)

  $value = $Url.Trim()
  if ($value -match '^[A-Za-z]:[\\/]') {
    $identity = [IO.Path]::GetFullPath($value).Replace('\', '/')
  } elseif ($value -match '^file://') {
    $identity = ([Uri]$value).LocalPath.Replace('\', '/')
  } elseif ($value -match '^[^@/\\]+@([^:]+):(.+)$') {
    $identity = "$($Matches[1])/$($Matches[2])"
  } elseif ($value -match '^[A-Za-z][A-Za-z0-9+.-]*://') {
    $uri = [Uri]$value
    $identity = "$($uri.Host)/$($uri.AbsolutePath.TrimStart('/'))"
  } else {
    $identity = [IO.Path]::GetFullPath($value).Replace('\', '/')
  }

  return $identity.TrimEnd('/').ToLowerInvariant() -replace '\.git$', ''
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

function Assert-RepositoryOrigin {
  param(
    [string]$Path,
    [string]$RequestedRepoUrl
  )

  $originUrl = & git -C $Path remote get-url origin 2>$null
  if ($LASTEXITCODE -ne 0) {
    throw "Existing Git checkout has no readable origin remote: $Path"
  }

  $actual = ConvertTo-RepositoryIdentity ($originUrl | Select-Object -Last 1)
  $expected = ConvertTo-RepositoryIdentity $RequestedRepoUrl
  if ($actual -ne $expected) {
    throw "Existing Git checkout origin does not match requested RepoUrl: $originUrl"
  }
}

function Assert-PluginManifest {
  param([string]$PluginPath)

  $manifestPath = Join-Path $PluginPath "plugin.json"
  if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    throw "Plugin manifest not found: $manifestPath"
  }

  try {
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
  } catch {
    throw "Plugin manifest is not valid JSON: $manifestPath"
  }

  if ($manifest.name -ne "dynamic-workshop") {
    throw "Plugin manifest name must be 'dynamic-workshop': $manifestPath"
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
  Assert-RepositoryOrigin -Path $repoDir -RequestedRepoUrl $RepoUrl
  Assert-PluginManifest $pluginDir

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
