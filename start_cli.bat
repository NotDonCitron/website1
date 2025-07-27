@echo off
title Trading Bot Presentation Generator - CLI
color 0B
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                🤖 Trading Bot Presentation Generator          ║
echo  ║                        CLI-Modus                             ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

REM Prüfe Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  ❌ Python nicht gefunden!
    pause
    exit /b 1
)

echo  🔧 CLI-Konfiguration
echo  ═══════════════════════
echo.

REM Benutzer-Eingaben
set /p signal_dir=" 📸 Signal-Screenshots Ordner eingeben: "
if "%signal_dir%"=="" (
    echo  ❌ Kein Ordner angegeben!
    pause
    exit /b 1
)

set /p result_dir=" 💰 Ergebnis-Screenshots Ordner eingeben: "
if "%result_dir%"=="" (
    echo  ❌ Kein Ordner angegeben!
    pause
    exit /b 1
)

set /p output_name=" 📊 Ausgabedatei-Name (ohne Endung): "
if "%output_name%"=="" set output_name=trading_bot_presentation

set /p template_choice=" 🎨 Template (1=Professional, 2=Dark, 3=Corporate): "
if "%template_choice%"=="" set template_choice=1

REM Template-Namen zuordnen
if "%template_choice%"=="1" set template_name=crypto_professional
if "%template_choice%"=="2" set template_name=modern_dark
if "%template_choice%"=="3" set template_name=corporate_blue

echo.
echo  🚀 Starte Verarbeitung...
echo  ═══════════════════════
echo  📁 Signale: %signal_dir%
echo  📁 Ergebnisse: %result_dir%
echo  📄 Ausgabe: %output_name%
echo  🎨 Template: %template_name%
echo.

REM CLI-Befehl ausführen
python main.py --cli --signal-dir "%signal_dir%" --result-dir "%result_dir%" --output "%output_name%" --template %template_name%

echo.
if errorlevel 0 (
    echo  ✅ Präsentation erfolgreich erstellt!
    echo  📁 Prüfen Sie den Output-Ordner für die fertige Datei.
) else (
    echo  ❌ Fehler bei der Verarbeitung!
    echo  🔍 Prüfen Sie die Log-Dateien für Details.
)

echo.
pause