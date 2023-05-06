import React, { useEffect, useState } from 'react'
import { Link, useParams, useLocation } from 'react-router-dom'
import Attraction from './Attraction';
function Attractions() {
    const { city } = useParams();

    const [locations, setLocations] = useState([]);

    useEffect(() => {
        fetch("/getattractions/" + city).then(
            res => res.json()
        ).then(
            data => {
                setLocations(data.locations);
                console.log(data.locations);
            }
        )
    }, [])
    return (

        <>
            {locations.map((location) => {
                return <div className='container my-4' key={location.name}>
                    <Attraction location={location} />
                </div>
            })}
        </>
    )
}

export default Attractions