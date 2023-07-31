import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import Home from './pages/Home.jsx'
import Dashboard from './pages/Dashboard.jsx'
import OnBoarding from './pages/OnBoarding.jsx'
import Chat from "./pages/Chat.jsx";
import {BrowserRouter, Routes, Route } from 'react-router-dom'


const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={ <Home/>}/>
        <Route path="/dashboard" element={ <Dashboard/>}/>
        <Route path="/onboarding" element={ <OnBoarding/>}/>
          <Route path="/chat" element={ <Chat/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
