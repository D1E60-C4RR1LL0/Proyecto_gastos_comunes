import React, { useState } from "react";
import { obtenerPendientes } from "../../services/api";

const ListadoPendientes = () => {
    const [año, setAño] = useState("");
    const [mes, setMes] = useState("");
    const [pendientes, setPendientes] = useState([]);
    const [mensaje, setMensaje] = useState("");

    const handleConsultar = async () => {
        try {
            const params = { hasta_año: parseInt(año) };
            if (mes) params.hasta_mes = parseInt(mes);

            const response = await obtenerPendientes(params);

            if (response.data.mensaje) {
                setMensaje(response.data.mensaje);
                setPendientes([]);
            } else {
                setMensaje("");
                setPendientes(response.data);
            }
        } catch (error) {
            setMensaje("Error al obtener los datos");
            console.error(error);
        }
    };

    return (
        <div>
            <h2>Listado de Gastos Pendientes</h2>
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    handleConsultar();
                }}
            >
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
                    Mes (opcional):
                    <input
                        type="number"
                        value={mes}
                        onChange={(e) => setMes(e.target.value)}
                    />
                </label>
                <button type="submit">Consultar</button>
            </form>

            {mensaje && <p>{mensaje}</p>}

            {pendientes.length > 0 && (
                <table>
                    <thead>
                        <tr>
                            <th>CodDepto</th>
                            <th>Mes</th>
                            <th>Año</th>
                            <th>Valor Cobrado</th>
                            <th>Valor Pagado</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {pendientes.map((pendiente) => (
                            <tr key={pendiente.IdCuotaGC}>
                                <td>{pendiente.CodDepto}</td>
                                <td>{pendiente.Mes}</td>
                                <td>{pendiente.Año}</td>
                                <td>{pendiente.ValorCobrado}</td>
                                <td>{pendiente.ValorPagado}</td>
                                <td>{pendiente.Estado}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default ListadoPendientes;
