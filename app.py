#!/usr/bin/env python3
"""
YouTube Downloader by JACH
Aplicación web portable para descargar videos de YouTube
© 2025 JACH - Todos los derechos reservados
APLICACIÓN PROTEGIDA CONTRA COPIA Y MODIFICACIÓN
"""

import os
import sys
import json
import subprocess
import threading
import webbrowser
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from flask import Flask, render_template_string, request, jsonify, send_from_directory
import yt_dlp
# from protection import verify_app_launch, protected_function, AppProtection

app = Flask(__name__)

# Configuración
PORT = 3000
BASE_DIR = Path(__file__).parent.absolute()
DOWNLOADS_DIR = BASE_DIR / 'downloads'
PUBLIC_DIR = BASE_DIR / 'public'

# Crear directorio de descargas si no existe
DOWNLOADS_DIR.mkdir(exist_ok=True)

# Configuración de yt-dlp
class MyLogger:
    def debug(self, msg):
        pass
    
    def warning(self, msg):
        print(f"⚠️  {msg}")
    
    def error(self, msg):
        print(f"❌ {msg}")

def get_video_info(url):
    """Obtiene información del video sin descargarlo"""
    ydl_opts = {
        'logger': MyLogger(),
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', 'Sin título'),
            'duration': info.get('duration', 0),
            'uploader': info.get('uploader', 'Desconocido'),
            'thumbnail': info.get('thumbnail', ''),
            'formats': info.get('formats', [])
        }

def download_video(url, format_type='best', audio_only=False):
    """Descarga el video con las opciones especificadas"""
    
    # Configurar opciones de descarga
    if audio_only:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(DOWNLOADS_DIR / '%(title)s.%(ext)s'),
            'logger': MyLogger(),
        }
    else:
        ydl_opts = {
            'format': format_type,
            'outtmpl': str(DOWNLOADS_DIR / '%(title)s.%(ext)s'),
            'logger': MyLogger(),
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Rutas de la API
@app.route('/')
def index():
    """Página principal"""
    try:
        with open(PUBLIC_DIR / 'index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Error: No se encontró el archivo index.html"

@app.route('/styles.css')
def styles():
    """Estilos CSS"""
    try:
        with open(PUBLIC_DIR / 'styles.css', 'r', encoding='utf-8') as f:
            response = app.response_class(f.read(), mimetype='text/css')
            return response
    except FileNotFoundError:
        return "/* Error: No se encontró el archivo styles.css */", 404

@app.route('/script.js')
def script():
    """JavaScript de la aplicación"""
    try:
        with open(PUBLIC_DIR / 'script.js', 'r', encoding='utf-8') as f:
            response = app.response_class(f.read(), mimetype='text/javascript')
            return response
    except FileNotFoundError:
        return "// Error: No se encontró el archivo script.js", 404

@app.route('/api/video-info', methods=['POST'])
def api_video_info():
    """Obtiene información del video"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL es requerida'}), 400
        
        # Validar URL de YouTube
        if not is_valid_youtube_url(url):
            return jsonify({'error': 'URL de YouTube no válida'}), 400
        
        video_info = get_video_info(url)
        return jsonify(video_info)
        
    except Exception as e:
        return jsonify({'error': f'Error obteniendo información: {str(e)}'}), 500

@app.route('/api/download', methods=['POST'])
def api_download():
    """Descarga el video"""
    try:
        data = request.get_json()
        url = data.get('url')
        format_type = data.get('format', 'best')
        quality = data.get('quality', 'best')
        
        if not url:
            return jsonify({'error': 'URL es requerida'}), 400
        
        # Determinar si es descarga de audio
        audio_only = format_type == 'mp3'
        
        # Descargar video
        download_video(url, quality, audio_only)
        
        return jsonify({
            'success': True,
            'message': 'Descarga completada exitosamente',
            'downloadPath': str(DOWNLOADS_DIR)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error en la descarga: {str(e)}'}), 500

@app.route('/api/open-downloads', methods=['POST'])
def api_open_downloads():
    """Abre la carpeta de descargas"""
    try:
        if sys.platform == "win32":
            os.startfile(str(DOWNLOADS_DIR))
        elif sys.platform == "darwin":  # macOS
            subprocess.run(['open', str(DOWNLOADS_DIR)])
        else:  # Linux
            subprocess.run(['xdg-open', str(DOWNLOADS_DIR)])
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': f'Error abriendo carpeta: {str(e)}'}), 500

def is_valid_youtube_url(url):
    """Valida si la URL es de YouTube"""
    parsed = urlparse(url)
    return (
        parsed.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be', 'm.youtube.com'] or
        'youtube.com' in parsed.netloc
    )

def open_browser():
    """Abre el navegador después de un delay"""
    import time
    time.sleep(1.5)
    webbrowser.open(f'http://localhost:{PORT}')

if __name__ == '__main__':
    # 🔒 INFORMACIÓN DE PROTECCIÓN 
    print("🔒 YouTube Downloader by JACH - Versión Protegida")
    print("© 2025 JACH - Todos los derechos reservados")
    print("🚫 Prohibida la redistribución sin autorización")
    
    print("\n🎥 YouTube Downloader by JACH")
    print(f"🚀 Iniciando servidor en http://localhost:{PORT}")
    print("📁 Carpeta de descargas:", DOWNLOADS_DIR)
    print("🔒 Aplicación protegida por JACH")
    
    # Abrir navegador en un hilo separado
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Iniciar servidor Flask
    app.run(host='localhost', port=PORT, debug=False)
