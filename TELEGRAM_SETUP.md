# 🤖 Configuración de Telegram Bot para Buddy Finanzas

## 📋 Pasos para configurar el bot

### 1. Crear el bot en Telegram

1. **Abre Telegram** y busca `@BotFather`
2. **Envía el comando:** `/newbot`
3. **Nombre del bot:** `Buddy Finanzas Bot`
4. **Username del bot:** `buddy_finanzas_bot` (debe terminar en `_bot`)
5. **Guarda el TOKEN** que te da BotFather

### 2. Configurar el webhook en Netlify

1. **Ve a Netlify Dashboard** → Tu sitio → Environment Variables
2. **Agrega la variable:**
   - **Key:** `TELEGRAM_BOT_TOKEN`
   - **Value:** El token que te dio BotFather

### 3. Configurar el webhook en Telegram

Ejecuta este comando (reemplaza `TU_TOKEN` y `TU_URL`):

```bash
curl -X POST "https://api.telegram.org/botTU_TOKEN/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://TU_SITIO.netlify.app/.netlify/functions/telegram"}'
```

**Ejemplo:**
```bash
curl -X POST "https://api.telegram.org/bot123456789:ABCdefGHIjklMNOpqrsTUVwxyz/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://buddywspserver.netlify.app/.netlify/functions/telegram"}'
```

### 4. Probar el bot

1. **Busca tu bot** en Telegram: `@buddy_finanzas_bot`
2. **Inicia conversación** con el bot
3. **Envía:** `/start`
4. **El bot debe responder** con instrucciones

## 🔧 Funcionalidades del bot

### ✅ Transacciones que reconoce:

**Gastos:**
- "Gasté Q50 en comida"
- "Pagué Q200 de renta"
- "Compré Q30 en supermercado"
- "Debitó Q100 de gasolina"

**Ingresos:**
- "Recibí Q3000 de salario"
- "Gané Q500 de venta"
- "Ingresó Q100 de inversión"

### 📂 Categorías automáticas:

**Gastos:**
- **Food & drinks:** comida, restaurante, supermercado, café
- **Transportation:** gasolina, gas, transporte, taxi, uber, carro
- **Entertainment:** cine, entretenimiento, gym, deporte, fiesta
- **Housing:** renta, servicio, internet, teléfono, luz, agua
- **Lifestyle:** ropa, farmacia, corte, cuidado
- **Miscellaneous:** todo lo demás

**Ingresos:**
- **Income:** salario, trabajo, sueldo, pago
- **Investments:** inversión, interés, dividendo
- **Other:** todo lo demás

## 🔐 Seguridad

- ✅ **Cada usuario** tiene su propio chat con el bot
- ✅ **Solo usuarios vinculados** pueden enviar transacciones
- ✅ **Datos se guardan** solo en la cuenta del usuario
- ✅ **No hay acceso cruzado** entre usuarios

## 🚀 Flujo de uso

1. **Usuario se registra** en la app web
2. **Vincula su Telegram** en Configuración → Telegram
3. **Envía transacciones** al bot
4. **Bot procesa** y guarda en Firebase
5. **Datos aparecen** en la app web

## 🛠️ Troubleshooting

### Bot no responde:
- ✅ Verifica que el TOKEN esté en Netlify Environment Variables
- ✅ Verifica que el webhook esté configurado correctamente
- ✅ Revisa los logs en Netlify Dashboard → Functions

### Usuario no puede vincular:
- ✅ Verifica que el usuario esté autenticado en Firebase
- ✅ Verifica que la colección `telegram_users` exista en Firestore

### Transacciones no se guardan:
- ✅ Verifica que Firebase esté configurado correctamente
- ✅ Verifica que el usuario esté vinculado
- ✅ Revisa los logs de la función `telegram.js`

## 📱 URLs importantes

- **Webhook:** `https://TU_SITIO.netlify.app/.netlify/functions/telegram`
- **Health check:** `https://TU_SITIO.netlify.app/.netlify/functions/health`
- **Bot en Telegram:** `@buddy_finanzas_bot`

## 🔄 Actualizar webhook

Si cambias la URL del webhook, ejecuta:

```bash
curl -X POST "https://api.telegram.org/botTU_TOKEN/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "NUEVA_URL"}'
```

## 🗑️ Eliminar webhook

```bash
curl -X POST "https://api.telegram.org/botTU_TOKEN/deleteWebhook"
```
