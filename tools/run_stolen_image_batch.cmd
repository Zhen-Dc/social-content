@echo off
set "PYTHON=C:\Social Content\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\python_embeded\python.exe"
set "ROOT=C:\Social Content"
set "LOG_DIR=C:\Social Content\Asset\Stolen Innocence\images"
cd /d "%ROOT%"
"%PYTHON%" "%ROOT%\tools\generate_stolen_innocence_images.py" --start 1 --end 42 --skip-existing --timeout 1800 > "%LOG_DIR%\batch-runner-stdout.log" 2> "%LOG_DIR%\batch-runner-stderr.log"
echo exit_code=%ERRORLEVEL% > "%LOG_DIR%\batch-runner-exit.txt"
