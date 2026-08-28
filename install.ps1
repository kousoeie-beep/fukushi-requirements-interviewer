param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("hermes", "codex", "both")]
    [string]$Target,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$SourceDir = Join-Path $PSScriptRoot "skills\fukushi-requirements-interviewer"
if (-not (Test-Path (Join-Path $SourceDir "SKILL.md"))) {
    throw "Skill本体が見つかりません: $SourceDir"
}

function Install-Skill {
    param([string]$Product)

    if ($Product -eq "hermes") {
        $BaseDir = if ($env:HERMES_HOME) { $env:HERMES_HOME } else { Join-Path $HOME ".hermes" }
    } else {
        $BaseDir = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
    }

    $SkillsDir = Join-Path $BaseDir "skills"
    $Destination = Join-Path $SkillsDir "fukushi-requirements-interviewer"
    New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

    if ((Test-Path $Destination) -and -not $Force) {
        throw "$Destination は既にあります。確認後に -Force を付けてください。"
    }
    if (Test-Path $Destination) {
        $Stamp = Get-Date -Format "yyyyMMddHHmmss"
        $Backup = "$Destination.backup.$Stamp"
        Move-Item -Path $Destination -Destination $Backup
        Write-Host "既存版を退避しました: $Backup"
    }

    Copy-Item -Recurse -Path $SourceDir -Destination $Destination
    Write-Host "Installed for $Product`: $Destination"
}

if ($Target -eq "hermes" -or $Target -eq "both") {
    Install-Skill "hermes"
}
if ($Target -eq "codex" -or $Target -eq "both") {
    Install-Skill "codex"
}

Write-Host "完了しました。新しい会話を開き、『ヒアリングスタート』と入力してください。"
