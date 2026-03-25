import React, { useState, useEffect } from 'react';
import { convertCurrency, getSupportedCurrencies } from '../services/api';
import './CurrencyConverter.css';

/**
 * 💱 Componente Principal del Conversor de Divisas
 * 
 * Este es el corazón de nuestra aplicación. Aquí manejamos:
 * - La entrada del usuario (cantidad y monedas)
 * - La comunicación con el backend para obtener las conversiones
 * - La visualización de los resultados
 * 
 * Todo está pensado para ser intuitivo y fácil de usar.
 */
function CurrencyConverter() {
  // 📦 Estados de la aplicación - Aquí guardamos toda la información mientras la app está corriendo
  const [amount, setAmount] = useState('100');  // El monto que el usuario quiere convertir
  const [fromCurrency, setFromCurrency] = useState('USD');  // De qué moneda convertimos
  const [toCurrency, setToCurrency] = useState('GTQ');  // A qué moneda convertimos
  const [result, setResult] = useState(null);  // El resultado de la conversión
  const [currencies, setCurrencies] = useState([]);  // Lista de todas las monedas disponibles
  const [loading, setLoading] = useState(false);  // ¿Estamos procesando una conversión?
  const [error, setError] = useState('');  // Mensaje de error si algo sale mal

  // 🎬 Cuando el componente se monta por primera vez, cargamos las monedas disponibles
  useEffect(() => {
    loadCurrencies();
  }, []);

  /**
   * Carga las monedas disponibles desde el backend
   * 
   * Esta función se ejecuta una sola vez al inicio para obtener
   * todas las monedas que el usuario puede seleccionar.
   */
  const loadCurrencies = async () => {
    try {
      const data = await getSupportedCurrencies();
      setCurrencies(data);
    } catch (err) {
      console.error('Error al cargar monedas:', err);
      setError('No se pudieron cargar las monedas, intenta recargar la página');
    }
  };

  /**
   * 🔄 Maneja la conversión cuando el usuario presiona el botón
   * 
   * Valida los datos ingresados, se comunica con el backend,
   * y muestra el resultado o un mensaje de error si algo falla.
   */
  const handleConvert = async (e) => {
    e.preventDefault();
    
    // ✅ Primero validamos que todo esté correcto antes de enviar la petición
    if (!amount || parseFloat(amount) <= 0) {
      setError('Por favor ingresa un monto válido mayor a 0');
      return;
    }

    if (fromCurrency === toCurrency) {
      setError('No tiene sentido convertir de una moneda a sí misma. Elige monedas diferentes 😊');
      return;
    }

    // 🚀 Todo bien, procedemos con la conversión
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await convertCurrency(amount, fromCurrency, toCurrency);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Ups, algo salió mal. Por favor intenta nuevamente.');
    } finally {
      setLoading(false);  // Ya terminamos, quitar el indicador de carga
    }
  };

  /**
   * 🔄 Intercambia las monedas (de ↔ a)
   * 
   * Función útil para cuando quieres hacer la conversión inversa.
   * Por ejemplo, si estabas convirtiendo USD -> GTQ, te cambia a GTQ -> USD.
   */
  const handleSwapCurrencies = () => {
    setFromCurrency(toCurrency);
    setToCurrency(fromCurrency);
    setResult(null);  // Limpiamos el resultado anterior
  };

  /**
   * ✍️ Valida y actualiza el monto mientras el usuario escribe
   * 
   * Solo permitimos números y un punto decimal (máximo 2 decimales).
   * Esto evita que el usuario ingrese letras o valores inválidos.
   */
  const handleAmountChange = (e) => {
    const value = e.target.value;
    // Esta expresión regular permite: números, un punto, y máximo 2 decimales
    if (value === '' || /^\d*\.?\d{0,2}$/.test(value)) {
      setAmount(value);
      setResult(null);  // Limpiamos el resultado anterior
      setError('');  // Limpiamos cualquier error
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
