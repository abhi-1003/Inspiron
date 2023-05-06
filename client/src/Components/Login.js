import React, { useState, useEffect } from 'react'
import { auth, provider, db } from './config'
import { signInWithPopup } from "firebase/auth"
import Home from './Home'
import { doc, setDoc } from "firebase/firestore";

function Login() {
    const [email, setEmail] = useState("")
    const handleClick = async (e) => {
        e.preventDefault();
        signInWithPopup(auth, provider).then(async (data) => {
            setEmail(data.user.email)
            localStorage.setItem("email", data.user.email)
            fetch("/addUser/" + data.user.email).then(
                res => res.json()
            ).then(
                console.log("user added")
            )
        })


    }

    useEffect(() => {
        setEmail(localStorage.getItem("email"))
    })


    return (
        <div>
            {email ? <Home /> :
                <div className="container my-3 p-5">
                    <form>
                        <div className="mb-3">
                            <label htmlFor="exampleInputEmail1" className="form-label">Name</label>
                            <input type="text" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" />
                        </div>
                        <button onClick={handleClick} type="submit" className="btn btn-primary">Sign in with google</button>
                    </form>
                </div>
            }
        </div>
    )
}

export default Login