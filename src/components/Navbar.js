import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('user'); // Eliminar datos del usuario.
        navigate('/');
    };

    return (
        <nav style={{ padding: '10px', backgroundColor: '#f4f4f4' }}>
            
            <button onClick={handleLogout} style={{ marginLeft: '50px' }}>Cerrar Sesión</button>
        </nav>
    );
}

export default Navbar;
