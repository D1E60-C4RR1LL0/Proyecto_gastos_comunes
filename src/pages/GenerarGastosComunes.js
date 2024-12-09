import React, { useState } from "react";
import axios from "axios";

const GenerarGastosComunes = () => {
    const [formData, setFormData] = useState({ mes: "", año: "", monto: "", codDepto: "" });
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(""); // Limpiar errores previos
        setResult(null); // Limpiar resultados previos

        try {
            const payload = {
                Mes: parseInt(formData.mes),
                Año: parseInt(formData.año),
                Monto: parseFloat(formData.monto),
            };

            // Incluir departamento si se proporciona
            if (formData.codDepto.trim() !== "") {
                payload.CodDepto = parseInt(formData.codDepto);
            }

            const response = await axios.post("http://localhost:5000/generar_gastos_comunes", payload);
            setResult(response.data);
        } catch (err) {
            setError(err.response?.data?.error || "Ocurrió un error inesperado");
        }
    };

    return (
        <div>
            <h1>Generar Gastos Comunes</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Mes:</label>
                    <input
                        type="number"
                        name="mes"
                        value={formData.mes}
                        onChange={handleInputChange}
                        placeholder="Mes (1-12)"
                        required
                        min="1"
                        max="12"
                    />
                </div>
                <div>
                    <label>Año:</label>
                    <input
                        type="number"
                        name="año"
                        value={formData.año}
                        onChange={handleInputChange}
                        placeholder="Año"
                        required
                        min="2000"
                    />
                </div>
                <div>
                    <label>Monto:</label>
                    <input
                        type="number"
                        name="monto"
                        value={formData.monto}
                        onChange={handleInputChange}
                        placeholder="Monto a cobrar"
                        required
                        min="0"
                        step="0.01"
                    />
                </div>
                <div>
                    <label>Código Departamento (Opcional):</label>
                    <input
                        type="text"
                        name="codDepto"
                        value={formData.codDepto}
                        onChange={handleInputChange}
                        placeholder="Ej: 101 (opcional)"
                    />
                </div>
                <button type="submit">Generar</button>
            </form>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {result && (
                <div>
                    <h2>Resultados</h2>
                    <pre>{JSON.stringify(result, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default GenerarGastosComunes;
