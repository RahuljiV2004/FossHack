import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import ScanResults from './components/ScanResults';
import './index.css';

function App() {
  return (
    <Router>
      <Navbar />
      <Features/>
      <Routes>
        <Route path="/" element={<Hero />} />
        <Route path="/scanresults" element={<ScanResults />} />
      </Routes>
      
    </Router>
  );
}

export default App;
