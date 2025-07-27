# 🚀 Trading Bot Presentation Generator - Installation

**Schnelle Installation und Setup in wenigen Minuten**

---

## ⚡ Express-Installation (Empfohlen)

### **Schritt 1: Repository herunterladen**
```bash
# Option A: Git Clone (falls Git installiert)
git clone https://github.com/yourusername/trading-bot-presentation-generator.git
cd trading-bot-presentation-generator

# Option B: ZIP-Download
# 1. GitHub-Repository öffnen
# 2. "Code" → "Download ZIP" klicken  
# 3. ZIP entpacken und Ordner öffnen
```

### **Schritt 2: Automatisches Setup**
```bash
# Automatische Installation starten
python setup.py
```

Das Setup-Skript übernimmt automatisch:
- ✅ Python-Version prüfen
- ✅ Dependencies installieren  
- ✅ Tesseract OCR Setup
- ✅ Verzeichnisse erstellen
- ✅ Beispieldateien generieren
- ✅ System-Tests durchführen

### **Schritt 3: Anwendung starten**

#### **Windows:**
```bash
# GUI-Modus (Anfänger-freundlich)
start_gui.bat

# CLI-Modus (Für Profis)
start_cli.bat
```

#### **macOS/Linux:**
```bash
# Skripte ausführbar machen
chmod +x start_gui.sh start_cli.sh

# GUI-Modus
./start_gui.sh

# CLI-Modus  
./start_cli.sh
```

---

## 🔧 Manuelle Installation

### **Voraussetzungen prüfen**

#### **1. Python-Version**
```bash
python --version
# Sollte Python 3.8 oder höher anzeigen

# Falls nicht installiert:
# Windows: https://python.org/downloads
# macOS: brew install python3
# Ubuntu: sudo apt install python3.11
```

#### **2. Pip aktualisieren**
```bash
python -m pip install --upgrade pip
```

### **Dependencies installieren**

#### **Core-Pakete**
```bash
pip install -r requirements.txt
```

**Bei Problemen einzeln installieren:**
```bash
# Grundlegende Pakete
pip install opencv-python pytesseract pillow numpy python-pptx

# Chart-Erstellung
pip install matplotlib seaborn pandas

# GUI-Framework (meist vorinstalliert)
pip install tkinter
```

### **Tesseract OCR installieren**

#### **Windows:**
1. **Download**: https://github.com/UB-Mannheim/tesseract/wiki
2. **Installation** nach: `C:\Program Files\Tesseract-OCR\`
3. **PATH setzen** oder `config.json` anpassen:
   ```json
   {
     "tesseract_path": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
   }
   ```

#### **macOS:**
```bash
# Mit Homebrew (empfohlen)
brew install tesseract

# Mit MacPorts
sudo port install tesseract
```

#### **Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-deu
```

#### **CentOS/RHEL:**
```bash
sudo yum install epel-release
sudo yum install tesseract tesseract-langpack-deu
```

### **Verzeichnisstruktur erstellen**
```bash
mkdir -p examples/signals examples/results output backups logs temp cache
```

---

## 🧪 Installation testen

### **Grundlegende Tests**
```bash
# Python-Imports testen
python -c "import cv2, pytesseract, numpy, tkinter; print('✅ Alle Imports erfolgreich')"

# Tesseract-Version prüfen
tesseract --version

# OCR-Test mit Beispielbild
python -c "import pytesseract; print('Tesseract Version:', pytesseract.get_tesseract_version())"
```

### **Vollständiger Systemtest**
```bash
python -c "
import sys
print('🐍 Python:', sys.version)

import cv2
print('📷 OpenCV:', cv2.__version__)

import pytesseract
print('🔤 Tesseract:', pytesseract.get_tesseract_version())

from pptx import Presentation
print('📊 PowerPoint: OK')

import tkinter
root = tkinter.Tk()
root.withdraw()
print('🖼️ GUI: OK')
root.destroy()

print('✅ Alle Tests bestanden!')
"
```

---

## 🎯 Erste Schritte nach Installation

### **1. Konfiguration anpassen**
```bash
# config.json editieren
notepad config.json  # Windows
nano config.json     # Linux/macOS
```

**Wichtige Einstellungen:**
```json
{
  "bot_data": {
    "referral_code": "HIER_IHREN_CODE_EINTRAGEN",
    "weekly_stats": {
      "trades": 59,
      "winrate": 84.7, 
      "roi": 31.690
    }
  }
}
```

### **2. Beispiel-Screenshots vorbereiten**
```bash
# Ordnerstruktur für Tests:
examples/
├── signals/        # Signal-Screenshots hier ablegen
└── results/        # Ergebnis-Screenshots hier ablegen
```

### **3. Erste Präsentation erstellen**

#### **GUI-Methode:**
1. `start_gui.bat` (Windows) oder `./start_gui.sh` (Linux/macOS)
2. Screenshots hochladen
3. "Bilder analysieren" klicken
4. Template auswählen
5. "Präsentation generieren"

#### **CLI-Methode:**
```bash
python main.py --cli \
  --signal-dir examples/signals \
  --result-dir examples/results \
  --output meine_erste_presentation \
  --template crypto_professional
```

---

## 🐛 Häufige Installationsprobleme

### **Problem: "python command not found"**
```bash
# Lösung 1: Python3 verwenden
python3 --version
python3 setup.py

# Lösung 2: Python zur PATH hinzufügen (Windows)
# Systemsteuerung → System → Erweiterte Systemeinstellungen → Umgebungsvariablen
```

### **Problem: "pip install schlägt fehl"**
```bash
# Lösung 1: Pip upgraden
python -m pip install --upgrade pip

# Lösung 2: Mit Administrator-Rechten (Windows)
# PowerShell als Administrator öffnen

# Lösung 3: Virtual Environment verwenden
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### **Problem: "Tesseract not found"**
```bash
# Lösung 1: PATH prüfen
tesseract --version

# Lösung 2: Vollständigen Pfad in config.json setzen
{
  "tesseract_path": "/usr/local/bin/tesseract"  # Linux/macOS
  "tesseract_path": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Windows
}

# Lösung 3: Erneut installieren
# Windows: Installer neu herunterladen
# Linux: sudo apt install --reinstall tesseract-ocr
# macOS: brew reinstall tesseract
```

### **Problem: "ModuleNotFoundError"**
```bash
# Lösung: Spezifische Module nachinstallieren
pip install opencv-python pytesseract pillow numpy python-pptx matplotlib pandas

# Bei OpenCV-Problemen:
pip uninstall opencv-python
pip install opencv-python-headless
```

### **Problem: "Permission denied"**
```bash
# Linux/macOS: Mit sudo installieren
sudo pip install -r requirements.txt

# Oder lokale Installation:
pip install --user -r requirements.txt

# Windows: PowerShell als Administrator
```

### **Problem: GUI startet nicht**
```bash
# Lösung 1: Tkinter nachinstallieren
# Ubuntu: sudo apt install python3-tk
# CentOS: sudo yum install tkinter

# Lösung 2: Display-Variable setzen (Linux)
export DISPLAY=:0

# Lösung 3: CLI-Version verwenden
python main.py --cli
```

---

## 🔄 Updates und Wartung

### **System aktualisieren**
```bash
# Repository aktualisieren
git pull origin main

# Dependencies aktualisieren  
pip install -r requirements.txt --upgrade

# Tesseract aktualisieren
# Windows: Neuen Installer herunterladen
# Linux: sudo apt upgrade tesseract-ocr
# macOS: brew upgrade tesseract
```

### **Cache leeren**
```bash
# Temporäre Dateien löschen
python -c "
import shutil, os
for folder in ['temp', 'cache', '__pycache__']:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f'🗑️ {folder} geleert')
"
```

### **Deinstallation**
```bash
# Dependencies deinstallieren
pip uninstall -r requirements.txt -y

# Projektordner löschen
# Windows: rmdir /s trading-bot-presentation-generator
# Linux/macOS: rm -rf trading-bot-presentation-generator
```

---

## 📋 System-Anforderungen

### **Minimal-Anforderungen**
- **OS**: Windows 10, macOS 10.15, Ubuntu 18.04
- **Python**: 3.8+
- **RAM**: 4GB
- **Speicher**: 2GB frei
- **CPU**: 2 Kerne

### **Empfohlene Konfiguration**
- **OS**: Windows 11, macOS 12+, Ubuntu 22.04
- **Python**: 3.11+
- **RAM**: 8GB+
- **Speicher**: 5GB frei (für große Bildmengen)
- **CPU**: 4+ Kerne
- **SSD**: Für bessere Performance

### **Netzwerk (Optional)**
- Internet-Verbindung für Updates
- Telegram-Bot Integration (optional)
- E-Mail-Versand (optional)

---

## 🆘 Support erhalten

### **Dokumentation**
- **README.md**: Vollständige Anleitung
- **Diese Datei**: Installation & Setup
- **Code-Kommentare**: Technische Details

### **Community Support**
- **GitHub Issues**: https://github.com/yourusername/trading-bot-presentation-generator/issues
- **Discord**: https://discord.gg/tradingbot-generator
- **Telegram**: @TradingBotGeneratorSupport

### **Professional Support**
- **E-Mail**: support@tradingbotgenerator.com
- **Consulting**: consulting@tradingbotgenerator.com
- **Custom Development**: dev@tradingbotgenerator.com

---

## ✅ Installation erfolgreich!

Nach erfolgreicher Installation sollten Sie folgende Dateien haben:

```
trading-bot-presentation-generator/
├── main.py                    ✅ Hauptanwendung
├── image_analyzer.py          ✅ OCR-Modul
├── presentation_builder.py    ✅ PowerPoint-Generator
├── templates.py              ✅ Design-Templates
├── config.json              ✅ Konfiguration
├── requirements.txt         ✅ Dependencies
├── setup.py                 ✅ Setup-Skript
├── start_gui.bat/.sh        ✅ GUI-Starter
├── start_cli.bat/.sh        ✅ CLI-Starter
├── README.md               ✅ Dokumentation
├── INSTALL.md             ✅ Diese Datei
└── examples/              ✅ Beispieldateien
```

**🚀 Bereit zum Start!** Führen Sie `start_gui.bat` (Windows) oder `./start_gui.sh` (Linux/macOS) aus!

---

*Zuletzt aktualisiert: 26. Juli 2024*