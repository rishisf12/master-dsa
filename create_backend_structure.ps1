# CampusPilot Backend Directory Structure Creator
# Run in VS Code Terminal (PowerShell) from project root (C:\Users\Appex\Documents\Default Project)

$root = "CampusPilot"
$backend = "backend\backend"

# Root folders
New-Item -ItemType Directory -Force -Path "$root\database" | Out-Null
New-Item -ItemType Directory -Force -Path "$root\frontend" | Out-Null

# Backend nested structure
$dirs = @(
    "$root\$backend\routes",
    "$root\$backend\services",
    "$root\$backend\utils",
    "$root\$backend\scripts",
    "$root\$backend\tests",
    "$root\$backend\uploads"
)

foreach ($d in $dirs) {
    New-Item -ItemType Directory -Force -Path $d | Out-Null
    Write-Host "Created: $d"
}

Write-Host "`n✅ Backend directory structure created under $root\$backend"
Write-Host "Structure:"
tree "$root\$backend" /F