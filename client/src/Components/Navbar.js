
import React, { useState, useEffect } from 'react'
import { Outlet, Link } from "react-router-dom";

function Navbar() {

    const [email, setEmail] = useState("")

    const handleLogOut = () => {
        localStorage.clear()
        setEmail("")
    }

    useEffect(() => {
        setEmail(localStorage.getItem("email"))
    })
    return (
        <>
            <nav className="navbar navbar-expand-lg bg-body-tertiary">
                <div className="container-fluid">
                    <a className="navbar-brand" href="#">OnlyHacks Travel Guide</a>
                    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            <li className="nav-item">
                                <Link className="nav-link" aria-current="page" to="/">Home</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" aria-current="page" to="/explore">Explore</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link" aria-current="page" to="/itinerary">Plan your trip</Link>
                            </li>
                            {
                                !email ? <li className="nav-item">
                                    <Link className='nav-link' aria-current="page" to="/login">Login</Link>
                                </li> :
                                    <li className="nav-item">
                                        <button onClick={handleLogOut} type='submit' className=" d-flex btn btn-primary" >Log Out</button>
                                    </li>
                            }
                        </ul>
                    </div>
                </div>
            </nav>

        </>
    )
}

export default Navbar