import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Cambia esto si tu backend está en otro dominio
  headers: {
    'Content-Type': 'application/json',
  },
});

// Endpoints
export const generarGastos = (data) => api.post('/generar_gastos_comunes', data);
export const marcarPago = (payload) => {
  // Enviar todo el payload en el cuerpo de la solicitud
  return api.put('/cuotasgc/editar', payload);
};
export const obtenerPendientes = (params) => api.get('/cuotasgc/pendientes', { params });
export const obtenerDepartamentos = () => api.get('/departamentos');
export const obtenerGastosPorDepartamento = (codDepto) =>
  api.get(`/departamentos/${codDepto}/gastos`);

export default api;