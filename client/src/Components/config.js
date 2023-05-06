// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
const firebaseConfig = {
    apiKey: "AIzaSyDRC582FlBbZhcdRi6kUSDsoYjRThLm7pw",
    authDomain: "inspiron23-dc43d.firebaseapp.com",
    projectId: "inspiron23-dc43d",
    storageBucket: "inspiron23-dc43d.appspot.com",
    messagingSenderId: "452111001252",
    appId: "1:452111001252:web:aedb4943d9cb1d96c12831",
    measurementId: "G-3KX461QBCV"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();
const provider = new GoogleAuthProvider();
const db = getFirestore(app)
export { auth, provider, db };