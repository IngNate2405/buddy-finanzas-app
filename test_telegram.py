#!/usr/bin/env python3
"""
Script de prueba para Telegram Reader
"""
import asyncio
import os
from dotenv import load_dotenv
from telegram_reader import TelegramReader

# Cargar variables de entorno
load_dotenv('telegram_config.env')

async def test_telegram():
    """Probar la conexión y lectura de mensajes"""
    print("🧪 Probando Telegram Reader...")
    
    # Verificar variables de entorno
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')
    phone = os.getenv('TELEGRAM_PHONE')
    
    if not all([api_id, api_hash, phone]):
        print("❌ Faltan variables de entorno en telegram_config.env")
        print("   Copia telegram_config.env.example a telegram_config.env")
        print("   y agrega tus valores de API")
        return
    
    print(f"✅ Variables encontradas:")
    print(f"   API ID: {api_id}")
    print(f"   API HASH: {api_hash[:10]}...")
    print(f"   PHONE: {phone}")
    
    reader = TelegramReader()
    
    try:
        print("\n🚀 Iniciando conexión...")
        await reader.start()
        
        print("\n👤 Información del usuario:")
        await reader.get_me()
        
        print("\n📱 Listando chats disponibles:")
        await reader.list_chats()
        
        print("\n📨 Leyendo mensajes guardados (últimos 5):")
        messages = await reader.read_saved_messages(5)
        
        if messages:
            print(f"\n✅ {len(messages)} mensajes encontrados:")
            for i, msg in enumerate(messages, 1):
                print(f"  {i}. [{msg['date']}] {msg['text']}")
        else:
            print("📭 No hay mensajes guardados")
            print("\n💡 Envía un mensaje a 'Mensajes guardados' en Telegram para probar")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Posibles soluciones:")
        print("   1. Verifica que las credenciales sean correctas")
        print("   2. Asegúrate de que el número de teléfono sea válido")
        print("   3. Revisa que tengas conexión a internet")
    finally:
        await reader.close()

if __name__ == "__main__":
    asyncio.run(test_telegram())
