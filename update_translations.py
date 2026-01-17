#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skript zum automatischen Einfügen von Übersetzungen in translations.js
Parst ui_texte_zum_uebersetzen.txt und texte_deutsch.txt und fügt fehlende Übersetzungen hinzu.
"""

import re
import json

# Sprach-Mapping: Datei-Codes zu translations.js Codes
LANG_MAPPING = {
    'DE': 'de',
    'EN': 'en',
    'FR': 'fr',
    'ES': 'es',
    'IT': 'it',
    'PL': 'pl',
    'NL': 'nl',
    'PT': 'pt',
    'CS': 'cs',
    'HU': 'hu',
    'SK': 'sk',
    'SL': 'sl',
    'HR': 'hr',
    'RO': 'ro',
    'BG': 'bg',
    'DA': 'da',
    'SV': 'sv',
    'FI': 'fi',
    'LT': 'lt',
    'LV': 'lv',
    'ET': 'et',
    'MT': 'mt',
    'EL': 'el',
    'GA': 'ga'
}

def parse_ui_texts(filename):
    """Parst ui_texte_zum_uebersetzen.txt und extrahiert UI-Texte für alle Sprachen."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sprachen durch leere Zeilen getrennt
    sections = content.split('\n\n')
    
    ui_texts = {}
    current_lang = None
    
    for section in sections:
        lines = section.strip().split('\n')
        if not lines or not lines[0]:
            continue
        
        # Prüfe ob erste Zeile ein Key-Value Paar ist (dann ist es eine neue Sprache)
        first_line = lines[0].strip()
        if ':' in first_line and not first_line.startswith('#'):
            # Neue Sprache - erkenne anhand des ersten Keys
            # Erste Sprache ist Deutsch
            if current_lang is None:
                current_lang = 'DE'
            else:
                # Versuche Sprache aus dem Kontext zu erkennen
                # Wenn wir bei einem bekannten Key anfangen, ist es eine neue Sprache
                key = first_line.split(':')[0].strip()
                if key == 'selectLanguageCountry':
                    # Neue Sprache beginnt
                    # Zähle wie viele Sprachen wir schon haben
                    lang_index = len(ui_texts)
                    lang_codes = ['DE', 'EN', 'FR', 'ES', 'IT', 'PL', 'NL', 'PT', 'CS', 'HU', 'SK', 'SL', 'HR', 'RO', 'BG', 'DA', 'SV', 'FI', 'LT', 'LV', 'ET', 'MT', 'EL', 'GA']
                    if lang_index < len(lang_codes):
                        current_lang = lang_codes[lang_index]
        
        # Parse Key-Value Paare
        for line in lines:
            line = line.strip()
            if not line or ':' not in line:
                continue
            
            # Key-Value Format: key: "value"
            match = re.match(r'^([a-zA-Z_]+):\s*"(.+)"$', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                
                if current_lang:
                    lang_code = LANG_MAPPING.get(current_lang, current_lang.lower())
                    if lang_code not in ui_texts:
                        ui_texts[lang_code] = {}
                    ui_texts[lang_code][key] = value
    
    return ui_texts

def parse_text_suggestions(filename):
    """Parst texte_deutsch.txt und extrahiert consumer/farmer Texte für alle Sprachen."""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    text_suggestions = {}
    current_lang = None
    current_type = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Prüfe ob es ein Sprach-Header ist
        # Format: ### **SPRACHE** oder ### **SPRACHE (Name)** oder SPRACHE (Name)
        lang_match = re.match(r'###?\s*\*\*([A-Z]{2})', line)
        if not lang_match:
            lang_match = re.match(r'^([A-Z]{2})\s*\(', line)
        
        if lang_match:
            lang_code = lang_match.group(1)
            if lang_code in LANG_MAPPING:
                current_lang = LANG_MAPPING[lang_code]
                if current_lang not in text_suggestions:
                    text_suggestions[current_lang] = {'consumer': [], 'farmer': []}
                current_type = None
                i += 1
                continue
        
        # Prüfe ob es ein consumer/farmer Header ist
        line_lower = line.lower()
        if '**consumer' in line_lower or 'consumator' in line_lower or 'spotřebitel' in line_lower or 'potrošač' in line_lower or 'potrošnik' in line_lower or 'kuluttaja' in line_lower or 'tarbija' in line_lower or 'patērētājs' in line_lower or 'vartotojas' in line_lower or 'konsumatur' in line_lower or 'καταναλωτής' in line_lower or 'tomhaltóir' in line_lower or 'потребител' in line_lower or 'forbruger' in line_lower or 'konsument' in line_lower:
            current_type = 'consumer'
            i += 1
            continue
        
        if '**farmer' in line_lower or 'agriculteur' in line_lower or 'agricoltore' in line_lower or 'agricultor' in line_lower or 'kmet' in line_lower or 'poljoprivrednik' in line_lower or 'zemědělec' in line_lower or 'poľnohospodár' in line_lower or 'gazdálkodó' in line_lower or 'fermier' in line_lower or 'landmand' in line_lower or 'jordbrukare' in line_lower or 'viljelijä' in line_lower or 'ūkininkas' in line_lower or 'lauksaimnieks' in line_lower or 'põllumees' in line_lower or 'põllumajandustootja' in line_lower or 'bidwi' in line_lower or 'αγρότης' in line_lower or 'γεωργός' in line_lower or 'feirmeoir' in line_lower or 'земеделец' in line_lower or 'земеделски производител' in line_lower:
            current_type = 'farmer'
            i += 1
            continue
        
        # Extrahiere Sätze (Bullet-Points oder normale Zeilen)
        if current_lang and current_type:
            # Entferne Bullet-Point Marker
            clean_line = re.sub(r'^\*\s*', '', line)
            clean_line = re.sub(r'^-\s*', '', clean_line)
            clean_line = clean_line.strip()
            
            # Wenn die Zeile lang genug ist und nicht leer
            if clean_line and len(clean_line) > 20:  # Mindestlänge für einen Satz
                # Entferne Markdown-Formatierung
                clean_line = re.sub(r'\*\*', '', clean_line)
                if clean_line not in text_suggestions[current_lang][current_type]:
                    text_suggestions[current_lang][current_type].append(clean_line)
        
        i += 1
    
    return text_suggestions

def update_translations_js(ui_texts, text_suggestions):
    """Aktualisiert translations.js mit den neuen Übersetzungen."""
    with open('translations.js', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    current_lang = None
    in_lang_block = False
    lang_start = None
    lang_indent = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Prüfe ob es eine Sprach-Definition ist: lang_code: {
        lang_match = re.match(r'(\s*)([a-z]{2}):\s*\{', line)
        if lang_match:
            current_lang = lang_match.group(2)
            lang_indent = len(lang_match.group(1))
            in_lang_block = True
            lang_start = i
            new_lines.append(line)
            i += 1
            continue
        
        # Wenn wir in einem Sprach-Block sind, prüfe ob er endet
        if in_lang_block and current_lang:
            # Prüfe ob ui, consumer, farmer bereits vorhanden sind
            has_ui = 'ui:' in ''.join(lines[lang_start:i+1])
            has_consumer = 'consumer:' in ''.join(lines[lang_start:i+1])
            has_farmer = 'farmer:' in ''.join(lines[lang_start:i+1])
            
            # Prüfe ob der Block endet (schließende Klammer auf gleicher Einrückungsebene)
            if re.match(r'\s{' + str(lang_indent) + r'}\},?\s*$', line):
                # Block endet - füge fehlende Teile hinzu
                # Finde das Ende von rotatingTexts
                rotating_end_idx = None
                for j in range(i-1, lang_start-1, -1):
                    if ']' in lines[j] and 'rotatingTexts' in ''.join(lines[lang_start:j+1]):
                        rotating_end_idx = j
                        break
                
                if rotating_end_idx is not None:
                    # Füge alle Zeilen bis zum Ende von rotatingTexts hinzu
                    for j in range(lang_start+1, rotating_end_idx+1):
                        new_lines.append(lines[j])
                    
                    # Füge ui hinzu
                    if not has_ui and current_lang in ui_texts:
                        indent = ' ' * (lang_indent + 4)
                        new_lines.append(f'{indent},\n')
                        new_lines.append(f'{indent}// UI-Texte\n')
                        new_lines.append(f'{indent}ui: {{\n')
                        ui_items = []
                        for key, value in sorted(ui_texts[current_lang].items()):
                            # Escape Quotes und Newlines
                            value_escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                            ui_items.append(f'{indent}    {key}: "{value_escaped}"')
                        new_lines.append(',\n'.join(ui_items))
                        new_lines.append(f'\n{indent}}}')
                    
                    # Füge consumer hinzu
                    if not has_consumer and current_lang in text_suggestions and text_suggestions[current_lang]['consumer']:
                        indent = ' ' * (lang_indent + 4)
                        new_lines.append(f'{indent},\n')
                        new_lines.append(f'{indent}// Textvorschläge\n')
                        new_lines.append(f'{indent}consumer: [\n')
                        consumer_items = []
                        for text in text_suggestions[current_lang]['consumer']:
                            text_escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                            consumer_items.append(f'{indent}    "{text_escaped}"')
                        new_lines.append(',\n'.join(consumer_items))
                        new_lines.append(f'\n{indent}]')
                    
                    # Füge farmer hinzu
                    if not has_farmer and current_lang in text_suggestions and text_suggestions[current_lang]['farmer']:
                        indent = ' ' * (lang_indent + 4)
                        new_lines.append(f'{indent},\n')
                        new_lines.append(f'{indent}farmer: [\n')
                        farmer_items = []
                        for text in text_suggestions[current_lang]['farmer']:
                            text_escaped = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                            farmer_items.append(f'{indent}    "{text_escaped}"')
                        new_lines.append(',\n'.join(farmer_items))
                        new_lines.append(f'\n{indent}]')
                    
                    # Füge die schließende Klammer hinzu
                    new_lines.append(line)
                    in_lang_block = False
                    current_lang = None
                    i += 1
                    continue
                else:
                    # Kein rotatingTexts gefunden, einfach die Zeile hinzufügen
                    new_lines.append(line)
                    i += 1
                    continue
            else:
                # Noch im Block, Zeile hinzufügen
                new_lines.append(line)
                i += 1
                continue
        else:
            # Normale Zeile
            new_lines.append(line)
            i += 1
    
    # Schreibe zurück
    with open('translations.js', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("translations.js wurde aktualisiert!")

def check_completeness():
    """Prüft die Vollständigkeit aller Übersetzungen."""
    with open('translations.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Finde alle Sprachen
    lang_pattern = r'([a-z]{2}):\s*\{'
    languages = re.findall(lang_pattern, content)
    
    print("\n=== VOLLSTÄNDIGKEITSPRÜFUNG ===\n")
    
    required_ui_keys = ['heroAlarm', 'selectLanguageCountry', 'language', 'country', 'continue', 
                        'selectRole', 'farmer', 'consumer', 'contactMEPs', 'copyEmails', 'sendEmail',
                        'textSuggestions', 'counterText', 'home', 'impressum', 'datenschutz']
    
    for lang in languages:
        has_rotating = f'{lang}: {{\\s*rotatingTexts:' in content or f'{lang}: {{[^}}]*rotatingTexts' in content
        has_ui = f'{lang}: {{[^}}]*ui:' in content
        has_consumer = f'{lang}: {{[^}}]*consumer:' in content
        has_farmer = f'{lang}: {{[^}}]*farmer:' in content
        
        status = []
        if has_rotating:
            status.append('✓ rotatingTexts')
        else:
            status.append('✗ rotatingTexts')
        
        if has_ui:
            status.append('✓ ui')
        else:
            status.append('✗ ui')
        
        if has_consumer:
            status.append('✓ consumer')
        else:
            status.append('✗ consumer')
        
        if has_farmer:
            status.append('✓ farmer')
        else:
            status.append('✗ farmer')
        
        print(f'{lang}: {" | ".join(status)}')

if __name__ == '__main__':
    print("Lade Übersetzungen...")
    
    # Parse UI-Texte
    print("Parse ui_texte_zum_uebersetzen.txt...")
    ui_texts = parse_ui_texts('ui_texte_zum_uebersetzen.txt')
    print(f"Gefunden: {len(ui_texts)} Sprachen mit UI-Texten")
    
    # Parse Textvorschläge
    print("Parse texte_deutsch.txt...")
    text_suggestions = parse_text_suggestions('texte_deutsch.txt')
    print(f"Gefunden: {len(text_suggestions)} Sprachen mit Textvorschlägen")
    
    # Aktualisiere translations.js
    print("Aktualisiere translations.js...")
    update_translations_js(ui_texts, text_suggestions)
    
    # Vollständigkeitsprüfung
    check_completeness()
    
    print("\nFertig!")

