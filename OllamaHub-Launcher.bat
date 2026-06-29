@echo off
REM ============================================================================
REM OllamaHub Launcher - Professional startup script
REM Run with: OllamaHub-Launcher.bat
REM ============================================================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM Check if PowerShell is available
where pwsh >nul 2>&1
if %errorlevel% neq 0 (
    where powershell >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: PowerShell not found. Please install PowerShell 7+ or use Windows PowerShell.
        pause
        exit /b 1
    )
    set PS_EXE=powershell.exe
) else (
    set PS_EXE=pwsh.exe
)

REM Run the PowerShell launcher
%PS_EXE% -NoProfile -ExecutionPolicy Bypass -File "%~dp0OllamaHub-Launcher.ps1" %*

REM Capture exit code
set EXIT_CODE=%errorlevel%

REM If an error occurred, keep window open
if %EXIT_CODE% neq 0 (
    echo.
    echo Error occurred. Press any key to close...
    pause >nul
)

exit /b %EXIT_CODE%
