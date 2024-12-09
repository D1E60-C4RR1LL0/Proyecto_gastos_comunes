import React, { useEffect, useState } from 'react';
import api from '../../services/api';

function UserClaimsPage() {
    const [claims, setClaims] = useState([]);
    const [newClaim, setNewClaim] = useState('');
    const [message, setMessage] = useState('');

    useEffect(() => {
        fetchClaims();
    }, []);

    const fetchClaims = async () => {
        try {
            const response = await api.get('/reclamos');
            setClaims(response.data);
        } catch (error) {
            console.error('Error fetching claims:', error);
        }
    };

    const handleCreateClaim = async () => {
        try {
            await api.post('/reclamos', {
                TextoReclamo: newClaim,
                RutArre: localStorage.getItem('rut'), // Ajustar según el backend
            });
            setMessage('Reclamo creado con éxito');
            fetchClaims();
        } catch (error) {
            setMessage('Error al crear reclamo: ' + error.response?.data?.error);
        }
    };

    return (
        <div>
            <h1>Mis Reclamos</h1>
            <input
                type="text"
                placeholder="Describe tu reclamo"
                value={newClaim}
                onChange={(e) => setNewClaim(e.target.value)}
            />
            <button onClick={handleCreateClaim}>Enviar Reclamo</button>
            {claims.map((claim) => (
                <p key={claim.IDReclamo}>{claim.TextoReclamo}</p>
            ))}
            {message && <p>{message}</p>}
        </div>
    );
}

export default UserClaimsPage;
