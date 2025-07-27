#!/usr/bin/env python3
"""
Setup Script für Trading Bot Presentation Generator
Automatische Installation und Konfiguration
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path

def print_banner():
    """Willkommens-Banner anzeigen"""
    banner = """
================================================================
             Trading Bot Presentation Generator
                     Automatisches Setup
================================================================
    """
    print(banner)

def check_python_version():
    """Python-Version prüfen"""
    print("Überprüfe Python-Version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("FEHLER: Python 3.8 oder höher erforderlich!")
        print(f"   Aktuelle Version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"OK: Python {version.major}.{version.minor}.{version.micro}")

def install_dependencies():
    """Python-Dependencies installieren"""
    print("\nInstalliere Python-Dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("OK: Dependencies erfolgreich installiert")
    except subprocess.CalledProcessError as e:
        print(f"FEHLER: beim Installieren der Dependencies: {e}")
        return False
    return True

def install_tesseract():
    """Tesseract OCR installieren"""
    print("\nÜberprüfe Tesseract OCR Installation...")
    
    # Tesseract-Installation prüfen
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("OK: Tesseract bereits installiert")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    system = platform.system().lower()
    
    if system == "windows":
        print("Windows erkannt - Tesseract-Installation erforderlich")
        print("Bitte installieren Sie Tesseract manuell:")
        print("   1. Download: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Installieren nach: C:\\Program Files\\Tesseract-OCR\\")
        print("   3. PATH-Variable setzen oder config.json anpassen")
        input("   Drücken Sie Enter wenn Installation abgeschlossen ist...")
        
    elif system == "darwin":  # macOS
        print("macOS erkannt - Installiere Tesseract via Homebrew...")
        try:
            subprocess.check_call(['brew', 'install', 'tesseract'])
            print("OK: Tesseract erfolgreich installiert")
        except subprocess.CalledProcessError:
            print("FEHLER: Homebrew nicht gefunden. Bitte installieren Sie Tesseract manuell:")
            print("   brew install tesseract")
            
    elif system == "linux":
        print("Linux erkannt - Installiere Tesseract...")
        try:
            # Ubuntu/Debian
            subprocess.check_call(['sudo', 'apt-get', 'update'])
            subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'tesseract-ocr', 'tesseract-ocr-deu'])
            print("OK: Tesseract erfolgreich installiert")
        except subprocess.CalledProcessError:
            print("FEHLER: Automatische Installation fehlgeschlagen")
            print("   Bitte installieren Sie manuell: sudo apt-get install tesseract-ocr")
    
    return True

def create_directories():
    """Erforderliche Verzeichnisse erstellen"""
    print("\nErstelle Verzeichnisstruktur...")
    
    directories = [
        "examples/signals",
        "examples/results", 
        "output",
        "backups",
        "logs",
        "temp",
        "cache"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   Ordner: {directory}")
    
    print("OK: Verzeichnisse erstellt")

def create_example_files():
    """Beispieldateien erstellen"""
    print("\nErstelle Beispieldateien...")
    
    # Beispiel-Config für Testzwecke
    test_config = {
        "test_mode": True,
        "sample_data": {
            "trades": [
                {"coin": "BTC", "roi": 25.5, "status": "win"},
                {"coin": "ETH", "roi": 18.3, "status": "win"},
                {"coin": "EPIC", "roi": 1250.0, "status": "win"}
            ]
        }
    }
    
    import json
    with open("examples/test_config.json", "w", encoding="utf-8") as f:
        json.dump(test_config, f, indent=2, ensure_ascii=False)
    
    # Batch-Skripte erstellen
    if platform.system().lower() == "windows":
        create_batch_files()
    else:
        create_shell_scripts()
    
    print("OK: Beispieldateien erstellt")

def create_batch_files():
    """Windows Batch-Dateien erstellen"""
    
    # Start GUI
    start_gui_bat = """@echo off
echo 🤖 Starte Trading Bot Presentation Generator...
python main.py
pause
"""
    
    with open("start_gui.bat", "w") as f:
        f.write(start_gui_bat)
    
    # Start CLI
    start_cli_bat = """@echo off
echo 🤖 Trading Bot Presentation Generator - CLI Mode
echo.
set /p signal_dir="Signal-Verzeichnis eingeben: "
set /p result_dir="Ergebnis-Verzeichnis eingeben: "
set /p output_file="Ausgabedatei (ohne Endung): "

python main.py --cli --signal-dir "%signal_dir%" --result-dir "%result_dir%" --output "%output_file%"
pause
"""
    
    with open("start_cli.bat", "w") as f:
        f.write(start_cli_bat)

def create_shell_scripts():
    """Unix Shell-Skripte erstellen"""
    
    # Start GUI
    start_gui_sh = """#!/bin/bash
echo "🤖 Starte Trading Bot Presentation Generator..."
python3 main.py
"""
    
    with open("start_gui.sh", "w") as f:
        f.write(start_gui_sh)
    os.chmod("start_gui.sh", 0o755)
    
    # Start CLI
    start_cli_sh = """#!/bin/bash
echo "🤖 Trading Bot Presentation Generator - CLI Mode"
echo
read -p "Signal-Verzeichnis eingeben: " signal_dir
read -p "Ergebnis-Verzeichnis eingeben: " result_dir
read -p "Ausgabedatei (ohne Endung): " output_file

python3 main.py --cli --signal-dir "$signal_dir" --result-dir "$result_dir" --output "$output_file"
"""
    
    with open("start_cli.sh", "w") as f:
        f.write(start_cli_sh)
    os.chmod("start_cli.sh", 0o755)

def run_tests():
    """Grundlegende Tests ausführen"""
    print("\nFühre Basistests aus...")
    
    try:
        # Import-Tests
        print("   Teste Imports...")
        import tkinter
        import cv2
        import pytesseract
        import numpy
        from pptx import Presentation
        print("   OK: Alle Imports erfolgreich")
        
        # Tesseract-Test
        print("   Teste Tesseract...")
        version = pytesseract.get_tesseract_version()
        print(f"   OK: Tesseract Version: {version}")
        
        # GUI-Test
        print("   Teste GUI-Komponenten...")
        root = tkinter.Tk()
        root.withdraw()  # Fenster nicht anzeigen
        root.destroy()
        print("   OK: GUI-Test erfolgreich")
        
        return True
        
    except Exception as e:
        print(f"   FEHLER: Test fehlgeschlagen: {e}")
        return False

def main():
    """Hauptfunktion für Setup"""
    print_banner()
    
    # System-Checks
    check_python_version()
    
    # Installation
    if not install_dependencies():
        print("\n❌ Setup fehlgeschlagen - Dependencies konnten nicht installiert werden")
        sys.exit(1)
    
    install_tesseract()
    create_directories()
    create_example_files()
    
    # Tests
    if run_tests():
        print("\nOK: Setup erfolgreich abgeschlossen!")
        print("\nSo starten Sie die Anwendung:")
        
        if platform.system().lower() == "windows":
            print("   GUI: Doppelklick auf start_gui.bat")
            print("   CLI: Doppelklick auf start_cli.bat")
            print("   Manuell: python main.py")
        else:
            print("   GUI: ./start_gui.sh")
            print("   CLI: ./start_cli.sh") 
            print("   Manuell: python3 main.py")
            
        print("\nDokumentation: Siehe README.md")
        print("Support: Siehe GitHub Issues")
        
    else:
        print("\nWARNUNG: Setup mit Warnungen abgeschlossen")
        print("   Bitte prüfen Sie die Tesseract-Installation")
        print("   und starten Sie die Anwendung manuell: python main.py")

if __name__ == "__main__":
    main()