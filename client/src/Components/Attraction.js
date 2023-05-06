import React from 'react'

function Attraction({ location }) {
    return (
        <>
            <div className="card p-3 mb-3">

                <img className="card-img-top" src={location['photoUrl']['url']} alt="Card image cap" />
                <div className="card-body">
                    <h5 className="card-title">{location['name']}</h5>
                    <p className="card-text">{location['description']}</p>
                    <p className="card-text"><small className="text-muted">Number of reviews: {location['numberofreviews']}</small></p>
                </div>
                <div>{location['open_now_text']}</div>
                <a href={location['bookingOptions']['url']}>Book Now!</a>
                <h5>Already Visited?</h5>
                <a href={location['write_review']}>Write A Review!</a>
            </div>
        </>

    )
}

export default Attraction