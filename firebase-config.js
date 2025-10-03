// Firebase configuration
// Configuración real de tu proyecto Firebase
const firebaseConfig = {
  apiKey: "AIzaSyCWRROAhqFeKks0X8aPuhTqb_aieJJh9Io",
  authDomain: "buddy-finanzas.firebaseapp.com",
  projectId: "buddy-finanzas",
  storageBucket: "buddy-finanzas.firebasestorage.app",
  messagingSenderId: "336603674170",
  appId: "1:336603674170:web:fa9c67f7e8b6d6f673a703"
};

// Initialize Firebase
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getFirestore, collection, doc, setDoc, getDoc, addDoc, updateDoc, deleteDoc, query, where, orderBy, onSnapshot } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

let app, db, auth;

try {
  app = initializeApp(firebaseConfig);
  db = getFirestore(app);
  auth = getAuth(app);
} catch (error) {
  console.error('Error initializing Firebase:', error);
  // Fallback configuration for development
  const fallbackConfig = {
    apiKey: "demo-key",
    authDomain: "demo.firebaseapp.com",
    projectId: "demo-project",
    storageBucket: "demo.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:demo"
  };
  app = initializeApp(fallbackConfig, 'fallback');
  db = getFirestore(app);
  auth = getAuth(app);
}

// Firebase service class
class FirebaseService {
  constructor() {
    this.db = db;
    this.auth = auth;
    this.userId = null;
  }

  // Get current user ID from auth
  getUserId() {
    // Check if in development mode
    if (localStorage.getItem('devMode') === 'true') {
      return localStorage.getItem('userId') || 'dev_user';
    }
    
    const user = this.auth.currentUser;
    return user ? user.uid : null;
  }

  // Set user ID (called after authentication)
  setUserId(userId) {
    this.userId = userId;
  }

  // Authentication methods
  async signIn(email, password) {
    try {
      if (!this.auth) {
        throw new Error('Firebase Auth no está disponible');
      }
      const userCredential = await signInWithEmailAndPassword(this.auth, email, password);
      this.setUserId(userCredential.user.uid);
      return userCredential.user;
    } catch (error) {
      console.error('Error en signIn:', error);
      throw error;
    }
  }

  async signUp(email, password) {
    try {
      if (!this.auth) {
        throw new Error('Firebase Auth no está disponible');
      }
      const userCredential = await createUserWithEmailAndPassword(this.auth, email, password);
      this.setUserId(userCredential.user.uid);
      return userCredential.user;
    } catch (error) {
      console.error('Error en signUp:', error);
      throw error;
    }
  }

  async signOut() {
    try {
      await signOut(this.auth);
      this.userId = null;
    } catch (error) {
      throw error;
    }
  }

  // Listen to auth state changes
  onAuthStateChanged(callback) {
    return onAuthStateChanged(this.auth, callback);
  }

  // Get current user
  getCurrentUser() {
    try {
      if (!this.auth) {
        return null;
      }
      return this.auth.currentUser;
    } catch (error) {
      console.error('Error getting current user:', error);
      return null;
    }
  }

  // Save transactions to Firestore
  async saveTransactions(transactions) {
    try {
      // Check if in development mode
      if (localStorage.getItem('devMode') === 'true') {
        localStorage.setItem('transactions', JSON.stringify(transactions));
        return;
      }
      
      const userDocRef = doc(this.db, 'users', this.userId);
      
      // Get existing document to preserve other fields
      const docSnap = await getDoc(userDocRef);
      const existingData = docSnap.exists() ? docSnap.data() : {};
      
      // Update only the transactions field and lastUpdated
      await setDoc(userDocRef, {
        ...existingData, // Preserve existing data (categories, etc.)
        transactions: transactions,
        lastUpdated: new Date()
      }, { merge: true });
      
      
      // Verify the save by reading back
      const verifySnap = await getDoc(userDocRef);
      if (verifySnap.exists()) {
        const verifyData = verifySnap.data();
      }
      
    } catch (error) {
      throw error; // Re-throw to be caught by caller
    }
  }

  // Load transactions from Firestore
  async loadTransactions() {
    try {
      // Check if in development mode
      if (localStorage.getItem('devMode') === 'true') {
        const transactions = JSON.parse(localStorage.getItem('transactions') || '[]');
        return transactions;
      }
      
      const userDocRef = doc(this.db, 'users', this.userId);
      const docSnap = await getDoc(userDocRef);
      
      if (docSnap.exists()) {
        const data = docSnap.data();
        return Array.isArray(data.transactions) ? data.transactions : [];
      } else {
        return [];
      }
    } catch (error) {
      return [];
    }
  }

  // Save categories to Firestore
  async saveCategories(categories) {
    try {
      const userDocRef = doc(this.db, 'users', this.userId);
      await setDoc(userDocRef, {
        categories: categories,
        lastUpdated: new Date()
      }, { merge: true });
    } catch (error) {
    }
  }

  // Load categories from Firestore
  async loadCategories() {
    try {
      // Check if in development mode
      if (localStorage.getItem('devMode') === 'true') {
        const categories = JSON.parse(localStorage.getItem('categoriesData') || '{}');
        return categories;
      }
      
      const userDocRef = doc(this.db, 'users', this.userId);
      const docSnap = await getDoc(userDocRef);
      
      if (docSnap.exists()) {
        const data = docSnap.data();
        return data.categories || {};
      } else {
        return {};
      }
    } catch (error) {
      return {};
    }
  }

  // Save current month
  async saveCurrentMonth(month, year) {
    try {
      const userDocRef = doc(this.db, 'users', this.userId);
      await setDoc(userDocRef, {
        currentMonth: month,
        currentYear: year,
        lastUpdated: new Date()
      }, { merge: true });
    } catch (error) {
    }
  }

  // Load current month
  async loadCurrentMonth() {
    try {
      const userDocRef = doc(this.db, 'users', this.userId);
      const docSnap = await getDoc(userDocRef);
      
      if (docSnap.exists()) {
        const data = docSnap.data();
        return {
          month: data.currentMonth || new Date().getMonth(),
          year: data.currentYear || new Date().getFullYear()
        };
      } else {
        return {
          month: new Date().getMonth(),
          year: new Date().getFullYear()
        };
      }
    } catch (error) {
      return {
        month: new Date().getMonth(),
        year: new Date().getFullYear()
      };
    }
  }

  // Sync all data to Firestore
  async syncToFirestore() {
    try {
      const transactions = JSON.parse(localStorage.getItem('transactions') || '[]');
      const categories = JSON.parse(localStorage.getItem('categoriesData') || '{}');
      const currentMonth = JSON.parse(localStorage.getItem('currentMonth') || '{}');

      await this.saveTransactions(transactions);
      await this.saveCategories(categories);
      
      if (currentMonth.month !== undefined && currentMonth.year !== undefined) {
        await this.saveCurrentMonth(currentMonth.month, currentMonth.year);
      }

    } catch (error) {
    }
  }

  // Load all data from Firestore
  async loadFromFirestore() {
    try {
      const transactions = await this.loadTransactions();
      const categories = await this.loadCategories();
      const currentMonth = await this.loadCurrentMonth();

      // Update localStorage
      localStorage.setItem('transactions', JSON.stringify(transactions));
      localStorage.setItem('categoriesData', JSON.stringify(categories));
      localStorage.setItem('currentMonth', JSON.stringify(currentMonth));

      return { transactions, categories, currentMonth };
    } catch (error) {
      return { transactions: [], categories: {}, currentMonth: { month: new Date().getMonth(), year: new Date().getFullYear() } };
    }
  }
}

// Export for use in other files
window.FirebaseService = FirebaseService;

// ES6 module export
export { FirebaseService };
