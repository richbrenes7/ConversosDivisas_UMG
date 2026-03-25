"""
💱 Rutas de Conversión de Divisas

Aquí están todos los endpoints (puntos de acceso) para convertir divisas.
Implementamos límites de velocidad para evitar sobrecargar el servicio,
y validamos cada dato que nos envías para garantizar resultados precisos.
"""

from fastapi import APIRouter, HTTPException, Request, Depends
from slowapi import Limiter
from slowapi.util import get_remote_address
import os

from app.models import (
    ConversionRequest,
    ConversionResponse,
    ExchangeRateResponse,
    CurrencyListResponse,
    ErrorResponse
)
from app.services.exchange_rate import ExchangeRateService
from app.utils.validators import validate_currency_code

# Creamos el enrutador que agrupa todos los endpoints de divisas
router = APIRouter()

# Configuramos cuántas peticiones puede hacer un usuario por minuto
# Esto protege nuestro servicio de abusos y mantiene la calidad para todos
limiter = Limiter(key_func=get_remote_address)
rate_limit = os.getenv("RATE_LIMIT_PER_MINUTE", "60")

# Inicializamos el servicio que se encarga de consultar las tasas de cambio
exchange_service = ExchangeRateService()


@router.post(
    "/convert",
    response_model=ConversionResponse,
    responses={
        400: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
@limiter.limit(f"{rate_limit}/minute")
async def convert_currency(
    request: Request,
    conversion: ConversionRequest
):
    """
    🔄 Convierte dinero de una moneda a otra

    Este es el corazón del conversor. Le das un monto y dos monedas,
    y te devolvemos cuánto vale ese dinero en la otra moneda.

    - **amount**: Cuánto dinero quieres convertir (debe ser más de 0)
    - **from_currency**: De qué moneda (ej: USD para dólares)
    - **to_currency**: A qué moneda (ej: EUR para euros)

    Ejemplo: Si conviertes 100 USD a EUR, te diremos cuántos euros son.
    """
    try:
        # Primero verificamos que los códigos de moneda sean válidos
        if not validate_currency_code(conversion.from_currency):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid currency code: {conversion.from_currency}"
            )
        
        if not validate_currency_code(conversion.to_currency):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid currency code: {conversion.to_currency}"
            )
        
        # Realizamos la conversión consultando las tasas de cambio actuales
        result = await exchange_service.convert(
            amount=conversion.amount,
            from_currency=conversion.from_currency,
            to_currency=conversion.to_currency
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        # Si algo sale mal, devolvemos un mensaje genérico para no exponer detalles internos
        raise HTTPException(
            status_code=500,
            detail="Ups, algo salió mal al convertir. Por favor intenta de nuevo."
        )


@router.get(
    "/exchange-rate",
    response_model=ExchangeRateResponse,
    responses={
        400: {"model": ErrorResponse},
        429: {"model": ErrorResponse}
    }
)
@limiter.limit(f"{rate_limit}/minute")
async def get_exchange_rate(
    request: Request,
    from_currency: str,
    to_currency: str
):
    """
    📊 Consulta la tasa de cambio entre dos monedas

    Si solo quieres saber a cómo está el cambio entre dos monedas
    sin convertir una cantidad específica, este es tu endpoint.

    - **from**: La moneda base (ej: USD)
    - **to**: La moneda que quieres comparar (ej: MXN)

    Ejemplo: Si consultas USD a MXN, te diré cuántos pesos vale 1 dólar.
    """
    try:
        # Convertimos las monedas a mayúsculas y validamos que existan
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        if not validate_currency_code(from_currency):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid currency code: {from_currency}"
            )
        
        if not validate_currency_code(to_currency):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid currency code: {to_currency}"
            )
        
        # Obtener tasa
        rate = await exchange_service.get_exchange_rate(
            from_currency=from_currency,
            to_currency=to_currency
        )
        
        return rate
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching exchange rate"
        )


@router.get(
    "/currencies",
    response_model=CurrencyListResponse,
    responses={429: {"model": ErrorResponse}}
)
@limiter.limit(f"{rate_limit}/minute")
async def get_supported_currencies(request: Request):
    """
    Obtiene la lista de monedas soportadas

    Retorna lista de monedas con su código ISO 4217 y nombre
    """
    try:
        currencies = await exchange_service.get_supported_currencies()
        return currencies
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while fetching currencies"
        )
