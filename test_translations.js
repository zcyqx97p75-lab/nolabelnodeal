// Test-Skript für Übersetzungen
const fs = require('fs');

// translations.js als String einlesen
const content = fs.readFileSync('translations.js', 'utf8');

// Alle Sprachen extrahieren
const langMatches = Array.from(content.matchAll(/^    ([a-z]{2}):/gm));
const languages = langMatches.map(m => m[1]);

console.log('=== ÜBERSETZUNGS-TEST ===\n');
console.log(`Gefundene Sprachen: ${languages.length}/24\n`);

// Erwartete UI-Keys (aus de)
const expectedUIKeys = [
    'heroAlarm', 'selectLanguageCountry', 'language', 'pleaseSelect', 'country',
    'continue', 'hintSelection', 'selectRole', 'farmer', 'consumer', 'hintRole',
    'contactMEPs', 'showAllMEPs', 'showOnlyCountry', 'searchByName', 'allCountries',
    'allFractions', 'sortByName', 'sortByCountry', 'selectAllVisible', 'semicolon',
    'comma', 'onePerLine', 'copyEmails', 'showTextSuggestions', 'textSuggestionsHint',
    'emailsCopied', 'selectMandatar', 'textSuggestions', 'selectSentences',
    'copySelected', 'copyAll', 'sentencesCopied', 'selectSentence', 'counterText',
    'dataSource', 'epPublic', 'noDataStored', 'impressum', 'datenschutz'
];

// Vollständige Sprachen (mit ui, consumer, farmer)
const fullLanguages = ['de', 'en', 'fr', 'es', 'it', 'pl', 'nl', 'pt', 'cs', 'hu'];
const newLanguages = ['sk', 'sl', 'hr', 'ro', 'bg', 'da', 'sv', 'fi', 'lt', 'lv', 'et', 'mt', 'el', 'ga'];

console.log('=== SPRACHEN-STATUS ===\n');

// Prüfe jede Sprache
let missingUI = [];
let missingRotating = [];

languages.forEach(lang => {
    // Prüfe ob rotatingTexts vorhanden
    const rotatingPattern = new RegExp(`${lang}:\\s*{[\\s\\S]*?rotatingTexts:\\s*\\[`, 'm');
    const hasRotating = rotatingPattern.test(content);
    
    // Prüfe ob ui vorhanden
    const uiPattern = new RegExp(`${lang}:\\s*{[\\s\\S]*?ui:\\s*{`, 'm');
    const hasUI = uiPattern.test(content);
    
    if (!hasRotating) {
        missingRotating.push(lang);
    }
    if (!hasUI && !newLanguages.includes(lang)) {
        missingUI.push(lang);
    }
    
    const status = hasUI ? '✓ Vollständig' : (hasRotating ? '⚠ Nur rotatingTexts' : '✗ Fehlt');
    console.log(`${lang.padEnd(3)}: ${status}`);
});

console.log('\n=== ZUSAMMENFASSUNG ===\n');
console.log(`Vollständige Sprachen (mit UI): ${fullLanguages.length}`);
console.log(`Neue Sprachen (nur rotatingTexts): ${newLanguages.length}`);
console.log(`Gesamt: ${languages.length}/24`);

if (missingRotating.length > 0) {
    console.log(`\n⚠ Fehlende rotatingTexts: ${missingRotating.join(', ')}`);
}
if (missingUI.length > 0) {
    console.log(`\n⚠ Fehlende UI-Texte: ${missingUI.join(', ')}`);
}

// Prüfe ob alle neuen Sprachen rotatingTexts haben
console.log('\n=== NEUE SPRACHEN (nur rotatingTexts) ===\n');
newLanguages.forEach(lang => {
    const pattern = new RegExp(`${lang}:\\s*{[\\s\\S]*?rotatingTexts:\\s*\\[[\\s\\S]*?\\]`, 'm');
    const hasRotating = pattern.test(content);
    console.log(`${lang}: ${hasRotating ? '✓ rotatingTexts vorhanden' : '✗ rotatingTexts fehlt'}`);
});

console.log('\n=== HINWEIS ===');
console.log('Neue Sprachen (sk, sl, hr, ro, bg, da, sv, fi, lt, lv, et, mt, el, ga)');
console.log('haben nur rotatingTexts. UI-Texte werden automatisch aus Englisch übernommen.');
console.log('(Fallback-Mechanismus in getTranslation())');

