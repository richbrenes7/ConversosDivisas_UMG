# 💱 Conversor de Divisas UMG

Aplicación web full-stack para conversión de divisas en tiempo real con arquitectura moderna y mejores prácticas de seguridad.

## 📚 Documentación

- [CICD_EXPLICACION.md](CICD_EXPLICACION.md) - Explicación completa del flujo CI/CD, webhooks y despliegue automático
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guía paso a paso para desplegar en Render y Netlify

## 🏗️ Arquitectura

- **Backend**: Python FastAPI con validación y rate limiting
- **Frontend**: React con diseño moderno y responsivo
- **Containerización**: Docker & Docker Compose
- **API Externa**: ExchangeRate-API para tasas de cambio en tiempo real
- **Deployment**: Render (backend) + Netlify (frontend) con CI/CD automático

## 🛠️ Stack Tecnológico

**Backend**:
- FastAPI 0.115.0
- Python 3.11.0
- Pydantic 2.9.2 (validación de datos)
- Uvicorn 0.32.0 (ASGI server)
- slowapi (rate limiting)
- httpx (cliente HTTP async)

**Frontend**:
- React 18.2.0
- Node.js 24.14.0
- Axios 1.6.5 (cliente HTTP)
- CSS moderno (variables CSS, flexbox, animations)

**DevOps & Deployment**:
- Docker & Docker Compose
- Render (backend PaaS)
- Netlify (frontend CDN/hosting)
- GitHub (control de versiones + webhooks CI/CD)

## 📋 Características

- Conversión de divisas en tiempo real  
- Soporte para múltiples monedas (USD, EUR, GTQ, MXN, y más)  
- Validación de entrada robusta  
- Rate limiting para prevenir abuso  
- CORS configurado correctamente  
- Manejo de errores completo  
- Diseño responsivo moderno  
- Containerizado con Docker  
- Hot reload en desarrollo  
- Health checks automatizados  

## 🔒 Seguridad

- Validación de entrada en backend y frontend
- Rate limiting (60 requests/minuto por defecto)
- CORS configurado adecuadamente
- Variables de entorno para secrets
- Sanitización de datos
- Headers de seguridad
- Sin exposición de errores internos

## 🔀 Workflow y CI/CD

**Estrategia de Branching**:
- `main` - Rama de producción (protegida)
- `dev` - Rama de desarrollo (staging)

**Integración Continua**:
- Los cambios se prueban localmente antes de push
- Pull requests hacia `dev` para revisión de código
- Merge a `main` solo después de testing en `dev`

**Despliegue Continuo**:
- Push a `main` → Deploy automático a producción
- Render detecta cambios via webhook y redeploya el backend
- Netlify detecta cambios via webhook y redeploya el frontend
- Tiempo de deploy: 2-3 minutos

Ver [CICD_EXPLICACION.md](CICD_EXPLICACION.md) para detalles técnicos del flujo completo.

## 🚀 Inicio Rápido

### Prerequisitos

- Docker Desktop instalado
- Git

### Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/richbrenes7/ConversosDivisas_UMG.git
cd ConversosDivisas_UMG

# 2. Cambiar a rama dev
git checkout dev

# 3. Configurar variables de entorno (opcional)
cp backend/.env.example backend/.env
# Editar backend/.env si quieres usar tu propia API key

# 4. Iniciar la aplicación
docker-compose up --build

# La aplicación estará disponible en:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - Docs API: http://localhost:8000/docs
```

### Detener la Aplicación

```bash
# Detener contenedores
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

## 📁 Estructura del Proyecto

```
ConversosDivisas_UMG/
├── backend/                    # API Python FastAPI
│   ├── app/
│   │   ├── main.py            # Aplicación principal
│   │   ├── models.py          # Modelos Pydantic
│   │   ├── routes/            # Endpoints de API
│   │   ├── services/          # Lógica de negocio
│   │   └── utils/             # Utilidades y validadores
│   ├── requirements.txt       # Dependencias Python
│   ├── Dockerfile            # Imagen Docker backend
│   └── .env.example          # Template de variables
│
├── frontend/                   # Aplicación React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── services/          # Cliente API
│   │   ├── App.js            # Componente principal
│   │   └── index.js          # Entry point
│   ├── public/               # Assets estáticos
│   ├── package.json          # Dependencias Node
│   └── Dockerfile            # Imagen Docker frontend
│
├── docker-compose.yml         # Orquestación de servicios
├── .gitignore                # Archivos ignorados
└── README.md                 # Este archivo
```

## 🔧 Desarrollo

### Ejecutar Tests

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test
```

### Ver Logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Acceder a Contenedor

```bash
# Backend
docker-compose exec backend /bin/bash

# Frontend
docker-compose exec frontend /bin/sh
```

## 📡 API Endpoints

### Health Check
```
GET /health
```

### Conversión de Divisas
```
POST /api/convert
Content-Type: application/json

{
  "amount": 100.00,
  "from_currency": "USD",
  "to_currency": "EUR"
}
```

### Monedas Soportadas
```
GET /api/currencies
```

### Tasa de Cambio
```
GET /api/exchange-rate?from=USD&to=EUR
```

### Documentación Interactiva

En desarrollo local:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🐛 Troubleshooting

### Puerto en uso

Si el puerto 3000 o 8000 está en uso:

```bash
# Cambiar puertos en docker-compose.yml
ports:
  - "3001:3000"  # frontend
  - "8001:8000"  # backend
```

### Permisos de Windows

Si hay problemas de permisos en Windows:

```bash
# Ejecutar Docker Desktop como Administrador
# O compartir la unidad en Docker Desktop Settings > Resources > File Sharing
```

### Hot Reload no funciona

```bash
# En docker-compose.yml, verificar que exista:
environment:
  - CHOKIDAR_USEPOLLING=true
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agrega nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crea un Pull Request hacia la rama `dev`

## 📝 Notas Importantes

- La API externa usa ExchangeRate-API con el plan gratuito (1500 requests/mes)
- Para producción se recomienda obtener una API key personalizada
- El rate limiting está configurado de forma conservadora, ajustar según necesidad
- Las tasas de cambio pueden tener un pequeño delay de caché para optimizar rendimiento
- Las variables de entorno deben configurarse correctamente antes del despliegue

## 📄 Licencia

Este proyecto es para fines educativos - Universidad Mariano Gálvez de Guatemala

## Autor

**Ricardo Brenes**  
GitHub: [@richbrenes7](https://github.com/richbrenes7)

---

Para más información sobre despliegue y CI/CD, consulta la documentación en [CICD_EXPLICACION.md](CICD_EXPLICACION.md) y [DEPLOYMENT.md](DEPLOYMENT.md).
