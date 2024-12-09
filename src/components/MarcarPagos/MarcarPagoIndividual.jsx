import React from 'react';
import MarcarPagosForm from './MarcarPagosForm';
import ListaGastos from './ListaGastos';

const MarcarPagoIndividual = ({ departamento }) => {
    return (
        <div>
            <h1>Marcar Pago para el Departamento {departamento}</h1>
            
            {/* Componente que muestra los gastos comunes del departamento */}
            <ListaGastos codDepto={departamento} />

            {/* Formulario para registrar pagos */}
            <MarcarPagosForm departamento={departamento} />
        </div>
    );
};

export default MarcarPagoIndividual;
