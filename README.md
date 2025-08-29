# 🎥 YouTube Downloader by JACH

[![Made by JACH](https://img.shields.io/badge/Made%20by-JACH-orange.svg)](https://github.com)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](#license)
[![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)](https://github.com)

Una aplicación web portable moderna para descargar videos de YouTube con una interfaz translúcida y elegante.

## ✨ Características

- 🎨 **Interfaz moderna** con efectos glassmorphism translúcidos
- 📱 **Web App Portable** - se ejecuta en el navegador
- 🎵 **Descarga MP3** - audio en alta calidad (192 kbps)
- 🎬 **Descarga MP4** - video en múltiples calidades
- 📦 **Archivo único** - ejecutable de ~18MB sin dependencias
- ⚡ **Súper rápido** - powered by yt-dlp
- 🔒 **100% seguro** - código verificado
- 🌍 **Universal** - funciona en cualquier PC Windows

## 🖼️ Screenshots

### Interfaz Principal
![Interfaz translúcida moderna con efectos glassmorphism]

### Barra Lateral "Made by JACH"
- Créditos prominentes del desarrollador
- Lista de características
- Diseño elegante con gradientes

## 🚀 Instalación y Uso

### Opción 1: Usar el Ejecutable (Recomendado)
1. Descarga `YouTube-Downloader-byJACH.exe` desde [Releases](../../releases)
2. Ejecuta el archivo (no requiere instalación)
3. Se abrirá automáticamente en tu navegador
4. ¡Empieza a descargar videos!

### Opción 2: Ejecutar desde el Código Fuente
```bash
# Clonar el repositorio
git clone https://github.com/MimirtimeZzz/youtube-downloader-byJACH.git
cd youtube-downloader-byJACH

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

## 📝 Instrucciones de Uso

1. **Ejecuta** `YouTube-Downloader-byJACH.exe`
2. **Se abre automáticamente** en tu navegador web
3. **Pega la URL** del video de YouTube
4. **Selecciona formato:**
   - 🎵 **MP3** para solo audio
   - 🎬 **MP4** para video completo
5. **Elige la calidad** deseada
6. **Haz clic en "Descargar"**
7. **Abre la carpeta** de descargas cuando termine

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python + Flask + yt-dlp
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Empaquetado**: PyInstaller
- **Descarga**: yt-dlp (la mejor librería para YouTube)
- **UI**: Glassmorphism design con efectos translúcidos

## 💻 Compatibilidad

- ✅ Windows 10/11 (32-bit y 64-bit)
- ✅ No requiere Python instalado
- ✅ No requiere dependencias adicionales
- ✅ 100% Portable
- ✅ Funciona offline una vez descargado

## 🔧 Desarrollo

### Construir el Ejecutable
```bash
# Instalar dependencias de desarrollo
pip install pyinstaller

# Crear ejecutable
python build_simple.py
```

El ejecutable se creará en la carpeta `release/`

### Estructura del Proyecto
```
youtube-downloader-byJACH/
├── app.py                 # Servidor Flask principal
├── protection.py          # Sistema de protección
├── requirements.txt       # Dependencias Python
├── build_simple.py        # Script de construcción
├── public/                # Archivos de la interfaz web
│   ├── index.html        # Página principal
│   ├── styles.css        # Estilos con efectos glassmorphism
│   └── script.js         # Lógica de la interfaz
├── downloads/            # Carpeta de descargas
└── release/              # Ejecutable final
    ├── YouTube-Downloader-byJACH.exe
    └── INSTRUCCIONES_JACH.txt
```

## 🔒 Protección y Licencia

Esta aplicación está protegida contra copia y modificación:

- 🚫 **Prohibida** la redistribución comercial sin autorización
- 🚫 **Prohibida** la modificación del código fuente
- 🚫 **Prohibida** la ingeniería inversa
- ✅ **Permitido** uso personal

## 🏷️ Créditos

**Made by JACH** - © 2025

- Desarrollador: JACH
- Versión: 1.0.0
- Fecha de creación: 29 de agosto de 2025

## 📧 Contacto

Si necesitas una licencia comercial o tienes dudas, contacta al desarrollador original: **JACH**

## 🤝 Contribuciones

Este es un proyecto propietario de JACH. Las contribuciones están restringidas al autor original.

## 📜 License

Copyright © 2025 JACH. Todos los derechos reservados.

Esta aplicación es software propietario. El uso está permitido solo para fines personales. 
Cualquier otro uso requiere autorización explícita del autor.

---

<div align="center">

**🎉 ¡Disfruta descargando tus videos favoritos de YouTube! 🎉**

[![Made with ❤️ by JACH](https://img.shields.io/badge/Made%20with%20❤️%20by-JACH-orange.svg)](https://github.com)

</div>
