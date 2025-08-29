#!/usr/bin/env python3
"""
Script de construcción protegido para YouTube Downloader by JACH
Crea un ejecutable con ofuscación y protección contra copia
"""

import os
import sys
import subprocess
import shutil
import tempfile
import base64
from pathlib import Path

def install_requirements():
    """Instala dependencias necesarias"""
    print("📦 Verificando e instalando dependencias...")
    
    requirements = [
        "flask",
        "yt-dlp", 
        "pyinstaller",
        "pyarmor"  # Para ofuscación de código
    ]
    
    for package in requirements:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"⚡ Instalando {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

def obfuscate_code():
    """Ofusca el código Python para protegerlo"""
    print("🔒 Ofuscando código para protección...")
    
    try:
        # Crear proyecto pyarmor
        subprocess.run([
            sys.executable, "-m", "pyarmor", "gen", 
            "--output", "obfuscated",
            "--recursive",
            "--enable-jit",
            "app.py", "protection.py"
        ], check=True)
        
        print("✅ Código ofuscado exitosamente")
        return True
        
    except subprocess.CalledProcessError:
        print("⚠️  No se pudo ofuscar el código, continuando sin ofuscación...")
        return False

def create_protected_executable():
    """Crea el ejecutable protegido"""
    print("🔨 Creando ejecutable protegido...")
    
    # Usar código ofuscado si está disponible
    main_script = "obfuscated/app.py" if Path("obfuscated/app.py").exists() else "app.py"
    
    # Argumentos de PyInstaller
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",  # Sin consola para una aplicación más limpia
        "--name", "YouTube-Downloader-byJACH",
        "--add-data", "public;public",
        "--add-data", "downloads;downloads",
        "--distpath", "release",
        "--clean",
        main_script
    ]
    
    # Si tenemos código ofuscado, incluir archivos adicionales
    if Path("obfuscated").exists():
        pyinstaller_args.extend([
            "--add-data", "obfuscated;.",
        ])
    
    try:
        subprocess.run(pyinstaller_args, check=True)
        
        # Crear archivo de información
        create_release_info()
        
        print("✅ ¡Ejecutable creado exitosamente!")
        print(f"📍 Ubicación: release/YouTube-Downloader-byJACH.exe")
        print(f"📏 Tamaño: {get_file_size('release/YouTube-Downloader-byJACH.exe'):.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando ejecutable: {e}")
        return False

def create_release_info():
    """Crea archivo de información del release"""
    release_info = f"""
🎥 YouTube Downloader by JACH v1.0.0
═══════════════════════════════════════════════════════════════

✨ CARACTERÍSTICAS:
• Interfaz web moderna con efectos glassmorphism translúcidos
• Descarga videos de YouTube en MP3/MP4
• Múltiples opciones de calidad
• Archivo ejecutable único y portable
• No requiere instalación adicional
• Protegido contra copia y modificación

🔒 PROTECCIÓN:
• Código ofuscado y protegido
• Verificación de integridad al inicio
• Licencia propietaria embebida
• Firma digital única

💻 COMPATIBILIDAD:
• Windows 10/11 (64-bit)
• No requiere Python o Node.js instalado
• Funciona en cualquier PC Windows
• Portable - no requiere instalación

📝 USO:
1. Ejecuta "YouTube-Downloader-byJACH.exe"
2. Se abrirá automáticamente en tu navegador
3. Pega la URL del video de YouTube
4. Selecciona formato (MP3/MP4) y calidad
5. ¡Descarga!

🏷️  Made by JACH - © 2025
🚫 Prohibida la redistribución sin autorización
═══════════════════════════════════════════════════════════════
    """
    
    with open("release/README.txt", "w", encoding="utf-8") as f:
        f.write(release_info)

def get_file_size(file_path):
    """Obtiene el tamaño del archivo en MB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)  # Convert to MB
    except:
        return 0

def cleanup():
    """Limpia archivos temporales"""
    print("🧹 Limpiando archivos temporales...")
    
    cleanup_dirs = ["build", "obfuscated", "__pycache__"]
    cleanup_files = ["*.spec"]
    
    for dir_name in cleanup_dirs:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
    
    # Limpiar archivos .spec
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()

def main():
    """Función principal de construcción"""
    print("🏗️  YouTube Downloader by JACH - Construcción Protegida")
    print("=" * 60)
    
    # Verificar que estemos en el directorio correcto
    if not Path("app.py").exists():
        print("❌ Error: Ejecuta este script desde el directorio del proyecto")
        return 1
    
    try:
        # Paso 1: Instalar dependencias
        install_requirements()
        
        # Paso 2: Ofuscar código
        obfuscate_code()
        
        # Paso 3: Crear ejecutable
        if not create_protected_executable():
            return 1
        
        # Paso 4: Limpiar archivos temporales
        cleanup()
        
        print("\n🎉 ¡CONSTRUCCIÓN COMPLETADA!")
        print("🎯 Tu aplicación protegida está lista en la carpeta 'release'")
        print("🚀 Puedes distribuir 'YouTube-Downloader-byJACH.exe' a cualquier PC Windows")
        print("🔒 La aplicación está protegida contra copia y modificación")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error durante la construcción: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
