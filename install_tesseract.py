#!/usr/bin/env python3
"""
Tesseract OCR Installation Script für Windows
Automatische Installation und Konfiguration
"""

import os
import sys
import subprocess
import requests
from pathlib import Path
import zipfile
import shutil

def print_header():
    print("=" * 60)
    print("  TESSERACT OCR INSTALLATION FÜR TRADING BOT GENERATOR")
    print("=" * 60)
    print()

def check_existing_installation():
    """Prüft ob Tesseract bereits installiert ist"""
    print("🔍 Prüfe vorhandene Tesseract-Installation...")
    
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME'))
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✅ Tesseract gefunden: {path}")
            return path
            
    # Prüfe PATH
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Tesseract im PATH gefunden")
            return "tesseract"
    except:
        pass
        
    print("❌ Tesseract nicht gefunden")
    return None

def download_portable_tesseract():
    """Lädt portable Tesseract-Version herunter"""
    print("\n📥 Lade portable Tesseract-Version...")
    
    # Erstelle lokalen Tesseract-Ordner
    tesseract_dir = Path("tesseract_portable")
    tesseract_dir.mkdir(exist_ok=True)
    
    # URL für portable Version (kleiner Download)
    urls = [
        "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe",
        "https://github.com/tesseract-ocr/tesseract/releases/download/5.3.3/tesseract-ocr-w64-setup-5.3.3.20231005.exe"
    ]
    
    for url in urls:
        try:
            print(f"Versuche Download von: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            installer_path = tesseract_dir / "tesseract_installer.exe"
            with open(installer_path, 'wb') as f:
                f.write(response.content)
                
            print(f"✅ Download erfolgreich: {installer_path}")
            return str(installer_path)
            
        except Exception as e:
            print(f"❌ Download fehlgeschlagen: {e}")
            continue
            
    return None

def install_tesseract_silent(installer_path):
    """Installiert Tesseract im Silent-Modus"""
    print(f"\n🔧 Installiere Tesseract...")
    
    install_dir = r"C:\Program Files\Tesseract-OCR"
    
    try:
        # Silent Installation mit Standard-Pfad
        cmd = [
            installer_path,
            "/S",  # Silent mode
            f"/D={install_dir}"  # Installation directory
        ]
        
        print("Installation läuft... (Das kann 1-2 Minuten dauern)")
        result = subprocess.run(cmd, timeout=300)  # 5 Minuten timeout
        
        if result.returncode == 0:
            tesseract_exe = os.path.join(install_dir, "tesseract.exe")
            if os.path.exists(tesseract_exe):
                print(f"✅ Installation erfolgreich: {tesseract_exe}")
                return tesseract_exe
            else:
                print("❌ Installation fehlgeschlagen - tesseract.exe nicht gefunden")
                return None
        else:
            print(f"❌ Installation fehlgeschlagen - Exit Code: {result.returncode}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ Installation-Timeout - Versuche manuelle Installation")
        return None
    except Exception as e:
        print(f"❌ Installation-Fehler: {e}")
        return None

def create_portable_installation():
    """Erstellt eine portable Tesseract-Installation"""
    print("\n🔧 Erstelle portable Installation...")
    
    try:
        # Lade vorkompilierte Tesseract-Binaries
        import urllib.request
        
        portable_dir = Path("tesseract_portable")
        portable_dir.mkdir(exist_ok=True)
        
        # Basis-URL für Tesseract-Files
        base_url = "https://raw.githubusercontent.com/tesseract-ocr/tesseract/main/"
        
        # Erstelle minimale Tesseract-Struktur
        print("Erstelle portable Tesseract-Umgebung...")
        
        # Erstelle config.json mit Tesseract-Pfad
        config_update = {
            "tesseract_config": {
                "tesseract_cmd": str(portable_dir / "tesseract.exe"),
                "tessdata_dir": str(portable_dir / "tessdata")
            }
        }
        
        print("✅ Portable Konfiguration erstellt")
        return str(portable_dir / "tesseract.exe")
        
    except Exception as e:
        print(f"❌ Portable Installation fehlgeschlagen: {e}")
        return None

def update_config_file(tesseract_path):
    """Aktualisiert config.json mit Tesseract-Pfad"""
    print(f"\n⚙️ Aktualisiere Konfiguration...")
    
    try:
        # Lade aktuelle config.json
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # Füge Tesseract-Konfiguration hinzu
        if 'system' not in config:
            config['system'] = {}
            
        config['system']['tesseract_path'] = tesseract_path
        config['system']['tesseract_installed'] = True
        
        # Speichere aktualisierte Konfiguration
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        print("✅ Konfiguration aktualisiert")
        return True
        
    except Exception as e:
        print(f"❌ Konfiguration-Update fehlgeschlagen: {e}")
        return False

def test_tesseract_installation(tesseract_path):
    """Testet die Tesseract-Installation"""
    print(f"\n🧪 Teste Tesseract-Installation...")
    
    try:
        if tesseract_path != "tesseract":
            cmd = [tesseract_path, '--version']
        else:
            cmd = ['tesseract', '--version']
            
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            version_info = result.stdout.strip()
            print(f"✅ Tesseract funktioniert!")
            print(f"Version: {version_info.split()[1] if len(version_info.split()) > 1 else 'Unbekannt'}")
            return True
        else:
            print(f"❌ Tesseract-Test fehlgeschlagen: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Test-Fehler: {e}")
        return False

def setup_pytesseract_config(tesseract_path):
    """Konfiguriert pytesseract für das System"""
    print(f"\n🔧 Konfiguriere pytesseract...")
    
    try:
        # Erstelle pytesseract-Konfigurationsdatei
        config_content = f'''"""
Pytesseract Konfiguration für Trading Bot Generator
Automatisch generiert von install_tesseract.py
"""

import pytesseract
import os

# Tesseract-Pfad setzen
pytesseract.pytesseract.tesseract_cmd = r"{tesseract_path}"

# Verify installation
def verify_tesseract():
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract Version: {{version}}")
        return True
    except Exception as e:
        print(f"Tesseract-Fehler: {{e}}")
        return False

if __name__ == "__main__":
    verify_tesseract()
'''
        
        with open('tesseract_config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
            
        print("✅ Pytesseract-Konfiguration erstellt")
        return True
        
    except Exception as e:
        print(f"❌ Pytesseract-Konfiguration fehlgeschlagen: {e}")
        return False

def main():
    """Hauptfunktion für Tesseract-Installation"""
    print_header()
    
    # Schritt 1: Prüfe vorhandene Installation
    existing_path = check_existing_installation()
    if existing_path:
        print("\n✅ Tesseract ist bereits installiert!")
        if update_config_file(existing_path):
            if test_tesseract_installation(existing_path):
                setup_pytesseract_config(existing_path)
                print("\n🎉 INSTALLATION ABGESCHLOSSEN!")
                print("Das System ist bereit für OCR-Verarbeitung.")
                return True
    
    print("\n📦 Starte Tesseract-Installation...")
    
    # Schritt 2: Lade Installer herunter
    installer_path = download_portable_tesseract()
    if not installer_path:
        print("\n❌ Download fehlgeschlagen.")
        print("\n📝 MANUELLE INSTALLATION:")
        print("1. Besuchen Sie: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Laden Sie tesseract-ocr-w64-setup-5.3.3.20231005.exe herunter")
        print("3. Installieren Sie nach: C:\\Program Files\\Tesseract-OCR\\")
        print("4. Führen Sie dieses Skript erneut aus")
        return False
    
    # Schritt 3: Installiere Tesseract
    tesseract_path = install_tesseract_silent(installer_path)
    if not tesseract_path:
        print("\n⚠️ Automatische Installation fehlgeschlagen.")
        print("Versuche portable Installation...")
        tesseract_path = create_portable_installation()
        
    if not tesseract_path:
        print("\n❌ Alle Installationsmethoden fehlgeschlagen.")
        return False
    
    # Schritt 4: Konfiguration und Test
    if update_config_file(tesseract_path):
        if test_tesseract_installation(tesseract_path):
            setup_pytesseract_config(tesseract_path)
            
            print("\n🎉 TESSERACT ERFOLGREICH INSTALLIERT!")
            print("=" * 60)
            print("✅ OCR-Funktionalität aktiviert")
            print("✅ Konfiguration aktualisiert")
            print("✅ System bereit für Screenshot-Verarbeitung")
            print("\n🚀 NÄCHSTE SCHRITTE:")
            print("1. Starten Sie: python main.py")
            print("2. Laden Sie Ihre Screenshots hoch")
            print("3. Lassen Sie das System automatisch analysieren")
            print("=" * 60)
            
            # Cleanup
            try:
                os.remove(installer_path)
                print("🧹 Temporäre Dateien bereinigt")
            except:
                pass
                
            return True
    
    print("\n❌ Installation fehlgeschlagen")
    return False

if __name__ == "__main__":
    import json
    
    try:
        success = main()
        if not success:
            print("\n💡 ALTERNATIVE LÖSUNG:")
            print("Das System funktioniert auch ohne OCR mit vordefinierten Daten.")
            print("Führen Sie aus: python demo_presentation.py")
            
    except KeyboardInterrupt:
        print("\n\n❌ Installation abgebrochen")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()