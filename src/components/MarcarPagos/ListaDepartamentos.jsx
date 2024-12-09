import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { obtenerDepartamentos } from '../../services/api';

const ListaDepartamentos = () => {
    const [departamentos, setDepartamentos] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchDepartamentos = async () => {
            try {
                const response = await obtenerDepartamentos();
                setDepartamentos(response.data); // La respuesta ahora solo tiene el número
            } catch (err) {
                setError('Error al cargar los departamentos');
                console.error(err);
            }
        };

        fetchDepartamentos();
    }, []);

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div>
            <h2>Selecciona un Departamento</h2>
            <ul>
                {departamentos.map((depto) => (
                    <li key={depto.Numero}>
                        <Link to={`/marcar-pago/${depto.Numero}`}>
                            Departamento {depto.Numero}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ListaDepartamentos;
