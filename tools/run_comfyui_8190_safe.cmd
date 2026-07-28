@echo off
set "PORTABLE_ROOT=C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable"
set "COMFY_ROOT=%PORTABLE_ROOT%\ComfyUI"
set "PYTHON=%PORTABLE_ROOT%\python_embeded\python.exe"
set "LOG_DIR=C:\Social Content\.tmp\comfyui-logs"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
cd /d "%COMFY_ROOT%"
"%PYTHON%" ".\main.py" --windows-standalone-build --disable-cuda-malloc --listen 127.0.0.1 --port 8190 > "%LOG_DIR%\runner-safe-stdout.log" 2> "%LOG_DIR%\runner-safe-stderr.log"
echo exit_code=%ERRORLEVEL% > "%LOG_DIR%\runner-safe-exit.txt"
