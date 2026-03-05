# --- OmniSuite startup script (with pause) -----------------
Set-Location "C:\OmniSuite"
.\venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload

Write-Host "`n----------------------------------------------------"
Write-Host "✅  Server stopped. Press Enter to close this window."
Write-Host "`nServer stopped. Press ENTER to close this window..."
[void][System.Console]::ReadLine()