# setup_project_structure.ps1
# Creates the entire project structure with all necessary folders and __init__.py files
# Run from: C:\Users\shane\Cursor Projects\projects\dts\time-tracking-app

Write-Host ""
Write-Host "=================================================="
Write-Host "SETTING UP PROJECT STRUCTURE"
Write-Host "=================================================="
Write-Host ""

$projectRoot = Get-Location
Write-Host "Project root: $projectRoot"
Write-Host ""

# Create folder structure
Write-Host "Creating directories..."

$dirs = @(
    "backend",
    "backend\app",
    "backend\app\routes",
    "frontend",
    "frontend\static",
    "frontend\static\css",
    "frontend\static\js",
    "frontend\pages"
)

foreach ($dir in $dirs) {
    $path = Join-Path $projectRoot $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
        Write-Host "  Created: $dir"
    } else {
        Write-Host "  Exists: $dir"
    }
}

Write-Host ""
Write-Host "Creating __init__.py files..."

# Create __init__.py files
$initFiles = @(
    "backend\app\__init__.py",
    "backend\app\routes\__init__.py"
)

$initContent = @"
"""
Time Tracking App - FastAPI application
"""
"@

foreach ($file in $initFiles) {
    $path = Join-Path $projectRoot $file
    if (-not (Test-Path $path)) {
        Set-Content -Path $path -Value $initContent
        Write-Host "  Created: $file"
    } else {
        Write-Host "  Exists: $file"
    }
}

Write-Host ""
Write-Host "=================================================="
Write-Host "PROJECT STRUCTURE READY!"
Write-Host "=================================================="
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Download these files from outputs to backend/:"
Write-Host "   - main.py"
Write-Host "   - requirements.txt"
Write-Host "   - models.py"
Write-Host ""
Write-Host "2. Download these files from outputs to backend/app/routes/:"
Write-Host "   - clients.py"
Write-Host "   - timesheet.py"
Write-Host "   - invoices.py"
Write-Host ""
Write-Host "3. Copy db_helper.py from old src/ folder to backend/"
Write-Host ""
Write-Host "4. Then run:"
Write-Host "   cd backend"
Write-Host "   pip install -r requirements.txt"
Write-Host "   python main.py"
Write-Host ""
