#!/usr/bin/env python3
"""
Script simple para crear ejecutable de YouTube Downloader by JACH
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🏗️  Creando YouTube Downloader by JACH...")
    print("=" * 50)
    
    # Crear directorio release si no existe
    Path("release").mkdir(exist_ok=True)
    
    # Comando de PyInstaller simplificado
    cmd = [
        sys.executable, "-m", "pyinstaller",
        "--onefile",
        "--name", "YouTube-Downloader-byJACH",
        "--add-data", "public;public",
        "--add-data", "downloads;downloads",
        "--distpath", "release",
        "--clean",
        "app.py"
    ]
    
    try:
        print("🔨 Creando ejecutable...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        exe_path = Path("release/YouTube-Downloader-byJACH.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✅ ¡Ejecutable creado exitosamente!")
            print(f"📍 Ubicación: {exe_path}")
            print(f"📏 Tamaño: {size_mb:.1f} MB")
            
            # Crear archivo de instrucciones
            instructions = """
🎥 YouTube Downloader by JACH v1.0.0

📋 INSTRUCCIONES DE USO:
1. Ejecuta "YouTube-Downloader-byJACH.exe" 
2. Se abrirá automáticamente en tu navegador
3. Pega la URL del video de YouTube
4. Selecciona formato (MP3/MP4) y calidad  
5. ¡Descarga!

✨ CARACTERÍSTICAS:
• Interfaz translúcida moderna
• Descarga MP3/MP4 en alta calidad
• No requiere instalación
• Funciona en cualquier PC Windows

🏷️ Made by JACH - © 2025
            """
            
            with open("release/INSTRUCCIONES.txt", "w", encoding="utf-8") as f:
                f.write(instructions)
            
            print("\n🎉 ¡LISTO!")
            print("🚀 Tu aplicación funciona en cualquier PC Windows")
            print("📦 Solo comparte la carpeta 'release' completa")
            
        else:
            print("❌ No se pudo crear el ejecutable")
            return 1
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de que PyInstaller esté instalado:")
        print("   python -m pip install pyinstaller")
        return 1
    
    # Limpiar archivos temporales
    cleanup_dirs = ["build", "__pycache__"]
    for dir_name in cleanup_dirs:
        if Path(dir_name).exists():
            import shutil
            shutil.rmtree(dir_name)
    
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
