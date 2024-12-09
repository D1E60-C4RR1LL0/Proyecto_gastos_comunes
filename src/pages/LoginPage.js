import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function LoginPage() {
    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    // En el handleLogin de LoginPage.js
    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            // Enviar solicitud al backend para iniciar sesión
            const response = await api.post('/acceso/login', {
                username: username,
                password: password,
            });

            // Guardar la información del usuario autenticado en localStorage
            const user = {
                username: username,
                Tipo: response.data.Tipo, // Asegúrate de que el backend devuelva el tipo de usuario
            };
            localStorage.setItem('user', JSON.stringify(user));

            // Mostrar mensaje de éxito y redirigir
            setMessage('Inicio de sesión exitoso');
            setTimeout(() => navigate('/dashboard'), 1000); // Redirige al Dashboard
        } catch (error) {
            // Manejo de errores en el inicio de sesión
            setMessage(error.response?.data?.error || 'Error en el inicio de sesión');
        }
    };


    const handleRegisterRedirect = () => {
        navigate('/register');
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Inicio de Sesión</h1>
            <form onSubmit={handleLogin}>
                <div>
                    <label>Nombre de Usuario:</label>
                    <input
                        type="text"
                        placeholder="Ingresa tu nombre de usuario"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Contraseña:</label>
                    <input
                        type="password"
                        placeholder="Ingresa tu contraseña"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Iniciar Sesión</button>
            </form>
            {message && <p style={{ marginTop: '10px', color: 'green' }}>{message}</p>}
            <button onClick={handleRegisterRedirect} style={{ marginTop: '10px' }}>
                ¿No tienes una cuenta? Regístrate aquí
            </button>
        </div>
    );
}

export default LoginPage;
