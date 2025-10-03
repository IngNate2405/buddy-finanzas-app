// Reglas de Firestore con Autenticación
// Máxima seguridad - solo usuarios autenticados

rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Solo usuarios autenticados pueden acceder a sus datos
    match /users/{userId} {
      allow read, write: if 
        request.auth != null && 
        request.auth.uid == userId;
    }
    
    // Regla para datos públicos (si los necesitas)
    match /public/{document} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
