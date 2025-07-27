#!/usr/bin/env python3
"""
Image Analyzer Module
OCR-basierte Analyse von Trading-Screenshots für automatische Datenextraktion

Features:
- OCR für Coin-Namen, Preise, ROI-Werte
- Intelligentes Matching zwischen Signal- und Ergebnis-Bildern
- Batch-Verarbeitung von Screenshots
- Konfidenz-basierte Filterung
"""

import os
import re
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from typing import Dict, List, Optional, Tuple, Any
import logging
from datetime import datetime
import json
from dataclasses import dataclass
from difflib import SequenceMatcher
import hashlib

@dataclass
class TradeData:
    """Datenklasse für Trade-Informationen"""
    coin: str = ""
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    roi: Optional[float] = None
    status: str = ""  # "win", "loss", "pending"
    timestamp: Optional[datetime] = None
    confidence: float = 0.0
    source_image: str = ""
    matched_image: Optional[str] = None

class ImageAnalyzer:
    """Hauptklasse für Bildanalyse und OCR"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or self._get_default_config()
        
        # OCR-Konfiguration
        self.ocr_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.%+-$'
        
        # Bekannte Coin-Namen für bessere Erkennung
        self.known_coins = self._load_known_coins()
        
        # Regex-Patterns für Datenextraktion
        self.patterns = {
            'coin': r'\b[A-Z]{2,8}\b',  # 2-8 Großbuchstaben
            'price': r'\$?\d+\.?\d*',   # Preise mit/ohne $
            'percentage': r'[+-]?\d+\.?\d*%',  # Prozentangaben
            'roi': r'[+-]?\d+\.?\d*%',
            'usdt': r'\d+\.?\d*\s*USDT'
        }
        
    def _get_default_config(self) -> Dict:
        """Standard-Konfiguration für Bildanalyse"""
        return {
            'ocr_confidence': 0.7,
            'auto_match_threshold': 0.8,
            'preprocessing': {
                'enhance_contrast': True,
                'denoise': True,
                'sharpen': True,
                'resize_factor': 2.0
            },
            'roi_detection': {
                'green_color_range': [(50, 100, 50), (80, 255, 255)],  # HSV
                'red_color_range': [(0, 100, 50), (10, 255, 255)]
            }
        }
        
    def _load_known_coins(self) -> List[str]:
        """Bekannte Coin-Namen laden"""
        default_coins = [
            'BTC', 'ETH', 'BNB', 'ADA', 'DOT', 'XRP', 'LINK', 'LTC', 'BCH',
            'UNI', 'THETA', 'XLM', 'VET', 'FIL', 'TRX', 'EOS', 'ATOM', 'NEO',
            'AVAX', 'LUNA', 'SOL', 'MATIC', 'ALGO', 'ICP', 'EGLD', 'RUNE',
            'EPIC', 'FLOKI', 'HBAR', 'COOK', 'TAO', 'ZORA', 'DOGE', 'SHIB'
        ]
        
        try:
            # Versuche, erweiterte Liste aus Datei zu laden
            with open('known_coins.json', 'r') as f:
                extended_coins = json.load(f)
                return list(set(default_coins + extended_coins))
        except FileNotFoundError:
            return default_coins
            
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Bildvorverarbeitung für bessere OCR-Ergebnisse"""
        try:
            # Bild laden
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Konnte Bild nicht laden: {image_path}")
                
            # In Graustufen konvertieren
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Konfiguration anwenden
            if self.config['preprocessing']['resize_factor'] != 1.0:
                height, width = gray.shape
                new_width = int(width * self.config['preprocessing']['resize_factor'])
                new_height = int(height * self.config['preprocessing']['resize_factor'])
                gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
                
            if self.config['preprocessing']['denoise']:
                gray = cv2.fastNlMeansDenoising(gray)
                
            if self.config['preprocessing']['enhance_contrast']:
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                gray = clahe.apply(gray)
                
            if self.config['preprocessing']['sharpen']:
                kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                gray = cv2.filter2D(gray, -1, kernel)
                
            # Binarisierung
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return binary
            
        except Exception as e:
            self.logger.error(f"Fehler bei Bildvorverarbeitung {image_path}: {e}")
            return None
            
    def extract_text_regions(self, image: np.ndarray) -> List[Dict]:
        """Textregionen extrahieren und analysieren"""
        try:
            # OCR mit Tesseract
            data = pytesseract.image_to_data(image, config=self.ocr_config, output_type=pytesseract.Output.DICT)
            
            regions = []
            n_boxes = len(data['level'])
            
            for i in range(n_boxes):
                confidence = int(data['conf'][i])
                if confidence > self.config['ocr_confidence'] * 100:
                    text = data['text'][i].strip()
                    if text:
                        regions.append({
                            'text': text,
                            'confidence': confidence / 100.0,
                            'bbox': (data['left'][i], data['top'][i], 
                                   data['width'][i], data['height'][i]),
                            'block_num': data['block_num'][i],
                            'par_num': data['par_num'][i],
                            'line_num': data['line_num'][i]
                        })
                        
            return regions
            
        except Exception as e:
            self.logger.error(f"Fehler bei Textextraktion: {e}")
            return []
            
    def detect_coin_name(self, text_regions: List[Dict]) -> Tuple[str, float]:
        """Coin-Namen aus Textregionen erkennen"""
        best_match = ""
        best_confidence = 0.0
        
        for region in text_regions:
            text = region['text'].upper()
            
            # Direkte Übereinstimmung mit bekannten Coins
            for coin in self.known_coins:
                if coin in text:
                    confidence = region['confidence']
                    if confidence > best_confidence:
                        best_match = coin
                        best_confidence = confidence
                        
            # Regex-basierte Erkennung
            matches = re.findall(self.patterns['coin'], text)
            for match in matches:
                if len(match) >= 2:  # Mindestens 2 Zeichen
                    # Ähnlichkeit zu bekannten Coins prüfen
                    for coin in self.known_coins:
                        similarity = SequenceMatcher(None, match, coin).ratio()
                        if similarity > 0.8:  # 80% Ähnlichkeit
                            confidence = region['confidence'] * similarity
                            if confidence > best_confidence:
                                best_match = coin
                                best_confidence = confidence
                                
        return best_match, best_confidence
        
    def detect_prices(self, text_regions: List[Dict]) -> List[Tuple[float, float]]:
        """Preise aus Text extrahieren"""
        prices = []
        
        for region in text_regions:
            text = region['text']
            matches = re.findall(self.patterns['price'], text)
            
            for match in matches:
                try:
                    # $ entfernen falls vorhanden
                    price_str = match.replace('$', '').strip()
                    price = float(price_str)
                    
                    # Plausibilitätsprüfung
                    if 0.000001 <= price <= 1000000:  # Realistischer Preisbereich
                        prices.append((price, region['confidence']))
                except ValueError:
                    continue
                    
        return prices
        
    def detect_roi(self, text_regions: List[Dict], image: np.ndarray) -> Tuple[Optional[float], str]:
        """ROI (Return on Investment) erkennen"""
        roi_values = []
        
        # Text-basierte ROI-Erkennung
        for region in text_regions:
            text = region['text']
            matches = re.findall(self.patterns['percentage'], text)
            
            for match in matches:
                try:
                    roi_str = match.replace('%', '').replace('+', '').strip()
                    roi = float(roi_str)
                    
                    # Plausibilitätsprüfung für ROI
                    if -100 <= roi <= 10000:  # -100% bis +10000%
                        roi_values.append((roi, region['confidence'], region['bbox']))
                except ValueError:
                    continue
                    
        # Farb-basierte Gewinn/Verlust-Erkennung
        color_status = self._detect_color_status(image)
        
        if roi_values:
            # Besten ROI-Wert auswählen (höchste Konfidenz)
            best_roi = max(roi_values, key=lambda x: x[1])
            return best_roi[0], color_status
        else:
            return None, color_status
            
    def _detect_color_status(self, image: np.ndarray) -> str:
        """Status anhand von Farben erkennen (Grün=Gewinn, Rot=Verlust)"""
        try:
            # BGR zu HSV konvertieren
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Grüne und rote Bereiche definieren
            green_lower = np.array(self.config['roi_detection']['green_color_range'][0])
            green_upper = np.array(self.config['roi_detection']['green_color_range'][1])
            red_lower = np.array(self.config['roi_detection']['red_color_range'][0])
            red_upper = np.array(self.config['roi_detection']['red_color_range'][1])
            
            # Masken erstellen
            green_mask = cv2.inRange(hsv, green_lower, green_upper)
            red_mask = cv2.inRange(hsv, red_lower, red_upper)
            
            # Pixel zählen
            green_pixels = cv2.countNonZero(green_mask)
            red_pixels = cv2.countNonZero(red_mask)
            
            if green_pixels > red_pixels * 1.5:  # Deutlich mehr grün
                return "win"
            elif red_pixels > green_pixels * 1.5:  # Deutlich mehr rot
                return "loss"
            else:
                return "neutral"
                
        except Exception as e:
            self.logger.error(f"Fehler bei Farberkennung: {e}")
            return "unknown"
            
    def analyze_image(self, image_path: str) -> Optional[Dict]:
        """Einzelnes Bild analysieren und Daten extrahieren"""
        try:
            self.logger.info(f"Analysiere Bild: {image_path}")
            
            # Bildvorverarbeitung
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                return None
                
            # Textregionen extrahieren
            text_regions = self.extract_text_regions(processed_image)
            if not text_regions:
                self.logger.warning(f"Keine Textregionen in {image_path} gefunden")
                return None
                
            # Coin-Namen erkennen
            coin, coin_confidence = self.detect_coin_name(text_regions)
            
            # Preise erkennen
            prices = self.detect_prices(text_regions)
            
            # ROI erkennen
            roi, status = self.detect_roi(text_regions, cv2.imread(image_path))
            
            # Ergebnis zusammenstellen
            result = {
                'coin': coin,
                'coin_confidence': coin_confidence,
                'prices': prices,
                'roi': roi,
                'status': status,
                'text_regions': len(text_regions),
                'source_image': image_path,
                'timestamp': datetime.now().isoformat(),
                'image_hash': self._calculate_image_hash(image_path)
            }
            
            # Zusätzliche Datenverarbeitung
            if prices:
                result['entry_price'] = prices[0][0]  # Erster erkannter Preis
                if len(prices) > 1:
                    result['exit_price'] = prices[1][0]  # Zweiter Preis falls vorhanden
                    
            # Vertrauen berechnen
            confidence_factors = [coin_confidence]
            if prices:
                confidence_factors.extend([p[1] for p in prices])
            result['overall_confidence'] = sum(confidence_factors) / len(confidence_factors)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Fehler bei Bildanalyse {image_path}: {e}")
            return None
            
    def _calculate_image_hash(self, image_path: str) -> str:
        """Bild-Hash für Duplikatserkennung berechnen"""
        try:
            with open(image_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
            
    def match_signals_to_results(self, processed_data: List[Dict]) -> List[Dict]:
        """Signal-Bilder mit Ergebnis-Bildern matchen"""
        try:
            # Daten nach Typ trennen
            signals = [d for d in processed_data if d['type'] == 'signal']
            results = [d for d in processed_data if d['type'] == 'result']
            
            matched_trades = []
            used_results = set()
            
            self.logger.info(f"Matching {len(signals)} Signale mit {len(results)} Ergebnissen")
            
            for signal in signals:
                signal_data = signal['data']
                if not signal_data or not signal_data.get('coin'):
                    continue
                    
                best_match = None
                best_score = 0
                
                for i, result in enumerate(results):
                    if i in used_results:
                        continue
                        
                    result_data = result['data']
                    if not result_data:
                        continue
                        
                    # Matching-Score berechnen
                    score = self._calculate_match_score(signal_data, result_data)
                    
                    if score > best_score and score >= self.config['auto_match_threshold']:
                        best_match = i
                        best_score = score
                        
                if best_match is not None:
                    # Match gefunden
                    result_data = results[best_match]['data']
                    
                    trade = {
                        'coin': signal_data['coin'],
                        'entry_price': signal_data.get('entry_price'),
                        'exit_price': result_data.get('exit_price'),
                        'roi': result_data.get('roi', signal_data.get('roi')),
                        'status': result_data.get('status', 'unknown'),
                        'signal_image': signal['path'],
                        'result_image': results[best_match]['path'],
                        'match_confidence': best_score,
                        'timestamp': signal_data.get('timestamp')
                    }
                    
                    matched_trades.append(trade)
                    used_results.add(best_match)
                    
                    self.logger.info(f"Match gefunden: {trade['coin']} (Score: {best_score:.2f})")
                else:
                    # Kein Match - Signal allein verwenden
                    trade = {
                        'coin': signal_data['coin'],
                        'entry_price': signal_data.get('entry_price'),
                        'roi': signal_data.get('roi'),
                        'status': signal_data.get('status', 'pending'),
                        'signal_image': signal['path'],
                        'result_image': None,
                        'match_confidence': 0.0,
                        'timestamp': signal_data.get('timestamp')
                    }
                    matched_trades.append(trade)
                    
            # Ungematchte Ergebnisse hinzufügen
            for i, result in enumerate(results):
                if i not in used_results:
                    result_data = result['data']
                    if result_data and result_data.get('coin'):
                        trade = {
                            'coin': result_data['coin'],
                            'exit_price': result_data.get('exit_price'),
                            'roi': result_data.get('roi'),
                            'status': result_data.get('status', 'unknown'),
                            'signal_image': None,
                            'result_image': result['path'],
                            'match_confidence': 0.0,
                            'timestamp': result_data.get('timestamp')
                        }
                        matched_trades.append(trade)
                        
            # Nach ROI sortieren (höchste zuerst)
            matched_trades.sort(key=lambda x: x.get('roi', 0), reverse=True)
            
            self.logger.info(f"Insgesamt {len(matched_trades)} Trades erstellt")
            return matched_trades
            
        except Exception as e:
            self.logger.error(f"Fehler beim Matching: {e}")
            return []
            
    def _calculate_match_score(self, signal_data: Dict, result_data: Dict) -> float:
        """Matching-Score zwischen Signal und Ergebnis berechnen"""
        score = 0.0
        max_score = 0.0
        
        # Coin-Name Übereinstimmung (wichtigster Faktor)
        if signal_data.get('coin') and result_data.get('coin'):
            max_score += 0.6
            if signal_data['coin'] == result_data['coin']:
                score += 0.6
            else:
                # Ähnlichkeit prüfen
                similarity = SequenceMatcher(None, signal_data['coin'], result_data['coin']).ratio()
                score += 0.6 * similarity * 0.5  # Reduzierter Score für ähnliche Namen
                
        # Timestamp-Nähe (falls verfügbar)
        signal_time = signal_data.get('timestamp')
        result_time = result_data.get('timestamp')
        if signal_time and result_time:
            max_score += 0.2
            try:
                signal_dt = datetime.fromisoformat(signal_time)
                result_dt = datetime.fromisoformat(result_time)
                time_diff = abs((result_dt - signal_dt).total_seconds())
                
                # Score basierend auf Zeitdifferenz (weniger als 1 Stunde = voller Score)
                if time_diff <= 3600:  # 1 Stunde
                    score += 0.2
                elif time_diff <= 86400:  # 1 Tag
                    score += 0.2 * (1 - time_diff / 86400)
            except Exception:
                pass
                
        # Preis-Konsistenz
        signal_price = signal_data.get('entry_price')
        result_price = result_data.get('entry_price') or result_data.get('exit_price')
        if signal_price and result_price:
            max_score += 0.2
            price_ratio = min(signal_price, result_price) / max(signal_price, result_price)
            if price_ratio > 0.8:  # Preise sind ähnlich
                score += 0.2 * price_ratio
                
        # Normalisierung
        if max_score > 0:
            return score / max_score
        else:
            return 0.0
            
    def batch_analyze(self, image_paths: List[str], 
                     progress_callback: Optional[callable] = None) -> List[Dict]:
        """Batch-Verarbeitung mehrerer Bilder"""
        results = []
        total = len(image_paths)
        
        for i, image_path in enumerate(image_paths):
            try:
                result = self.analyze_image(image_path)
                if result:
                    results.append({
                        'path': image_path,
                        'data': result,
                        'index': i
                    })
                    
                if progress_callback:
                    progress_callback(i + 1, total)
                    
            except Exception as e:
                self.logger.error(f"Fehler bei Batch-Analyse {image_path}: {e}")
                continue
                
        return results
        
    def export_analysis_report(self, trades: List[Dict], output_path: str):
        """Analyse-Bericht als JSON exportieren"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_trades': len(trades),
                'summary': {
                    'total_trades': len(trades),
                    'winning_trades': len([t for t in trades if t.get('status') == 'win']),
                    'losing_trades': len([t for t in trades if t.get('status') == 'loss']),
                    'pending_trades': len([t for t in trades if t.get('status') == 'pending']),
                    'avg_roi': sum([t.get('roi', 0) for t in trades]) / len(trades) if trades else 0
                },
                'trades': trades,
                'config': self.config
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Analyse-Bericht exportiert: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Fehler beim Exportieren des Berichts: {e}")

# Hilfsfunktionen für erweiterte Bildverarbeitung
class AdvancedImageProcessor:
    """Erweiterte Bildverarbeitungstools"""
    
    @staticmethod
    def remove_noise(image: np.ndarray) -> np.ndarray:
        """Rauschen entfernen"""
        return cv2.medianBlur(image, 5)
        
    @staticmethod
    def enhance_text_regions(image: np.ndarray) -> np.ndarray:
        """Textregionen hervorheben"""
        # Morphologische Operationen für Textverbesserung
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        enhanced = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        return enhanced
        
    @staticmethod
    def detect_tables(image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Tabellen in Bildern erkennen"""
        # Horizontale und vertikale Linien erkennen
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
        
        horizontal_lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, horizontal_kernel)
        vertical_lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, vertical_kernel)
        
        # Schnittpunkte finden (vereinfacht)
        table_structure = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0.0)
        
        # Konturen finden
        contours, _ = cv2.findContours(table_structure, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        tables = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 100 and h > 50:  # Mindestgröße für Tabellen
                tables.append((x, y, w, h))
                
        return tables

if __name__ == "__main__":
    # Test-Code
    import sys
    
    if len(sys.argv) > 1:
        analyzer = ImageAnalyzer()
        result = analyzer.analyze_image(sys.argv[1])
        
        if result:
            print("=== ANALYSE-ERGEBNIS ===")
            print(f"Coin: {result.get('coin', 'Nicht erkannt')}")
            print(f"ROI: {result.get('roi', 'N/A')}%")
            print(f"Status: {result.get('status', 'Unbekannt')}")
            print(f"Konfidenz: {result.get('overall_confidence', 0):.2f}")
            print(f"Textregionen: {result.get('text_regions', 0)}")
        else:
            print("Keine Daten erkannt")
    else:
        print("Usage: python image_analyzer.py <image_path>")