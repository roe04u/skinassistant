# PowerShell launcher for Skin AI Assistant
# Starts all services with dynamic port mapping

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "       Skin AI Assistant - Starting All Services" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to the skin_ai_assistant subdirectory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skinAiDir = Join-Path $scriptDir "skin_ai_assistant"

if (-Not (Test-Path $skinAiDir)) {
    Write-Error "skin_ai_assistant directory not found at: $skinAiDir"
    exit 1
}

Set-Location -Path $skinAiDir

# Check if virtual environment exists
$venvActivate = Join-Path $skinAiDir ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    . $venvActivate
} else {
    Write-Host "No virtual environment found. Using global Python..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Launching services..." -ForegroundColor Green
Write-Host ""

# Run the Python launcher
python run_all.py
