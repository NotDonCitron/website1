@echo off
title Trading Bot Presentation Generator
color 0A
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                🤖 Trading Bot Presentation Generator          ║
echo  ║                        GUI-Modus                             ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo  🚀 Starte Anwendung...
echo.

REM Prüfe ob Python verfügbar ist
python --version >nul 2>&1
if errorlevel 1 (
    echo  ❌ Python nicht gefunden!
    echo  📥 Bitte installieren Sie Python 3.8+ von: https://python.org
    echo.
    pause
    exit /b 1
)

REM Prüfe ob main.py existiert
if not exist "main.py" (
    echo  ❌ main.py nicht gefunden!
    echo  📁 Bitte stellen Sie sicher, dass Sie im richtigen Verzeichnis sind.
    echo.
    pause
    exit /b 1
)

REM Starte die Anwendung
echo  ✅ Python gefunden, starte GUI...
echo.
python main.py

REM Wenn Fehler auftreten
if errorlevel 1 (
    echo.
    echo  ❌ Fehler beim Starten der Anwendung!
    echo  🔧 Mögliche Lösungen:
    echo     1. Führen Sie zuerst 'python setup.py' aus
    echo     2. Installieren Sie Dependencies: 'pip install -r requirements.txt'
    echo     3. Prüfen Sie die README.md für Details
    echo.
)

pause