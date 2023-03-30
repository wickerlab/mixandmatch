import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import OnBoarding from './pages/OnBoarding'
import {BrowserRouter, Routes, Route } from 'react-router-dom'

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={ <Home/>}/>
        <Route path="/dashboard" element={ <Dashboard/>}/>
        <Route path="/onboarding" element={ <OnBoarding/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
