import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Importar Link
import { obtenerDepartamentos } from '../../services/api';

const ListaDepartamentos = () => {
    const [departamentos, setDepartamentos] = useState([]);
    const [mensaje, setMensaje] = useState('');

    useEffect(() => {
        const fetchDepartamentos = async () => {
            try {
                const response = await obtenerDepartamentos();
                setDepartamentos(response.data);
            } catch (error) {
                setMensaje('Error al cargar los departamentos');
            }
        };
        fetchDepartamentos();
    }, []);

    return (
        <div className="contenedor-departamentos">
            <h2>Selecciona un Departamento</h2>
            {mensaje && <p className="mensaje-error">{mensaje}</p>}
            {departamentos.length > 0 ? (
                <ul className="lista-departamentos">
                    {departamentos.map((depto) => (
                        <li key={depto.Numero}>
                            <Link to={`/marcar-pago/${depto.Numero}`} className="enlace-departamento">
                                Departamento {depto.Numero}
                            </Link>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No hay departamentos disponibles</p>
            )}
        </div>
    );
};

export default ListaDepartamentos;
