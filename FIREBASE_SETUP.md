# 🔥 Configuración de Firebase Firestore

## Pasos para configurar Firebase en tu aplicación

### 1. Crear proyecto en Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Haz clic en **"Crear un proyecto"**
3. Nombra tu proyecto: `buddy-finanzas` (o el nombre que prefieras)
4. Desactiva Google Analytics (opcional)
5. Haz clic en **"Crear proyecto"**

### 2. Configurar Firestore Database

1. En el panel izquierdo, haz clic en **"Firestore Database"**
2. Haz clic en **"Crear base de datos"**
3. Selecciona **"Comenzar en modo de prueba"** (por ahora)
4. Elige una ubicación cercana (ej: `us-central1`)

### 3. Obtener configuración de Firebase

1. Haz clic en el ícono de configuración (⚙️) → **"Configuración del proyecto"**
2. Ve a la pestaña **"General"**
3. En **"Tus apps"**, haz clic en el ícono web (</>)
4. Registra tu app con el nombre: `buddy-finanzas-web`
5. **Copia la configuración** que te da

### 4. Actualizar configuración en tu app

1. Abre el archivo `firebase-config.js`
2. Reemplaza la configuración de ejemplo con la tuya:

```javascript
const firebaseConfig = {
  apiKey: "tu-api-key-real",
  authDomain: "tu-proyecto-real.firebaseapp.com",
  projectId: "tu-proyecto-real-id",
  storageBucket: "tu-proyecto-real.appspot.com",
  messagingSenderId: "123456789",
  appId: "tu-app-id-real"
};
```

### 5. Configurar reglas de seguridad (opcional)

En Firebase Console → Firestore Database → Reglas:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Permitir lectura y escritura solo a usuarios autenticados
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Para modo de prueba (temporal)
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

## 🚀 Funcionalidades implementadas

### ✅ Sincronización automática
- **Auto-sync cada 30 segundos**
- **Sync cuando cambias datos** (transacciones, categorías, mes actual)
- **Botón de sincronización manual** en la interfaz

### ✅ Datos sincronizados
- **Transacciones**: Todas tus transacciones se guardan en la nube
- **Categorías**: Tus categorías personalizadas se sincronizan
- **Mes actual**: El mes que estás viendo se recuerda
- **ID de usuario único**: Cada usuario tiene sus propios datos

### ✅ Funcionamiento offline
- **LocalStorage como respaldo**: Si no hay internet, funciona con datos locales
- **Sincronización automática**: Cuando vuelve la conexión, se sincroniza automáticamente

## 🎯 Cómo usar

1. **Configura Firebase** siguiendo los pasos arriba
2. **Abre tu aplicación** en el navegador
3. **Verás un botón azul** (☁️) en la parte superior derecha
4. **Haz clic en el botón** para sincronizar manualmente
5. **Los datos se sincronizan automáticamente** cada 30 segundos

## 📊 Estructura de datos en Firestore

```javascript
// Colección: users
// Documento: user_1234567890_abc123def
{
  transactions: [
    {
      id: 1757748736049,
      amount: 100,
      type: "income",
      category: "salary",
      date: "2025-01-15",
      note: "Pago mensual"
    }
  ],
  categories: {
    "salary": {
      name: "Salary",
      icon: "fas fa-money-bill",
      color: "bg-green-400"
    }
  },
  currentMonth: 0, // Enero
  currentYear: 2025,
  lastUpdated: "2025-01-15T10:30:00Z"
}
```

## 🔧 Solución de problemas

### Error: "Firebase not initialized"
- Verifica que la configuración en `firebase-config.js` sea correcta
- Asegúrate de que el proyecto Firebase esté activo

### Error: "Permission denied"
- Verifica las reglas de Firestore
- Asegúrate de que estén en modo de prueba temporalmente

### Los datos no se sincronizan
- Verifica la conexión a internet
- Revisa la consola del navegador para errores
- Haz clic en el botón de sincronización manual

## 💰 Costos

- **Gratis hasta**: 50,000 lecturas/día, 20,000 escrituras/día
- **Para una app personal**: Completamente gratis
- **Para múltiples usuarios**: Muy económico

## 🎉 ¡Listo!

Tu aplicación ahora tiene:
- ✅ **Respaldo en la nube**
- ✅ **Sincronización automática**
- ✅ **Funcionamiento offline**
- ✅ **Datos seguros y persistentes**

¡Disfruta de tu app de finanzas con respaldo en la nube! 🚀
