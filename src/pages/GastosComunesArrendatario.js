import React, { useState } from "react";
import axios from "axios";

const GastosComunesArrendatario = () => {
    const [rut, setRut] = useState("");
    const [gastos, setGastos] = useState([]);
    const [error, setError] = useState("");

    const handleConsultar = async () => {
        setError(""); // Limpiar errores previos
        setGastos([]); // Limpiar datos previos

        try {
            const response = await axios.get(`http://localhost:5000/mis_gastos_comunes`, {
                params: { Rut: rut },
            });
            setGastos(response.data);
        } catch (err) {
            setError(err.response?.data?.error || "Ocurrió un error inesperado");
        }
    };

    return (
        <div>
            <h1>Mis Gastos Comunes</h1>
            <div>
                <label>Ingrese su RUT:</label>
                <input
                    type="text"
                    value={rut}
                    onChange={(e) => setRut(e.target.value)}
                    placeholder="Ej: 12345678-9"
                />
                <button onClick={handleConsultar}>Consultar</button>
            </div>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {gastos.length > 0 && (
                <div>
                    <h2>Resultados</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Departamento</th>
                                <th>Mes</th>
                                <th>Año</th>
                                <th>Valor Cobrado</th>
                                <th>Valor Pagado</th>
                                <th>Estado</th>
                                <th>Fecha Pago</th>
                            </tr>
                        </thead>
                        <tbody>
                            {gastos.map((gasto, index) => (
                                <tr key={index}>
                                    <td>{gasto.Departamento}</td>
                                    <td>{gasto.Mes}</td>
                                    <td>{gasto.Año}</td>
                                    <td>{gasto.ValorCobrado}</td>
                                    <td>{gasto.ValorPagado}</td>
                                    <td>{gasto.Estado}</td>
                                    <td>{gasto.FechaPago || "No registrado"}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default GastosComunesArrendatario;

