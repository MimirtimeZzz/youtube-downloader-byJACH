@echo off
echo 🏗️  Creando YouTube Downloader by JACH...
echo.

echo 📦 Instalando PyInstaller si es necesario...
python -m pip install pyinstaller --quiet

echo 🔨 Generando ejecutable portable...
python -m pyinstaller --onefile --windowed --name "YouTube-Downloader-byJACH" --add-data "public;public" --add-data "downloads;downloads" app.py

echo.
echo ✅ ¡Ejecutable creado exitosamente!
echo 📍 Ubicación: dist\YouTube-Downloader-byJACH.exe
echo.
echo 🎉 ¡Tu aplicación está lista!
echo 💡 Para usar: ejecuta el archivo .exe desde la carpeta dist
echo.
pause
