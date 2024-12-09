import React from 'react';
import { useParams } from 'react-router-dom';
import MarcarPagoIndividual from './MarcarPagoIndividual';

const MarcarPagoIndividualWrapper = () => {
    const { departamento } = useParams();

    return <MarcarPagoIndividual departamento={departamento} />;
};

export default MarcarPagoIndividualWrapper;
