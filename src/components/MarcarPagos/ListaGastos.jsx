import React, { useEffect, useState } from 'react';
import { obtenerGastosPorDepartamento } from '../../services/api';

const ListaGastos = ({ codDepto }) => {
    const [gastos, setGastos] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchGastos = async () => {
            try {
                const response = await obtenerGastosPorDepartamento(codDepto);
                setGastos(response.data);
            } catch (err) {
                if (err.response && err.response.status === 404) {
                    setError('No se encontraron gastos comunes para este departamento.');
                } else {
                    setError('Error al cargar los gastos comunes.');
                }
                console.error(err);
            }
        };

        fetchGastos();
    }, [codDepto]);

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div>
            <h2>Gastos Comunes del Departamento {codDepto}</h2>
            {gastos.length > 0 ? (
                <table>
                    <thead>
                        <tr>
                            <th>Mes</th>
                            <th>Año</th>
                            <th>Valor Cobrado</th>
                            <th>Valor Pagado</th>
                            <th>Estado</th>
                            <th>Fecha de Pago</th>
                        </tr>
                    </thead>
                    <tbody>
                        {gastos.map((gasto, index) => (
                            <tr key={index}>
                                <td>{gasto.Mes}</td>
                                <td>{gasto.Año}</td>
                                <td>{gasto.ValorCobrado}</td>
                                <td>{gasto.ValorPagado || '-'}</td>
                                <td>{gasto.Estado}</td>
                                <td>{gasto.FechaPago || '-'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No hay gastos comunes registrados para este departamento.</p>
            )}
        </div>
    );
};

export default ListaGastos;
