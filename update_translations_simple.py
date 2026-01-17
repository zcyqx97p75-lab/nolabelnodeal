#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Einfaches Skript zum Einfügen von Übersetzungen in translations.js
"""

import re

LANG_MAPPING = {
    'DE': 'de', 'EN': 'en', 'FR': 'fr', 'ES': 'es', 'IT': 'it', 'PL': 'pl',
    'NL': 'nl', 'PT': 'pt', 'CS': 'cs', 'HU': 'hu', 'SK': 'sk', 'SL': 'sl',
    'HR': 'hr', 'RO': 'ro', 'BG': 'bg', 'DA': 'da', 'SV': 'sv', 'FI': 'fi',
    'LT': 'lt', 'LV': 'lv', 'ET': 'et', 'MT': 'mt', 'EL': 'el', 'GA': 'ga'
}

def parse_ui_texts(filename):
    """Parst ui_texte_zum_uebersetzen.txt"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = content.split('\n\n')
    ui_texts = {}
    # Tatsächliche Reihenfolge in der Datei
    lang_map = {
        'Bitte wähle': 'DE', 'Please select': 'EN', 'Veuillez choisir': 'FR',
        'Seleccione': 'ES', 'Seleziona': 'IT', 'Wybierz': 'PL', 'Selecteer': 'NL',
        'Selecionar': 'PT', 'Vyberte jazyk a zemi': 'CS', 'Válasszon': 'HU',
        'Vyberte jazyk a krajinu': 'SK', 'Izberite jezik': 'SL', 'Izaberite': 'HR',
        'Selectați': 'RO', 'Изберете': 'BG', 'Vælg': 'DA', 'Välj': 'SV',
        'Valitse': 'FI', 'Pasirinkite': 'LT', 'Izvēlēties': 'LV', 'Vali keel': 'ET',
        'Agħżel': 'MT', 'Επιλέξτε': 'EL', 'Roghnaigh': 'GA'
    }
    
    for section in sections:
        lines = section.strip().split('\n')
        if not lines or not lines[0]:
            continue
        
        first_line = lines[0].strip()
        # Prüfe ob es eine neue Sprache ist (beginnt mit selectLanguageCountry)
        if first_line.startswith('selectLanguageCountry:'):
            # Erkenne Sprache
            current_lang = None
            for key, lang in lang_map.items():
                if key in first_line:
                    current_lang = lang
                    break
            
            if current_lang:
                lang_code = LANG_MAPPING.get(current_lang)
                if lang_code:
                    if lang_code not in ui_texts:
                        ui_texts[lang_code] = {}
                    # Parse alle Zeilen dieser Sektion
                    for line in lines:
                        line = line.strip()
                        if not line or ':' not in line:
                            continue
                        match = re.match(r'^([a-zA-Z_]+):\s*"(.+)"$', line)
                        if match:
                            key = match.group(1)
                            value = match.group(2)
                            ui_texts[lang_code][key] = value
    
    return ui_texts

def parse_text_suggestions(filename):
    """Parst texte_deutsch.txt"""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    text_suggestions = {}
    current_lang = None
    current_type = None
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        
        # Sprach-Header
        lang_match = re.match(r'###?\s*\*\*([A-Z]{2})', line_stripped)
        if not lang_match:
            lang_match = re.match(r'^([A-Z]{2})\s*\(', line_stripped)
        if lang_match:
            lang_code = LANG_MAPPING.get(lang_match.group(1))
            if lang_code:
                current_lang = lang_code
                if current_lang not in text_suggestions:
                    text_suggestions[current_lang] = {'consumer': [], 'farmer': []}
                current_type = None
            continue
        
        # consumer/farmer Header
        line_lower = line_stripped.lower()
        if any(x in line_lower for x in ['**consumer', 'consumator', 'spotřebitel', 'potrošač', 'potrošnik', 'kuluttaja', 'tarbija', 'patērētājs', 'vartotojas', 'konsumatur', 'καταναλωτής', 'tomhaltóir', 'потребител', 'forbruger', 'konsument']):
            current_type = 'consumer'
            continue
        if any(x in line_lower for x in ['**farmer', 'agriculteur', 'agricoltore', 'agricultor', 'kmet', 'poljoprivrednik', 'zemědělec', 'poľnohospodár', 'gazdálkodó', 'fermier', 'landmand', 'jordbrukare', 'viljelijä', 'ūkininkas', 'lauksaimnieks', 'põllumees', 'põllumajandustootja', 'bidwi', 'αγρότης', 'γεωργός', 'feirmeoir', 'земеделец', 'земеделски производител']):
            current_type = 'farmer'
            continue
        
        # Sätze extrahieren
        if current_lang and current_type:
            clean_line = re.sub(r'^\*\s*', '', line_stripped)
            clean_line = re.sub(r'^-\s*', '', clean_line)
            clean_line = re.sub(r'\*\*', '', clean_line).strip()
            if clean_line and len(clean_line) > 20:
                if clean_line not in text_suggestions[current_lang][current_type]:
                    text_suggestions[current_lang][current_type].append(clean_line)
    
    return text_suggestions

def update_translations():
    """Aktualisiert translations.js"""
    print("Lade Übersetzungen...")
    ui_texts = parse_ui_texts('ui_texte_zum_uebersetzen.txt')
    print(f"Gefunden: {len(ui_texts)} Sprachen mit UI-Texten")
    
    text_suggestions = parse_text_suggestions('texte_deutsch.txt')
    print(f"Gefunden: {len(text_suggestions)} Sprachen mit Textvorschlägen")
    
    # Lese translations.js
    with open('translations.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Für jede Sprache, die nur rotatingTexts hat, füge ui, consumer, farmer hinzu
    for lang_code in ['bg', 'da', 'et', 'fi', 'ga', 'hr', 'lt', 'lv', 'mt', 'ro', 'sk', 'sl', 'sv', 'el']:
        # Finde die Sprach-Definition
        pattern = rf'({lang_code}:\s*{{[^}}]*rotatingTexts:\s*\[[^\]]+\]\s*)(}})'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            before = match.group(1)
            after = match.group(2)
            
            # Prüfe ob bereits ui, consumer, farmer vorhanden sind
            if 'ui:' in before or 'consumer:' in before or 'farmer:' in before:
                print(f"{lang_code}: Übersetzungen bereits vorhanden, überspringe...")
                continue
            
            # Baue neuen Inhalt
            new_content = before.rstrip()
            
            # Füge ui hinzu
            if lang_code in ui_texts:
                new_content += ',\n        // UI-Texte\n        ui: {\n'
                ui_items = []
                for key in sorted(ui_texts[lang_code].keys()):
                    value = ui_texts[lang_code][key]
                    value_escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                    ui_items.append(f'            {key}: "{value_escaped}"')
                new_content += ',\n'.join(ui_items)
                new_content += '\n        }'
            
            # Füge consumer hinzu
            if lang_code in text_suggestions and text_suggestions[lang_code]['consumer']:
                new_content += ',\n        // Textvorschläge\n        consumer: [\n'
                consumer_items = []
                for text in text_suggestions[lang_code]['consumer']:
                    text_escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                    consumer_items.append(f'            "{text_escaped}"')
                new_content += ',\n'.join(consumer_items)
                new_content += '\n        ]'
            
            # Füge farmer hinzu
            if lang_code in text_suggestions and text_suggestions[lang_code]['farmer']:
                new_content += ',\n        farmer: [\n'
                farmer_items = []
                for text in text_suggestions[lang_code]['farmer']:
                    text_escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                    farmer_items.append(f'            "{text_escaped}"')
                new_content += ',\n'.join(farmer_items)
                new_content += '\n        ]'
            
            new_content += '\n    }'
            
            # Ersetze
            content = content[:match.start()] + new_content + content[match.end():]
            print(f"{lang_code}: Übersetzungen eingefügt")
    
    # Schreibe zurück
    with open('translations.js', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\nFertig!")

if __name__ == '__main__':
    update_translations()

