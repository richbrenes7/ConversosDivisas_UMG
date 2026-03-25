/**
 * 🌐 Cliente API - Servicio de Comunicación con el Backend
 * 
 * Este archivo maneja toda la comunicación entre nuestro frontend (lo que ves)
 * y el backend (el servidor que procesa las conversiones).
 * 
 * Usamos Axios que es como un "cartero" que envía y recibe mensajes
 * entre tu navegador y nuestro servidor.
 */

import axios from 'axios';

// 🔗 La dirección de nuestro backend (puede cambiar entre desarrollo y producción)
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Creamos una instancia personalizada de Axios con configuración por defecto
 * 
 * Esto es como tener un "cartero" configurado con:
 * - La dirección base de nuestro servidor
 * - Un tiempo máximo de espera (10 segundos)
 * - El tipo de datos que enviamos (JSON)
 */
const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,  // Si tarda más de 10 segundos, cancelamos la petición
  headers: {
    'Content-Type': 'application/json',  // Le decimos que enviamos datos en formato JSON
  },
});

/**
 * 🛡️ Interceptor de respuestas - Maneja errores de forma amigable
 * 
 * Este "guardián" atrapa cualquier problema que ocurra al comunicarnos
 * con el servidor y convierte los errores técnicos en mensajes que
 * los usuarios puedan entender.
 */
api.interceptors.response.use(
  (response) => response,  // Si todo sale bien, solo devolvemos la respuesta
  (error) => {
    // Si hay un problema, lo convertimos en un mensaje claro
    if (error.response) {
      // El servidor respondió pero con un error (400, 500, etc.)
      const message = error.response.data?.message || error.response.data?.detail || 'Algo salió mal con tu solicitud';
      throw new Error(message);
    } else if (error.request) {
      // No pudimos contactar con el servidor (sin internet, servidor caído, etc.)
      throw new Error('No pudimos conectar con el servidor. Verifica tu conexión a internet.');
    } else {
      // Cualquier otro tipo de error extraño
      throw new Error('Ocurrió un error inesperado. Por favor intenta de nuevo.');
    }
  }
);

/**
 * 💱 Convierte un monto de una moneda a otra
 * 
 * Esta es la función principal que usas cuando quieres saber
 * cuánto vale tu dinero en otra moneda.
 * 
 * @param {number} amount - Cuánto dinero quieres convertir
 * @param {string} fromCurrency - De qué moneda (ej: "USD")
 * @param {string} toCurrency - A qué moneda (ej: "GTQ")
 * @returns {Promise} Los datos de la conversión con el resultado
 */
export const convertCurrency = async (amount, fromCurrency, toCurrency) => {
  try {
    const response = await api.post('/api/convert', {
      amount: parseFloat(amount),  // Nos aseguramos que sea un número
      from_currency: fromCurrency,
      to_currency: toCurrency,
    });
    return response.data;
  } catch (error) {
    throw error;  // Si algo falla, pasamos el error para que se muestre al usuario
  }
};

/**
 * 📋 Obtiene la lista de monedas disponibles
 * 
 * Cuando la app se inicia, llamamos esta función para saber
 * qué monedas puede elegir el usuario en los selectores.
 * 
 * @returns {Promise} Array con todas las monedas disponibles
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
