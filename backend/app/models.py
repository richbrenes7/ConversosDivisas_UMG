"""
📋 Modelos de Datos - Conversor de Divisas

Aquí definimos cómo deben verse los datos que entran y salen de nuestra API.
Implementamos validación estricta para asegurarnos de que todo esté correcto
antes de procesarlo. Piensa en esto como un "control de calidad" automático.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from decimal import Decimal


class ConversionRequest(BaseModel):
    """
    📥 Lo que necesitamos para hacer una conversión
    
    Cuando quieres convertir dinero, estos son los datos que debes enviarnos.
    Los validamos automáticamente para evitar errores.
    """
    amount: float = Field(
        ...,
        gt=0,
        le=1000000000,
        description="¿Cuánto dinero quieres convertir? Debe ser mayor que 0 y menor a mil millones"
    )
    from_currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Código de 3 letras de la moneda origen (ejemplo: USD, EUR, MXN)"
    )
    to_currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Código de 3 letras de la moneda destino (ejemplo: GTQ, EUR, JPY)"
    )

    @validator('from_currency', 'to_currency')
    def validate_currency_code(cls, v):
        """
        Verificamos que el código de moneda sea válido
        
        Los códigos deben ser de 3 letras, sin números ni caracteres especiales.
        Los convertimos automáticamente a mayúsculas por si vienen en minúsculas.
        """
        v = v.upper()
        if not v.isalpha():
            raise ValueError('El código de moneda solo puede contener letras (ejemplo: USD, no US1)')
        return v

    @validator('amount')
    def validate_amount(cls, v):
        """
        Verificamos que el monto tenga máximo 2 decimales
        
        Trabajamos con dinero real, así que no aceptamos más de 2 decimales.
        Por ejemplo: 100.50 es válido, pero 100.555 no lo es.
        """
        if round(v, 2) != v:
            raise ValueError('El monto solo puede tener hasta 2 decimales (ejemplo: 100.50)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 100.00,
                "from_currency": "USD",
                "to_currency": "GTQ"
            }
        }


class ConversionResponse(BaseModel):
    """
    📤 Lo que te devolvemos después de la conversión
    
    Después de procesar tu solicitud, te enviamos todos estos datos
    para que sepas exactamente qué se convirtió y cuándo.
    """
    amount: float = Field(..., description="La cantidad original que querías convertir")
    from_currency: str = Field(..., description="De qué moneda la convertiste")
    to_currency: str = Field(..., description="A qué moneda la convertiste")
    exchange_rate: float = Field(..., description="La tasa de cambio que usamos (cuánto vale 1 unidad)")
    converted_amount: float = Field(..., description="El resultado: cuánto dinero tienes en la nueva moneda")
    timestamp: str = Field(..., description="Cuándo se hizo esta conversión")

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 100.00,
                "from_currency": "USD",
                "to_currency": "GTQ",
                "exchange_rate": 7.85,
                "converted_amount": 785.00,
                "timestamp": "2026-03-24T12:00:00Z"
            }
        }


class ExchangeRateResponse(BaseModel):
    """📊 Información de la tasa de cambio entre dos monedas"""
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
