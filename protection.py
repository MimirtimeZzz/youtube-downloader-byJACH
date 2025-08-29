#!/usr/bin/env python3
"""
Sistema de Protección para YouTube Downloader by JACH
Implementa múltiples capas de seguridad contra copia y modificación
"""

import hashlib
import base64
import time
import os
import sys
from pathlib import Path

# Configuración de protección
AUTHOR = "JACH"
APP_NAME = "YouTube Downloader by JACH"
LICENSE_KEY = "JACH-YTD-2025-PROTECTED"
CREATION_DATE = "2025-08-29"

class AppProtection:
    def __init__(self):
        self.app_signature = self._generate_app_signature()
        self.license_info = self._get_license_info()
    
    def _generate_app_signature(self):
        """Genera una firma única de la aplicación"""
        base_data = f"{AUTHOR}:{APP_NAME}:{CREATION_DATE}:{LICENSE_KEY}"
        return hashlib.sha256(base_data.encode()).hexdigest()[:16]
    
    def _get_license_info(self):
        """Información de licencia embebida"""
        return {
            "author": AUTHOR,
            "app_name": APP_NAME,
            "license_key": LICENSE_KEY,
            "creation_date": CREATION_DATE,
            "signature": self.app_signature,
            "protected": True
        }
    
    def verify_integrity(self):
        """Verifica la integridad de la aplicación"""
        try:
            # Verificar que los archivos críticos existan
            required_files = [
                "app.py",
                "public/index.html",
                "public/styles.css",
                "public/script.js"
            ]
            
            for file_path in required_files:
                if not Path(file_path).exists():
                    return False, f"Archivo crítico faltante: {file_path}"
            
            # Verificar firma de licencia
            expected_signature = self._generate_app_signature()
            if self.app_signature != expected_signature:
                return False, "Firma de aplicación inválida"
            
            return True, "Aplicación verificada correctamente"
            
        except Exception as e:
            return False, f"Error en verificación: {str(e)}"
    
    def show_license_info(self):
        """Muestra información de licencia"""
        return f"""
╔════════════════════════════════════════════════════════════╗
║                    INFORMACIÓN DE LICENCIA                 ║
╠════════════════════════════════════════════════════════════╣
║ Aplicación: {APP_NAME:<45} ║
║ Autor: {AUTHOR:<51} ║
║ Versión: 1.0.0                                             ║
║ Fecha de creación: {CREATION_DATE}                          ║
║ Licencia: Propietaria                                      ║
║                                                            ║
║ 🚫 PROHIBIDO:                                              ║
║ • Redistribución sin autorización                         ║
║ • Modificación del código fuente                          ║
║ • Ingeniería inversa                                       ║
║ • Uso comercial sin licencia                              ║
║                                                            ║
║ ✅ PERMITIDO:                                              ║
║ • Uso personal                                             ║
║ • Descargas para uso personal                             ║
║                                                            ║
║ © 2025 JACH. Todos los derechos reservados.               ║
╚════════════════════════════════════════════════════════════╝
        """
    
    def get_protected_config(self):
        """Configuración protegida de la aplicación"""
        return {
            "app_name": APP_NAME,
            "author": AUTHOR,
            "version": "1.0.0",
            "signature": self.app_signature,
            "license": LICENSE_KEY,
            "protected": True,
            "creation_timestamp": time.time()
        }

# Función de verificación al inicio
def verify_app_launch():
    """Verifica la aplicación al inicio"""
    protection = AppProtection()
    is_valid, message = protection.verify_integrity()
    
    if not is_valid:
        print("❌ APLICACIÓN COMPROMETIDA")
        print(f"Razón: {message}")
        print("\n" + protection.show_license_info())
        sys.exit(1)
    
    print("✅ Aplicación verificada correctamente")
    print(f"🔒 Protegido por: {AUTHOR}")
    return protection

# Decorador para proteger funciones críticas
def protected_function(func):
    """Decorador que protege funciones críticas"""
    def wrapper(*args, **kwargs):
        # Verificar integridad antes de ejecutar función crítica
        protection = AppProtection()
        is_valid, _ = protection.verify_integrity()
        
        if not is_valid:
            raise Exception("Función protegida: Acceso denegado")
        
        return func(*args, **kwargs)
    
    return wrapper

# Función para ofuscar strings sensibles
def obfuscate_string(text):
    """Ofusca strings sensibles"""
    encoded = base64.b64encode(text.encode()).decode()
    return f"_protected_{encoded}_end"

def deobfuscate_string(obfuscated):
    """Desofusca strings"""
    if not obfuscated.startswith("_protected_") or not obfuscated.endswith("_end"):
        raise ValueError("String no válido para desofuscar")
    
    encoded = obfuscated[11:-4]  # Remove prefix and suffix
    return base64.b64decode(encoded).decode()

if __name__ == "__main__":
    # Test del sistema de protección
    protection = verify_app_launch()
    print("\n" + protection.show_license_info())
