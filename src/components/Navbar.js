import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="logo">
        <a href="/">PenTest Pilot</a>
      </div>
      <div className="menu">
        <a href="/">Explore</a>
        <a href="/">Features</a>
        <a href="/" className="login-btn">Login</a>
      </div>
    </nav>
  );
}

export default Navbar;
