import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Crear instancia de axios con configuración por defecto
const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Error de respuesta del servidor
      const message = error.response.data?.message || error.response.data?.detail || 'Error en la solicitud';
      throw new Error(message);
    } else if (error.request) {
      // Error de red
      throw new Error('No se pudo conectar con el servidor. Verifica tu conexión.');
    } else {
      // Otro tipo de error
      throw new Error('Ocurrió un error inesperado.');
    }
  }
);

/**
 * Convierte un monto de una moneda a otra
 */
export const convertCurrency = async (amount, fromCurrency, toCurrency) => {
  try {
    const response = await api.post('/api/convert', {
      amount: parseFloat(amount),
      from_currency: fromCurrency,
      to_currency: toCurrency,
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Obtiene la lista de monedas soportadas
 */
export const getSupportedCurrencies = async () => {
  try {
    const response = await api.get('/api/currencies');
    return response.data.currencies;
  } catch (error) {
    throw error;
  }
};

/**
 * Obtiene la tasa de cambio entre dos monedas
 */
export const getExchangeRate = async (fromCurrency, toCurrency) => {
  try {
    const response = await api.get('/api/exchange-rate', {
      params: {
        from: fromCurrency,
        to: toCurrency,
      },
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Verifica el estado de la API
 */
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default api;
