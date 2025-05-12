<#
.SYNOPSIS
  Full setup for Resonance Sandbox (v0.2.0) when already extracted.
.DESCRIPTION
  1. (Re)creates a virtual environment.
  2. Installs dependencies and editable package.
  3. Runs pytest.
  4. Generates assets.
  5. Performs CLI sanity checks.
  6. Builds sdist and wheel.
#>

# 1) Create venv if missing
if (-Not (Test-Path .\.venv)) {
    Write-Host "==> Creating virtual environment..."
    python -m venv .\.venv
} else {
    Write-Host "==> Virtual environment already exists."
}

# 2) Activate venv
Write-Host "==> Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

# 3) Install dependencies
Write-Host "==> Installing/upgrading pip and dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4) Install project in editable mode
Write-Host "==> Installing resonance_sandbox (editable)..."
pip install -e .

# 5) Run tests
Write-Host "==> Running test suite..."
pytest -q
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Tests failed. Exiting."
    exit 1
}

# 6) Generate sample assets
Write-Host "==> Generating assets (CSV + graphs)..."
python -m resonance_sandbox.scripts.generate_assets

# 7) CLI sanity checks
Write-Host "==> CLI check: --null-test"
resonance-sandbox --null-test
Write-Host "==> CLI check: --positive-test"
resonance-sandbox --positive-test

# 8) Build distributions
Write-Host "==> Building source and wheel distributions..."
python setup.py sdist bdist_wheel

Write-Host "✅ All steps completed successfully."
