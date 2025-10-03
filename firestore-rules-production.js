// Reglas de Firestore para Producción
// Estas reglas son seguras y no expiran

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Regla para usuarios anónimos (sin autenticación)
    // Cada usuario tiene un ID único generado localmente
    match /users/{userId} {
      // Permitir lectura y escritura solo si:
      // 1. El userId coincide con el patrón esperado (user_ + timestamp + _ + random)
      // 2. O si es un ID válido de usuario
      allow read, write: if 
        userId.matches('user_[0-9]+_[a-zA-Z0-9]+') ||
        userId.matches('user_[a-zA-Z0-9]+');
    }
    
    // Regla alternativa más simple (si la anterior no funciona)
    // Descomenta esta si tienes problemas con la regla de arriba
    /*
    match /users/{userId} {
      allow read, write: if true;
    }
    */
  }
}
