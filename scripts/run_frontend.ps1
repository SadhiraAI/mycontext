# Kill any process on port 5173, then start the frontend. Run from project root.
$ErrorActionPreference = "SilentlyContinue"
$conn = Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue
if ($conn) { $conn.OwningProcess | Sort-Object -Unique | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue } }
Set-Location (Join-Path $PSScriptRoot ".." "app" "web")
npm run dev
