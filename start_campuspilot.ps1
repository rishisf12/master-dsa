# CampusPilot Start Script - Starts both backend (with venv) and frontend

param([switch]$SkipBackend, [switch]$SkipFrontend, [switch]$RecreateVenv, [switch]$SkipSeed)

$ErrorActionPreference = "Stop"
$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$backendDir = Join-Path $rootDir "CampusPilot\backend\backend"
$frontendDir = Join-Path $rootDir "CampusPilot\frontend"
$venvDir = Join-Path $backendDir ".venv"

# Find compatible Python (3.10 preferred, then 3.11, then 3.12)
$pythonCmd = $null
$pythonArgs = @()
foreach ($ver in @("3.10", "3.11", "3.12")) {
    try {
        & py -$ver -c "import sys" 2>$null
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "py"
            $pythonArgs = "-$ver"
            Write-Host "  Using Python: py -$ver" -ForegroundColor Green
            break
        }
    } catch { }
}
if (-not $pythonCmd) {
    Write-Host "ERROR: Python 3.10, 3.11, or 3.12 required." -ForegroundColor Red
    Write-Host "Install from python.org or use 'py -3.10', 'py -3.11', 'py -3.12'" -ForegroundColor Yellow
    exit 1
}

$pipExe = Join-Path (Join-Path $venvDir "Scripts") "pip.exe"

Write-Host "================================================================="
Write-Host "        CampusPilot - ClassPilot Start Script"
Write-Host "================================================================="
Write-Host ""

if (-not $SkipBackend) {
    Write-Host "[+] Backend Setup" -ForegroundColor Green
    
    if ($RecreateVenv -or -not (Test-Path $venvDir)) {
        Write-Host "  Creating virtual environment..." -ForegroundColor Yellow
        if (Test-Path $venvDir) { Remove-Item -Recurse -Force $venvDir }
        & $pythonCmd $pythonArgs -m venv $venvDir
        Write-Host "  [OK] Virtual environment created at $venvDir" -ForegroundColor Green
    } else {
        Write-Host "  Using existing virtual environment" -ForegroundColor Gray
    }

    Write-Host "  Upgrading pip..." -ForegroundColor Yellow
    & $pipExe install --upgrade pip -q

    # Set env var for pydantic-core build (needed for Python 3.13+)
    $env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY = "1"

    Write-Host "  Installing Python dependencies..." -ForegroundColor Yellow
    & $pipExe install -r (Join-Path $rootDir "CampusPilot\requirements.txt")
    Write-Host "  [OK] Dependencies installed" -ForegroundColor Green

    if (-not $SkipSeed) {
        Write-Host "  Seeding database..." -ForegroundColor Yellow
        Set-Location $backendDir
        $venvPython = Join-Path $venvDir "Scripts\python.exe"
        & $venvPython scripts/seed.py
        Write-Host "  [OK] Database seeded" -ForegroundColor Green
    }

    Write-Host "  Starting FastAPI server on http://localhost:8000 ..." -ForegroundColor Yellow
    $pythonPath = & $pythonCmd $pythonArgs -c "import sys; print(sys.executable)"
    $backendProcess = Start-Process -FilePath $pythonPath -ArgumentList "-m uvicorn main:app --reload --port 8000" -WorkingDirectory $backendDir -PassThru
    Write-Host "  [OK] Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green
    Start-Sleep 3
}

if (-not $SkipFrontend) {
    Write-Host "`n[+] Frontend Setup" -ForegroundColor Green
    
    if (-not (Test-Path (Join-Path $frontendDir "node_modules"))) {
        Write-Host "  Installing npm dependencies..." -ForegroundColor Yellow
        Set-Location $frontendDir
        npm install
        Write-Host "  [OK] npm dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "  node_modules exists, skipping npm install" -ForegroundColor Gray
    }

    Write-Host "  Starting Vite dev server on http://localhost:5173 ..." -ForegroundColor Yellow
    Set-Location $frontendDir
    $frontendProcess = Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory $frontendDir -PassThru
    Write-Host "  [OK] Frontend started (PID: $($frontendProcess.Id))" -ForegroundColor Green
}

Write-Host "`n================================================================="
Write-Host "  CampusPilot is running!"
Write-Host "  * Frontend: http://localhost:5173"
Write-Host "  * Backend API: http://localhost:8000"
Write-Host "  * API Docs: http://localhost:8000/docs"
Write-Host "  * Health: http://localhost:8000/health"
Write-Host "================================================================="
Write-Host ""
Write-Host "Press Ctrl+C to stop all servers..." -ForegroundColor Gray

try {
    while ($true) { Start-Sleep 1 }
} finally {
    Write-Host "`nStopping servers..." -ForegroundColor Yellow
    if ($backendProcess) { Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue }
    if ($frontendProcess) { Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue }
    Write-Host "Done." -ForegroundColor Green
}