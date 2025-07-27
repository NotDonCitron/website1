#!/usr/bin/env python3
"""
Template Manager Module
Verwaltung verschiedener Design-Vorlagen für Trading-Bot Präsentationen

Features:
- Verschiedene professionelle Templates
- Anpassbare Farb-Schemata
- Layout-Konfiguration
- Animation-Presets
- Corporate Design Optionen
"""

import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

class TemplateType(Enum):
    """Verfügbare Template-Typen"""
    CRYPTO_PROFESSIONAL = "crypto_professional"
    MODERN_DARK = "modern_dark"
    CORPORATE_BLUE = "corporate_blue"
    MINIMALIST = "minimalist"
    GAMING_STYLE = "gaming_style"

@dataclass
class ColorScheme:
    """Farbschema für Templates"""
    primary: RGBColor
    secondary: RGBColor
    accent: RGBColor
    success: RGBColor
    danger: RGBColor
    warning: RGBColor
    text: RGBColor
    text_secondary: RGBColor
    background: RGBColor
    background_secondary: RGBColor

@dataclass
class FontConfig:
    """Font-Konfiguration"""
    title_font: str = "Arial Black"
    heading_font: str = "Arial"
    body_font: str = "Arial"
    code_font: str = "Consolas"
    title_size: int = 44
    heading_size: int = 32
    body_size: int = 18
    caption_size: int = 14

@dataclass
class LayoutConfig:
    """Layout-Konfiguration"""
    margins: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)  # top, right, bottom, left
    content_width: float = 8.5
    content_height: float = 6.0
    image_max_width: float = 6.0
    image_max_height: float = 4.0
    chart_width: float = 8.0
    chart_height: float = 4.5

@dataclass
class AnimationConfig:
    """Animation-Konfiguration"""
    slide_transition: str = "fade"
    element_entrance: str = "fly_in_from_right"
    element_emphasis: str = "pulse"
    duration: float = 0.75
    auto_advance: bool = False

@dataclass
class TemplateConfig:
    """Vollständige Template-Konfiguration"""
    name: str
    description: str
    color_scheme: ColorScheme
    font_config: FontConfig
    layout_config: LayoutConfig
    animation_config: AnimationConfig
    slide_layouts: Dict[str, str] = field(default_factory=dict)
    custom_elements: Dict[str, Any] = field(default_factory=dict)

class TemplateManager:
    """Hauptklasse für Template-Verwaltung"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.templates = {}
        self._load_default_templates()
        
    def _load_default_templates(self):
        """Standard-Templates laden"""
        
        # Crypto Professional Template
        self.templates[TemplateType.CRYPTO_PROFESSIONAL.value] = TemplateConfig(
            name="Crypto Professional",
            description="Professionelles Design für Kryptowährungs-Trading",
            color_scheme=ColorScheme(
                primary=RGBColor(26, 35, 126),          # Dunkelblau
                secondary=RGBColor(63, 81, 181),         # Blau
                accent=RGBColor(255, 193, 7),            # Gold
                success=RGBColor(76, 175, 80),           # Grün
                danger=RGBColor(244, 67, 54),            # Rot
                warning=RGBColor(255, 152, 0),           # Orange
                text=RGBColor(33, 33, 33),               # Dunkelgrau
                text_secondary=RGBColor(117, 117, 117),  # Grau
                background=RGBColor(248, 249, 250),      # Hellgrau
                background_secondary=RGBColor(255, 255, 255)  # Weiß
            ),
            font_config=FontConfig(
                title_font="Montserrat Black",
                heading_font="Montserrat Bold",
                body_font="Open Sans",
                title_size=48,
                heading_size=36,
                body_size=20
            ),
            layout_config=LayoutConfig(
                margins=(0.8, 0.8, 0.8, 0.8),
                content_width=8.7,
                content_height=6.2
            ),
            animation_config=AnimationConfig(
                slide_transition="push",
                element_entrance="fly_in_from_bottom",
                duration=0.5
            ),
            slide_layouts={
                "title": "professional_title",
                "content": "professional_content",
                "comparison": "professional_comparison",
                "chart": "professional_chart"
            }
        )
        
        # Modern Dark Template
        self.templates[TemplateType.MODERN_DARK.value] = TemplateConfig(
            name="Modern Dark",
            description="Modernes dunkles Design für Tech-affine Zielgruppen",
            color_scheme=ColorScheme(
                primary=RGBColor(18, 18, 18),            # Schwarz
                secondary=RGBColor(45, 45, 45),          # Dunkelgrau
                accent=RGBColor(0, 230, 118),            # Neongrün
                success=RGBColor(0, 200, 83),            # Grün
                danger=RGBColor(255, 82, 82),            # Neonrot
                warning=RGBColor(255, 183, 77),          # Gelb
                text=RGBColor(255, 255, 255),            # Weiß
                text_secondary=RGBColor(180, 180, 180),  # Hellgrau
                background=RGBColor(30, 30, 30),         # Dunkelgrau
                background_secondary=RGBColor(40, 40, 40)  # Grau
            ),
            font_config=FontConfig(
                title_font="Roboto Black",
                heading_font="Roboto Bold",
                body_font="Roboto",
                code_font="JetBrains Mono",
                title_size=46,
                heading_size=34,
                body_size=19
            ),
            layout_config=LayoutConfig(
                margins=(1.0, 1.0, 1.0, 1.0),
                content_width=8.5,
                content_height=6.0
            ),
            animation_config=AnimationConfig(
                slide_transition="fade",
                element_entrance="appear",
                duration=0.3
            )
        )
        
        # Corporate Blue Template
        self.templates[TemplateType.CORPORATE_BLUE.value] = TemplateConfig(
            name="Corporate Blue",
            description="Klassisches Corporate Design für Business-Präsentationen",
            color_scheme=ColorScheme(
                primary=RGBColor(0, 77, 153),            # Corporate Blau
                secondary=RGBColor(0, 102, 204),         # Hellblau
                accent=RGBColor(255, 140, 0),            # Orange
                success=RGBColor(34, 139, 34),           # Grün
                danger=RGBColor(220, 20, 60),            # Rot
                warning=RGBColor(255, 165, 0),           # Orange
                text=RGBColor(51, 51, 51),               # Grau
                text_secondary=RGBColor(102, 102, 102),  # Hellgrau
                background=RGBColor(255, 255, 255),      # Weiß
                background_secondary=RGBColor(245, 245, 245)  # Hellgrau
            ),
            font_config=FontConfig(
                title_font="Calibri Bold",
                heading_font="Calibri",
                body_font="Calibri",
                title_size=42,
                heading_size=30,
                body_size=18
            ),
            layout_config=LayoutConfig(
                margins=(1.2, 1.2, 1.2, 1.2),
                content_width=8.1,
                content_height=5.6
            ),
            animation_config=AnimationConfig(
                slide_transition="wipe",
                element_entrance="fly_in_from_left",
                duration=0.6
            )
        )
        
        # Minimalist Template
        self.templates[TemplateType.MINIMALIST.value] = TemplateConfig(
            name="Minimalist",
            description="Cleanes, minimalistisches Design mit Fokus auf Inhalte",
            color_scheme=ColorScheme(
                primary=RGBColor(60, 60, 60),            # Dunkelgrau
                secondary=RGBColor(120, 120, 120),       # Grau
                accent=RGBColor(100, 149, 237),          # Cornflower Blue
                success=RGBColor(60, 179, 113),          # Medium Sea Green
                danger=RGBColor(205, 92, 92),            # Indian Red
                warning=RGBColor(238, 130, 238),         # Violet
                text=RGBColor(40, 40, 40),               # Dunkelgrau
                text_secondary=RGBColor(100, 100, 100),  # Grau
                background=RGBColor(255, 255, 255),      # Weiß
                background_secondary=RGBColor(250, 250, 250)  # Off-White
            ),
            font_config=FontConfig(
                title_font="Helvetica Neue Light",
                heading_font="Helvetica Neue",
                body_font="Helvetica Neue",
                title_size=40,
                heading_size=28,
                body_size=16
            ),
            layout_config=LayoutConfig(
                margins=(1.5, 1.5, 1.5, 1.5),
                content_width=7.5,
                content_height=5.0
            ),
            animation_config=AnimationConfig(
                slide_transition="none",
                element_entrance="fade",
                duration=0.4
            )
        )
        
        # Gaming Style Template
        self.templates[TemplateType.GAMING_STYLE.value] = TemplateConfig(
            name="Gaming Style",
            description="Gaming-inspiriertes Design für jüngere Zielgruppen",
            color_scheme=ColorScheme(
                primary=RGBColor(138, 43, 226),          # Blue Violet
                secondary=RGBColor(75, 0, 130),          # Indigo
                accent=RGBColor(255, 20, 147),           # Deep Pink
                success=RGBColor(50, 205, 50),           # Lime Green
                danger=RGBColor(255, 69, 0),             # Red Orange
                warning=RGBColor(255, 215, 0),           # Gold
                text=RGBColor(255, 255, 255),            # Weiß
                text_secondary=RGBColor(200, 200, 200),  # Hellgrau
                background=RGBColor(25, 25, 25),         # Sehr Dunkelgrau
                background_secondary=RGBColor(35, 35, 35)  # Dunkelgrau
            ),
            font_config=FontConfig(
                title_font="Impact",
                heading_font="Arial Black",
                body_font="Arial",
                code_font="Courier New",
                title_size=50,
                heading_size=38,
                body_size=22
            ),
            layout_config=LayoutConfig(
                margins=(0.7, 0.7, 0.7, 0.7),
                content_width=8.8,
                content_height=6.6
            ),
            animation_config=AnimationConfig(
                slide_transition="split",
                element_entrance="bounce",
                duration=0.8
            )
        )
        
        self.logger.info(f"Loaded {len(self.templates)} templates")
        
    def get_template(self, template_name: str) -> Optional[TemplateConfig]:
        """Template nach Namen abrufen"""
        return self.templates.get(template_name)
        
    def get_available_templates(self) -> List[str]:
        """Liste verfügbarer Templates"""
        return list(self.templates.keys())
        
    def get_template_info(self) -> Dict[str, Dict[str, str]]:
        """Informationen über alle Templates"""
        info = {}
        for name, template in self.templates.items():
            info[name] = {
                'name': template.name,
                'description': template.description,
                'primary_color': f"#{template.color_scheme.primary.rgb:06x}",
                'accent_color': f"#{template.color_scheme.accent.rgb:06x}",
                'font_family': template.font_config.title_font
            }
        return info
        
    def create_custom_template(self, name: str, base_template: str = "crypto_professional", 
                             modifications: Dict = None) -> bool:
        """Benutzerdefiniertes Template erstellen"""
        try:
            if base_template not in self.templates:
                self.logger.error(f"Base template '{base_template}' not found")
                return False
                
            # Basis-Template kopieren
            base = self.templates[base_template]
            custom_template = TemplateConfig(
                name=name,
                description=f"Custom template based on {base.name}",
                color_scheme=base.color_scheme,
                font_config=base.font_config,
                layout_config=base.layout_config,
                animation_config=base.animation_config,
                slide_layouts=base.slide_layouts.copy(),
                custom_elements=base.custom_elements.copy()
            )
            
            # Modifikationen anwenden
            if modifications:
                self._apply_template_modifications(custom_template, modifications)
                
            # Custom Template speichern
            self.templates[name] = custom_template
            
            self.logger.info(f"Created custom template: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating custom template: {e}")
            return False
            
    def _apply_template_modifications(self, template: TemplateConfig, modifications: Dict):
        """Modifikationen auf Template anwenden"""
        
        # Farb-Modifikationen
        if 'colors' in modifications:
            color_mods = modifications['colors']
            for color_name, color_value in color_mods.items():
                if hasattr(template.color_scheme, color_name):
                    if isinstance(color_value, str):
                        # Hex-String zu RGBColor konvertieren
                        rgb_color = self._hex_to_rgb_color(color_value)
                        setattr(template.color_scheme, color_name, rgb_color)
                    elif isinstance(color_value, (list, tuple)) and len(color_value) == 3:
                        # RGB-Tupel zu RGBColor konvertieren
                        setattr(template.color_scheme, color_name, RGBColor(*color_value))
                        
        # Font-Modifikationen
        if 'fonts' in modifications:
            font_mods = modifications['fonts']
            for font_attr, font_value in font_mods.items():
                if hasattr(template.font_config, font_attr):
                    setattr(template.font_config, font_attr, font_value)
                    
        # Layout-Modifikationen
        if 'layout' in modifications:
            layout_mods = modifications['layout']
            for layout_attr, layout_value in layout_mods.items():
                if hasattr(template.layout_config, layout_attr):
                    setattr(template.layout_config, layout_attr, layout_value)
                    
        # Animation-Modifikationen
        if 'animations' in modifications:
            anim_mods = modifications['animations']
            for anim_attr, anim_value in anim_mods.items():
                if hasattr(template.animation_config, anim_attr):
                    setattr(template.animation_config, anim_attr, anim_value)
                    
    def _hex_to_rgb_color(self, hex_color: str) -> RGBColor:
        """Hex-String zu RGBColor konvertieren"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return RGBColor(r, g, b)
        else:
            raise ValueError(f"Invalid hex color: {hex_color}")
            
    def export_template(self, template_name: str, output_path: str) -> bool:
        """Template als JSON exportieren"""
        try:
            if template_name not in self.templates:
                self.logger.error(f"Template '{template_name}' not found")
                return False
                
            template = self.templates[template_name]
            
            # Template zu serialisierbarem Dict konvertieren
            template_dict = self._template_to_dict(template)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(template_dict, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Template exported to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting template: {e}")
            return False
            
    def import_template(self, template_path: str, template_name: str = None) -> bool:
        """Template aus JSON importieren"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_dict = json.load(f)
                
            # Dict zu TemplateConfig konvertieren
            template = self._dict_to_template(template_dict)
            
            if template_name:
                template.name = template_name
                
            # Template speichern
            self.templates[template.name.lower().replace(' ', '_')] = template
            
            self.logger.info(f"Template imported: {template.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error importing template: {e}")
            return False
            
    def _template_to_dict(self, template: TemplateConfig) -> Dict:
        """TemplateConfig zu Dict konvertieren"""
        return {
            'name': template.name,
            'description': template.description,
            'color_scheme': {
                'primary': self._rgb_color_to_hex(template.color_scheme.primary),
                'secondary': self._rgb_color_to_hex(template.color_scheme.secondary),
                'accent': self._rgb_color_to_hex(template.color_scheme.accent),
                'success': self._rgb_color_to_hex(template.color_scheme.success),
                'danger': self._rgb_color_to_hex(template.color_scheme.danger),
                'warning': self._rgb_color_to_hex(template.color_scheme.warning),
                'text': self._rgb_color_to_hex(template.color_scheme.text),
                'text_secondary': self._rgb_color_to_hex(template.color_scheme.text_secondary),
                'background': self._rgb_color_to_hex(template.color_scheme.background),
                'background_secondary': self._rgb_color_to_hex(template.color_scheme.background_secondary)
            },
            'font_config': {
                'title_font': template.font_config.title_font,
                'heading_font': template.font_config.heading_font,
                'body_font': template.font_config.body_font,
                'code_font': template.font_config.code_font,
                'title_size': template.font_config.title_size,
                'heading_size': template.font_config.heading_size,
                'body_size': template.font_config.body_size,
                'caption_size': template.font_config.caption_size
            },
            'layout_config': {
                'margins': template.layout_config.margins,
                'content_width': template.layout_config.content_width,
                'content_height': template.layout_config.content_height,
                'image_max_width': template.layout_config.image_max_width,
                'image_max_height': template.layout_config.image_max_height,
                'chart_width': template.layout_config.chart_width,
                'chart_height': template.layout_config.chart_height
            },
            'animation_config': {
                'slide_transition': template.animation_config.slide_transition,
                'element_entrance': template.animation_config.element_entrance,
                'element_emphasis': template.animation_config.element_emphasis,
                'duration': template.animation_config.duration,
                'auto_advance': template.animation_config.auto_advance
            },
            'slide_layouts': template.slide_layouts,
            'custom_elements': template.custom_elements
        }
        
    def _dict_to_template(self, template_dict: Dict) -> TemplateConfig:
        """Dict zu TemplateConfig konvertieren"""
        
        # ColorScheme erstellen
        color_data = template_dict['color_scheme']
        color_scheme = ColorScheme(
            primary=self._hex_to_rgb_color(color_data['primary']),
            secondary=self._hex_to_rgb_color(color_data['secondary']),
            accent=self._hex_to_rgb_color(color_data['accent']),
            success=self._hex_to_rgb_color(color_data['success']),
            danger=self._hex_to_rgb_color(color_data['danger']),
            warning=self._hex_to_rgb_color(color_data['warning']),
            text=self._hex_to_rgb_color(color_data['text']),
            text_secondary=self._hex_to_rgb_color(color_data['text_secondary']),
            background=self._hex_to_rgb_color(color_data['background']),
            background_secondary=self._hex_to_rgb_color(color_data['background_secondary'])
        )
        
        # FontConfig erstellen
        font_data = template_dict['font_config']
        font_config = FontConfig(**font_data)
        
        # LayoutConfig erstellen
        layout_data = template_dict['layout_config']
        layout_config = LayoutConfig(**layout_data)
        
        # AnimationConfig erstellen
        anim_data = template_dict['animation_config']
        animation_config = AnimationConfig(**anim_data)
        
        return TemplateConfig(
            name=template_dict['name'],
            description=template_dict['description'],
            color_scheme=color_scheme,
            font_config=font_config,
            layout_config=layout_config,
            animation_config=animation_config,
            slide_layouts=template_dict.get('slide_layouts', {}),
            custom_elements=template_dict.get('custom_elements', {})
        )
        
    def _rgb_color_to_hex(self, rgb_color: RGBColor) -> str:
        """RGBColor zu Hex-String konvertieren"""
        return f"#{rgb_color.rgb:06x}"
        
    def get_marketing_templates(self) -> Dict[str, TemplateConfig]:
        """Spezielle Marketing-Templates"""
        marketing_templates = {}
        
        # High-Impact Template für Conversion-Optimierung
        marketing_templates['high_impact'] = TemplateConfig(
            name="High Impact Marketing",
            description="Conversion-optimiertes Design für maximale Wirkung",
            color_scheme=ColorScheme(
                primary=RGBColor(220, 20, 60),           # Crimson
                secondary=RGBColor(255, 69, 0),          # Red Orange
                accent=RGBColor(255, 215, 0),            # Gold
                success=RGBColor(50, 205, 50),           # Lime Green
                danger=RGBColor(178, 34, 34),            # Fire Brick
                warning=RGBColor(255, 140, 0),           # Dark Orange
                text=RGBColor(0, 0, 0),                  # Schwarz
                text_secondary=RGBColor(64, 64, 64),     # Dunkelgrau
                background=RGBColor(255, 255, 255),      # Weiß
                background_secondary=RGBColor(255, 250, 240)  # Floral White
            ),
            font_config=FontConfig(
                title_font="Impact",
                heading_font="Arial Black",
                body_font="Arial",
                title_size=52,
                heading_size=40,
                body_size=24
            ),
            layout_config=LayoutConfig(
                margins=(0.5, 0.5, 0.5, 0.5),
                content_width=9.0,
                content_height=6.5
            ),
            animation_config=AnimationConfig(
                slide_transition="push",
                element_entrance="zoom",
                duration=0.6
            )
        )
        
        # Trust Builder Template
        marketing_templates['trust_builder'] = TemplateConfig(
            name="Trust Builder",
            description="Vertrauensvolles Design für seriöse Präsentationen",
            color_scheme=ColorScheme(
                primary=RGBColor(25, 25, 112),           # Midnight Blue
                secondary=RGBColor(70, 130, 180),        # Steel Blue
                accent=RGBColor(184, 134, 11),           # Dark Goldenrod
                success=RGBColor(34, 139, 34),           # Forest Green
                danger=RGBColor(165, 42, 42),            # Brown
                warning=RGBColor(255, 165, 0),           # Orange
                text=RGBColor(47, 79, 79),               # Dark Slate Gray
                text_secondary=RGBColor(105, 105, 105),  # Dim Gray
                background=RGBColor(248, 248, 255),      # Ghost White
                background_secondary=RGBColor(240, 248, 255)  # Alice Blue
            ),
            font_config=FontConfig(
                title_font="Times New Roman Bold",
                heading_font="Times New Roman",
                body_font="Georgia",
                title_size=44,
                heading_size=32,
                body_size=18
            ),
            layout_config=LayoutConfig(
                margins=(1.2, 1.2, 1.2, 1.2),
                content_width=8.1,
                content_height=5.6
            ),
            animation_config=AnimationConfig(
                slide_transition="fade",
                element_entrance="appear",
                duration=0.5
            )
        )
        
        return marketing_templates
        
    def customize_for_brand(self, template_name: str, brand_colors: Dict[str, str], 
                          brand_fonts: Dict[str, str] = None, 
                          logo_path: str = None) -> str:
        """Template für spezifische Marke anpassen"""
        try:
            if template_name not in self.templates:
                self.logger.error(f"Template '{template_name}' not found")
                return ""
                
            # Neuen Template-Namen generieren
            custom_name = f"{template_name}_branded"
            
            # Modifikationen zusammenstellen
            modifications = {}
            
            if brand_colors:
                modifications['colors'] = brand_colors
                
            if brand_fonts:
                modifications['fonts'] = brand_fonts
                
            # Custom Template erstellen
            success = self.create_custom_template(custom_name, template_name, modifications)
            
            if success and logo_path:
                # Logo-Information zu Custom Elements hinzufügen
                self.templates[custom_name].custom_elements['brand_logo'] = logo_path
                
            return custom_name if success else ""
            
        except Exception as e:
            self.logger.error(f"Error customizing template for brand: {e}")
            return ""
            
    def generate_template_preview(self, template_name: str, output_path: str) -> bool:
        """Template-Vorschau generieren"""
        try:
            if template_name not in self.templates:
                return False
                
            template = self.templates[template_name]
            
            # HTML-Vorschau generieren
            html_content = self._generate_template_preview_html(template)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating template preview: {e}")
            return False
            
    def _generate_template_preview_html(self, template: TemplateConfig) -> str:
        """HTML-Vorschau für Template generieren"""
        colors = template.color_scheme
        fonts = template.font_config
        
        html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{template.name} - Template Vorschau</title>
    <style>
        body {{
            font-family: '{fonts.body_font}', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: {self._rgb_color_to_hex(colors.background)};
            color: {self._rgb_color_to_hex(colors.text)};
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: {self._rgb_color_to_hex(colors.background_secondary)};
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .template-header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background: {self._rgb_color_to_hex(colors.primary)};
            color: white;
            border-radius: 8px;
        }}
        .template-title {{
            font-family: '{fonts.title_font}', sans-serif;
            font-size: {fonts.title_size}px;
            margin: 0;
        }}
        .template-description {{
            font-size: {fonts.body_size}px;
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .color-palette {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}
        .color-item {{
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
        }}
        .font-showcase {{
            margin: 30px 0;
        }}
        .font-item {{
            margin: 15px 0;
            padding: 15px;
            border-left: 4px solid {self._rgb_color_to_hex(colors.accent)};
            background: {self._rgb_color_to_hex(colors.background)};
        }}
        .sample-slide {{
            background: {self._rgb_color_to_hex(colors.background_secondary)};
            border: 2px solid {self._rgb_color_to_hex(colors.primary)};
            border-radius: 10px;
            padding: 30px;
            margin: 30px 0;
        }}
        .slide-title {{
            font-family: '{fonts.heading_font}', sans-serif;
            font-size: {fonts.heading_size}px;
            color: {self._rgb_color_to_hex(colors.primary)};
            margin-bottom: 20px;
        }}
        .slide-content {{
            font-size: {fonts.body_size}px;
            line-height: 1.6;
        }}
        .accent-text {{
            color: {self._rgb_color_to_hex(colors.accent)};
            font-weight: bold;
        }}
        .success-text {{
            color: {self._rgb_color_to_hex(colors.success)};
            font-weight: bold;
        }}
        .danger-text {{
            color: {self._rgb_color_to_hex(colors.danger)};
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="template-header">
            <h1 class="template-title">{template.name}</h1>
            <p class="template-description">{template.description}</p>
        </div>
        
        <h2>Farbpalette</h2>
        <div class="color-palette">
            <div class="color-item" style="background-color: {self._rgb_color_to_hex(colors.primary)}">
                Primary<br>{self._rgb_color_to_hex(colors.primary)}
            </div>
            <div class="color-item" style="background-color: {self._rgb_color_to_hex(colors.secondary)}">
                Secondary<br>{self._rgb_color_to_hex(colors.secondary)}
            </div>
            <div class="color-item" style="background-color: {self._rgb_color_to_hex(colors.accent)}">
                Accent<br>{self._rgb_color_to_hex(colors.accent)}
            </div>
            <div class="color-item" style="background-color: {self._rgb_color_to_hex(colors.success)}">
                Success<br>{self._rgb_color_to_hex(colors.success)}
            </div>
            <div class="color-item" style="background-color: {self._rgb_color_to_hex(colors.danger)}">
                Danger<br>{self._rgb_color_to_hex(colors.danger)}
            </div>
        </div>
        
        <h2>Typografie</h2>
        <div class="font-showcase">
            <div class="font-item">
                <div style="font-family: '{fonts.title_font}'; font-size: {fonts.title_size}px;">
                    Titel-Schrift: {fonts.title_font}
                </div>
            </div>
            <div class="font-item">
                <div style="font-family: '{fonts.heading_font}'; font-size: {fonts.heading_size}px;">
                    Überschrift-Schrift: {fonts.heading_font}
                </div>
            </div>
            <div class="font-item">
                <div style="font-family: '{fonts.body_font}'; font-size: {fonts.body_size}px;">
                    Fließtext-Schrift: {fonts.body_font}
                </div>
            </div>
        </div>
        
        <h2>Beispiel-Slide</h2>
        <div class="sample-slide">
            <h3 class="slide-title">🚀 Trading Bot Performance</h3>
            <div class="slide-content">
                <p>Unser automatisierter Trading Bot zeigt <span class="accent-text">außergewöhnliche Ergebnisse</span>:</p>
                <ul>
                    <li><span class="success-text">✅ 84.7% Erfolgsrate</span> bei allen Trades</li>
                    <li><span class="success-text">✅ +31.690% ROI</span> diese Woche</li>
                    <li><span class="accent-text">⚡ 59 Trades</span> automatisch ausgeführt</li>
                    <li><span class="danger-text">⚠️ Minimales Risiko</span> durch Stop-Loss</li>
                </ul>
                <p>Starten Sie noch heute und profitieren Sie von <span class="accent-text">bewiesenen Ergebnissen</span>!</p>
            </div>
        </div>
        
        <h2>Layout-Konfiguration</h2>
        <div class="font-item">
            <p><strong>Ränder:</strong> {template.layout_config.margins}</p>
            <p><strong>Content-Breite:</strong> {template.layout_config.content_width}"</p>
            <p><strong>Content-Höhe:</strong> {template.layout_config.content_height}"</p>
            <p><strong>Chart-Größe:</strong> {template.layout_config.chart_width}" × {template.layout_config.chart_height}"</p>
        </div>
        
        <h2>Animation-Einstellungen</h2>
        <div class="font-item">
            <p><strong>Slide-Übergang:</strong> {template.animation_config.slide_transition}</p>
            <p><strong>Element-Eingang:</strong> {template.animation_config.element_entrance}</p>
            <p><strong>Dauer:</strong> {template.animation_config.duration}s</p>
        </div>
    </div>
</body>
</html>"""
        
        return html

if __name__ == "__main__":
    # Test-Code
    manager = TemplateManager()
    
    print("=== VERFÜGBARE TEMPLATES ===")
    for template_name in manager.get_available_templates():
        template = manager.get_template(template_name)
        print(f"• {template.name}: {template.description}")
        
    print("\n=== TEMPLATE-INFORMATIONEN ===")
    info = manager.get_template_info()
    for name, details in info.items():
        print(f"{name}:")
        print(f"  Name: {details['name']}")
        print(f"  Beschreibung: {details['description']}")
        print(f"  Primärfarbe: {details['primary_color']}")
        print(f"  Akzentfarbe: {details['accent_color']}")
        
    # Custom Template Test
    print("\n=== CUSTOM TEMPLATE TEST ===")
    modifications = {
        'colors': {
            'primary': '#FF6B35',
            'accent': '#F7931E'
        },
        'fonts': {
            'title_size': 48,
            'body_size': 20
        }
    }
    
    success = manager.create_custom_template("my_custom", "crypto_professional", modifications)
    if success:
        print("✅ Custom Template erfolgreich erstellt!")
        
        # Vorschau generieren
        preview_success = manager.generate_template_preview("my_custom", "template_preview.html")
        if preview_success:
            print("✅ Template-Vorschau generiert: template_preview.html")
    else:
        print("❌ Fehler beim Erstellen des Custom Templates")