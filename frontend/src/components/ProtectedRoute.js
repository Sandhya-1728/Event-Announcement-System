import React, { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const ProtectedRoute = () => {
    const { isAuthenticated, loading } = useContext(AuthContext);

    // Show loading state while checking authentication
    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    // Redirect to login if not authenticated
    return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoute; 