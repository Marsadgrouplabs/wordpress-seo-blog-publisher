# Installs this skill for Claude Code and/or Codex on this computer.
# Usage: powershell -ExecutionPolicy Bypass -File .\install.ps1 [-Target claude|codex|both]
param(
    [ValidateSet('claude', 'codex', 'both')][string]$Target = 'both',
    [string]$HomeDir = $HOME
)
$ErrorActionPreference = 'Stop'
$Name = 'wordpress-seo-blog-publisher'
$Source = Join-Path $PSScriptRoot "skills\$Name"
if (-not (Test-Path (Join-Path $Source 'SKILL.md'))) { throw "Skill files not found in $Source" }

$Roots = @()
if ($Target -in 'claude', 'both') { $Roots += (Join-Path $HomeDir '.claude\skills') }
if ($Target -in 'codex', 'both') { $Roots += (Join-Path $HomeDir '.agents\skills') }

foreach ($Root in $Roots) {
    New-Item -ItemType Directory -Force -Path $Root | Out-Null
    $Dest = Join-Path $Root $Name
    if (Test-Path $Dest) {
        $Backup = Join-Path $Root (".$Name.backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
        Move-Item -LiteralPath $Dest -Destination $Backup
        Write-Host "Previous version kept at: $Backup"
    }
    Copy-Item -LiteralPath $Source -Destination $Dest -Recurse
    Write-Host "Installed: $Dest"
}
Write-Host 'Done. Start a new session to use the skill.'
