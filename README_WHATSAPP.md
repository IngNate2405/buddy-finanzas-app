# 📱 Integración WhatsApp Business - Buddy Finanzas

¡Automatiza tus finanzas personales con WhatsApp! Envía mensajes de transacciones y se procesarán automáticamente en tu aplicación.

## ✨ Características

- 🤖 **Reconocimiento automático** de transacciones en mensajes
- 🧠 **Clasificación inteligente** usando IA (OpenAI)
- 📊 **Sincronización** con tu aplicación existente
- 🎯 **Detección automática** de tipo (ingreso/gasto)
- 📱 **Interfaz web** para configuración

## 🚀 Inicio Rápido

### 1. Configuración Automática
```bash
# Ejecutar configuración
python setup-whatsapp.py
```

### 2. Configurar Variables
Edita el archivo `.env`:
```env
WHATSAPP_ACCESS_TOKEN=tu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=tu_phone_id_aqui
OPENAI_API_KEY=sk-tu_key_aqui  # Opcional
```

### 3. Iniciar Servidor
```bash
# Windows
start-whatsapp.bat

# Linux/Mac
./start-whatsapp.sh
```

## 📱 Cómo Usar

### Enviar Transacciones por WhatsApp

Envía mensajes a tu número de WhatsApp Business:

**Gastos:**
- "Gasté Q100 en comida"
- "Compré Q50 de gasolina"
- "Pagué Q200 de renta"
- "Q100 en restaurante"

**Ingresos:**
- "Recibí Q1000 de salario"
- "Gané Q500"
- "Ingresó Q2000"

### Respuesta Automática

La aplicación responderá con:
```
✅ Transacción registrada:
💰 Gasto: Q100
📂 Categoría: Food & drinks
📝 Descripción: Gasté Q100 en comida
```

## 🛠️ Configuración Detallada

### 1. WhatsApp Business API

1. **Crear App en Meta for Developers**
   - Ve a [developers.facebook.com](https://developers.facebook.com)
   - Crea nueva app → WhatsApp Business API

2. **Obtener Credenciales**
   - Access Token: WhatsApp > API Setup
   - Phone Number ID: WhatsApp > API Setup

3. **Configurar Webhook**
   - URL: `https://tu-dominio.com/webhook`
   - Verify Token: `buddy_finanzas_webhook`
   - Eventos: `messages`

### 2. Desarrollo Local (ngrok)

```bash
# Instalar ngrok
# https://ngrok.com/download

# Crear túnel
ngrok http 5000

# Usar URL de ngrok como webhook
# Ejemplo: https://abc123.ngrok.io/webhook
```

### 3. OpenAI (Opcional)

Para clasificación avanzada:
1. Crear cuenta en [OpenAI](https://platform.openai.com)
2. Generar API Key
3. Agregar al archivo `.env`

## 📊 Categorías Automáticas

### Gastos
- **Food & drinks**: comida, restaurante, supermercado
- **Transportation**: gasolina, transporte, taxi
- **Entertainment**: cine, entretenimiento, gym
- **Housing**: renta, servicios, internet
- **Lifestyle**: ropa, farmacia, cuidado personal
- **Miscellaneous**: otros gastos

### Ingresos
- **Income**: salario, trabajo
- **Investments**: inversiones, intereses
- **Other**: otros ingresos

## 🔧 Interfaz Web

Accede a `whatsapp-settings.html` para:
- ✅ Estado de conexión
- ⚙️ Configuración de credenciales
- 📊 Transacciones recientes
- 🧪 Pruebas de integración

## 📁 Estructura de Archivos

```
├── whatsapp-webhook.py          # Servidor principal
├── whatsapp-settings.html       # Interfaz de configuración
├── setup-whatsapp.py            # Script de configuración
├── start-whatsapp.bat           # Inicio en Windows
├── start-whatsapp.sh            # Inicio en Linux/Mac
├── requirements.txt                # Dependencias Python
├── whatsapp-config.env         # Plantilla de configuración
└── WHATSAPP_INTEGRATION.md    # Documentación completa
```

## 🐛 Solución de Problemas

### Error: "Firebase no disponible"
```bash
# Verificar credenciales de Firebase
# Archivo: firebase-credentials.json
```

### Error: "WhatsApp no configurado"
```bash
# Verificar variables de entorno
# Archivo: .env
```

### Error: "Webhook no verificado"
```bash
# Verificar URL del webhook
# Verificar Verify Token
```

## 📈 Monitoreo

### Logs del Servidor
```bash
# Ver logs en tiempo real
tail -f whatsapp-webhook.log
```

### Estado de Conexión
- 🟢 Verde: Funcionando
- 🔴 Rojo: Error
- 🟡 Amarillo: Configuración incompleta

## 🔒 Seguridad

- ✅ Credenciales en variables de entorno
- ✅ Tokens con expiración
- ✅ Validación de transacciones
- ✅ Verificación de webhook

## 📚 Recursos

- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Meta for Developers](https://developers.facebook.com/)
- [OpenAI API](https://platform.openai.com/)
- [ngrok](https://ngrok.com/)

## 🤝 Soporte

Si tienes problemas:

1. ✅ Verifica los logs del servidor
2. ✅ Comprueba la configuración
3. ✅ Asegúrate de que el webhook está configurado
4. ✅ Prueba con mensajes simples

---

**¡Disfruta de la automatización de tus finanzas! 🎉**
