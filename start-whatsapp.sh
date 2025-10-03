#!/bin/bash

echo "🚀 Iniciando WhatsApp Webhook para Buddy Finanzas..."
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "📥 Instala Python3 desde tu gestor de paquetes"
    exit 1
fi

# Verificar si el archivo de configuración existe
if [ ! -f "whatsapp-webhook.py" ]; then
    echo "❌ Archivo whatsapp-webhook.py no encontrado"
    echo "📁 Asegúrate de estar en el directorio correcto"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

echo "🔧 Activando entorno virtual..."
source venv/bin/activate

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo
echo "🚀 Iniciando servidor de WhatsApp..."
echo "📱 El servidor estará disponible en: http://localhost:5000"
echo "🔗 Webhook URL: http://localhost:5000/webhook"
echo
echo "⚠️  Para desarrollo, usa ngrok para crear un túnel público"
echo "📖 Instrucciones completas en: WHATSAPP_INTEGRATION.md"
echo

python3 whatsapp-webhook.py
