import React, { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Attractions from './Components/Attractions';
import Explore from './Components/Explore';

import Home from "./Components/Home"
import Itinerary from "./Components/Itinerary"
import Login from './Components/Login';
import Navbar from './Components/Navbar';
import Register from './Components/Register';
import Slider from "./Components/slider/Slider";


function App() {

  return (
    <>
      <Navbar />
      <Routes>
        <Route index element={<Home />} />
        <Route path="itinerary" element={<Itinerary />} />
        {/* <Route path="getattractions/:city" element={<Attractions />} /> */}
        <Route path="/explore" element={<Explore />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </>

  )
}

export default App
