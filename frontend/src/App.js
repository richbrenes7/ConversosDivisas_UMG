/**
 * 🎨 Componente Principal de la Aplicación
 * 
 * Este es el punto de entrada de nuestra aplicación de conversión de divisas.
 * Aquí organizamos la estructura visual: header, contenido principal y footer.
 * 
 * Universidad Mariano Gálvez - Proyecto de Desarrollo de Software
 */

import React from 'react';
import CurrencyConverter from './components/CurrencyConverter';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="app-container">
        {/* 🎯 Encabezado con el título de la aplicación */}
        <header className="app-header">
          <h1>💱 Conversor de Divisas</h1>
          <p>Universidad Mariano Gálvez</p>
        </header>
        
        {/* 📱 Contenido principal - Aquí va el conversor */}
        <main className="app-main">
          <CurrencyConverter />
        </main>
        
        {/* 📄 Pie de página con información adicional */}
        <footer className="app-footer">
          <p>© 2026 UMG - Desarrollo de Software</p>
          <p>Tasas de cambio actualizadas en tiempo real</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
