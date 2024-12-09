import React, { useState, useEffect } from 'react';
import api from '../../services/api'; // Asegúrate de que `api` esté configurado con la base URL correcta

function UserProfilePage() {
    const [user, setUser] = useState(null); // Estado para guardar datos del usuario
    const [message, setMessage] = useState(''); // Mensajes de error o estado

    useEffect(() => {
        const username = localStorage.getItem('username'); // Asegúrate de guardar el `username` al iniciar sesión

        if (username) {
            fetchUserProfile(username);
        } else {
            setMessage('No se encontró el usuario actual en el almacenamiento local.');
        }
    }, []);

    const fetchUserProfile = async (username) => {
        try {
            // Llamada al endpoint con el parámetro de username
            const response = await api.get(`/acceso/${username}`); // Revisa que `username` se pase correctamente
            setUser(response.data); // Guardar los datos del usuario en el estado
        } catch (error) {
            // Manejo de errores
            const errorMsg = error.response?.data?.error || 'Error desconocido al cargar el perfil';
            setMessage(errorMsg);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Perfil del Usuario</h1>
            {message && <p style={{ color: 'red' }}>{message}</p>}
            {user ? (
                <div>
                    <p><strong>Nombre de Usuario:</strong> {user.username}</p>
                    <p><strong>Tipo de Usuario:</strong> {user.Tipo}</p>
                    <p><strong>Fecha de Creación:</strong> {user.fechaCreacion}</p>
                    <p><strong>Último Acceso:</strong> {user.fechaUltimoAcceso || 'No registrado'}</p>
                </div>
            ) : (
                !message && <p>Cargando datos del perfil...</p>
            )}
        </div>
    );
}

export default UserProfilePage;
