@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_comfyui_portable.ps1" %*
exit /b %ERRORLEVEL%
