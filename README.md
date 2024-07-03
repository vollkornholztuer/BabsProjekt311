# Bildanalyse und Bildsynthese Projekt

Dieses Projekt ist für die Uni und macht super viel Spaß.

## Installation von allen Dependencies für die Entwicklung (Windows 10/11)

1. Python 3.11.7 installieren: https://www.python.org/downloads/release/python-3117/  
1.1. Falls mehrere Python versionen installiert sind: Die Pfade unter "PATH" von Python 3.11 in den Systemumgebungsvariablen nach ganz oben Setzen (höchte Priorität).

2. Github Repo herunterladen und in VSCode öffnen.

3. Python Version innerhalb vom VSCode-Terminal mit `python --version` prüfen ("Python 3.11.7" sollte in der Konsole stehen).  
3.1. Python 3.11.7 als interpreter in VSCode auswählen (Sicherheitshalber).

4. Virtuelles Environment in VSCode einrichten.  
4.1. In Konsole `python -m venv .venv` eingeben (mehr Hilfe: https://www.youtube.com/watch?v=GZbeL5AcTgw)

5. Requirements installieren (mediapipe/etc)
(VSCode: Ctrl+Shift+P --> `Python: Create Terminal`)  
In Konsole eingeben: `pip install -r requirements.txt`  

# Troubleshooting

## OpenCV hat kein Intellisense
1. VSCode: Ctrl+Shift+P --> `Preferences: Open User Settings (JSON)` auswählen  
2. folgende Zeilen einfügen:  
`"python.autoComplete.extraPaths": [".venv\\Lib\\site-packages\\opencv_python-4.9.0.80.dist-info"],`  
`"python.analysis.extraPaths": [".venv\\Lib\\site-packages\\opencv_python-4.9.0.80.dist-info"],`  

3. VSCode: Ctrl+Shift+P --> `Preferences: Open Workspace Settings (JSON)` auswählen  
4. folgende Zeile einfügen:  
   `"python.autoComplete.extraPaths": [".venv\\Lib\\site-packages\\opencv_python-4.9.0.80.dist-info"],`  
   `"python.analysis.extraPaths": [".venv\\Lib\\site-packages\\opencv_python-4.9.0.80.dist-info"],`

Wenn bei den Strings in der Json schon was vorhanden ist, z.B. bei `"python.autoComplete.extraPaths"`, einfach den Pfad als String im Array hinzufügen.
Beispiel:
`"python.analysis.extraPaths": [
        "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\cv2",
        ".venv\\Lib\\site-packages\\opencv_python-4.9.0.80.dist-info"
    ],`

# Exe erstellen
1. Pyinstaller installieren: `pip install pyinstaller`
2. Datei auswählen `pyinstaller babs.spec`
3. Image Ordner muss sich im selben Ordner wie die .exe befinden
3. `babs.exe` ausführen