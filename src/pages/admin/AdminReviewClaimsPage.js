import React, { useEffect, useState } from 'react';
import api from '../../services/api';

function AdminReviewClaimsPage() {
    const [claims, setClaims] = useState([]);
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

    const handleMarkAsViewed = async (idReclamo) => {
        try {
            await api.put(`/reclamos/${idReclamo}/visto`);
            setMessage('Reclamo marcado como visto');
            fetchClaims();
        } catch (error) {
            setMessage('Error al actualizar reclamo: ' + error.response?.data?.error);
        }
    };

    return (
        <div>
            <h1>Revisar Reclamos</h1>
            {claims.map((claim) => (
                <div key={claim.IDReclamo}>
                    <p>
                        {claim.TextoReclamo} - {claim.Estado}
                    </p>
                    <button onClick={() => handleMarkAsViewed(claim.IDReclamo)}>Marcar como visto</button>
                </div>
            ))}
            {message && <p>{message}</p>}
        </div>
    );
}

export default AdminReviewClaimsPage;
