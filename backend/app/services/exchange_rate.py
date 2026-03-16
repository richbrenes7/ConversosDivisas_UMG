"""
Exchange Rate Service - Lógica de negocio para tasas de cambio
Implementa caché y manejo robusto de errores
"""

import httpx
from datetime import datetime, timedelta
from typing import Dict, Optional
import os


class ExchangeRateService:
    """Servicio para obtener tasas de cambio de API externa"""
    
    def __init__(self):
        self.base_url = os.getenv(
            "EXCHANGE_API_URL",
            "https://api.exchangerate-api.com/v4/latest"
        )
        self.cache: Dict[str, tuple] = {}  # {currency: (rates, timestamp)}
        self.cache_duration = timedelta(hours=1)
        
        # Monedas soportadas (principales)
        self.supported_currencies = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GTQ": "Guatemalan Quetzal",
            "MXN": "Mexican Peso",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "CAD": "Canadian Dollar",
            "AUD": "Australian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "BRL": "Brazilian Real",
            "ARS": "Argentine Peso",
            "COP": "Colombian Peso",
            "CRC": "Costa Rican Colón",
            "HNL": "Honduran Lempira",
            "NIO": "Nicaraguan Córdoba"
        }
    
    def _is_cache_valid(self, currency: str) -> bool:
        """Verifica si el caché para una moneda es válido"""
        if currency not in self.cache:
            return False
        
        _, timestamp = self.cache[currency]
        return datetime.now() - timestamp < self.cache_duration
    
    async def _fetch_rates(self, base_currency: str) -> Dict:
        """Obtiene tasas de cambio de la API externa"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/{base_currency}")
                response.raise_for_status()
                data = response.json()
                
                # Cachear resultados
                self.cache[base_currency] = (data["rates"], datetime.now())
                
                return data["rates"]
        
        except httpx.HTTPError as e:
            raise Exception(f"Error fetching exchange rates: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    async def get_exchange_rate(self, from_currency: str, to_currency: str) -> Dict:
        """
        Obtiene la tasa de cambio entre dos monedas
        
        Args:
            from_currency: Código de moneda origen
            to_currency: Código de moneda destino
        
        Returns:
            Dict con información de tasa de cambio
        """
        # Verificar si está en caché
        if self._is_cache_valid(from_currency):
            rates, _ = self.cache[from_currency]
        else:
            rates = await self._fetch_rates(from_currency)
        
        # Verificar que la moneda destino exista
        if to_currency not in rates:
            raise Exception(f"Currency {to_currency} not supported")
        
        return {
            "base_currency": from_currency,
            "target_currency": to_currency,
            "rate": rates[to_currency],
            "timestamp": datetime.now().isoformat()
        }
    
    async def convert(
        self,
        amount: float,
        from_currency: str,
        to_currency: str
    ) -> Dict:
        """
        Convierte un monto de una moneda a otra
        
        Args:
            amount: Monto a convertir
            from_currency: Código de moneda origen
            to_currency: Código de moneda destino
        
        Returns:
            Dict con resultado de conversión
        """
        # Obtener tasa de cambio
        rate_info = await self.get_exchange_rate(from_currency, to_currency)
        rate = rate_info["rate"]
        
        # Calcular conversión
        converted_amount = round(amount * rate, 2)
        
        return {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "exchange_rate": rate,
            "converted_amount": converted_amount,
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_supported_currencies(self) -> Dict:
        """
        Obtiene lista de monedas soportadas
        
        Returns:
            Dict con lista de monedas
        """
        currencies_list = [
            {"code": code, "name": name}
            for code, name in self.supported_currencies.items()
        ]
        
        return {
            "currencies": currencies_list,
            "total": len(currencies_list)
        }
