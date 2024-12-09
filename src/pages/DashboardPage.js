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
        <div style={{ padding: '20px' }}>
            <Navbar />
            <h1>Dashboard</h1>
            <p>Bienvenido, {user?.username || 'Usuario'}</p>
            <p>Rol: {user?.Tipo || 'N/A'}</p>

            {/* Opciones para Administrador */}
            {user?.Tipo === 'Administrador' && (
                <div>
                    <h2>Opciones de Administrador</h2>
                    <ul>
                        <li>
                            <button onClick={() => navigate('/gestion-usuarios-departamentos')}>
                                Gestionar Usuarios
                            </button>
                        </li>
                        <li>
                            <button onClick={() => navigate('/review-claims')}>
                                Revisar Reclamos
                            </button>
                        </li>
                        <li>
                            <button onClick={() => navigate('/reports')}>
                                Ver Informes
                            </button>
                        </li>
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

            {/* Opciones para Usuario */}
            {user?.Tipo === 'Usuario' && (
                <div>
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
