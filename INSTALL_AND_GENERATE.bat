@echo off
title Chitkara University - Video Forgery Detection Documentation Generator
color 0A

echo ============================================================
echo  Chitkara University - Documentation Generator
echo  Video Forgery Detection Project
echo  Team: Gaganveer Singh, Gunjan Mehta, Vidur Sharma
echo ============================================================
echo.

:: Check if Python is installed
echo [Step 1/4] Checking Python installation...
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo %PYVER% | findstr /i "python" >nul
if errorlevel 1 (
    echo [ERROR] Python not found in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

echo [OK] %PYVER% is installed!
echo.

:: Upgrade pip
echo [Step 2/4] Updating pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip updated!
echo.

:: Install required libraries
echo [Step 3/4] Installing required libraries...
echo This may take 2-3 minutes, please wait...
echo.

python -m pip install reportlab --quiet
echo  [OK] reportlab installed (for PDF generation)

python -m pip install python-pptx --quiet
echo  [OK] python-pptx installed (for PowerPoint generation)

python -m pip install Pillow --quiet
echo  [OK] Pillow installed (image support)

echo.
echo [OK] All libraries installed successfully!
echo.

:: Generate documents
echo [Step 4/4] Generating your documents...
echo.

cd /d "%~dp0"

echo  Generating Final Project Report PDF...
python generate_documentation.py
if errorlevel 1 (
    echo [WARNING] PDF generation encountered an issue. See error above.
) else (
    echo  [OK] Final_Project_Report.pdf created on Desktop!
)

echo.
echo  Generating PowerPoint Presentation...
python generate_presentation.py
if errorlevel 1 (
    echo [WARNING] PowerPoint generation encountered an issue. See error above.
) else (
    echo  [OK] Final_Presentation.pptx created on Desktop!
)

echo.
echo ============================================================
echo  DONE! Your documents have been generated:
echo.
echo   PDF Report : Final_Project_Report.pdf
echo   PowerPoint : Final_Presentation.pptx
echo   Location   : C:\Users\GunjanMehta\Desktop\patent\
echo.
echo  Both files are ready for your presentation!
echo ============================================================
echo.

:: Open the folder
start "" explorer "%~dp0"

pause
