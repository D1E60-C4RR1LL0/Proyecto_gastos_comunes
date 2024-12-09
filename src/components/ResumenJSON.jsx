import React, { useState } from 'react';
import './ResumenJSON.css'; // Opcional, para estilos personalizados

const ResumenJSON = ({ data }) => {
    const [isVisible, setIsVisible] = useState(false);

    return (
        <div className="resumen-json-container">
            <button onClick={() => setIsVisible(!isVisible)} className="toggle-button">
                {isVisible ? "Cerrar Resumen" : "Ver Resumen"}
            </button>
            {isVisible && (
                <div className="resumen-json-modal">
                    <h3>Resumen de Datos</h3>
                    <pre>{JSON.stringify(data, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default ResumenJSON;
