## Bildanalyse und Bildsynthese Projekt

Dieses Projekt ist für die Uni und macht super viel Spaß.

## Installation von allen Dependencies (Windows 10/11)

1. Python 3.11.7 installieren: https://www.python.org/downloads/release/python-3117/
1.1. Falls andere Python versionen installiert sind: Die Pfade von Python 3.11 in den Systemumgebungsvariablen nach ganz oben Setzen (höchte Priorität)

2. Github Repo herunterladen und in VSCode öffnen.

3. python version innerhalb vom VSCode-Terminal mit `python --version` prüfen ("Python 3.11.7" sollte in der Konsole stehen)
3.1. Python 3.11.7 als interpreter in VSCode auswählen (Sicherheitshalber)

4. Virtuelles Environment in VSCode einrichten
4.1. in Konsole `python -m venv .venv` einrichten (mehr Hilfe: https://www.youtube.com/watch?v=GZbeL5AcTgw)
   
5. CUDA 12 Toolkit herunterladen: https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64
(zwingend Notwendig für ZED SDK)

6. ZED SDK installieren: https://www.stereolabs.com/developers/release
6.1. Rechner neustarten (Wie von Installationswizard verlangt)
   
7. ZED SDK Python-API installieren in virtuellem environment:
(VSCode: Ctrl+Shift+P --> `Python: Create Terminal`)
In Konsole eingeben: `pip install cython numpy opencv-python pyopengl`
(Quelle: https://www.stereolabs.com/docs/app-development/python/install#getting-started)

7.1 Mediapipe wie ZED SDK Python-API (Schritt 7 installieren) mit `pip install mediapipe`

8. get_python_api.py ausführen um den Rest der Dependencies für die ZED SDK installieren.

9. Profit???

## Troubleshooting

# OpenCV hat kein Intellisense
1. VSCode: Ctrl+Shift+P --> `Preferences: Open User Settings (JSON)` auswählen
2. folgende Zeilen einfügen:
   `"python.autoComplete.extraPaths": [".venv\\Lib\\site-packages\\opencv_python-4.9.0.80.dist-info"],`
   `"python.analysis.extraPaths": [".venv\\Lib\\site-packages\\opencv_python-4.9.0.80.dist-info"],`
3. VSCode: Ctrl+Shift+P --> `Preferences: Open Workspace Settings (JSON)` auswählen
4. folgende Zeile einfügen:
   `"python.autoComplete.extraPaths": [".venv\\Lib\\site-packages\\opencv_python-4.9.0.80.dist-info"],`
   `"python.analysis.extraPaths": [".venv\\Lib\\site-packages\\opencv_python-4.9.0.80.dist-info"],`
