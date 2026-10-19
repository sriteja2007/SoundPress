$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$DistDir = Join-Path $ScriptDir "dist"
if (-not (Test-Path $DistDir)) {
    New-Item -ItemType Directory -Path $DistDir | Out-Null
}

$ExePath = Join-Path $DistDir "SoundPress.exe"
$Url = "https://github.com/anjudeepveerla/SHORTGUN-KEYBOARD-BY-VAD-/releases/download/v2.2.0/ShotgunKeyboard-Windows-x64.exe"

Write-Host "Downloading SoundPress Windows Portable Executable..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $Url -OutFile $ExePath

Copy-Item $ExePath (Join-Path $DistDir "ShotgunKeyboard-Windows-x64.exe") -Force

Write-Host "Successfully downloaded to $ExePath" -ForegroundColor Green
Write-Host "You can now run SoundPress by double-clicking run.bat or dist\SoundPress.exe" -ForegroundColor Green
