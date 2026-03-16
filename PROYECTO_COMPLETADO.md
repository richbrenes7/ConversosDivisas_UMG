# 🎉 PROYECTO CONVERSOR DE DIVISAS - COMPLETADO

## ✅ Estado del Proyecto

**Rama actual**: `dev`  
**Commit**: `02452a2` - Implementación completa  
**Archivos creados**: 30 archivos principales  
**Estado**: ✅ Listo para ejecutar

---

## 📁 Estructura del Proyecto

```
ConversosDivisas_UMG/
├── backend/                         # Python FastAPI
│   ├── app/
│   │   ├── main.py                 # ✅ Aplicación principal
│   │   ├── models.py               # ✅ Modelos Pydantic
│   │   ├── routes/
│   │   │   └── currency.py         # ✅ Endpoints API
│   │   ├── services/
│   │   │   └── exchange_rate.py    # ✅ Lógica de negocio
│   │   └── utils/
│   │       └── validators.py       # ✅ Validaciones
│   ├── tests/
│   │   └── test_exchange_rate.py   # ✅ Tests unitarios
│   ├── requirements.txt            # ✅ Dependencias Python
│   ├── Dockerfile                  # ✅ Imagen Docker
│   └── .env.example                # ✅ Template de configuración
│
├── frontend/                        # React App
│   ├── src/
│   │   ├── components/
│   │   │   ├── CurrencyConverter.js     # ✅ Componente principal
│   │   │   └── CurrencyConverter.css    # ✅ Estilos del conversor
│   │   ├── services/
│   │   │   └── api.js              # ✅ Cliente HTTP
│   │   ├── App.js                  # ✅ Componente raíz
│   │   ├── App.css                 # ✅ Estilos globales
│   │   ├── index.js                # ✅ Entry point
│   │   └── App.test.js             # ✅ Tests
│   ├── public/
│   │   └── index.html              # ✅ HTML template
│   ├── package.json                # ✅ Dependencias Node
│   ├── Dockerfile                  # ✅ Imagen Docker
│   └── .env.example                # ✅ Template de configuración
│
├── docker-compose.yml               # ✅ Orquestación completa
├── .gitignore                       # ✅ Archivos ignorados
└── README.md                        # ✅ Documentación completa
```

---

## 🚀 CÓMO EJECUTAR EL PROYECTO

### Opción 1: Con Docker (RECOMENDADO)

```bash
# 1. Asegúrate de estar en la carpeta del proyecto
cd Data\ConversosDivisas_UMG

# 2. Verificar que Docker Desktop esté corriendo
docker --version

# 3. Iniciar la aplicación completa
docker-compose up --build

# Espera a que termine de construir (primera vez puede tardar 3-5 minutos)
# Verás estos mensajes cuando esté listo:
# - backend_1   | INFO: Uvicorn running on http://0.0.0.0:8000
# - frontend_1  | webpack compiled successfully

# 4. Abrir en el navegador:
#    Frontend: http://localhost:3000
#    Backend API: http://localhost:8000
#    Docs API: http://localhost:8000/docs
```

### Opción 2: Desarrollo Manual (Sin Docker)

#### Backend:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Backend corriendo en: http://localhost:8000
```

#### Frontend (en otra terminal):
```bash
cd frontend
npm install
npm start
# Frontend corriendo en: http://localhost:3000
```

---

## 🎨 Características Implementadas

### Backend (FastAPI)
✅ API REST con FastAPI  
✅ Validación de datos con Pydantic  
✅ Rate limiting (60 requests/minuto)  
✅ CORS configurado  
✅ Caché de tasas de cambio (1 hora)  
✅ Manejo de errores robusto  
✅ Health checks  
✅ Documentación automática (Swagger)  
✅ Tests unitarios  

### Frontend (React)
✅ Interfaz moderna y responsiva  
✅ Diseño con gradientes y animaciones  
✅ Validación de formularios  
✅ Manejo de estados con hooks  
✅ Cliente HTTP con Axios  
✅ Feedback visual (loading, errores)  
✅ Responsive mobile-first  
✅ Botón de intercambio de monedas  

### Seguridad
✅ Validación en backend y frontend  
✅ Rate limiting  
✅ Sanitización de datos  
✅ Variables de entorno  
✅ Usuario no-root en containers  
✅ Sin exposición de errores internos  

### DevOps
✅ Docker multi-stage builds  
✅ Docker Compose  
✅ Hot reload activado  
✅ Health checks  
✅ Redes aisladas  
✅ Volúmenes para desarrollo  

---

## 📖 Endpoints API Disponibles

### Health Check
```
GET /health
```

### Convertir Divisas
```
POST /api/convert
Content-Type: application/json

{
  "amount": 100.00,
  "from_currency": "USD",
  "to_currency": "GTQ"
}
```

### Obtener Tasa de Cambio
```
GET /api/exchange-rate?from=USD&to=EUR
```

### Listar Monedas Soportadas
```
GET /api/currencies
```

---

## 💱 Monedas Soportadas

- **USD** - US Dollar
- **EUR** - Euro  
- **GTQ** - Guatemalan Quetzal ⭐
- **MXN** - Mexican Peso
- **GBP** - British Pound
- **JPY** - Japanese Yen
- **CAD** - Canadian Dollar
- **AUD** - Australian Dollar
- **CHF** - Swiss Franc
- **CNY** - Chinese Yuan
- **BRL** - Brazilian Real
- **ARS** - Argentine Peso
- **COP** - Colombian Peso
- **CRC** - Costa Rican Colón
- **HNL** - Honduran Lempira
- **NIO** - Nicaraguan Córdoba

---

## 🧪 Ejecutar Tests

```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test
```

---

## 📊 Ver Logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

---

## 🛑 Detener la Aplicación

```bash
# Detener contenedores
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

---

## 🔄 Workflow para Contributors

### 1. Clonar y Preparar
```bash
git clone https://github.com/richbrenes7/ConversosDivisas_UMG.git
cd ConversosDivisas_UMG
git checkout dev
```

### 2. Ejecutar Localmente
```bash
docker-compose up --build
```

### 3. Hacer Cambios
```bash
# Crear branch feature
git checkout -b feature/nueva-funcionalidad

# Hacer cambios en el código...
# El hot reload actualizará automáticamente

# Commit
git add .
git commit -m "feat: descripción del cambio"
```

### 4. Push y Pull Request
```bash
git push origin feature/nueva-funcionalidad
# Crear PR en GitHub hacia rama dev
```

---

## 🐛 Troubleshooting

### Puerto en Uso
```bash
# Cambiar puertos en docker-compose.yml
ports:
  - "3001:3000"  # frontend
  - "8001:8000"  # backend
```

### Reconstruir Imágenes
```bash
docker-compose build --no-cache
docker-compose up
```

### Ver Errores de Construcción
```bash
docker-compose build backend
docker-compose build frontend
```

### Limpiar Docker
```bash
docker-compose down -v
docker system prune -a
```

---

## 📝 Próximos Pasos Sugeridos

### Features
- [ ] Agregar historial de conversiones
- [ ] Guardar conversiones favoritas
- [ ] Gráficas de tendencias de tasas
- [ ] Modo oscuro
- [ ] Múltiples idiomas (i18n)
- [ ] PWA (Progressive Web App)

### Técnicas
- [ ] CI/CD con GitHub Actions
- [ ] Tests de integración
- [ ] Tests E2E con Cypress
- [ ] Monitoring con Prometheus
- [ ] Logging centralizado
- [ ] Deploy en cloud (AWS/Azure/GCP)

---

## 👥 Información del Proyecto

**Universidad**: Universidad Mariano Gálvez  
**Curso**: Desarrollo de Software  
**Año**: 2026  
**Rama de Desarrollo**: `dev`  
**Rama de Producción**: `main`  

---

## 📚 Recursos Adicionales

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Documentación React](https://react.dev/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [ExchangeRate-API](https://www.exchangerate-api.com/)

---

## ✅ Checklist de Verificación

Antes de hacer push, verifica:

- [ ] La aplicación corre con `docker-compose up`
- [ ] Frontend accesible en http://localhost:3000
- [ ] Backend accesible en http://localhost:8000
- [ ] API docs en http://localhost:8000/docs
- [ ] Tests pasan: `docker-compose exec backend pytest`
- [ ] Sin errores en consola del navegador
- [ ] Sin errores en logs de Docker
- [ ] .env y .env.local no están en el commit
- [ ] README actualizado si hay cambios importantes

---

## 🎉 ¡Listo para Usar!

El proyecto está **100% funcional** y listo para que cualquier contributor lo clone y ejecute localmente.

**Comando Rápido**:
```bash
git clone https://github.com/richbrenes7/ConversosDivisas_UMG.git
cd ConversosDivisas_UMG
git checkout dev
docker-compose up --build
```

**¡Abre http://localhost:3000 y empieza a convertir divisas!** 💱
