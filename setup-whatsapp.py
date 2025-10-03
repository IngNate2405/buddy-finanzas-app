#!/usr/bin/env python3
"""
Script de configuración para la integración de WhatsApp Business
Configura automáticamente el entorno y las dependencias
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header():
    print("🚀 Buddy Finanzas - Configuración de WhatsApp Business")
    print("=" * 60)
    print()

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_dependencies():
    """Instalar dependencias de Python"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_env_file():
    """Crear archivo de configuración de entorno"""
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️ Archivo .env ya existe")
        return True
    
    print("📝 Creando archivo de configuración...")
    
    env_content = """# Configuración de WhatsApp Business API
WHATSAPP_VERIFY_TOKEN=buddy_finanzas_webhook
WHATSAPP_ACCESS_TOKEN=tu_token_de_acceso_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id_aqui

# Configuración de OpenAI para clasificación automática
OPENAI_API_KEY=tu_openai_api_key_aqui

# Configuración del servidor
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
        return True
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

def create_firebase_credentials_template():
    """Crear plantilla para credenciales de Firebase"""
    creds_file = Path("firebase-credentials.json")
    if creds_file.exists():
        print("⚠️ Archivo firebase-credentials.json ya existe")
        return True
    
    print("📝 Creando plantilla de credenciales de Firebase...")
    
    template = {
        "type": "service_account",
        "project_id": "buddy-finanzas",
        "private_key_id": "tu_private_key_id_aqui",
        "private_key": "-----BEGIN PRIVATE KEY-----\ntu_private_key_aqui\n-----END PRIVATE KEY-----\n",
        "client_email": "tu_client_email_aqui",
        "client_id": "tu_client_id_aqui",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "tu_client_cert_url_aqui"
    }
    
    try:
        with open("firebase-credentials-template.json", "w") as f:
            json.dump(template, f, indent=2)
        print("✅ Plantilla firebase-credentials-template.json creada")
        print("   📋 Copia este archivo como 'firebase-credentials.json' y actualiza los valores")
        return True
    except Exception as e:
        print(f"❌ Error creando plantilla: {e}")
        return False

def create_startup_script():
    """Crear script de inicio"""
    print("📝 Creando script de inicio...")
    
    startup_content = """#!/usr/bin/env python3
\"\"\"
Script de inicio para WhatsApp Webhook
\"\"\"

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar configuración
required_vars = ['WHATSAPP_ACCESS_TOKEN', 'WHATSAPP_PHONE_NUMBER_ID']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print("❌ Variables de entorno faltantes:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\\n📝 Configura las variables en el archivo .env")
    sys.exit(1)

# Iniciar servidor
if __name__ == '__main__':
    from whatsapp-webhook import app
    app.run(host='0.0.0.0', port=5000, debug=True)
"""
    
    try:
        with open("start-whatsapp.py", "w") as f:
            f.write(startup_content)
        
        # Hacer ejecutable en sistemas Unix
        if os.name != 'nt':
            os.chmod("start-whatsapp.py", 0o755)
        
        print("✅ Script de inicio creado: start-whatsapp.py")
        return True
    except Exception as e:
        print(f"❌ Error creando script de inicio: {e}")
        return False

def create_ngrok_setup():
    """Crear configuración para ngrok (túnel local)"""
    print("📝 Creando configuración para ngrok...")
    
    ngrok_content = """# Configuración de ngrok para WhatsApp Webhook
# Instala ngrok: https://ngrok.com/download

# Comando para crear túnel:
# ngrok http 5000

# URL resultante será algo como: https://abc123.ngrok.io
# Usa esta URL como webhook en Meta for Developers:
# https://abc123.ngrok.io/webhook

# Verificar webhook:
# curl -X GET "https://abc123.ngrok.io/webhook?hub.mode=subscribe&hub.verify_token=buddy_finanzas_webhook&hub.challenge=test"
"""
    
    try:
        with open("ngrok-setup.md", "w") as f:
            f.write(ngrok_content)
        print("✅ Configuración de ngrok creada: ngrok-setup.md")
        return True
    except Exception as e:
        print(f"❌ Error creando configuración de ngrok: {e}")
        return False

def show_next_steps():
    """Mostrar pasos siguientes"""
    print("\n🎉 ¡Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Configura las variables en el archivo .env")
    print("2. Configura las credenciales de Firebase (opcional)")
    print("3. Crea una app en Meta for Developers")
    print("4. Configura el webhook con ngrok o tu servidor")
    print("5. Ejecuta: python start-whatsapp.py")
    print("\n📚 Documentación:")
    print("   - WhatsApp Business API: https://developers.facebook.com/docs/whatsapp")
    print("   - ngrok: https://ngrok.com/")
    print("   - OpenAI API: https://platform.openai.com/")

def main():
    print_header()
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Instalar dependencias
    if not install_dependencies():
        return False
    
    # Crear archivos de configuración
    create_env_file()
    create_firebase_credentials_template()
    create_startup_script()
    create_ngrok_setup()
    
    # Mostrar pasos siguientes
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
