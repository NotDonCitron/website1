#!/usr/bin/env python3
"""
Trading Bot Presentation Generator
Automatische PowerPoint-Präsentationserstellung für Trading-Bot Marketing

Author: Trading Bot Marketing Team
Version: 1.0.0
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime

from image_analyzer import ImageAnalyzer
from presentation_builder import PresentationBuilder
from templates import TemplateManager

class TradingBotPresentationApp:
    """Hauptanwendung für die Trading-Bot Präsentationserstellung"""
    
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.image_analyzer = ImageAnalyzer()
        self.presentation_builder = PresentationBuilder()
        self.template_manager = TemplateManager()
        
        # GUI Setup
        self.root = tk.Tk()
        self.setup_gui()
        
    def setup_logging(self):
        """Logging-Konfiguration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('trading_bot_generator.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Konfiguration laden"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.logger.warning("Config file not found, using defaults")
            self.config = self.get_default_config()
            self.save_config()
            
    def get_default_config(self) -> Dict:
        """Standard-Konfiguration"""
        return {
            "bot_data": {
                "name": "Bybit Trading Bot",
                "description": "Automatischer Telegram-Signal Bot für Bybit",
                "referral_code": "9EEDV9",
                "weekly_stats": {
                    "period": "17.07-22.07",
                    "trades": 59,
                    "winrate": 84.7,
                    "roi": 31.690
                },
                "top_performers": [
                    {"coin": "EPIC", "roi": 5261},
                    {"coin": "FLOKI", "roi": 1453},
                    {"coin": "HBAR", "roi": 1403}
                ],
                "example_trades": [
                    {"coin": "COOK", "roi": 142.92},
                    {"coin": "LTC", "roi": 159.0},
                    {"coin": "TAO", "roi": 132.91},
                    {"coin": "ZORA", "roi": 1538.61}
                ]
            },
            "presentation": {
                "title": "Profitabler Trading Bot - Beweise & Statistiken",
                "language": "de",
                "template": "crypto_professional",
                "include_charts": True,
                "include_cta": True,
                "max_slides_per_trade": 1
            },
            "processing": {
                "ocr_confidence": 0.7,
                "auto_match_threshold": 0.8,
                "backup_enabled": True,
                "batch_size": 50
            }
        }
        
    def save_config(self):
        """Konfiguration speichern"""
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
            
    def setup_gui(self):
        """GUI initialisieren"""
        self.root.title("Trading Bot Presentation Generator v1.0")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        # Style konfigurieren
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        
        self.create_main_interface()
        
    def create_main_interface(self):
        """Hauptoberfläche erstellen"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(header_frame, text="🤖 Trading Bot Presentation Generator", 
                 style='Title.TLabel').pack()
        ttk.Label(header_frame, text="Automatische PowerPoint-Erstellung für Trading-Bot Marketing").pack()
        
        # Tabs erstellen
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tab 1: Bild-Upload
        self.create_upload_tab(notebook)
        
        # Tab 2: Einstellungen
        self.create_settings_tab(notebook)
        
        # Tab 3: Präsentation
        self.create_presentation_tab(notebook)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Bereit für Upload...")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief='sunken', anchor='w')
        status_bar.pack(fill='x', side='bottom')
        
    def create_upload_tab(self, notebook):
        """Upload-Tab erstellen"""
        upload_frame = ttk.Frame(notebook)
        notebook.add(upload_frame, text="📁 Bilder Upload")
        
        # Upload Bereich
        upload_section = ttk.LabelFrame(upload_frame, text="Screenshot Upload", padding=20)
        upload_section.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Signal Screenshots
        ttk.Label(upload_section, text="Signal Screenshots:", style='Heading.TLabel').pack(anchor='w')
        self.signal_frame = ttk.Frame(upload_section)
        self.signal_frame.pack(fill='x', pady=5)
        
        ttk.Button(self.signal_frame, text="📸 Signal Screenshots auswählen", 
                  command=self.select_signal_images).pack(side='left')
        self.signal_count_var = tk.StringVar(value="0 Dateien")
        ttk.Label(self.signal_frame, textvariable=self.signal_count_var).pack(side='left', padx=10)
        
        # Ergebnis Screenshots
        ttk.Label(upload_section, text="Ergebnis Screenshots:", style='Heading.TLabel').pack(anchor='w', pady=(20,0))
        self.result_frame = ttk.Frame(upload_section)
        self.result_frame.pack(fill='x', pady=5)
        
        ttk.Button(self.result_frame, text="💰 Ergebnis Screenshots auswählen", 
                  command=self.select_result_images).pack(side='left')
        self.result_count_var = tk.StringVar(value="0 Dateien")
        ttk.Label(self.result_frame, textvariable=self.result_count_var).pack(side='left', padx=10)
        
        # Verarbeitung
        process_frame = ttk.Frame(upload_section)
        process_frame.pack(fill='x', pady=20)
        
        self.process_btn = ttk.Button(process_frame, text="🔄 Bilder analysieren", 
                                     command=self.process_images, state='disabled')
        self.process_btn.pack()
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(upload_section, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(pady=10)
        
        # Ergebnisse
        self.results_text = tk.Text(upload_section, height=10, width=80)
        self.results_text.pack(fill='both', expand=True, pady=10)
        
        # Variablen für Dateipfade
        self.signal_images = []
        self.result_images = []
        self.processed_trades = []
        
    def create_settings_tab(self, notebook):
        """Einstellungen-Tab erstellen"""
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Einstellungen")
        
        # Bot Daten
        bot_section = ttk.LabelFrame(settings_frame, text="Bot Informationen", padding=20)
        bot_section.pack(fill='x', padx=20, pady=10)
        
        # Referral Code
        ttk.Label(bot_section, text="Referral Code:").grid(row=0, column=0, sticky='w', pady=5)
        self.referral_var = tk.StringVar(value=self.config['bot_data']['referral_code'])
        ttk.Entry(bot_section, textvariable=self.referral_var, width=20).grid(row=0, column=1, padx=10)
        
        # Wochenstatistiken
        ttk.Label(bot_section, text="Wochenstatistiken:").grid(row=1, column=0, sticky='w', pady=5)
        stats_frame = ttk.Frame(bot_section)
        stats_frame.grid(row=1, column=1, padx=10, sticky='w')
        
        ttk.Label(stats_frame, text="Trades:").grid(row=0, column=0)
        self.trades_var = tk.StringVar(value=str(self.config['bot_data']['weekly_stats']['trades']))
        ttk.Entry(stats_frame, textvariable=self.trades_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(stats_frame, text="Winrate %:").grid(row=0, column=2, padx=(10,0))
        self.winrate_var = tk.StringVar(value=str(self.config['bot_data']['weekly_stats']['winrate']))
        ttk.Entry(stats_frame, textvariable=self.winrate_var, width=10).grid(row=0, column=3, padx=5)
        
        # Präsentations-Einstellungen
        pres_section = ttk.LabelFrame(settings_frame, text="Präsentationseinstellungen", padding=20)
        pres_section.pack(fill='x', padx=20, pady=10)
        
        # Template Auswahl
        ttk.Label(pres_section, text="Template:").grid(row=0, column=0, sticky='w', pady=5)
        self.template_var = tk.StringVar(value=self.config['presentation']['template'])
        template_combo = ttk.Combobox(pres_section, textvariable=self.template_var, 
                                     values=['crypto_professional', 'modern_dark', 'corporate_blue'])
        template_combo.grid(row=0, column=1, padx=10, sticky='w')
        
        # Sprache
        ttk.Label(pres_section, text="Sprache:").grid(row=1, column=0, sticky='w', pady=5)
        self.language_var = tk.StringVar(value=self.config['presentation']['language'])
        lang_combo = ttk.Combobox(pres_section, textvariable=self.language_var, 
                                 values=['de', 'en'])
        lang_combo.grid(row=1, column=1, padx=10, sticky='w')
        
        # Checkboxen
        self.charts_var = tk.BooleanVar(value=self.config['presentation']['include_charts'])
        ttk.Checkbutton(pres_section, text="Performance Charts einschließen", 
                       variable=self.charts_var).grid(row=2, column=0, columnspan=2, sticky='w', pady=5)
        
        self.cta_var = tk.BooleanVar(value=self.config['presentation']['include_cta'])
        ttk.Checkbutton(pres_section, text="Call-to-Action Slides einschließen", 
                       variable=self.cta_var).grid(row=3, column=0, columnspan=2, sticky='w', pady=5)
        
        # Speichern Button
        ttk.Button(settings_frame, text="💾 Einstellungen speichern", 
                  command=self.save_settings).pack(pady=20)
        
    def create_presentation_tab(self, notebook):
        """Präsentations-Tab erstellen"""
        pres_frame = ttk.Frame(notebook)
        notebook.add(pres_frame, text="📊 Präsentation")
        
        # Generierung
        gen_section = ttk.LabelFrame(pres_frame, text="Präsentation generieren", padding=20)
        gen_section.pack(fill='x', padx=20, pady=10)
        
        # Ausgabe Optionen
        ttk.Label(gen_section, text="Ausgabeformat:").pack(anchor='w')
        self.output_format = tk.StringVar(value="pptx")
        format_frame = ttk.Frame(gen_section)
        format_frame.pack(anchor='w', pady=5)
        
        ttk.Radiobutton(format_frame, text="PowerPoint (.pptx)", 
                       variable=self.output_format, value="pptx").pack(side='left')
        ttk.Radiobutton(format_frame, text="PDF", 
                       variable=self.output_format, value="pdf").pack(side='left', padx=10)
        ttk.Radiobutton(format_frame, text="HTML", 
                       variable=self.output_format, value="html").pack(side='left')
        
        # Ausgabepfad
        output_frame = ttk.Frame(gen_section)
        output_frame.pack(fill='x', pady=10)
        ttk.Label(output_frame, text="Ausgabepfad:").pack(anchor='w')
        
        path_frame = ttk.Frame(output_frame)
        path_frame.pack(fill='x', pady=5)
        self.output_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "presentation"))
        ttk.Entry(path_frame, textvariable=self.output_path_var, width=50).pack(side='left', fill='x', expand=True)
        ttk.Button(path_frame, text="📁", command=self.select_output_path).pack(side='right', padx=(5,0))
        
        # Generieren Button
        self.generate_btn = ttk.Button(gen_section, text="🚀 Präsentation generieren", 
                                      command=self.generate_presentation, state='disabled')
        self.generate_btn.pack(pady=20)
        
        # Vorschau
        preview_section = ttk.LabelFrame(pres_frame, text="Vorschau", padding=20)
        preview_section.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.preview_text = tk.Text(preview_section, height=15, width=80)
        preview_scroll = ttk.Scrollbar(preview_section, orient='vertical', command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scroll.set)
        
        self.preview_text.pack(side='left', fill='both', expand=True)
        preview_scroll.pack(side='right', fill='y')
        
    def select_signal_images(self):
        """Signal-Bilder auswählen"""
        files = filedialog.askopenfilenames(
            title="Signal Screenshots auswählen",
            filetypes=[("Bilder", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("Alle Dateien", "*.*")]
        )
        if files:
            self.signal_images = list(files)
            self.signal_count_var.set(f"{len(files)} Dateien")
            self.update_process_button()
            self.logger.info(f"Selected {len(files)} signal images")
            
    def select_result_images(self):
        """Ergebnis-Bilder auswählen"""
        files = filedialog.askopenfilenames(
            title="Ergebnis Screenshots auswählen",
            filetypes=[("Bilder", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("Alle Dateien", "*.*")]
        )
        if files:
            self.result_images = list(files)
            self.result_count_var.set(f"{len(files)} Dateien")
            self.update_process_button()
            self.logger.info(f"Selected {len(files)} result images")
            
    def update_process_button(self):
        """Verarbeitungs-Button Status aktualisieren"""
        if self.signal_images or self.result_images:
            self.process_btn.configure(state='normal')
        else:
            self.process_btn.configure(state='disabled')
            
    def process_images(self):
        """Bilder verarbeiten"""
        try:
            self.status_var.set("Verarbeite Bilder...")
            self.progress_var.set(0)
            self.results_text.delete(1.0, tk.END)
            
            all_images = self.signal_images + self.result_images
            total_images = len(all_images)
            
            if total_images == 0:
                messagebox.showwarning("Keine Bilder", "Bitte wählen Sie Bilder aus.")
                return
                
            processed_data = []
            
            for i, image_path in enumerate(all_images):
                self.results_text.insert(tk.END, f"Verarbeite: {os.path.basename(image_path)}\n")
                self.results_text.see(tk.END)
                self.root.update()
                
                # OCR-Analyse
                analysis = self.image_analyzer.analyze_image(image_path)
                if analysis:
                    processed_data.append({
                        'path': image_path,
                        'type': 'signal' if image_path in self.signal_images else 'result',
                        'data': analysis
                    })
                    self.results_text.insert(tk.END, f"  ✓ Erkannt: {analysis.get('coin', 'Unbekannt')}\n")
                else:
                    self.results_text.insert(tk.END, f"  ✗ Keine Daten erkannt\n")
                
                # Progress aktualisieren
                progress = ((i + 1) / total_images) * 100
                self.progress_var.set(progress)
                self.root.update()
                
            # Matching durchführen
            self.results_text.insert(tk.END, "\n=== Matching-Phase ===\n")
            self.processed_trades = self.image_analyzer.match_signals_to_results(processed_data)
            
            self.results_text.insert(tk.END, f"✓ {len(self.processed_trades)} Trades erfolgreich gematched\n")
            
            # Vorschau aktualisieren
            self.update_preview()
            
            # UI aktualisieren
            self.generate_btn.configure(state='normal')
            self.status_var.set(f"Verarbeitung abgeschlossen - {len(self.processed_trades)} Trades erkannt")
            
        except Exception as e:
            self.logger.error(f"Error processing images: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Verarbeiten der Bilder: {e}")
            self.status_var.set("Fehler bei der Verarbeitung")
            
    def update_preview(self):
        """Vorschau aktualisieren"""
        self.preview_text.delete(1.0, tk.END)
        
        if not self.processed_trades:
            self.preview_text.insert(tk.END, "Keine verarbeiteten Trades verfügbar.")
            return
            
        self.preview_text.insert(tk.END, "=== PRÄSENTATIONS-VORSCHAU ===\n\n")
        self.preview_text.insert(tk.END, f"Template: {self.template_var.get()}\n")
        self.preview_text.insert(tk.END, f"Sprache: {self.language_var.get()}\n")
        self.preview_text.insert(tk.END, f"Anzahl Trades: {len(self.processed_trades)}\n\n")
        
        for i, trade in enumerate(self.processed_trades[:5], 1):  # Nur erste 5 anzeigen
            self.preview_text.insert(tk.END, f"Slide {i}: {trade.get('coin', 'Unbekannt')}\n")
            self.preview_text.insert(tk.END, f"  ROI: {trade.get('roi', 'N/A')}%\n")
            self.preview_text.insert(tk.END, f"  Entry: {trade.get('entry_price', 'N/A')}\n")
            self.preview_text.insert(tk.END, f"  Status: {trade.get('status', 'N/A')}\n\n")
            
        if len(self.processed_trades) > 5:
            self.preview_text.insert(tk.END, f"... und {len(self.processed_trades) - 5} weitere Trades\n")
            
    def save_settings(self):
        """Einstellungen speichern"""
        try:
            self.config['bot_data']['referral_code'] = self.referral_var.get()
            self.config['bot_data']['weekly_stats']['trades'] = int(self.trades_var.get())
            self.config['bot_data']['weekly_stats']['winrate'] = float(self.winrate_var.get())
            self.config['presentation']['template'] = self.template_var.get()
            self.config['presentation']['language'] = self.language_var.get()
            self.config['presentation']['include_charts'] = self.charts_var.get()
            self.config['presentation']['include_cta'] = self.cta_var.get()
            
            self.save_config()
            messagebox.showinfo("Gespeichert", "Einstellungen wurden gespeichert!")
            self.logger.info("Settings saved successfully")
            
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")
            
    def select_output_path(self):
        """Ausgabepfad auswählen"""
        path = filedialog.askdirectory(title="Ausgabeordner auswählen")
        if path:
            self.output_path_var.set(path)
            
    def generate_presentation(self):
        """Präsentation generieren"""
        try:
            if not self.processed_trades:
                messagebox.showwarning("Keine Daten", "Bitte verarbeiten Sie zuerst Bilder.")
                return
                
            self.status_var.set("Generiere Präsentation...")
            
            # Output-Pfad vorbereiten
            output_path = self.output_path_var.get()
            os.makedirs(output_path, exist_ok=True)
            
            # Dateiname generieren
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trading_bot_presentation_{timestamp}"
            
            # Präsentation erstellen
            success = self.presentation_builder.create_presentation(
                trades_data=self.processed_trades,
                config=self.config,
                template=self.template_var.get(),
                output_path=os.path.join(output_path, filename),
                format=self.output_format.get()
            )
            
            if success:
                self.status_var.set("Präsentation erfolgreich erstellt!")
                messagebox.showinfo("Erfolg", 
                                   f"Präsentation wurde erfolgreich erstellt!\n"
                                   f"Pfad: {os.path.join(output_path, filename)}.{self.output_format.get()}")
            else:
                self.status_var.set("Fehler beim Erstellen der Präsentation")
                messagebox.showerror("Fehler", "Präsentation konnte nicht erstellt werden.")
                
        except Exception as e:
            self.logger.error(f"Error generating presentation: {e}")
            messagebox.showerror("Fehler", f"Fehler beim Generieren: {e}")
            
    def run(self):
        """Anwendung starten"""
        self.root.mainloop()

def main():
    """Hauptfunktion"""
    parser = argparse.ArgumentParser(description='Trading Bot Presentation Generator')
    parser.add_argument('--cli', action='store_true', help='CLI Mode starten')
    parser.add_argument('--config', help='Konfigurationsdatei')
    parser.add_argument('--signal-dir', help='Verzeichnis mit Signal-Screenshots')
    parser.add_argument('--result-dir', help='Verzeichnis mit Ergebnis-Screenshots')
    parser.add_argument('--output', help='Ausgabepfad')
    parser.add_argument('--template', default='crypto_professional', help='Template auswählen')
    
    args = parser.parse_args()
    
    if args.cli:
        # CLI Mode
        print("Trading Bot Presentation Generator - CLI Mode")
        print("=" * 50)
        
        if args.signal_dir and args.result_dir:
            run_cli_mode(args)
        else:
            print("Fehler: --signal-dir und --result-dir sind im CLI-Modus erforderlich")
            sys.exit(1)
    else:
        # GUI Mode
        app = TradingBotPresentationApp()
        app.run()

def run_cli_mode(args):
    """CLI Modus ausführen"""
    try:
        print("Initialisiere Module...")
        analyzer = ImageAnalyzer()
        builder = PresentationBuilder()
        
        # Bilder sammeln
        signal_images = []
        result_images = []
        
        if os.path.isdir(args.signal_dir):
            for ext in ['*.png', '*.jpg', '*.jpeg']:
                signal_images.extend(Path(args.signal_dir).glob(ext))
                
        if os.path.isdir(args.result_dir):
            for ext in ['*.png', '*.jpg', '*.jpeg']:
                result_images.extend(Path(args.result_dir).glob(ext))
                
        print(f"Gefunden: {len(signal_images)} Signal-Bilder, {len(result_images)} Ergebnis-Bilder")
        
        # Verarbeitung
        all_images = [(str(img), 'signal') for img in signal_images] + \
                    [(str(img), 'result') for img in result_images]
        
        processed_data = []
        for i, (img_path, img_type) in enumerate(all_images):
            print(f"Verarbeite ({i+1}/{len(all_images)}): {os.path.basename(img_path)}")
            analysis = analyzer.analyze_image(img_path)
            if analysis:
                processed_data.append({
                    'path': img_path,
                    'type': img_type,
                    'data': analysis
                })
                
        # Matching
        trades = analyzer.match_signals_to_results(processed_data)
        print(f"✓ {len(trades)} Trades erfolgreich gematched")
        
        # Konfiguration laden
        config = TradingBotPresentationApp().get_default_config()
        if args.config and os.path.exists(args.config):
            with open(args.config, 'r') as f:
                config.update(json.load(f))
                
        # Präsentation erstellen
        output_path = args.output or f"trading_bot_presentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        success = builder.create_presentation(
            trades_data=trades,
            config=config,
            template=args.template,
            output_path=output_path,
            format='pptx'
        )
        
        if success:
            print(f"✅ Präsentation erfolgreich erstellt: {output_path}.pptx")
        else:
            print("❌ Fehler beim Erstellen der Präsentation")
            
    except Exception as e:
        print(f"❌ Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()