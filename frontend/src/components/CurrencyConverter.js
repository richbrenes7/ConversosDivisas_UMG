import React, { useState, useEffect } from 'react';
import { convertCurrency, getSupportedCurrencies } from '../services/api';
import './CurrencyConverter.css';

function CurrencyConverter() {
  // Estados
  const [amount, setAmount] = useState('100');
  const [fromCurrency, setFromCurrency] = useState('USD');
  const [toCurrency, setToCurrency] = useState('GTQ');
  const [result, setResult] = useState(null);
  const [currencies, setCurrencies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Cargar monedas al montar el componente
  useEffect(() => {
    loadCurrencies();
  }, []);

  const loadCurrencies = async () => {
    try {
      const data = await getSupportedCurrencies();
      setCurrencies(data);
    } catch (err) {
      console.error('Error loading currencies:', err);
      setError('No se pudieron cargar las monedas');
    }
  };

  const handleConvert = async (e) => {
    e.preventDefault();
    
    // Validaciones
    if (!amount || parseFloat(amount) <= 0) {
      setError('Por favor ingresa un monto válido');
      return;
    }

    if (fromCurrency === toCurrency) {
      setError('Por favor selecciona monedas diferentes');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await convertCurrency(amount, fromCurrency, toCurrency);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Error al convertir. Por favor intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleSwapCurrencies = () => {
    setFromCurrency(toCurrency);
    setToCurrency(fromCurrency);
    setResult(null);
  };

  const handleAmountChange = (e) => {
    const value = e.target.value;
    // Permitir solo números y un punto decimal
    if (value === '' || /^\d*\.?\d{0,2}$/.test(value)) {
      setAmount(value);
      setResult(null);
      setError('');
    }
  };

  return (
    <div className="converter-container">
      <div className="converter-card">
        <div className="card-header">
          <div className="currency-icon">💱</div>
          <h2>Convertidor de Divisas</h2>
          <p>Conversión en tiempo real</p>
        </div>

        <form onSubmit={handleConvert} className="converter-form">
          {/* Cantidad */}
          <div className="form-group">
            <label htmlFor="amount">Cantidad</label>
            <div className="input-wrapper">
              <input
                id="amount"
                type="text"
                value={amount}
                onChange={handleAmountChange}
                placeholder="100.00"
                required
                className="amount-input"
              />
            </div>
          </div>

          {/* Moneda de Origen */}
          <div className="form-group">
            <label htmlFor="fromCurrency">De</label>
            <select
              id="fromCurrency"
              value={fromCurrency}
              onChange={(e) => {
                setFromCurrency(e.target.value);
                setResult(null);
              }}
              className="currency-select"
            >
              {currencies.map((currency) => (
                <option key={currency.code} value={currency.code}>
                  {currency.code} - {currency.name}
                </option>
              ))}
            </select>
          </div>

          {/* Botón de Intercambio */}
          <div className="swap-button-container">
            <button
              type="button"
              onClick={handleSwapCurrencies}
              className="swap-button"
              title="Intercambiar monedas"
            >
              <span className="swap-icon">⇅</span>
            </button>
          </div>

          {/* Moneda de Destino */}
          <div className="form-group">
            <label htmlFor="toCurrency">A</label>
            <select
              id="toCurrency"
              value={toCurrency}
              onChange={(e) => {
                setToCurrency(e.target.value);
                setResult(null);
              }}
              className="currency-select"
            >
              {currencies.map((currency) => (
                <option key={currency.code} value={currency.code}>
                  {currency.code} - {currency.name}
                </option>
              ))}
            </select>
          </div>

          {/* Botón de Conversión */}
          <button
            type="submit"
            disabled={loading}
            className={`convert-button ${loading ? 'loading' : ''}`}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Convirtiendo...
              </>
            ) : (
              'Convertir'
            )}
          </button>
        </form>

        {/* Mensaje de Error */}
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        {/* Resultado */}
        {result && (
          <div className="result-container">
            <div className="result-header">
              <span className="result-icon">✓</span>
              Resultado
            </div>
            
            <div className="result-content">
              <div className="result-amount-from">
                <span className="amount-value">{result.amount.toFixed(2)}</span>
                <span className="currency-code">{result.from_currency}</span>
              </div>
              
              <div className="result-equals">=</div>
              
              <div className="result-amount-to">
                <span className="amount-value highlight">
                  {result.converted_amount.toFixed(2)}
                </span>
                <span className="currency-code">{result.to_currency}</span>
              </div>
            </div>

            <div className="result-details">
              <div className="exchange-rate">
                <span className="label">Tasa de cambio:</span>
                <span className="value">
                  1 {result.from_currency} = {result.exchange_rate.toFixed(4)} {result.to_currency}
                </span>
              </div>
              <div className="timestamp">
                <span className="label">Actualizado:</span>
                <span className="value">
                  {new Date(result.timestamp).toLocaleString('es-GT')}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Info adicional */}
      <div className="info-box">
        <p>
          <strong>💡 Tip:</strong> Las tasas de cambio se actualizan cada hora
        </p>
      </div>
    </div>
  );
}

export default CurrencyConverter;
