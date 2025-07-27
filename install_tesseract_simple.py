#!/usr/bin/env python3
"""
Einfache Tesseract OCR Installation für Windows
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_tesseract():
    """Prüft Tesseract-Installation"""
    print("Pruefe Tesseract-Installation...")
    
    # Prüfe Standard-Pfade
    paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    
    for path in paths:
        if os.path.exists(path):
            print(f"OK: Tesseract gefunden: {path}")
            return path
    
    # Prüfe PATH
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("OK: Tesseract im PATH gefunden")
            return "tesseract"
    except:
        pass
    
    print("FEHLER: Tesseract nicht gefunden")
    return None

def update_config(tesseract_path):
    """Aktualisiert config.json"""
    print("Aktualisiere Konfiguration...")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if 'system' not in config:
            config['system'] = {}
        
        config['system']['tesseract_path'] = tesseract_path
        config['system']['tesseract_installed'] = True
        
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("OK: Konfiguration aktualisiert")
        return True
        
    except Exception as e:
        print(f"FEHLER: Konfiguration fehlgeschlagen: {e}")
        return False

def test_tesseract(tesseract_path):
    """Testet Tesseract"""
    print("Teste Tesseract...")
    
    try:
        if tesseract_path != "tesseract":
            cmd = [tesseract_path, '--version']
        else:
            cmd = ['tesseract', '--version']
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("OK: Tesseract funktioniert!")
            print(f"Version: {result.stdout.split()[1] if len(result.stdout.split()) > 1 else 'Unbekannt'}")
            return True
        else:
            print(f"FEHLER: Test fehlgeschlagen: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"FEHLER: Test-Exception: {e}")
        return False

def install_instructions():
    """Zeigt Installationsanweisungen"""
    print("\n" + "="*60)
    print("MANUELLE TESSERACT-INSTALLATION ERFORDERLICH")
    print("="*60)
    print()
    print("SCHRITT 1: Download")
    print("Besuchen Sie: https://github.com/UB-Mannheim/tesseract/wiki")
    print("Laden Sie herunter: tesseract-ocr-w64-setup-5.3.3.20231005.exe")
    print()
    print("SCHRITT 2: Installation")
    print("1. Fuehren Sie den Installer aus")
    print("2. Installieren Sie nach: C:\\Program Files\\Tesseract-OCR\\")
    print("3. Lassen Sie alle Standard-Einstellungen")
    print()
    print("SCHRITT 3: Verification")
    print("Fuehren Sie danach aus: python install_tesseract_simple.py")
    print()
    print("ALTERNATIVE: System ohne OCR nutzen")
    print("Fuehren Sie aus: python demo_presentation.py")
    print("="*60)

def main():
    print("TESSERACT OCR INSTALLATION")
    print("="*40)
    
    # Prüfe Installation
    tesseract_path = check_tesseract()
    
    if tesseract_path:
        # Update Konfiguration
        if update_config(tesseract_path):
            if test_tesseract(tesseract_path):
                print("\nERFOLG: Tesseract ist einsatzbereit!")
                print("Starten Sie jetzt: python main.py")
                print("Oder verwenden Sie: python start_gui.bat")
                
                # Test mit pytesseract
                try:
                    import pytesseract
                    if tesseract_path != "tesseract":
                        pytesseract.pytesseract.tesseract_cmd = tesseract_path
                    version = pytesseract.get_tesseract_version()
                    print(f"Pytesseract Version: {version}")
                    print("OCR-System vollstaendig funktionsfaehig!")
                    return True
                except Exception as e:
                    print(f"Warnung: Pytesseract-Test fehlgeschlagen: {e}")
                    return True
    
    # Installation erforderlich
    install_instructions()
    return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\nInfo: System funktioniert auch ohne OCR")
            print("Demo-Praesentation mit Ihren Daten: python demo_presentation.py")
    except Exception as e:
        print(f"Fehler: {e}")
        import traceback
        traceback.print_exc()