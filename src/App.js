import React from 'react';
import './styles/styles.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import AdminReviewClaimsPage from './pages/admin/AdminReviewClaimsPage';
import AdminReportsPage from './pages/admin/AdminReportsPage';
import UserProfilePage from './pages/user/UserProfilePage';
import UserClaimsPage from './pages/user/UserClaimsPage';
import UserPaymentsPage from './pages/user/UserPaymentsPage';

import GastosComunesForm from './components/GastosComunes/GastosComunesForm';
import MarcarPagosForm from './components/MarcarPagos/MarcarPagosForm';
import ListadoPendientes from './components/ListadoPendientes/ListadoPendientes';
import MarcarPagoIndividualWrapper from './components/MarcarPagos/MarcarPagoIndividualWrapper';
import ListaDepartamentos from './components/MarcarPagos/ListaDepartamentos';

function App() {
  return (
    <Router>
      <Routes>
        {/* Rutas principales */}
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />

        {/* Funcionalidades de Gastos Comunes */}
        <Route path="/mis-gastos-comunes" element={<ListadoPendientes />} />
        <Route path="/generar-gastos-comunes" element={<GastosComunesForm />} />
        <Route path="/marcar-pago" element={<MarcarPagosForm />} />
        <Route path="/marcar-pago/:departamento" element={<MarcarPagoIndividualWrapper />} />
        <Route path="/lista-departamentos" element={<ListaDepartamentos />} />

        {/* Rutas de Admin */}
        <Route path="/review-claims" element={<AdminReviewClaimsPage />} />
        <Route path="/reports" element={<AdminReportsPage />} />

        {/* Rutas de Usuario */}
        <Route path="/profile" element={<UserProfilePage />} />
        <Route path="/claims" element={<UserClaimsPage />} />
        <Route path="/payments" element={<UserPaymentsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
