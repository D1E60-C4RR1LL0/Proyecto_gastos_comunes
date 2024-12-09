import React, { useState } from 'react';
import { marcarPago } from '../../services/api';

const MarcarPagosForm = ({ departamento }) => {
    const [mes, setMes] = useState('');
    const [año, setAño] = useState('');
    const [fechaPago, setFechaPago] = useState('');
    const [valorPagado, setValorPagado] = useState('');
    const [mensaje, setMensaje] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const payload = {
                CodDepto: departamento, // Asegúrate de que este prop esté correctamente definido
                Mes: parseInt(mes),
                Año: parseInt(año),
                FechaPago: fechaPago,
                ValorPagado: parseFloat(valorPagado),
            };
    
            console.log("Payload enviado:", payload); // Verifica qué se está enviando
    
            const response = await marcarPago(payload);
            setMensaje(`Pago registrado con éxito. Estado actual: ${response.data.cuota.Estado}`);
            console.log(response.data);
        } catch (error) {
            if (error.response) {
                setMensaje(error.response.data.error || 'Error al registrar el pago');
            } else {
                setMensaje('Error al registrar el pago');
            }
            console.error(error);
        }
    };
    

    return (
        <div>
            <h2>Marcar como Pagado</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Mes:
                    <input
                        type="number"
                        value={mes}
                        onChange={(e) => setMes(e.target.value)}
                        required
                    />
                </label>
                <label>
                    Año:
                    <input
                        type="number"
                        value={año}
                        onChange={(e) => setAño(e.target.value)}
                        required
                    />
                </label>
                <label>
                    Fecha de Pago:
                    <input
                        type="date"
                        value={fechaPago}
                        onChange={(e) => setFechaPago(e.target.value)}
                        required
                    />
                </label>
                <label>
                    Valor Pagado:
                    <input
                        type="number"
                        step="0.01"
                        value={valorPagado}
                        onChange={(e) => setValorPagado(e.target.value)}
                        required
                    />
                </label>
                <button type="submit">Registrar Pago</button>
            </form>
            {mensaje && <p>{mensaje}</p>}
        </div>
    );
};

export default MarcarPagosForm;
