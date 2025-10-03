@echo off
echo 🚀 Iniciando WhatsApp Webhook para Buddy Finanzas...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 📥 Descarga Python desde: https://python.org/downloads/
    pause
    exit /b 1
)

REM Verificar si el archivo de configuración existe
if not exist "whatsapp-webhook.py" (
    echo ❌ Archivo whatsapp-webhook.py no encontrado
    echo 📁 Asegúrate de estar en el directorio correcto
    pause
    exit /b 1
)

REM Instalar dependencias si es necesario
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

echo 📦 Instalando dependencias...
pip install -r requirements.txt

echo.
echo 🚀 Iniciando servidor de WhatsApp...
echo 📱 El servidor estará disponible en: http://localhost:5000
echo 🔗 Webhook URL: http://localhost:5000/webhook
echo.
echo ⚠️  Para desarrollo, usa ngrok para crear un túnel público
echo 📖 Instrucciones completas en: WHATSAPP_INTEGRATION.md
echo.

python whatsapp-webhook.py

pause
