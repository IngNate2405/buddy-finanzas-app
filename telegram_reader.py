#!/usr/bin/env python3
"""
Script para leer mensajes de Telegram y procesar transacciones
"""
import asyncio
import json
import os
from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

# Configuración
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')
SESSION_NAME = 'buddy_finanzas_session'

class TelegramReader:
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        
    async def start(self):
        """Iniciar el cliente de Telegram"""
        await self.client.start(phone=PHONE)
        print("✅ Cliente de Telegram iniciado")
        
    async def get_me(self):
        """Obtener información del usuario actual"""
        me = await self.client.get_me()
        print(f"👤 Usuario: {me.first_name} {me.last_name or ''} (@{me.username or 'sin username'})")
        return me
        
    async def list_chats(self):
        """Listar todos los chats disponibles"""
        print("\n📱 Chats disponibles:")
        async for dialog in self.client.iter_dialogs():
            print(f"  - {dialog.name} (ID: {dialog.id})")
            
    async def read_messages_from_chat(self, chat_name_or_id, limit=10):
        """Leer mensajes de un chat específico"""
        try:
            # Obtener el chat
            if isinstance(chat_name_or_id, str):
                # Buscar por nombre
                chat = await self.client.get_entity(chat_name_or_id)
            else:
                # Usar ID directamente
                chat = await self.client.get_entity(chat_name_or_id)
                
            print(f"\n📨 Leyendo mensajes de: {chat.title or chat.first_name}")
            
            # Leer mensajes
            messages = await self.client.get_messages(chat, limit=limit)
            
            results = []
            for message in messages:
                if message.text:
                    results.append({
                        'id': message.id,
                        'text': message.text,
                        'date': message.date.isoformat(),
                        'sender': message.sender_id if message.sender_id else None
                    })
                    
            return results
            
        except Exception as e:
            print(f"❌ Error leyendo mensajes: {e}")
            return []
            
    async def read_saved_messages(self, limit=10):
        """Leer mensajes guardados (chat contigo mismo)"""
        try:
            me = await self.get_me()
            return await self.read_messages_from_chat(me.id, limit)
        except Exception as e:
            print(f"❌ Error leyendo mensajes guardados: {e}")
            return []
            
    async def close(self):
        """Cerrar el cliente"""
        await self.client.disconnect()
        print("🔌 Cliente desconectado")

async def main():
    """Función principal"""
    print("🚀 Iniciando Telegram Reader...")
    
    # Verificar variables de entorno
    if not all([API_ID, API_HASH, PHONE]):
        print("❌ Faltan variables de entorno:")
        print("   - TELEGRAM_API_ID")
        print("   - TELEGRAM_API_HASH") 
        print("   - TELEGRAM_PHONE")
        return
        
    reader = TelegramReader()
    
    try:
        await reader.start()
        await reader.get_me()
        
        # Listar chats disponibles
        await reader.list_chats()
        
        # Leer mensajes guardados
        print("\n📨 Leyendo mensajes guardados...")
        messages = await reader.read_saved_messages(5)
        
        if messages:
            print(f"\n✅ {len(messages)} mensajes encontrados:")
            for msg in messages:
                print(f"  📝 {msg['text']}")
        else:
            print("📭 No hay mensajes guardados")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await reader.close()

if __name__ == "__main__":
    asyncio.run(main())
