import React, { useEffect, useState } from 'react'
import { Link, useParams, useLocation } from 'react-router-dom'
function Itinerary() {
    const [data, setData] = useState([]);
    const [search, setSearch] = useState("");
    const [duration, setDuration] = useState("");
    const handleClick = () => {

        fetch("/getitinerary/" + search + "/" + duration).then(
            res => res.json()
        ).then(
            data => {
                setData(data.response);
                console.log(data.response);
            }
        )
    }
    return (
        <div className="container my-3">
            <input value={search} onChange={(e) => {
                setSearch(e.target.value)
            }} placeholder='Name of the city you are travelling to' type="text" className="form-control" id="searchText" aria-describedby="emailHelp"></input>
            <input value={duration} onChange={(e) => {
                setDuration(e.target.value)
            }} placeholder='Duration' type="text" className="my-3 form-control" id="durationText" aria-describedby="emailHelp"></input>

            <div className='my-3'>
                <button onClick={handleClick} type='submit' className="btn btn-primary" >Get Itinerary</button>

            </div>
            {data.length != 0 ?
                <>
                    <hr />
                    <h4>Your Personalized travel Itinerary</h4>
                    <hr />
                </>
                : null}
            <ul className="list-group">
                {
                    data.map((item) => {
                        return <li className="list-group-item">{item}</li>
                    })

                }
            </ul>

        </div>
    )
}

export default Itinerary