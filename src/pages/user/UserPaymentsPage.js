import React, { useEffect, useState } from 'react';
import api from '../../services/api';

function UserPaymentsPage() {
    const [payments, setPayments] = useState([]);

    useEffect(() => {
        fetchPayments();
    }, []);

    const fetchPayments = async () => {
        try {
            const response = await api.get(`/cuotasgc/departamento/${localStorage.getItem('CodDepto')}`);
            setPayments(response.data);
        } catch (error) {
            console.error('Error fetching payments:', error);
        }
    };

    return (
        <div>
            <h1>Mis Pagos</h1>
            {payments.map((payment) => (
                <p key={payment.IdCuotaGC}>
                    Mes: {payment.Mes} - Año: {payment.Año} - Estado: {payment.Estado}
                </p>
            ))}
        </div>
    );
}

export default UserPaymentsPage;
