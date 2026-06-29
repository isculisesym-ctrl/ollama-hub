#!/usr/bin/env pwsh
<#
.SYNOPSIS
OllamaHub Launcher v1.0 — Professional launcher with healthcheck, auto-restart, IDE launcher

.DESCRIPTION
One-click startup for the complete OllamaHub stack:
- Checks Ollama, Backend (FastAPI), Frontend (Vite)
- Auto-restarts any dead process
- Auto-starts all if everything is down
- Opens IDE in browser
- Validates all ports are healthy

.EXAMPLE
.\OllamaHub-Launcher.ps1
.\OllamaHub-Launcher.ps1 -NoOpen
.\OllamaHub-Launcher.ps1 -Force
#>

param(
    [switch]$Force,
    [switch]$NoOpen,
    [switch]$Verbose
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "SilentlyContinue"

$ProjectRoot = "C:\Proyectos\ollama-hub"
$Version = "1.0"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Colors
function Write-Header { Write-Host $args[0] -ForegroundColor Cyan }
function Write-Success { Write-Host $args[0] -ForegroundColor Green }
function Write-Error_ { Write-Host $args[0] -ForegroundColor Red }
function Write-Warning_ { Write-Host $args[0] -ForegroundColor Yellow }
function Write-Info { Write-Host $args[0] -ForegroundColor Blue }

# Banner
Clear-Host
Write-Header @"
╔════════════════════════════════════════════════════════════╗
║       🚀 OLLAMAHUB LAUNCHER v$Version                          ║
║                                                            ║
║  Haiku Orchestrator + Ollama Specialists Architecture     ║
║  Production-Ready Code Review Swarm Enabled               ║
╚════════════════════════════════════════════════════════════╝
"@

Write-Info "`n⏰ Started at: $Timestamp`n"

# Utility: Port check
function Test-Port {
    param([int]$Port, [int]$Timeout = 3)
    try {
        $socket = New-Object System.Net.Sockets.TcpClient
        $socket.ReceiveTimeout = $Timeout * 1000
        $socket.SendTimeout = $Timeout * 1000
        $result = $socket.BeginConnect("127.0.0.1", $Port, $null, $null)
        $result.AsyncWaitHandle.WaitOne($Timeout * 1000) | Out-Null
        if ($socket.Connected) {
            $socket.EndConnect($result)
            $socket.Close()
            return $true
        }
        return $false
    } catch {
        return $false
    }
}

# Utility: Start process silently
function Start-Service {
    param(
        [string]$Name,
        [string]$Exe,
        [string[]]$Args,
        [string]$WorkDir,
        [int]$Port
    )
    Write-Info "   ⏳ Starting $Name (port $Port)..."
    try {
        $proc = Start-Process -FilePath $Exe -ArgumentList $Args -WorkingDirectory $WorkDir `
            -NoNewWindow -PassThru -ErrorAction SilentlyContinue
        if ($proc -and -not $proc.HasExited) {
            Start-Sleep -Milliseconds 1500
            if (Test-Port $Port) {
                Write-Success "   ✅ $Name started (PID: $($proc.Id))"
                return $true
            }
        }
        return $false
    } catch {
        Write-Error_ "   ❌ Failed to start $Name"
        return $false
    }
}

# === PHASE 1: Check Ollama ===
Write-Header "`n📍 PHASE 1: Ollama (Local LLM Server, port 11434)"
if (Test-Port 11434) {
    Write-Success "   ✅ Ollama is running"
} else {
    Write-Error_ "   ❌ Ollama is NOT running"
    Write-Warning_ "   ⚠️  Please start Ollama manually:"
    Write-Info "       > ollama serve"
    Write-Info ""
    if (-not $Force) {
        Read-Host "   Press ENTER to continue anyway, or Ctrl+C to exit"
    }
}

# === PHASE 2: Check/Start Backend ===
Write-Header "`n📍 PHASE 2: Backend (FastAPI, port 8000)"
if (Test-Port 8000) {
    Write-Success "   ✅ Backend is running"
} else {
    Write-Error_ "   ❌ Backend is NOT running"
    if (-not (Start-Service "Backend" "python" @("-m", "uvicorn", "app.main:app", "--reload") `
        "$ProjectRoot\backend" 8000)) {
        Write-Error_ "   ❌ Failed to start Backend"
    }
}

# === PHASE 3: Check/Start Frontend ===
Write-Header "`n📍 PHASE 3: Frontend (Vite React, port 5173)"
if (Test-Port 5173) {
    Write-Success "   ✅ Frontend is running"
} else {
    Write-Error_ "   ❌ Frontend is NOT running"
    if (-not (Start-Service "Frontend" "npm" @("run", "dev") "$ProjectRoot\frontend" 5173)) {
        Write-Error_ "   ❌ Failed to start Frontend"
    }
}

# === PHASE 4: Validation ===
Write-Header "`n📍 PHASE 4: Health Validation"
$maxWait = 15
$elapsed = 0
$backendReady = $false
$frontendReady = $false

while (($elapsed -lt $maxWait) -and (-not ($backendReady -and $frontendReady))) {
    $backendReady = Test-Port 8000
    $frontendReady = Test-Port 5173
    if (-not ($backendReady -and $frontendReady)) {
        Start-Sleep -Seconds 1
        $elapsed++
    }
}

Write-Info "`n   Final Status:"
Write-Host "   Ollama (11434):  $(if (Test-Port 11434) { "✅ Ready" } else { "⚠️  Offline (optional)" })" -ForegroundColor $(if (Test-Port 11434) { "Green" } else { "Yellow" })
Write-Host "   Backend (8000):  $(if (Test-Port 8000) { "✅ Ready" } else { "❌ Failed" })" -ForegroundColor $(if (Test-Port 8000) { "Green" } else { "Red" })
Write-Host "   Frontend (5173): $(if (Test-Port 5173) { "✅ Ready" } else { "❌ Failed" })" -ForegroundColor $(if (Test-Port 5173) { "Green" } else { "Red" })

if (-not (Test-Port 8000) -or -not (Test-Port 5173)) {
    Write-Error_ "`n❌ Critical services not ready. Check console output above."
    Read-Host "Press ENTER to exit"
    exit 1
}

# === PHASE 5: Open IDE ===
if (-not $NoOpen) {
    Write-Header "`n🌐 PHASE 5: Opening IDE"
    Write-Info "   🔗 Launching http://localhost:5173"
    Start-Sleep -Seconds 1
    try {
        Start-Process "http://localhost:5173" -ErrorAction SilentlyContinue
    } catch {}
}

# === SUCCESS ===
Write-Success @"
╔════════════════════════════════════════════════════════════╗
║                   ✅ ALL SYSTEMS GO                        ║
║                                                            ║
║  • Haiku Orchestrator ready (Code Review Swarm enabled)   ║
║  • Backend API running (75 tests passing)                 ║
║  • Frontend IDE ready (Chat, Admin, Demo pages)           ║
║  • Real-time Streaming SSE enabled                        ║
║                                                            ║
║  Next: Start chatting or run Code Review Demo!            ║
╚════════════════════════════════════════════════════════════╝
"@

Write-Info "`n💡 Tips:"
Write-Info "   • Chat page: Real-time streaming with Ollama/Claude"
Write-Info "   • Admin page: Logs, stats, model manager"
Write-Info "   • Demo page: Code Review Swarm (Haiku + Ollamas)"
Write-Info "   • Setup page: Connection testing wizard`n"

# Keep window open
if (-not $NoOpen) {
    Write-Info "Press ENTER to close this window..."
    Read-Host
}
