import React, { useState } from 'react';
import { generarGastos } from '../../services/api';

const GastosComunesForm = () => {
    const [mes, setMes] = useState('');
    const [año, setAño] = useState('');
    const [monto, setMonto] = useState('');
    const [codDepto, setCodDepto] = useState('');
    const [mensaje, setMensaje] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validaciones en el frontend
        if (mes && (parseInt(mes) < 1 || parseInt(mes) > 12)) {
            setMensaje('El mes debe estar entre 1 y 12, o déjelo vacío para generar todo el año.');
            return;
        }
        if (!año) {
            setMensaje('El año es obligatorio.');
            return;
        }
        if (!monto || parseFloat(monto) <= 0) {
            setMensaje('El monto debe ser un número mayor a 0.');
            return;
        }

        try {
            const payload = {
                Mes: mes ? parseInt(mes) : null, // Si el mes está vacío, enviar null
                Año: parseInt(año),
                Monto: parseFloat(monto),
            };

            if (codDepto) {
                payload.CodDepto = parseInt(codDepto); // Agregar CodDepto solo si se especifica
            }

            const response = await generarGastos(payload);
            setMensaje('Gastos comunes generados con éxito');
            console.log(response.data);
        } catch (error) {
            if (error.response && error.response.status === 409) {
                setMensaje('Ya existen gastos comunes para el mes y año especificados');
            } else {
                setMensaje('Error al generar gastos comunes');
            }
            console.error(error);
        }
    };

    return (
        <div>
            <h2>Generar Gastos Comunes</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Mes (opcional):
                    <input
                        type="number"
                        value={mes}
                        onChange={(e) => setMes(e.target.value)}
                        placeholder="Dejar vacío para generar todo el año"
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
                    Monto:
                    <input
                        type="number"
                        step="0.01"
                        value={monto}
                        onChange={(e) => setMonto(e.target.value)}
                        required
                    />
                </label>
                <label>
                    Código de Departamento (opcional):
                    <input
                        type="number"
                        value={codDepto}
                        onChange={(e) => setCodDepto(e.target.value)}
                        placeholder="Dejar vacío para todos los departamentos"
                    />
                </label>
                <button type="submit">Generar</button>
            </form>
            {mensaje && <p>{mensaje}</p>}
        </div>
    );
};

export default GastosComunesForm;
