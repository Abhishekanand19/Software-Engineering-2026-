@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo ==============================================================
echo   LAB 7 - ATM FUZZ TESTING (ONE COMMAND)
echo ==============================================================
echo.

REM Reuse a local virtual environment when present (including failed installs).
if exist ".venv\Scripts\python.exe" goto install

REM Choose a widely supported Windows Python release with binary wheels.
where py >nul 2>nul
if errorlevel 1 goto fallback

py -3.12 -c "import sys; assert sys.version_info >= (3,12)" >nul 2>nul
if not errorlevel 1 (
    echo Creating Python 3.12 virtual environment...
    py -3.12 -m venv .venv
    goto checkvenv
)
py -3.13 -c "import sys" >nul 2>nul
if not errorlevel 1 (
    echo Creating Python 3.13 virtual environment...
    py -3.13 -m venv .venv
    goto checkvenv
)
py -3.11 -c "import sys" >nul 2>nul
if not errorlevel 1 (
    echo Creating Python 3.11 virtual environment...
    py -3.11 -m venv .venv
    goto checkvenv
)
py -3.10 -c "import sys" >nul 2>nul
if not errorlevel 1 (
    echo Creating Python 3.10 virtual environment...
    py -3.10 -m venv .venv
    goto checkvenv
)

:fallback
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.12 from python.org.
    exit /b 1
)
echo Creating virtual environment with installed Python...
python -m venv .venv

:checkvenv
if errorlevel 1 (
    echo ERROR: Could not create the Python virtual environment.
    exit /b 1
)

:install
echo.
echo [Dependencies] Python in local virtual environment:
".venv\Scripts\python.exe" --version
if errorlevel 1 (
    echo ERROR: The .venv environment is damaged.
    echo Delete the Lab-7\.venv directory, then run this script again.
    exit /b 1
)

echo.
echo [Dependencies] Updating pip and installing PREBUILT wheels only...
REM --isolated disregards pip config/env overrides such as no-binary.
".venv\Scripts\python.exe" -m pip --isolated install --disable-pip-version-check --index-url https://pypi.org/simple --only-binary=:all: --upgrade pip setuptools wheel
if errorlevel 1 goto dependency_error
".venv\Scripts\python.exe" -m pip --isolated install --disable-pip-version-check --index-url https://pypi.org/simple --only-binary=:all: -r requirements.txt
if errorlevel 1 goto dependency_error

echo.
echo [Validation] Running before/after applications and fuzz tests...
".venv\Scripts\python.exe" run_lab7.py
if errorlevel 1 (
    echo ERROR: Lab 7 checks did not complete. Read the evidence directory.
    exit /b 1
)

echo.
echo SUCCESS: Evidence logs saved under Lab-7\evidence
if exist "PES1UG24CS017_Lab7_Fuzz_Testing_Report.pdf" (
    echo Screenshot report PDF is ready.
) else (
    echo Add your four genuine screenshots, then rerun Setup-Lab7.cmd.
)
exit /b 0

:dependency_error
echo.
echo ERROR: Could not install the required binary wheels.
echo This is an environment/package installation problem, NOT an ATM code failure.
echo Run this command to check Python versions:
echo     py -0p
echo If you have Python 3.12, remove the Lab-7\.venv folder and rerun.
echo If not, install Python 3.12 and rerun after removing the folder.
echo No Microsoft C++ Build Tools are needed if prebuilt wheels are available.
exit /b 1
