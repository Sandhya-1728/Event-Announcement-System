import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        // Check if user is logged in
        const token = localStorage.getItem('token');
        const userData = localStorage.getItem('user');

        if (token && userData) {
            setIsLoggedIn(true);
            setUser(JSON.parse(userData));
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setIsLoggedIn(false);
        setUser(null);
        navigate('/login');
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-logo">
                    Event Announcements
                </Link>
                <div className="navbar-menu">
                    <Link to="/" className="navbar-item">Home</Link>
                    <Link to="/submit" className="navbar-item">Submit Event</Link>
                    <Link to="/subscribe" className="navbar-item">Subscribe</Link>

                    {isLoggedIn ? (
                        <div className="navbar-auth">
                            <span className="navbar-welcome">Welcome, {user?.name}</span>
                            <button onClick={handleLogout} className="navbar-button">Logout</button>
                        </div>
                    ) : (
                        <div className="navbar-auth">
                            <Link to="/login" className="navbar-button">Login</Link>
                            <Link to="/register" className="navbar-button">Register</Link>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
}

export default Navbar; 