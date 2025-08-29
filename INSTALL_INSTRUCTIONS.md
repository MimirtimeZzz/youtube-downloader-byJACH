# YouTube Downloader by JACH - Instrucciones de Instalación

## Opción 1: Usando Node.js (Recomendado para Web App)

### Paso 1: Instalar Node.js
1. Ve a https://nodejs.org/
2. Descarga la versión LTS para Windows
3. Ejecuta el instalador
4. Reinicia tu terminal

### Paso 2: Instalar dependencias del proyecto
```powershell
cd youtube-downloader-byJACH
npm install
```

### Paso 3: Descargar yt-dlp
```powershell
mkdir bin
# Descargar yt-dlp.exe desde https://github.com/yt-dlp/yt-dlp/releases/latest
# Colocar yt-dlp.exe en la carpeta bin/
```

### Paso 4: Ejecutar la aplicación
```powershell
npm start
```

### Paso 5: Crear ejecutable portable
```powershell
npm run build
```

## Opción 2: Usando Python (Alternativa más simple)

Si prefieres una solución más simple sin Node.js, puedo crear una versión en Python que es más fácil de empaquetar.

### Ventajas de la versión Python:
- ✅ Más fácil de instalar y empaquetar
- ✅ PyInstaller crea ejecutables más pequeños
- ✅ Menos dependencias
- ✅ Misma interfaz web pero con Flask

¿Prefieres continuar con Node.js o cambiar a Python?

---

## Características de la aplicación:
- 🎨 Interfaz web moderna y responsive
- 🔥 Descarga videos en MP4/MP3
- ⚡ Selección de calidad
- 📁 Abre carpeta de descargas automáticamente
- 🏷️ "Made by JACH" prominentemente mostrado
- 📦 Empaquetado en un solo archivo .exe
