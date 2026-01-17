# Deployment-Anleitung für GitHub und Railway

## Schritt 1: GitHub Repository erstellen

1. Gehe zu [GitHub.com](https://github.com) und erstelle ein neues Repository
2. Name: z.B. `no-label-no-deal` oder `campaign-website`
3. **WICHTIG**: Repository als **öffentlich** oder **privat** erstellen (je nach Bedarf)
4. **NICHT** "Initialize with README" auswählen (wir haben bereits Dateien)

## Schritt 2: Lokales Repository mit GitHub verbinden

```bash
cd "/Users/ewald/no label no deal"

# Ersten Commit machen
git commit -m "Initial commit: Campaign website with 24 EU languages"

# GitHub Repository als Remote hinzufügen (ersetze USERNAME und REPO-NAME)
git remote add origin https://github.com/USERNAME/REPO-NAME.git

# Branch umbenennen zu main (falls nötig)
git branch -M main

# Code zu GitHub pushen
git push -u origin main
```

## Schritt 3: Railway Deployment

### Option A: Über GitHub (empfohlen)

1. Gehe zu [Railway.app](https://railway.app)
2. Melde dich an (kostenlos mit GitHub)
3. Klicke auf "New Project"
4. Wähle "Deploy from GitHub repo"
5. Wähle dein Repository aus
6. Railway erkennt automatisch die `railway.json` Konfiguration
7. Die Website wird automatisch deployed

### Option B: Manuell über Railway CLI

```bash
# Railway CLI installieren (falls noch nicht vorhanden)
npm i -g @railway/cli

# Login
railway login

# Projekt initialisieren
railway init

# Deployen
railway up
```

## Wichtige Hinweise

- **Port**: Railway setzt automatisch die `$PORT` Variable. Die `railway.json` nutzt diese bereits.
- **CSV-Datei**: Die `EU_Parlamentarier_aktuell_mit_Mail.csv` muss im Repository sein, damit sie geladen werden kann.
- **URL**: Nach dem Deployment bekommst du eine URL wie: `https://your-project.railway.app`

## Troubleshooting

### CSV-Datei wird nicht geladen
- Stelle sicher, dass die CSV-Datei im Root-Verzeichnis liegt
- Prüfe die Browser-Konsole auf CORS-Fehler
- Railway sollte CORS automatisch erlauben

### Website lädt nicht
- Prüfe die Railway-Logs: `railway logs`
- Stelle sicher, dass `railway.json` korrekt ist
- Port sollte `$PORT` verwenden (Railway setzt diese Variable)

## Alternative: Netlify (einfacher für statische Websites)

Falls Railway Probleme macht, ist Netlify noch einfacher:

1. Gehe zu [Netlify.com](https://netlify.com)
2. "Add new site" → "Import an existing project"
3. Verbinde mit GitHub
4. Build command: (leer lassen)
5. Publish directory: `/` (Root)
6. Deploy!

Netlify ist perfekt für statische Websites und benötigt keine Konfiguration.


