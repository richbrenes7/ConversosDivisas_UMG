"""
Modelos Pydantic para validación de datos
Implementa validación estricta y sanitización
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal


class ConversionRequest(BaseModel):
    """Modelo para solicitud de conversión"""
    amount: float = Field(
        ...,
        gt=0,
        le=1000000000,
        description="Cantidad a convertir (debe ser positiva y menor a 1 billón)"
    )
    from_currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Código de moneda origen (ISO 4217)"
    )
    to_currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Código de moneda destino (ISO 4217)"
    )

    @validator('from_currency', 'to_currency')
    def validate_currency_code(cls, v):
        """Validar que el código de moneda esté en mayúsculas y sea alfabético"""
        v = v.upper()
        if not v.isalpha():
            raise ValueError('Currency code must contain only letters')
        return v

    @validator('amount')
    def validate_amount(cls, v):
        """Validar que el monto tenga máximo 2 decimales"""
        if round(v, 2) != v:
            raise ValueError('Amount must have at most 2 decimal places')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 100.00,
                "from_currency": "USD",
                "to_currency": "EUR"
            }
        }


class ConversionResponse(BaseModel):
    """Modelo para respuesta de conversión"""
    amount: float = Field(..., description="Cantidad original")
    from_currency: str = Field(..., description="Moneda origen")
    to_currency: str = Field(..., description="Moneda destino")
    exchange_rate: float = Field(..., description="Tasa de cambio")
    converted_amount: float = Field(..., description="Cantidad convertida")
    timestamp: str = Field(..., description="Timestamp de la conversión")

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 100.00,
                "from_currency": "USD",
                "to_currency": "EUR",
                "exchange_rate": 0.85,
                "converted_amount": 85.00,
                "timestamp": "2026-03-16T12:00:00Z"
            }
        }


class ExchangeRateResponse(BaseModel):
    """Modelo para respuesta de tasa de cambio"""
    base_currency: str
    target_currency: str
    rate: float
    timestamp: str


class CurrencyListResponse(BaseModel):
    """Modelo para lista de monedas soportadas"""
    currencies: list[dict[str, str]]
    total: int


class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    error: str
    message: str
    details: Optional[str] = None
