import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function RegisterPage() {
    const navigate = useNavigate();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [rut, setRut] = useState('');
    const [tipo, setTipo] = useState('residente'); // Valor predeterminado para el tipo de usuario
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        setMessage('');
        setError('');
    
        try {
            const response = await api.post('/acceso', {
                username: username,
                password: password,
                Tipo: tipo, 
                Rut: rut
            });
    
            setMessage(response.data.message);
            setTimeout(() => navigate('/'), 1000);
        } catch (error) {
            if (error.response) {
                if (error.response.status === 400) {
                    setError('Faltan campos requeridos. Revisa tus datos.');
                } else if (error.response.status === 409) {
                    setError('El nombre de usuario ya está registrado. Prueba con otro.');
                } else {
                    setError(error.response.data.error || 'Error desconocido durante el registro.');
                }
            } else {
                setError('Error de conexión con el servidor.');
            }
        }
    };
    

    const handleLoginRedirect = () => {
        navigate('/');
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Página de Registro</h1>
            <form onSubmit={handleRegister}>
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
                <div>
                    <label>RUT:</label>
                    <input
                        type="text"
                        placeholder="Ingresa tu RUT"
                        value={rut}
                        onChange={(e) => setRut(e.target.value)}
                    />
                </div>
                <div>
                    <label>Tipo de Usuario:</label>
                    <select value={tipo} onChange={(e) => setTipo(e.target.value)} required>
                        <option value="Administrador">Administrador</option>
                        <option value="Usuario">Usuario</option>
                        <option value="otro">Otro</option>
                    </select>
                </div>
                <button type="submit">Registrar</button>
            </form>
            {message && <p style={{ marginTop: '10px', color: 'green' }}>{message}</p>}
            {error && <p style={{ marginTop: '10px', color: 'red' }}>{error}</p>}
            <button onClick={handleLoginRedirect} style={{ marginTop: '10px' }}>
                ¿Ya tienes una cuenta? Inicia sesión aquí
            </button>
        </div>
    );
}

export default RegisterPage;
