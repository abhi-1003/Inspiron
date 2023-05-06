import firebase from "firebase"
import "firebase/firestore"

// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDRC582FlBbZhcdRi6kUSDsoYjRThLm7pw",
    authDomain: "inspiron23-dc43d.firebaseapp.com",
    projectId: "inspiron23-dc43d",
    storageBucket: "inspiron23-dc43d.appspot.com",
    messagingSenderId: "452111001252",
    appId: "1:452111001252:web:aedb4943d9cb1d96c12831",
    measurementId: "G-3KX461QBCV"
};

firebase.initializeApp(firebaseConfig)

export default firebase