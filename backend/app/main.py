"""
🏦 Aplicación FastAPI - Conversor de Divisas UMG

Esta es la aplicación principal del conversor de divisas.
Implementamos las mejores prácticas de seguridad para proteger tu información
y ofrecerte un servicio confiable y rápido.

Autor: Universidad Mariano Gálvez
Versión: 1.0.0
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

from app.routes import currency

# Configuramos el limitador de peticiones para evitar abuso del servicio
# Esto protege nuestra API de recibir demasiadas solicitudes de un mismo usuario
limiter = Limiter(key_func=get_remote_address)

# Creamos nuestra aplicación principal con toda su configuración
app = FastAPI(
    title="Conversor de Divisas API",
    description="API REST para conversión de divisas con mejores prácticas de seguridad",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Conectamos el limitador de peticiones con nuestra app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuramos CORS para permitir que nuestro frontend se comunique con el backend
# CORS = Compartir recursos entre diferentes dominios de forma segura
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Incluimos todas las rutas relacionadas con conversión de divisas
app.include_router(currency.router, prefix="/api", tags=["Currency"])


# Endpoint para verificar que el servicio está funcionando correctamente
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Verifica el estado del servicio
    
    Este endpoint lo usamos para monitorear que todo está funcionando bien.
    Es como tomarle el pulso a nuestra aplicación ❤️
    """
    return {
        "status": "healthy",
        "service": "conversor-divisas-api",
        "version": "1.0.0"
    }


# Página principal de la API - aquí damos la bienvenida
@app.get("/", tags=["Root"])
async def root():
    """
    Página de inicio de la API
    
    Aquí te damos la bienvenida y te mostramos información básica
    sobre cómo usar nuestra API de conversión de divisas.
    """
    return {
        "message": "Conversor de Divisas API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Capturamos cualquier error inesperado para manejarlo de forma segura
# Nunca mostramos detalles técnicos que puedan comprometer la seguridad
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Manejador de errores globales
    
    Si algo sale mal, atrapamos el error aquí para darte un mensaje
    amigable sin exponer detalles internos del sistema.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
