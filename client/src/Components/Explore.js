
import React, { useState, useEffect } from 'react'
import { Outlet, Link } from "react-router-dom";
import Attraction from './Attraction';
import Slider from './slider/Slider';


function Explore() {

    const [city, setCity] = useState("");
    const [email, setEmail] = useState("default")
    const [locations, setLocations] = useState([]);

    const handleClick = () => {
        console.log(email)
        fetch("/getattractions/" + city + "/" + email).then(
            res => res.json()
        ).then(
            data => {
                setLocations(data.locations);
                console.log(data.locations);
            }
        )
    }

    useEffect(() => {
        setEmail(localStorage.getItem("email"))

    }, [])

    return (
        <>
            <Slider />


            <div className="container my-3">
                <input value={city} onChange={(e) => {
                    setCity(e.target.value)
                }} placeholder='search for city' type="text" className="form-control" id="cityText" aria-describedby="emailHelp"></input>
                <div className='my-3'>
                    <button onClick={handleClick} type='submit' className="btn btn-primary" >Get Attractions</button>
                </div>

                <div className="my-3">
                    {locations.map((location) => {
                        return <div className='container my-4' key={location.name}>
                            <Attraction location={location} />
                        </div>
                    })}
                </div>
            </div>

        </>
    )
}

export default Explore