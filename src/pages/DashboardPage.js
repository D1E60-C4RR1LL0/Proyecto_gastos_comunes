import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

function DashboardPage() {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Obtén el usuario desde localStorage
        const userData = JSON.parse(localStorage.getItem('user'));

        if (!userData) {
            // Redirige al login si no hay usuario
            navigate('/');
        } else {
            setUser(userData);
        }
    }, [navigate]);

    if (!user) {
        return <p>Cargando...</p>;
    }

    return (
        <div className="dashboard-container">
    <Navbar />
    <h1>Dashboard</h1>
    <p>Bienvenido, {user?.username || 'Usuario'}</p>
    <p>Rol: {user?.Tipo || 'N/A'}</p>

    {user?.Tipo === 'Administrador' && (
        <div className="admin-options">
            <h2>Opciones de Administrador</h2>
            <ul className="dash">
                <li>
                    <button onClick={() => navigate('/generar-gastos-comunes')}>
                        Generar Gastos Comunes
                    </button>
                </li>
                <li>
                    <button onClick={() => navigate('/lista-departamentos')}>
                        Pagar Gastos Comunes
                    </button>
                </li>
                <li>
                    <button onClick={() => navigate('/mis-gastos-comunes')}>
                        Gastos pendientes
                    </button>
                </li>
            </ul>
        </div>
    )}

    {user?.Tipo === 'Usuario' && (
        <div className="user-options">
            <h2>Opciones del Usuario</h2>
            <ul>
                <li>
                    <button onClick={() => navigate('/payments')}>
                        Mis Pagos
                    </button>
                </li>
                <li>
                    <button onClick={() => navigate('/claims')}>
                        Reclamos
                    </button>
                </li>
                <li>
                    <button onClick={() => navigate('/profile')}>
                        Perfil
                    </button>
                </li>
            </ul>
        </div>
    )}
</div>
    );
}

export default DashboardPage;
