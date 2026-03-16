"""
Tests para el servicio de tasas de cambio
"""

import pytest
from app.services.exchange_rate import ExchangeRateService


@pytest.fixture
def exchange_service():
    return ExchangeRateService()


@pytest.mark.asyncio
async def test_convert_usd_to_eur(exchange_service):
    """Test conversión USD a EUR"""
    result = await exchange_service.convert(100, "USD", " EUR")
    
    assert result["amount"] == 100
    assert result["from_currency"] == "USD"
    assert result["to_currency"] == "EUR"
    assert result["converted_amount"] > 0
    assert result["exchange_rate"] > 0


@pytest.mark.asyncio
async def test_get_supported_currencies(exchange_service):
    """Test obtener monedas soportadas"""
    result = await exchange_service.get_supported_currencies()
    
    assert "currencies" in result
    assert "total" in result
    assert result["total"] > 0
    assert len(result["currencies"]) > 0


@pytest.mark.asyncio
async def test_get_exchange_rate(exchange_service):
    """Test obtener tasa de cambio"""
    result = await exchange_service.get_exchange_rate("USD", "EUR")
    
    assert result["base_currency"] == "USD"
    assert result["target_currency"] == "EUR"
    assert result["rate"] > 0
    assert "timestamp" in result
