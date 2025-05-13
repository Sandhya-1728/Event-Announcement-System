import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import EventList from './components/EventList';
import EventForm from './components/EventForm';
import SubscribeForm from './components/SubscribeForm';

function App() {
    return (
        <Router>
            <div className="App">
                <Navbar />
                <main className="container">
                    <Routes>
                        <Route path="/" element={<EventList />} />
                        <Route path="/submit" element={<EventForm />} />
                        <Route path="/subscribe" element={<SubscribeForm />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
}

export default App; 