#!/usr/bin/env python3
"""
Webhook para WhatsApp Business API
Recibe mensajes y procesa transacciones automáticamente
"""

import json
import os
import re
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import openai

app = Flask(__name__)
CORS(app)

# Configuración de Firebase
try:
    # Intentar usar las credenciales de Firebase si están disponibles
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase inicializado correctamente")
except Exception as e:
    print(f"⚠️ Firebase no disponible: {e}")
    db = None

# Configuración de OpenAI para clasificación de transacciones
openai.api_key = os.getenv('OPENAI_API_KEY')

class WhatsAppWebhook:
    def __init__(self):
        self.verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN', 'buddy_finanzas_webhook')
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        
    def verify_webhook(self, mode, token, challenge):
        """Verificar el webhook de WhatsApp"""
        if mode == 'subscribe' and token == self.verify_token:
            print("✅ Webhook verificado correctamente")
            return challenge
        return None
    
    def process_message(self, message_data):
        """Procesar mensaje recibido de WhatsApp"""
        try:
            # Extraer información del mensaje
            message = message_data.get('messages', [{}])[0]
            from_number = message.get('from', '')
            message_text = message.get('text', {}).get('body', '')
            message_id = message.get('id', '')
            
            print(f"📱 Mensaje recibido de {from_number}: {message_text}")
            
            # Procesar el mensaje como posible transacción
            transaction = self.parse_transaction(message_text)
            
            if transaction:
                # Guardar transacción en Firebase
                self.save_transaction(transaction, from_number)
                
                # Enviar confirmación al usuario
                self.send_confirmation(from_number, transaction)
                
                return {"status": "success", "message": "Transacción procesada"}
            else:
                # Enviar mensaje de ayuda si no se reconoce como transacción
                self.send_help_message(from_number)
                return {"status": "info", "message": "Mensaje de ayuda enviado"}
                
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")
            return {"status": "error", "message": str(e)}
    
    def parse_transaction(self, text):
        """Analizar texto para extraer información de transacción"""
        # Patrones comunes para transacciones
        patterns = {
            # Patrones para gastos
            'expense_patterns': [
                r'gasté?\s*Q?\s*(\d+(?:\.\d{2})?)',  # "gasté Q100"
                r'compré?\s*Q?\s*(\d+(?:\.\d{2})?)',  # "compré Q50"
                r'pagué?\s*Q?\s*(\d+(?:\.\d{2})?)',   # "pagué Q25"
                r'Q?\s*(\d+(?:\.\d{2})?)\s*en\s*(.+)', # "Q100 en comida"
                r'Q?\s*(\d+(?:\.\d{2})?)\s*para\s*(.+)', # "Q50 para gasolina"
            ],
            # Patrones para ingresos
            'income_patterns': [
                r'recibí?\s*Q?\s*(\d+(?:\.\d{2})?)',  # "recibí Q1000"
                r'gané?\s*Q?\s*(\d+(?:\.\d{2})?)',   # "gané Q500"
                r'ingresó?\s*Q?\s*(\d+(?:\.\d{2})?)', # "ingresó Q2000"
                r'salario\s*Q?\s*(\d+(?:\.\d{2})?)', # "salario Q3000"
            ]
        }
        
        # Buscar patrones de gastos
        for pattern in patterns['expense_patterns']:
            match = re.search(pattern, text.lower())
            if match:
                amount = float(match.group(1))
                category = self.classify_transaction(text, 'expense')
                return {
                    'amount': amount,
                    'type': 'expense',
                    'category': category,
                    'description': text,
                    'date': datetime.now().isoformat(),
                    'source': 'whatsapp'
                }
        
        # Buscar patrones de ingresos
        for pattern in patterns['income_patterns']:
            match = re.search(pattern, text.lower())
            if match:
                amount = float(match.group(1))
                category = self.classify_transaction(text, 'income')
                return {
                    'amount': amount,
                    'type': 'income',
                    'category': category,
                    'description': text,
                    'date': datetime.now().isoformat(),
                    'source': 'whatsapp'
                }
        
        return None
    
    def classify_transaction(self, text, transaction_type):
        """Clasificar automáticamente la categoría de la transacción usando IA"""
        try:
            # Usar OpenAI para clasificar la transacción
            if openai.api_key:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": """Eres un experto en clasificación de transacciones financieras. 
                            Clasifica el siguiente texto en una de estas categorías:
                            
                            Para gastos:
                            - Food & drinks (comida, restaurante, supermercado, café)
                            - Transportation (gasolina, transporte, taxi, uber)
                            - Entertainment (cine, entretenimiento, gym, deportes)
                            - Housing (renta, servicios, internet, teléfono)
                            - Lifestyle (ropa, farmacia, cuidado personal)
                            - Miscellaneous (otros gastos no categorizados)
                            
                            Para ingresos:
                            - Income (salario, trabajo)
                            - Investments (inversiones, intereses)
                            - Other (otros ingresos)
                            
                            Responde solo con el nombre de la categoría, nada más."""
                        },
                        {
                            "role": "user",
                            "content": f"Tipo: {transaction_type}\nTexto: {text}"
                        }
                    ],
                    max_tokens=50,
                    temperature=0.3
                )
                
                category = response.choices[0].message.content.strip()
                print(f"🤖 IA clasificó como: {category}")
                return category
                
        except Exception as e:
            print(f"⚠️ Error en clasificación IA: {e}")
        
        # Fallback: clasificación básica por palabras clave
        return self.basic_classification(text, transaction_type)
    
    def basic_classification(self, text, transaction_type):
        """Clasificación básica por palabras clave"""
        text_lower = text.lower()
        
        if transaction_type == 'expense':
            # Clasificación de gastos
            if any(word in text_lower for word in ['comida', 'restaurante', 'supermercado', 'café', 'comer']):
                return 'Food & drinks'
            elif any(word in text_lower for word in ['gasolina', 'gas', 'transporte', 'taxi', 'uber', 'carro']):
                return 'Transportation'
            elif any(word in text_lower for word in ['cine', 'entretenimiento', 'gym', 'deporte', 'fiesta']):
                return 'Entertainment'
            elif any(word in text_lower for word in ['renta', 'servicio', 'internet', 'teléfono', 'luz', 'agua']):
                return 'Housing'
            elif any(word in text_lower for word in ['ropa', 'farmacia', 'corte', 'cuidado']):
                return 'Lifestyle'
            else:
                return 'Miscellaneous'
        
        else:  # income
            if any(word in text_lower for word in ['salario', 'trabajo', 'sueldo', 'pago']):
                return 'Income'
            elif any(word in text_lower for word in ['inversión', 'interés', 'dividendo']):
                return 'Investments'
            else:
                return 'Other'
    
    def save_transaction(self, transaction, phone_number):
        """Guardar transacción en Firebase"""
        try:
            if db:
                # Crear documento de transacción
                transaction_doc = {
                    'amount': transaction['amount'],
                    'type': transaction['type'],
                    'category': transaction['category'],
                    'description': transaction['description'],
                    'date': transaction['date'],
                    'source': transaction['source'],
                    'phone_number': phone_number,
                    'created_at': datetime.now().isoformat()
                }
                
                # Guardar en la colección de transacciones
                db.collection('whatsapp_transactions').add(transaction_doc)
                print(f"✅ Transacción guardada: {transaction}")
                
                # También intentar guardar en la estructura existente del usuario
                self.sync_to_user_data(transaction, phone_number)
                
            else:
                print("⚠️ Firebase no disponible, transacción no guardada")
                
        except Exception as e:
            print(f"❌ Error guardando transacción: {e}")
    
    def sync_to_user_data(self, transaction, phone_number):
        """Sincronizar transacción con los datos del usuario existente"""
        try:
            # Buscar usuario por número de teléfono
            users_ref = db.collection('users')
            users = users_ref.where('phone_number', '==', phone_number).limit(1).get()
            
            if users:
                user_doc = users[0]
                user_id = user_doc.id
                
                # Obtener transacciones existentes del usuario
                user_data = user_doc.to_dict()
                existing_transactions = user_data.get('transactions', [])
                
                # Agregar nueva transacción
                new_transaction = {
                    'id': f"whatsapp_{datetime.now().timestamp()}",
                    'amount': transaction['amount'],
                    'type': transaction['type'],
                    'category': transaction['category'],
                    'date': transaction['date'].split('T')[0],  # Solo la fecha
                    'month': datetime.now().month - 1,  # 0-indexed
                    'year': datetime.now().year,
                    'source': 'whatsapp'
                }
                
                existing_transactions.append(new_transaction)
                
                # Actualizar documento del usuario
                user_doc.reference.update({
                    'transactions': existing_transactions,
                    'lastUpdated': datetime.now().isoformat()
                })
                
                print(f"✅ Transacción sincronizada con usuario {user_id}")
            else:
                print(f"⚠️ Usuario con teléfono {phone_number} no encontrado")
                
        except Exception as e:
            print(f"❌ Error sincronizando con usuario: {e}")
    
    def send_confirmation(self, phone_number, transaction):
        """Enviar confirmación al usuario"""
        try:
            message = f"✅ Transacción registrada:\n"
            message += f"💰 {transaction['type'].title()}: Q{transaction['amount']}\n"
            message += f"📂 Categoría: {transaction['category']}\n"
            message += f"📝 Descripción: {transaction['description']}"
            
            self.send_whatsapp_message(phone_number, message)
            
        except Exception as e:
            print(f"❌ Error enviando confirmación: {e}")
    
    def send_help_message(self, phone_number):
        """Enviar mensaje de ayuda"""
        try:
            message = """🤖 Buddy Finanzas - Ayuda

Para registrar una transacción, envía un mensaje como:
• "Gasté Q100 en comida"
• "Compré Q50 de gasolina" 
• "Recibí Q1000 de salario"
• "Pagué Q200 de renta"

¡Soy inteligente y clasifico automáticamente tus transacciones! 💡"""
            
            self.send_whatsapp_message(phone_number, message)
            
        except Exception as e:
            print(f"❌ Error enviando ayuda: {e}")
    
    def send_whatsapp_message(self, phone_number, message):
        """Enviar mensaje a través de WhatsApp API"""
        try:
            if not self.access_token or not self.phone_number_id:
                print("⚠️ Credenciales de WhatsApp no configuradas")
                return
            
            url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'messaging_product': 'whatsapp',
                'to': phone_number,
                'type': 'text',
                'text': {'body': message}
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"✅ Mensaje enviado a {phone_number}")
            else:
                print(f"❌ Error enviando mensaje: {response.text}")
                
        except Exception as e:
            print(f"❌ Error en envío de WhatsApp: {e}")

# Inicializar webhook
webhook = WhatsAppWebhook()

@app.route('/webhook', methods=['GET', 'POST'])
def handle_webhook():
    """Manejar webhook de WhatsApp"""
    if request.method == 'GET':
        # Verificación del webhook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        result = webhook.verify_webhook(mode, token, challenge)
        if result:
            return result
        else:
            return 'Error', 403
    
    elif request.method == 'POST':
        # Procesar mensaje
        try:
            data = request.get_json()
            print(f"📨 Webhook recibido: {json.dumps(data, indent=2)}")
            
            # Verificar que es un mensaje válido
            if 'entry' in data and len(data['entry']) > 0:
                entry = data['entry'][0]
                if 'changes' in entry and len(entry['changes']) > 0:
                    change = entry['changes'][0]
                    if 'value' in change and 'messages' in change['value']:
                        result = webhook.process_message(change['value'])
                        return jsonify(result)
            
            return jsonify({"status": "no_message"})
            
        except Exception as e:
            print(f"❌ Error procesando webhook: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Verificar estado del servicio"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "firebase": "connected" if db else "disconnected"
    })

if __name__ == '__main__':
    print("🚀 Iniciando servidor de WhatsApp Webhook...")
    print("📱 Configuración:")
    print(f"   - Verify Token: {webhook.verify_token}")
    print(f"   - Access Token: {'✅ Configurado' if webhook.access_token else '❌ No configurado'}")
    print(f"   - Phone Number ID: {'✅ Configurado' if webhook.phone_number_id else '❌ No configurado'}")
    print(f"   - Firebase: {'✅ Conectado' if db else '❌ Desconectado'}")
    print(f"   - OpenAI: {'✅ Configurado' if openai.api_key else '❌ No configurado'}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
