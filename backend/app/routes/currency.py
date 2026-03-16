"""
Currency Routes - Endpoints para conversión de divisas
Implementa rate limiting y validación
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

# Crear router
router = APIRouter()

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address)
rate_limit = os.getenv("RATE_LIMIT_PER_MINUTE", "60")

# Instanciar servicio
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
    Convierte un monto de una moneda a otra

    - **amount**: Monto a convertir (debe ser positivo)
    - **from_currency**: Código ISO 4217 de moneda origen (ej: USD)
    - **to_currency**: Código ISO 4217 de moneda destino (ej: EUR)
    """
    try:
        # Validar códigos de moneda
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
        
        # Realizar conversión
        result = await exchange_service.convert(
            amount=conversion.amount,
            from_currency=conversion.from_currency,
            to_currency=conversion.to_currency
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred during conversion"
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
    Obtiene la tasa de cambio entre dos monedas

    - **from**: Código ISO 4217 de moneda origen
    - **to**: Código ISO 4217 de moneda destino
    """
    try:
        # Normalizar y validar
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
