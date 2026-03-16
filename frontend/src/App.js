import React from 'react';
import CurrencyConverter from './components/CurrencyConverter';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="app-container">
        <header className="app-header">
          <h1>💱 Conversor de Divisas</h1>
          <p>Universidad Mariano Gálvez</p>
        </header>
        
        <main className="app-main">
          <CurrencyConverter />
        </main>
        
        <footer className="app-footer">
          <p>© 2026 UMG - Desarrollo de Software</p>
          <p>Tasas de cambio actualizadas en tiempo real</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
