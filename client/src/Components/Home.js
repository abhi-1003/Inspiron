
import React, { useState, useEffect } from 'react'
import { Outlet, Link } from "react-router-dom";
import Attraction from './Attraction';
import Recommendation from './Recommendation';
import Slider from './slider/Slider'

function Home() {


    const [recoms, setRecoms] = useState([]);
    const [email, setEmail] = useState("default")

    useEffect(() => {
        setEmail(localStorage.getItem("email"))
        console.log(email)
        // console.log("fetching")

    }, [])

    useEffect(() => {
        console.log(email)
        if (email != "default") {
            console.log("fetching")
            fetch("/getRecommendations/" + email).then(
                res => res.json()
            ).then(
                data => {
                    setRecoms(data.recoms);
                    console.log(data.recoms);
                }
            )
        }
    }, [email])


    return (
        <>
            <Slider />

            <div className='container my-4' >
                <h4>Personalised Recommendations based on your previous searches</h4>
                <hr />
                {recoms.map((recom) => {
                    return <div key={recom.name}><Recommendation location={recom} /></div>
                })}

            </div>

        </>
    )
}

export default Home