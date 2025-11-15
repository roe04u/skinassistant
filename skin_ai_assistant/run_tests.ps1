Write-Host "=== Running Skin AI tests (pytest) ==="
Write-Host ""

Set-Location -Path $PSScriptRoot

# Check for virtual environment
$venvActivate = Join-Path $PSScriptRoot ".venv\Scripts\Activate.ps1"
if (-Not (Test-Path $venvActivate)) {
    Write-Error "Virtual environment not found. Create it and install requirements first."
    exit 1
}
. $venvActivate

# Set up dynamic port mapping for test environment
Write-Host "Setting up test environment with dynamic ports..."

# Find a free port for test backend (if needed)
$env:BACKEND_PORT = "8000"
$env:SKINAI_API_URL = "http://127.0.0.1:8000"

Write-Host "Backend Port: $env:BACKEND_PORT"
Write-Host "API URL: $env:SKINAI_API_URL"
Write-Host ""

# Run pytest with verbose output and coverage
Write-Host "Running pytest..."
pytest tests -vv --tb=short

$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "✅ All tests passed!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Some tests failed. Exit code: $exitCode" -ForegroundColor Red
}

exit $exitCode