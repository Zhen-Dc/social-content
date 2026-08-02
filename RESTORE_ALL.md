# Restore All Clean-Room Backups

This is the single-command entry point for restoring the four sanitized
repositories after a clean Windows installation.

## Prerequisites

Install these from their official sources first:

- Git for Windows
- GitHub CLI
- WSL 2 with an Ubuntu distribution named `Ubuntu`
- a fresh Codex installation
- a fresh official Hermes installation

The command authenticates GitHub interactively if necessary. It never restores
credentials, executable code, configuration, caches, databases, dependencies,
models, or media.

## One-Paste Command

Open **PowerShell as Administrator**, paste the complete block below once, and
press Enter:

```powershell
& {
    Set-StrictMode -Version Latest
    $ErrorActionPreference = 'Stop'

    foreach ($commandName in @('git', 'gh')) {
        if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
            throw "$commandName is not installed. Install Git for Windows and GitHub CLI first."
        }
    }

    gh auth status -h github.com *> $null
    if ($LASTEXITCODE -ne 0) {
        gh auth login -h github.com -p https -w
        if ($LASTEXITCODE -ne 0) { throw 'GitHub authentication failed.' }
    }

    $testRoot = $env:RECOVERY_TEST_ROOT
    $homeRoot = if ($testRoot) { [IO.Path]::GetFullPath($testRoot) } else { [IO.Path]::GetFullPath($HOME) }
    $repositoryRoot = Join-Path $homeRoot 'Recovery\Repositories'
    New-Item -ItemType Directory -Path $repositoryRoot -Force | Out-Null

    if ($testRoot) {
        $hermesTarget = Join-Path $homeRoot 'WSL-Hermes\.hermes'
        $socialTarget = Join-Path $homeRoot 'Social Content'
    } else {
        $wslUser = (& wsl.exe -d Ubuntu -- whoami).Trim()
        if ($LASTEXITCODE -ne 0 -or -not $wslUser) {
            throw 'The Ubuntu WSL distribution is unavailable.'
        }
        $hermesTarget = '\\wsl$\Ubuntu\home\' + $wslUser + '\.hermes'
        $socialTarget = 'C:\Social Content'
    }

    $repositories = [ordered]@{
        'master-hermes-backup' = 'Zhen-Dc/master-hermes-backup'
        'codex-memory-backup'  = 'Zhen-Dc/codex-memory-backup'
        'stan-os'              = 'Zhen-Dc/stan-os'
        'social-content'       = 'Zhen-Dc/social-content'
    }

    function Sync-RecoveryRepository([string]$Name, [string]$Slug) {
        $destination = Join-Path $repositoryRoot $Name
        if (Test-Path -LiteralPath (Join-Path $destination '.git')) {
            git -C $destination pull --ff-only
        } elseif (Test-Path -LiteralPath $destination) {
            if (@(Get-ChildItem -LiteralPath $destination -Force).Count -gt 0) {
                throw "Recovery directory exists but is not a Git repository: $destination"
            }
            gh repo clone $Slug $destination
        } else {
            gh repo clone $Slug $destination
        }
        if ($LASTEXITCODE -ne 0) { throw "Repository sync failed: $Slug" }
        return $destination
    }

    function Get-CanonicalHash([string]$Path) {
        $utf8 = [Text.UTF8Encoding]::new($false)
        $text = [IO.File]::ReadAllText($Path).Replace("`r`n", "`n").Replace("`r", "`n")
        $sha = [Security.Cryptography.SHA256]::Create()
        try {
            return ([BitConverter]::ToString($sha.ComputeHash($utf8.GetBytes($text)))).Replace('-', '').ToLowerInvariant()
        } finally {
            $sha.Dispose()
        }
    }

    function Test-RecoveryRepository([string]$Root) {
        $rootFull = [IO.Path]::GetFullPath($Root)
        $payload = @(Get-ChildItem -LiteralPath $rootFull -Recurse -File -Force |
            Where-Object { $_.FullName -notmatch '\\.git(\\|$)' })
        $badFiles = @($payload | Where-Object { $_.Extension.ToLowerInvariant() -notin @('.md', '.txt') })
        if ($badFiles.Count -gt 0) {
            throw "Forbidden file type found in $rootFull"
        }

        $manifest = Join-Path $rootFull 'MANIFEST.md'
        if (-not (Test-Path -LiteralPath $manifest)) { throw "Missing manifest: $rootFull" }
        $entries = @{}
        foreach ($line in [IO.File]::ReadAllLines($manifest)) {
            if ($line -match '^\| `([0-9a-f]{64})` \| `(.+)` \|$') {
                $entries[$matches[2]] = $matches[1]
            }
        }

        foreach ($relativePath in $entries.Keys) {
            $candidate = [IO.Path]::GetFullPath((Join-Path $rootFull $relativePath.Replace('/', '\')))
            if (-not $candidate.StartsWith($rootFull + '\', [StringComparison]::OrdinalIgnoreCase)) {
                throw "Unsafe manifest path: $relativePath"
            }
            if (-not (Test-Path -LiteralPath $candidate)) { throw "Missing manifest file: $relativePath" }
            if ((Get-CanonicalHash $candidate) -ne $entries[$relativePath]) {
                throw "Manifest mismatch: $relativePath"
            }
        }

        $payloadWithoutManifest = @($payload | Where-Object { $_.Name -ne 'MANIFEST.md' })
        if ($payloadWithoutManifest.Count -ne $entries.Count) {
            throw "Manifest does not cover every payload file in $rootFull"
        }
    }

    function Copy-TextTree([string]$Source, [string]$Destination) {
        if (-not (Test-Path -LiteralPath $Source)) { return }
        $sourceFull = [IO.Path]::GetFullPath($Source)
        $destinationFull = [IO.Path]::GetFullPath($Destination)
        New-Item -ItemType Directory -Path $destinationFull -Force | Out-Null
        foreach ($file in @(Get-ChildItem -LiteralPath $sourceFull -Recurse -File -Force)) {
            if ($file.Extension.ToLowerInvariant() -notin @('.md', '.txt')) { continue }
            $relativePath = $file.FullName.Substring($sourceFull.Length).TrimStart('\')
            $target = [IO.Path]::GetFullPath((Join-Path $destinationFull $relativePath))
            if (-not $target.StartsWith($destinationFull + '\', [StringComparison]::OrdinalIgnoreCase)) {
                throw "Unsafe restore path: $target"
            }
            New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
            Copy-Item -LiteralPath $file.FullName -Destination $target -Force
        }
    }

    $localRepositories = @{}
    foreach ($entry in $repositories.GetEnumerator()) {
        $localRepositories[$entry.Key] = Sync-RecoveryRepository $entry.Key $entry.Value
        Test-RecoveryRepository $localRepositories[$entry.Key]
    }

    $codexSource = Join-Path $localRepositories['codex-memory-backup'] 'codex'
    $codexTarget = Join-Path $homeRoot '.codex'
    Copy-TextTree (Join-Path $codexSource 'memories') (Join-Path $codexTarget 'memories')
    Copy-TextTree (Join-Path $codexSource 'personal-skills') (Join-Path $codexTarget 'skills')
    if (Test-Path -LiteralPath (Join-Path $codexSource 'AGENTS.md')) {
        New-Item -ItemType Directory -Path $codexTarget -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $codexSource 'AGENTS.md') -Destination (Join-Path $codexTarget 'AGENTS.md') -Force
    }

    $hermesRepository = $localRepositories['master-hermes-backup']
    $hermesSource = Join-Path $hermesRepository 'hermes'
    New-Item -ItemType Directory -Path $hermesTarget -Force | Out-Null
    foreach ($name in @('SOUL.md', 'MEMORY_AGENT_RULES.md')) {
        $sourceFile = Join-Path $hermesSource $name
        if (Test-Path -LiteralPath $sourceFile) {
            Copy-Item -LiteralPath $sourceFile -Destination (Join-Path $hermesTarget $name) -Force
        }
    }
    Copy-TextTree (Join-Path $hermesSource 'memories') (Join-Path $hermesTarget 'memories')
    Copy-TextTree (Join-Path $hermesSource 'custom-skills') (Join-Path $hermesTarget 'skills')

    $masterTarget = Join-Path $homeRoot 'Master Project\master hermes'
    $masterDocs = Join-Path $hermesRepository 'operating-docs\master-hermes'
    New-Item -ItemType Directory -Path (Join-Path $masterTarget 'Agent\subagents') -Force | Out-Null
    $masterMap = [ordered]@{
        'AGENTS.md' = 'AGENTS.md'
        'CLAUDE.md' = 'CLAUDE.md'
        'root-README.md' = 'README.md'
        'Agent-README.md' = 'Agent\README.md'
        'router-cheat-sheet.md' = 'Agent\subagents\router-cheat-sheet.md'
    }
    foreach ($entry in $masterMap.GetEnumerator()) {
        $sourceFile = Join-Path $masterDocs $entry.Key
        if (Test-Path -LiteralPath $sourceFile) {
            $targetFile = Join-Path $masterTarget $entry.Value
            New-Item -ItemType Directory -Path (Split-Path -Parent $targetFile) -Force | Out-Null
            Copy-Item -LiteralPath $sourceFile -Destination $targetFile -Force
        }
    }

    Copy-TextTree $localRepositories['stan-os'] (Join-Path $homeRoot 'Master Project\Stan OS\AIS-OS')
    Copy-TextTree $localRepositories['social-content'] $socialTarget

    Write-Host ''
    Write-Host 'Restore completed and verified.' -ForegroundColor Green
    Write-Host "Repositories: $repositoryRoot"
    Write-Host "Codex:       $codexTarget"
    Write-Host "Hermes:      $hermesTarget"
    Write-Host "Stan OS:     $(Join-Path $homeRoot 'Master Project\Stan OS\AIS-OS')"
    Write-Host "Social:      $socialTarget"
    Write-Host 'Next: follow setup.md in the Codex and Hermes recovery repositories to reinstall omitted software and credentials.'
}
```

## Designated Folders

| Recovery data | Destination |
|---|---|
| Repository clones | `%USERPROFILE%\Recovery\Repositories\` |
| Codex memories | `%USERPROFILE%\.codex\memories\` |
| Codex personal skill specifications | `%USERPROFILE%\.codex\skills\` |
| Hermes identity and memories | `\\wsl$\Ubuntu\home\<username>\.hermes\` |
| Master Hermes operating documents | `%USERPROFILE%\Master Project\master hermes\` |
| Stan OS documentation | `%USERPROFILE%\Master Project\Stan OS\AIS-OS\` |
| Social Content documentation | `C:\Social Content\` |

The command is rerunnable. Existing repository clones are updated with
`git pull --ff-only`, and reviewed text files are copied over their designated
counterparts. It does not delete unrelated files in the destination folders.
