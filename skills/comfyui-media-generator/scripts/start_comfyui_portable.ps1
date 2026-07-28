param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8190,
    [int[]]$FallbackPorts = @(8191, 8192, 8193, 8194, 8195, 8196, 8197, 8198, 8199),
    [int]$StartupTimeoutSeconds = 90
)

$ErrorActionPreference = "Stop"

$PortableRoot = "C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable"
$ComfyRoot = Join-Path $PortableRoot "ComfyUI"
$PythonExe = Join-Path $PortableRoot "python_embeded\python.exe"
$StateFile = "C:\Social Content\.tmp\comfyui_server.json"

function Test-ComfyUi {
    param([string]$HostAddress, [int]$Port)

    try {
        Invoke-RestMethod -Uri "http://${HostAddress}:$Port/system_stats" -TimeoutSec 5 | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Test-TcpPortOpen {
    param([string]$HostAddress, [int]$Port)

    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $result = $client.BeginConnect($HostAddress, $Port, $null, $null)
        if (-not $result.AsyncWaitHandle.WaitOne(1000)) {
            return $false
        }
        $client.EndConnect($result)
        return $true
    }
    catch {
        return $false
    }
    finally {
        $client.Close()
    }
}

function Save-ComfyUiState {
    param([string]$HostAddress, [int]$Port, [int]$ProcessId = 0)

    $stateDir = Split-Path -Parent $StateFile
    if (-not (Test-Path -LiteralPath $stateDir)) {
        New-Item -ItemType Directory -Path $stateDir | Out-Null
    }

    [ordered]@{
        server = "http://${HostAddress}:$Port"
        host = $HostAddress
        port = $Port
        pid = $ProcessId
        updated_at = (Get-Date).ToString("o")
    } | ConvertTo-Json | Set-Content -LiteralPath $StateFile -Encoding UTF8
}

$candidatePorts = @($Port) + $FallbackPorts | Select-Object -Unique

foreach ($candidatePort in $candidatePorts) {
    if (Test-ComfyUi -HostAddress $HostAddress -Port $candidatePort) {
        Save-ComfyUiState -HostAddress $HostAddress -Port $candidatePort
        "already_running http://${HostAddress}:$candidatePort"
        exit 0
    }
}

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Portable Python not found: $PythonExe"
}

if (-not (Test-Path -LiteralPath (Join-Path $ComfyRoot "main.py"))) {
    throw "ComfyUI main.py not found under: $ComfyRoot"
}

foreach ($candidatePort in $candidatePorts) {
    if (Test-TcpPortOpen -HostAddress $HostAddress -Port $candidatePort) {
        "skip_busy_port http://${HostAddress}:$candidatePort"
        continue
    }

    $processInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $processInfo.FileName = $PythonExe
    $processInfo.WorkingDirectory = $ComfyRoot
    $processInfo.Arguments = ".\main.py --listen $HostAddress --port $candidatePort"
    $processInfo.UseShellExecute = $false
    $processInfo.CreateNoWindow = $true

    # Start-Process can crash on this machine because both Path and PATH exist in
    # the inherited environment. Normalize the child PATH before launch.
    $environment = $processInfo.Environment
    try { $environment.Remove("Path") } catch {}
    try { $environment.Remove("PATH") } catch {}
    $environment["PATH"] = "$($PortableRoot)\python_embeded;C:\Windows\System32;C:\Windows;C:\Windows\System32\Wbem"
    $environment["PYTHONIOENCODING"] = "utf-8"
    $environment["PYTHONUTF8"] = "1"

    $process = [System.Diagnostics.Process]::Start($processInfo)

    $deadline = (Get-Date).AddSeconds($StartupTimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if ($process.HasExited) {
            "failed_port http://${HostAddress}:$candidatePort exit_code=$($process.ExitCode)"
            break
        }

        if (Test-ComfyUi -HostAddress $HostAddress -Port $candidatePort) {
            Save-ComfyUiState -HostAddress $HostAddress -Port $candidatePort -ProcessId $process.Id
            "started pid=$($process.Id) http://${HostAddress}:$candidatePort"
            exit 0
        }

        Start-Sleep -Seconds 3
    }

    if (-not $process.HasExited) {
        try { $process.Kill() } catch {}
    }
}

throw "Could not start ComfyUI on any candidate port: $($candidatePorts -join ', ')"
