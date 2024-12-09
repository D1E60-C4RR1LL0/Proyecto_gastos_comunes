import React, { useState, useEffect } from 'react';
import api from '../../services/api';

function AdminReportsPage() {
    const [report, setReport] = useState([]);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    const handleGenerateClaimsReport = async () => {
        setLoading(true);
        try {
            const response = await api.get('/informes/reclamos'); // Cambia el endpoint si es necesario
            setReport(response.data);
            setLoading(false);
        } catch (error) {
            setMessage('Error al generar informe de reclamos: ' + (error.response?.data?.error || 'Error desconocido'));
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Informes de Reclamos</h1>
            <button onClick={handleGenerateClaimsReport} style={{ marginBottom: '20px' }}>
                Generar Informe de Reclamos
            </button>
            {loading && <p>Cargando informe...</p>}
            {message && <p style={{ color: 'red' }}>{message}</p>}
            <div>
                {report.length > 0 ? (
                    report.map((item) => (
                        <div key={item.IdReclamo} style={{ border: '1px solid #ccc', marginBottom: '10px', padding: '10px' }}>
                            <p><strong>ID Reclamo:</strong> {item.IdReclamo}</p>
                            <p><strong>Texto:</strong> {item.TextoReclamo}</p>
                            <p><strong>Estado:</strong> {item.Estado}</p>
                            <p><strong>Fecha:</strong> {item.FechaReclamo}</p>
                        </div>
                    ))
                ) : (
                    <p>No hay datos para mostrar.</p>
                )}
            </div>
        </div>
    );
}

export default AdminReportsPage;
