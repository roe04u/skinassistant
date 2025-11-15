# Skin AI Assistant - Quick Setup Script
# Run this to install dependencies in the virtual environment

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "       Skin AI Assistant - Dependency Installation" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skinAiDir = Join-Path $scriptDir "skin_ai_assistant"

if (-Not (Test-Path $skinAiDir)) {
    Write-Error "skin_ai_assistant directory not found!"
    exit 1
}

Set-Location -Path $skinAiDir

# Check if virtual environment exists
$venvPath = Join-Path $skinAiDir ".venv"
if (-Not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment!"
        exit 1
    }
}

# Activate virtual environment and install dependencies
Write-Host "Installing dependencies in virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\pip.exe" install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host "       Setup Complete! All dependencies installed." -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To run the application:" -ForegroundColor Cyan
    Write-Host "   1. cd skin_ai_assistant" -ForegroundColor White
    Write-Host "   2. .venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "   3. cd .." -ForegroundColor White
    Write-Host "   4. python run_all.py" -ForegroundColor White
    Write-Host ""
    Write-Host "Or simply run from project root:" -ForegroundColor Cyan
    Write-Host "   .\start_skin_ai.ps1" -ForegroundColor White
} else {
    Write-Error "Failed to install dependencies!"
    exit 1
}
