@echo off

REM Check if the 'requests' library is installed
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo The 'requests' library is not installed.
    echo Installing the library...
    pip install requests
)

python nobel_people_fetcher.py

pause