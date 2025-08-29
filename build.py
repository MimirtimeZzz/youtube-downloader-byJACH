#!/usr/bin/env python3
"""
Script para crear el ejecutable portable de YouTube Downloader by JACH
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("🏗️  Construyendo YouTube Downloader by JACH...")
    
    base_dir = Path(__file__).parent.absolute()
    dist_dir = base_dir / "dist"
    
    # Verificar que PyInstaller esté instalado
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ PyInstaller no está instalado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Crear spec file para PyInstaller
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['{base_dir}'],
    binaries=[],
    datas=[
        ('public', 'public'),
        ('downloads', 'downloads'),
    ],
    hiddenimports=[
        'yt_dlp',
        'flask',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTube-Downloader-byJACH',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    # Escribir archivo spec
    spec_file = base_dir / "youtube_downloader.spec"
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # Construir ejecutable
    print("🔨 Creando ejecutable...")
    try:
        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--onefile",
            str(spec_file)
        ], check=True, cwd=base_dir)
        
        print("✅ ¡Ejecutable creado exitosamente!")
        print(f"📍 Ubicación: {dist_dir / 'YouTube-Downloader-byJACH.exe'}")
        print("\n🎉 ¡Tu aplicación está lista!")
        print("💡 Para usar: simplemente ejecuta el archivo .exe")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la construcción: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
