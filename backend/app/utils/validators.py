"""
Validators - Utilidades para validación de datos
Implementa validaciones adicionales y sanitización
"""

import re
from typing import Optional


def validate_currency_code(code: str) -> bool:
    """
    Valida que un código de moneda sea válido (ISO 4217)
    
    Args:
        code: Código de moneda a validar
    
    Returns:
        bool: True si es válido, False si no
    """
    if not code or not isinstance(code, str):
        return False
    
    # Debe ser exactamente 3 caracteres alfabéticos
    pattern = r'^[A-Z]{3}$'
    return bool(re.match(pattern, code.upper()))


def validate_amount(amount: float, min_value: float = 0.01, max_value: float = 1000000000) -> bool:
    """
    Valida que un monto esté dentro de rangos permitidos
    
    Args:
        amount: Monto a validar
        min_value: Valor mínimo permitido
        max_value: Valor máximo permitido
    
    Returns:
        bool: True si es válido, False si no
    """
    if not isinstance(amount, (int, float)):
        return False
    
    if amount < min_value or amount > max_value:
        return False
    
    # Verificar que tenga máximo 2 decimales
    if round(amount, 2) != amount:
        return False
    
    return True


def sanitize_string(text: str, max_length: int = 100) -> str:
    """
    Sanitiza un string removiendo caracteres peligrosos
    
    Args:
        text: Texto a sanitizar
        max_length: Longitud máxima permitida
    
    Returns:
        str: Texto sanitizado
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remover caracteres no alfanuméricos excepto espacios, guiones y guiones bajos
    sanitized = re.sub(r'[^a-zA-Z0-9\s\-_]', '', text)
    
    # Limitar longitud
    sanitized = sanitized[:max_length]
    
    # Remover espacios extras
    sanitized = ' '.join(sanitized.split())
    
    return sanitized


def validate_email(email: str) -> bool:
    """
    Valida formato de email
    
    Args:
        email: Email a validar
    
    Returns:
        bool: True si es válido, False si no
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
