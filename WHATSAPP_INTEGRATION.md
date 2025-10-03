# Integración WhatsApp Business - Buddy Finanzas

Esta integración permite recibir transacciones a través de WhatsApp Business y procesarlas automáticamente en tu aplicación de finanzas personales.

## 🚀 Características

- **Reconocimiento automático** de transacciones en mensajes de WhatsApp
- **Clasificación inteligente** de categorías usando IA (OpenAI)
- **Detección automática** de tipo de transacción (ingreso/gasto)
- **Sincronización** con la base de datos existente
- **Interfaz web** para configuración y monitoreo

## 📋 Requisitos

- Python 3.8+
- Cuenta de WhatsApp Business
- Cuenta en Meta for Developers
- (Opcional) API Key de OpenAI para clasificación avanzada

## 🛠️ Instalación

### 1. Configuración Automática

```bash
# Ejecutar script de configuración
python setup-whatsapp.py
```

### 2. Configuración Manual

```bash
# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de configuración
cp whatsapp-config.env .env
```

## ⚙️ Configuración

### 1. Variables de Entorno

Edita el archivo `.env` con tus credenciales:

```env
# WhatsApp Business API
WHATSAPP_VERIFY_TOKEN=buddy_finanzas_webhook
WHATSAPP_ACCESS_TOKEN=tu_token_de_acceso
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id

# OpenAI (opcional)
OPENAI_API_KEY=sk-tu_api_key_aqui
```

### 2. Configuración de WhatsApp Business

1. **Crear App en Meta for Developers**
   - Ve a [developers.facebook.com](https://developers.facebook.com)
   - Crea una nueva app
   - Agrega el producto "WhatsApp Business API"

2. **Obtener Credenciales**
   - Access Token: En la sección de WhatsApp > API Setup
   - Phone Number ID: En la sección de WhatsApp > API Setup

3. **Configurar Webhook**
   - URL del webhook: `https://tu-dominio.com/webhook`
   - Verify Token: `buddy_finanzas_webhook`
   - Suscribirse a eventos: `messages`

### 3. Configuración de Firebase (Opcional)

Si quieres usar Firebase para almacenar las transacciones:

```bash
# Descargar credenciales de Firebase
# Guardar como firebase-credentials.json
```

## 🚀 Uso

### 1. Iniciar Servidor

```bash
python start-whatsapp.py
```

### 2. Configurar Túnel (Desarrollo)

Para desarrollo local, usa ngrok:

```bash
# Instalar ngrok
# https://ngrok.com/download

# Crear túnel
ngrok http 5000

# Usar la URL de ngrok como webhook
# Ejemplo: https://abc123.ngrok.io/webhook
```

### 3. Enviar Mensajes de Prueba

Envía mensajes a tu número de WhatsApp Business:

```
Gasté Q100 en comida
Compré Q50 de gasolina
Recibí Q1000 de salario
Pagué Q200 de renta
```

## 📱 Interfaz Web

Accede a la configuración en: `whatsapp-settings.html`

- **Estado de conexión**
- **Configuración de credenciales**
- **Transacciones recientes**
- **Pruebas de integración**

## 🤖 Clasificación Automática

### Patrones Reconocidos

**Gastos:**
- "Gasté Q100 en comida"
- "Compré Q50 de gasolina"
- "Pagué Q200 de renta"
- "Q100 en restaurante"

**Ingresos:**
- "Recibí Q1000 de salario"
- "Gané Q500"
- "Ingresó Q2000"

### Categorías Automáticas

- **Food & drinks**: comida, restaurante, supermercado
- **Transportation**: gasolina, transporte, taxi
- **Entertainment**: cine, entretenimiento, gym
- **Housing**: renta, servicios, internet
- **Lifestyle**: ropa, farmacia, cuidado personal
- **Miscellaneous**: otros gastos

## 🔧 API Endpoints

### Webhook
```
POST /webhook
GET /webhook?hub.mode=subscribe&hub.verify_token=...&hub.challenge=...
```

### Health Check
```
GET /health
```

## 📊 Estructura de Datos

### Transacción Procesada
```json
{
  "amount": 100,
  "type": "expense",
  "category": "Food & drinks",
  "description": "Gasté Q100 en comida",
  "date": "2024-01-15T10:30:00",
  "source": "whatsapp",
  "phone_number": "+50212345678"
}
```

## 🐛 Solución de Problemas

### Error: "Firebase no disponible"
- Verifica las credenciales de Firebase
- Asegúrate de que el archivo `firebase-credentials.json` existe

### Error: "WhatsApp no configurado"
- Verifica las variables de entorno
- Asegúrate de que el Access Token es válido

### Error: "Webhook no verificado"
- Verifica que la URL del webhook es correcta
- Asegúrate de que el Verify Token coincide

## 📈 Monitoreo

### Logs del Servidor
```bash
# Ver logs en tiempo real
tail -f whatsapp-webhook.log
```

### Estado de Conexión
- Verde: Configurado y funcionando
- Rojo: Desconectado o error
- Amarillo: Configuración incompleta

## 🔒 Seguridad

- Las credenciales se almacenan en variables de entorno
- Los tokens de WhatsApp tienen expiración
- Las transacciones se validan antes de guardar
- El webhook verifica la autenticidad de los mensajes

## 📚 Recursos Adicionales

- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Meta for Developers](https://developers.facebook.com/)
- [OpenAI API](https://platform.openai.com/)
- [ngrok](https://ngrok.com/)

## 🤝 Soporte

Si tienes problemas con la integración:

1. Verifica los logs del servidor
2. Comprueba la configuración de variables de entorno
3. Asegúrate de que el webhook está correctamente configurado
4. Prueba con mensajes simples primero

---

**¡Disfruta de la automatización de tus finanzas con WhatsApp! 🎉**
