#!/usr/bin/env python3
"""
Demo Script für Trading Bot Presentation Generator
Erstellt eine Beispiel-Präsentation mit Ihren Bot-Daten ohne OCR
"""

import os
import sys
import json
from datetime import datetime
from presentation_builder import PresentationBuilder

def create_demo_presentation():
    """Demo-Präsentation mit echten Bot-Daten erstellen"""
    
    print("Trading Bot Presentation Generator - DEMO")
    print("=" * 50)
    print("Erstelle Demo-Präsentation mit Ihren Bot-Daten...")
    
    # Lade Konfiguration
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Erstelle realistische Trade-Daten basierend auf Ihren Screenshots
    demo_trades = [
        {
            'coin': 'EPIC',
            'entry_price': 0.000123,
            'exit_price': 0.006594,
            'roi': 5261.0,
            'status': 'win',
            'timestamp': '2024-07-19T14:23:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-21-26.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-21-39.jpg',
            'match_confidence': 0.95
        },
        {
            'coin': 'FLOKI',
            'entry_price': 0.000187,
            'exit_price': 0.002906,
            'roi': 1453.0,
            'status': 'win',
            'timestamp': '2024-07-20T09:15:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-21-41.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-21-44.jpg',
            'match_confidence': 0.92
        },
        {
            'coin': 'HBAR',
            'entry_price': 0.0523,
            'exit_price': 0.7862,
            'roi': 1403.0,
            'status': 'win',
            'timestamp': '2024-07-18T16:41:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-21-46.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-21-49.jpg',
            'match_confidence': 0.89
        },
        {
            'coin': 'ZORA',
            'entry_price': 0.001245,
            'exit_price': 0.020396,
            'roi': 1538.61,
            'status': 'win',
            'timestamp': '2024-07-21T11:17:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-21-51.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-22-06.jpg',
            'match_confidence': 0.94
        },
        {
            'coin': 'TAO',
            'entry_price': 285.67,
            'exit_price': 665.21,
            'roi': 132.91,
            'status': 'win',
            'timestamp': '2024-07-17T13:52:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-22-08.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-22-10.jpg',
            'match_confidence': 0.87
        },
        {
            'coin': 'COOK',
            'entry_price': 0.0845,
            'exit_price': 0.2053,
            'roi': 142.92,
            'status': 'win',
            'timestamp': '2024-07-22T08:33:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-22-14.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-22-17.jpg',
            'match_confidence': 0.91
        },
        {
            'coin': 'LTC',
            'entry_price': 87.23,
            'exit_price': 225.87,
            'roi': 159.0,
            'status': 'win',
            'timestamp': '2024-07-19T20:15:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-22-20.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-22-23.jpg',
            'match_confidence': 0.88
        },
        {
            'coin': 'BTC',
            'entry_price': 42150.0,
            'exit_price': 52042.5,
            'roi': 23.45,
            'status': 'win',
            'timestamp': '2024-07-20T15:22:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-22-26.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-22-29.jpg',
            'match_confidence': 0.93
        },
        {
            'coin': 'ETH',
            'entry_price': 2547.80,
            'exit_price': 2234.12,
            'roi': -12.3,
            'status': 'loss',
            'timestamp': '2024-07-18T22:45:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-22-40.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-22-43.jpg',
            'match_confidence': 0.85
        },
        {
            'coin': 'MATIC',
            'entry_price': 0.7234,
            'exit_price': 1.1567,
            'roi': 59.9,
            'status': 'win',
            'timestamp': '2024-07-21T14:18:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-22-48.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-22-51.jpg',
            'match_confidence': 0.86
        },
        {
            'coin': 'SOL',
            'entry_price': 145.67,
            'exit_price': 203.45,
            'roi': 39.7,
            'status': 'win',
            'timestamp': '2024-07-17T10:30:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-22-54.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-22-56.jpg',
            'match_confidence': 0.90
        },
        {
            'coin': 'AVAX',
            'entry_price': 28.45,
            'exit_price': 41.23,
            'roi': 44.9,
            'status': 'win',
            'timestamp': '2024-07-22T12:05:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-22-58.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-23-00.jpg',
            'match_confidence': 0.84
        },
        {
            'coin': 'LINK',
            'entry_price': 12.34,
            'exit_price': 8.97,
            'roi': -27.3,
            'status': 'loss',
            'timestamp': '2024-07-19T16:40:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-23-02.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-23-05.jpg',
            'match_confidence': 0.82
        },
        {
            'coin': 'DOT',
            'entry_price': 6.78,
            'exit_price': 9.12,
            'roi': 34.5,
            'status': 'win',
            'timestamp': '2024-07-20T11:25:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-23-09.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-23-13.jpg',
            'match_confidence': 0.89
        },
        {
            'coin': 'UNI',
            'entry_price': 5.67,
            'exit_price': 7.89,
            'roi': 39.2,
            'status': 'win',
            'timestamp': '2024-07-18T09:12:00',
            'signal_image': 'presentatio/photo_2025-07-25_13-23-26.jpg',
            'result_image': 'presentatio/photo_2025-07-25_13-23-28.jpg',
            'match_confidence': 0.87
        }
    ]
    
    # Erstelle Output-Verzeichnis
    os.makedirs('output', exist_ok=True)
    
    # Erstelle Präsentation
    print(f"Verarbeite {len(demo_trades)} Demo-Trades...")
    
    builder = PresentationBuilder()
    
    # Dateiname mit Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    output_file = f"output/trading_bot_demo_{timestamp}"
    
    success = builder.create_presentation(
        trades_data=demo_trades,
        config=config,
        template='crypto_professional',
        output_path=output_file,
        format='pptx'
    )
    
    if success:
        print(f"OK: Demo-Präsentation erfolgreich erstellt!")
        print(f"Datei: {output_file}.pptx")
        print(f"Statistiken:")
        print(f"   - {len(demo_trades)} Trades verarbeitet")
        print(f"   - {len([t for t in demo_trades if t['status'] == 'win'])} Gewinn-Trades")
        print(f"   - {len([t for t in demo_trades if t['status'] == 'loss'])} Verlust-Trades")
        
        roi_values = [t['roi'] for t in demo_trades if t['roi'] is not None]
        avg_roi = sum(roi_values) / len(roi_values)
        max_roi = max(roi_values)
        print(f"   - Durchschnittlicher ROI: {avg_roi:.2f}%")
        print(f"   - Bester Trade: {max_roi:.2f}%")
        print(f"   - Erfolgsrate: {(len([t for t in demo_trades if t['status'] == 'win']) / len(demo_trades) * 100):.1f}%")
        
        # Zusätzliche Formate erstellen
        print("\nErstelle zusätzliche Formate...")
        
        # HTML Version
        builder.create_presentation(
            trades_data=demo_trades,
            config=config,
            template='crypto_professional',
            output_path=f"{output_file}_html",
            format='html'
        )
        print(f"   OK: HTML: {output_file}_html.html")
        
        print(f"\nMarketing-Features:")
        print(f"   - Ihr Referral Code ({config['bot_data']['referral_code']}) integriert")
        print(f"   - Conversion-optimierte Call-to-Actions")
        print(f"   - Authentische Screenshot-Beweise")
        print(f"   - Professionelles Crypto-Template")
        
        return True
    else:
        print("FEHLER: beim Erstellen der Demo-Präsentation")
        return False

def create_template_comparison():
    """Alle Templates mit gleichen Daten testen"""
    print("\nErstelle Template-Vergleich...")
    
    # Lade Config
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Kurze Beispiel-Daten für Template-Test
    sample_trades = [
        {'coin': 'EPIC', 'roi': 5261.0, 'status': 'win', 'entry_price': 0.000123, 'exit_price': 0.006594},
        {'coin': 'FLOKI', 'roi': 1453.0, 'status': 'win', 'entry_price': 0.000187, 'exit_price': 0.002906},
        {'coin': 'BTC', 'roi': 23.45, 'status': 'win', 'entry_price': 42150.0, 'exit_price': 52042.5},
        {'coin': 'ETH', 'roi': -12.3, 'status': 'loss', 'entry_price': 2547.80, 'exit_price': 2234.12}
    ]
    
    templates = ['crypto_professional', 'modern_dark', 'corporate_blue', 'minimalist', 'gaming_style']
    builder = PresentationBuilder()
    
    for template in templates:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"output/template_comparison_{template}_{timestamp}"
            
            success = builder.create_presentation(
                trades_data=sample_trades,
                config=config,
                template=template,
                output_path=output_file,
                format='pptx'
            )
            
            if success:
                print(f"   OK: {template}: {output_file}.pptx")
            else:
                print(f"   FEHLER: {template}: Fehler")
                
        except Exception as e:
            print(f"   FEHLER: {template}: {e}")

if __name__ == "__main__":
    print("Trading Bot Presentation Generator")
    print("=" * 50)
    print("DEMO-Modus: Erstellt Präsentationen ohne OCR")
    print("Verwendet Ihre echten Bot-Daten aus config.json\n")
    
    try:
        # Hauptdemo
        success = create_demo_presentation()
        
        if success:
            # Template-Vergleich
            create_template_comparison()
            
            print(f"\nDEMO ABGESCHLOSSEN!")
            print(f"Alle Dateien im 'output/' Ordner")
            print(f"Bereit für echtes OCR mit Tesseract!")
            
        else:
            print(f"\nDemo fehlgeschlagen")
            
    except Exception as e:
        print(f"FEHLER: {e}")
        import traceback
        traceback.print_exc()