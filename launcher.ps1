#!/usr/bin/env pwsh
<#
.SYNOPSIS
OllamaHub Launcher — Healthcheck, restart, and open IDE

.DESCRIPTION
- Checks if Ollama, Backend, Frontend are running
- Restarts any dead process
- Starts all if everything is down
- Opens browser to IDE
#>

param(
    [switch]$Force,
    [switch]$NoOpen
)

$ErrorActionPreference = "Stop"
$ProjectRoot = "C:\Proyectos\ollama-hub"

Write-Host "🚀 OllamaHub Launcher" -ForegroundColor Cyan
Write-Host "=====================`n" -ForegroundColor Cyan

function Test-Port {
    param([int]$Port)
    $socket = New-Object Net.Sockets.TcpClient
    try {
        $socket.Connect("127.0.0.1", $Port)
        $socket.Close()
        return $true
    } catch {
        return $false
    }
}

function Start-Process-Background {
    param([string]$Name, [string]$Exe, [string[]]$Args, [string]$WorkDir)
    Write-Host "  ▶ Starting $Name..." -ForegroundColor Yellow
    Start-Process -FilePath $Exe -ArgumentList $Args -WorkingDirectory $WorkDir -WindowStyle Minimized -NoNewWindow | Out-Null
    Start-Sleep -Seconds 2
}

# 1. Check Ollama (port 11434)
Write-Host "1️⃣  Checking Ollama..." -ForegroundColor Green
if (Test-Port 11434) {
    Write-Host "  ✅ Ollama running" -ForegroundColor Green
} else {
    Write-Host "  ❌ Ollama NOT running" -ForegroundColor Red
    if ($Force) {
        Write-Host "  ⚠️  Ollama should be started manually (ollama serve)" -ForegroundColor Yellow
    }
}

# 2. Check Backend (port 8000)
Write-Host "`n2️⃣  Checking Backend..." -ForegroundColor Green
if (Test-Port 8000) {
    Write-Host "  ✅ Backend running" -ForegroundColor Green
} else {
    Write-Host "  ❌ Backend NOT running" -ForegroundColor Red
    Write-Host "  ▶ Starting Backend..." -ForegroundColor Yellow
    Start-Process-Background "Backend" "python" @("-m", "uvicorn", "app.main:app", "--reload") "$ProjectRoot\backend"
}

# 3. Check Frontend (port 5173)
Write-Host "`n3️⃣  Checking Frontend..." -ForegroundColor Green
if (Test-Port 5173) {
    Write-Host "  ✅ Frontend running" -ForegroundColor Green
} else {
    Write-Host "  ❌ Frontend NOT running" -ForegroundColor Red
    Write-Host "  ▶ Starting Frontend..." -ForegroundColor Yellow
    Start-Process-Background "Frontend" "npm" @("run", "dev") "$ProjectRoot\frontend"
}

# 4. Validate all
Write-Host "`n4️⃣  Validation..." -ForegroundColor Green
$WaitCount = 0
while ((-not (Test-Port 8000)) -or (-not (Test-Port 5173))) {
    if ($WaitCount -gt 10) {
        Write-Host "  ⚠️  Timeout waiting for services" -ForegroundColor Yellow
        break
    }
    Write-Host "  ⏳ Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    $WaitCount++
}

# Final status
Write-Host "`n📊 Final Status:" -ForegroundColor Cyan
Write-Host "  Ollama (11434):   $(if (Test-Port 11434) { '✅' } else { '❌' })" -ForegroundColor $(if (Test-Port 11434) { 'Green' } else { 'Red' })
Write-Host "  Backend (8000):   $(if (Test-Port 8000) { '✅' } else { '❌' })" -ForegroundColor $(if (Test-Port 8000) { 'Green' } else { 'Red' })
Write-Host "  Frontend (5173):  $(if (Test-Port 5173) { '✅' } else { '❌' })" -ForegroundColor $(if (Test-Port 5173) { 'Green' } else { 'Red' })

if (-not $NoOpen) {
    Write-Host "`n🌐 Opening IDE..." -ForegroundColor Cyan
    Start-Sleep -Seconds 2
    Start-Process "http://localhost:5173"
}

Write-Host "`n✅ Done! Start chatting." -ForegroundColor Green
