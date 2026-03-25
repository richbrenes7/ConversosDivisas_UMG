# 🔄 CI/CD con GitHub, Render y Netlify - Guía Completa

## ¿Qué es CI/CD?

**CI/CD** significa **Continuous Integration / Continuous Deployment** (Integración Continua / Despliegue Continuo).

Es un proceso automatizado que:
1. **Detecta** cuando haces cambios en tu código
2. **Prueba** que todo funcione correctamente
3. **Despliega** automáticamente a producción

**Analogía simple:** Es como tener un asistente que, cada vez que guardas tu trabajo, lo revisa y lo publica automáticamente en internet para que todos lo vean.

---

## 🏗️ Arquitectura de Nuestro Proyecto

```
┌─────────────────────────────────────────────────────────────┐
│                         DESARROLLADOR                        │
│                                                              │
│  Escribe código → git add → git commit → git push          │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                         GITHUB                               │
│                    (Repositorio Central)                     │
│                                                              │
│  • Almacena todo el código                                  │
│  • Guarda el historial de cambios                          │
│  • Rama: dev (desarrollo)                                   │
└──────────────┬──────────────────────────┬───────────────────┘
               │                          │
               │ Webhook                  │ Webhook
               │ (notificación)           │ (notificación)
               ▼                          ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│   RENDER (Backend)       │   │   NETLIFY (Frontend)     │
│                          │   │                          │
│  1. Detecta cambios      │   │  1. Detecta cambios      │
│  2. Clona repositorio    │   │  2. Clona repositorio    │
│  3. Instala dependencias │   │  3. Instala dependencias │
│  4. Inicia servidor      │   │  4. Construye app React  │
│                          │   │  5. Publica archivos     │
│  ✓ API en vivo          │   │  ✓ Sitio web en vivo    │
└──────────────────────────┘   └──────────────────────────┘
               │                          │
               │                          │
               ▼                          ▼
        https://conversosdivisas-umg     https://conversordivisasumg
        .onrender.com                    .netlify.app
```

---

## 🔗 ¿Cómo se Conectan GitHub, Render y Netlify?

### 1. **GitHub → Render/Netlify: Webhooks**

Un **webhook** es como un "toque en el hombro" automático.

**Cómo funciona:**
1. Cuando haces `git push` a GitHub
2. GitHub envía una notificación (webhook) a Render y Netlify
3. Les dice: "¡Oye! Hay código nuevo disponible"
4. Render y Netlify responden: "¡Recibido! Vamos a desplegarlo"

**Configuración:**
- ✅ Cuando conectaste tu repositorio en Render/Netlify, automáticamente se creó el webhook
- ✅ No necesitas hacer nada más
- ✅ GitHub maneja todo internamente

---

## 🚀 Flujo Completo de CI/CD - Paso a Paso

### Escenario: Quieres cambiar el color del botón en el frontend

```
PASO 1: Desarrollo Local
┌─────────────────────────────────────────┐
│  Tu Computadora                         │
│  ────────────────                       │
│  1. Abres VSCode                        │
│  2. Modificas el CSS del botón          │
│  3. Pruebas localmente (localhost:3000) │
│  4. Te gusta el resultado               │
└─────────────────────────────────────────┘
                  │
                  │ git add .
                  │ git commit -m "Cambiar color del botón"
                  │ git push origin dev
                  ▼
PASO 2: GitHub Recibe el Cambio
┌─────────────────────────────────────────┐
│  GitHub                                 │
│  ──────                                 │
│  1. Recibe tu código nuevo              │
│  2. Lo guarda en la rama 'dev'          │
│  3. Dispara webhooks a Render/Netlify   │
└─────────────────────────────────────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
      ▼                       ▼
PASO 3A: Render (Backend)    PASO 3B: Netlify (Frontend)
┌──────────────────┐          ┌──────────────────┐
│ Render Dashboard │          │ Netlify Dashboard│
│ ──────────────── │          │ ──────────────── │
│ Estado: Building │          │ Estado: Building │
│                  │          │                  │
│ Logs:            │          │ Logs:            │
│ → Clonando repo  │          │ → Clonando repo  │
│ → Installing...  │          │ → npm install    │
│ → Starting...    │          │ → npm run build  │
│ ✓ Live          │          │ → Publicando...  │
│                  │          │ ✓ Published      │
└──────────────────┘          └──────────────────┘
      │                              │
      │ 2-3 minutos                  │ 1-2 minutos
      ▼                              ▼
PASO 4: Aplicación Desplegada
┌─────────────────────────────────────────┐
│  Internet (Producción)                  │
│  ──────────────────                     │
│  • Backend actualizado (si cambió)      │
│  • Frontend actualizado con nuevo color │
│  • Usuarios ven los cambios             │
│  • ¡Sin intervención manual!            │
└─────────────────────────────────────────┘
```

---

## 🎯 Render: Backend CI/CD

### ¿Qué hace Render automáticamente?

Render es perfecto para aplicaciones backend (APIs, servidores).

#### Proceso de Despliegue en Render:

```bash
# 1. DETECCIÓN
GitHub envía webhook → Render detecta cambio en rama 'dev'

# 2. CLONACIÓN
git clone https://github.com/richbrenes7/ConversosDivisas_UMG.git --branch dev

# 3. NAVEGACIÓN
cd backend/

# 4. CONFIGURACIÓN DEL ENTORNO
- Detecta .python-version → Usa Python 3.11.0
- Lee variables de entorno (API_KEY, CORS_ORIGINS, etc.)

# 5. INSTALACIÓN DE DEPENDENCIAS
pip install -r requirements.txt

# 6. INICIO DEL SERVIDOR
uvicorn app.main:app --host 0.0.0.0 --port $PORT

# 7. HEALTH CHECKS
- Render verifica que la app responda en /health
- Si responde OK → Marca como "Live"
- Si falla → Mantiene versión anterior y notifica error

# 8. ACTUALIZACIÓN EN VIVO
- Transición sin downtime (zero-downtime deployment)
- Tu API nunca se cae durante el despliegue
```

#### Configuración Crítica en Render:

| Configuración | Valor | ¿Qué hace? |
|--------------|-------|------------|
| **Branch** | `dev` | Qué rama monitorear |
| **Root Directory** | `backend` | Dónde está el código |
| **Build Command** | `pip install -r requirements.txt` | Cómo instalar dependencias |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | Cómo iniciar la app |
| **Auto-Deploy** | ✅ On | Despliegue automático activado |

#### Archivos que Render Lee:

1. **`.python-version`** → Especifica la versión de Python
   ```
   3.11.0
   ```

2. **`requirements.txt`** → Lista de dependencias
   ```
   fastapi==0.115.0
   uvicorn[standard]==0.32.0
   ...
   ```

3. **`Procfile`** (opcional) → Comando de inicio
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

---

## 🌐 Netlify: Frontend CI/CD

### ¿Qué hace Netlify automáticamente?

Netlify está optimizado para sitios estáticos y aplicaciones React/Vue/Angular.

#### Proceso de Despliegue en Netlify:

```bash
# 1. DETECCIÓN
GitHub envía webhook → Netlify detecta cambio en rama 'dev'

# 2. CLONACIÓN
git clone https://github.com/richbrenes7/ConversosDivisas_UMG.git --branch dev

# 3. NAVEGACIÓN
cd frontend/

# 4. INSTALACIÓN DE NODE.JS
- Detecta package.json → Instala Node.js 18
- Lee variables de entorno (REACT_APP_API_URL)

# 5. INSTALACIÓN DE DEPENDENCIAS
npm install

# 6. CONSTRUCCIÓN DE LA APLICACIÓN
npm run build
# Esto ejecuta: react-scripts build
# Genera carpeta: frontend/build/ con archivos HTML/CSS/JS optimizados

# 7. OPTIMIZACIÓN AUTOMÁTICA
- Compresión de archivos (Gzip)
- Minificación de JS/CSS
- Optimización de imágenes
- Cache de assets

# 8. PUBLICACIÓN
- Sube archivos a Netlify CDN (Content Delivery Network)
- Distribuye en múltiples servidores globalmente
- Configura HTTPS automáticamente

# 9. REDIRECCIONES
- Configura reglas de _redirects para SPA
- Asegura que todas las rutas funcionen

# 10. ACTIVACIÓN
- Cambia DNS a la nueva versión
- Despliegue instantáneo sin downtime
```

#### Configuración Crítica en Netlify:

| Configuración | Valor | ¿Qué hace? |
|--------------|-------|------------|
| **Branch** | `dev` | Qué rama monitorear |
| **Base Directory** | `frontend` | Dónde está el código |
| **Build Command** | `npm run build` | Cómo construir la app |
| **Publish Directory** | `frontend/build` | Qué carpeta publicar |
| **Environment Variables** | `REACT_APP_API_URL=https://...` | Variables de entorno |

#### Archivos que Netlify Lee:

1. **`netlify.toml`** → Configuración de build y redirects
   ```toml
   [build]
     base = "frontend"
     command = "npm run build"
     publish = "build"
   
   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

2. **`package.json`** → Dependencias y scripts
   ```json
   {
     "scripts": {
       "start": "react-scripts start",
       "build": "react-scripts build"
     }
   }
   ```

3. **`public/_redirects`** → Reglas de ruteo para SPA
   ```
   /*    /index.html   200
   ```

---

## ⚡ Ventajas del CI/CD Automatizado

### Sin CI/CD (Manual) 😰
```
1. Terminas de codear
2. Abres FileZilla/FTP
3. Conectas al servidor
4. Subes archivos uno por uno
5. SSH al servidor
6. Reinicias el servicio manualmente
7. Rezas para que funcione
8. Si algo falla, reviertes manualmente
9. Tardas 30-60 minutos
10. Estrés y posibles errores humanos
```

### Con CI/CD (Automático) 😎
```
1. Terminas de codear
2. git push origin dev
3. Esperas 2-3 minutos
4. ✅ Todo desplegado y funcionando
5. Si algo falla, rollback automático
6. Logs detallados de qué pasó
7. Sin estrés, sin errores manuales
```

---

## 🔍 Monitoreo y Logs

### Ver el Progreso del Despliegue

#### En Render:
1. Ve a tu servicio en el dashboard
2. Click en la pestaña **"Logs"**
3. Verás en tiempo real:
   ```
   ==> Build started
   ==> Installing dependencies
   ==> Starting server
   ==> Your service is live 🎉
   ```

#### En Netlify:
1. Ve a tu sitio en el dashboard
2. Click en la pestaña **"Deploys"**
3. Click en el deploy más reciente
4. Verás:
   ```
   Build: Building
   → npm install
   → npm run build
   Deploy: Published
   ```

---

## 🛡️ Seguridad y Mejores Prácticas

### Variables de Entorno (Secrets)

**❌ NUNCA hagas esto:**
```javascript
// ❌ Código con secrets hardcodeados
const API_KEY = "mi-clave-super-secreta-123";
```

**✅ Siempre haz esto:**
```javascript
// ✅ Usar variables de entorno
const API_KEY = process.env.API_KEY;
```

**¿Por qué?**
- Los secrets no quedan en el código
- No se suben a GitHub
- Cada ambiente (dev, prod) puede tener values diferentes
- Render y Netlify los inyectan de forma segura

### Ramas y Ambientes

```
main (producción)  →  Netlify/Render (Producción)
  ↑
  │ merge cuando está listo
  │
dev (desarrollo)   →  Netlify/Render (Staging)
  ↑
  │ commits diarios
  │
feature/nueva      →  Solo local
```

---

## 🔄 Rollback (Volver Atrás)

### Si algo sale mal después de un deploy:

#### En Render:
1. Ve a **"Deployments"** en tu servicio
2. Click en un deploy anterior que funcionaba
3. Click **"Rollback to this version"**
4. ✅ Vuelve a la versión anterior en segundos

#### En Netlify:
1. Ve a **"Deploys"**
2. Click en un deploy anterior
3. Click **"Publish deploy"**
4. ✅ Tu sitio vuelve a la versión anterior

---

## 📊 Flujo de Trabajo Recomendado

### Desarrollo de una Nueva Funcionalidad

```bash
# 1. Crear rama de feature
git checkout -b feature/nuevo-boton
git push origin feature/nuevo-boton

# 2. Desarrollar y probar localmente
# ... escribes código ...
npm start  # frontend
uvicorn app.main:app --reload  # backend

# 3. Commit cuando funcione
git add .
git commit -m "feat: Agregar botón de favoritos"
git push origin feature/nuevo-boton

# 4. Hacer Pull Request en GitHub
# GitHub → Create Pull Request
# feature/nuevo-boton → dev

# 5. Revisar código (Code Review)
# Compañero revisa los cambios

# 6. Merge a dev
# GitHub → Merge Pull Request

# 7. CI/CD Automático
# ✅ Render despliega backend
# ✅ Netlify despliega frontend

# 8. Probar en staging
# https://conversordivisasumg.netlify.app

# 9. Si todo está bien, merge a main
git checkout main
git merge dev
git push origin main

# 10. Producción actualizada
# ✅ Todo en vivo
```

---

## 🎓 Conceptos Clave

### Webhook
**Definición:** Una notificación HTTP automática que un servicio envía a otro cuando ocurre un evento.

**Ejemplo:** GitHub le dice a Netlify "hay código nuevo" → Netlify responde "ok, lo despliego"

### Build
**Definición:** El proceso de convertir tu código fuente en una aplicación ejecutable.

**Frontend:** `npm run build` → Genera HTML/CSS/JS optimizado
**Backend:** `pip install` → Instala dependencias

### Deploy / Deployment
**Definición:** Publicar tu aplicación en internet para que los usuarios la usen.

### Zero-Downtime Deployment
**Definición:** Desplegar sin que tu app se caiga ni un segundo.

**Cómo funciona:**
1. Render/Netlify mantiene la versión vieja corriendo
2. Construye la nueva versión en paralelo
3. Cuando está lista, cambia el tráfico instantáneamente
4. Los usuarios nunca ven un error

---

## 🆚 Render vs Netlify: ¿Cuándo usar cada uno?

| Aspecto | Render | Netlify |
|---------|--------|---------|
| **Mejor para** | APIs, Backends, Bases de Datos | Sitios estáticos, SPAs, JAMstack |
| **Tecnologías** | Python, Node.js, Go, Docker | React, Vue, Angular, HTML |
| **Proceso** | Servidor siempre corriendo | Build una vez, servir archivos |
| **Costo** | CPU/RAM → Server activo | Ancho de banda → Archivos estáticos |
| **Velocidad** | Depende del servidor | CDN global (muy rápido) |
| **Casos de uso** | Lógica de negocio, autenticación | Interfaz de usuario |

---

## 🎯 Resumen Final

### ¿Qué aprendiste?

1. **CI/CD** = Automatización del despliegue
2. **GitHub** = Centro de control del código
3. **Webhooks** = Notificaciones automáticas
4. **Render** = Servidor para backend (Python/FastAPI)
5. **Netlify** = CDN para frontend (React)
6. **Variables de entorno** = Secrets seguros
7. **Rollback** = Volver atrás si algo falla
8. **Zero-downtime** = Sin caídas durante despliegues

### El flujo en 3 pasos:

```
1. git push origin dev
   ↓
2. GitHub notifica a Render y Netlify
   ↓
3. Deploy automático en 2-3 minutos
```

**Resultado:** Tu aplicación siempre está actualizada, sin esfuerzo manual, sin errores humanos, sin estrés. 🚀

---

## 📚 Recursos Adicionales

- [GitHub Actions](https://docs.github.com/en/actions) - CI/CD directamente en GitHub
- [Render Docs](https://render.com/docs) - Documentación oficial
- [Netlify Docs](https://docs.netlify.com/) - Documentación oficial
- [The Twelve-Factor App](https://12factor.net/) - Mejores prácticas

---

**Autor:** Universidad Mariano Gálvez - Proyecto Conversor de Divisas  
**Fecha:** Marzo 2026  
**Repositorio:** https://github.com/richbrenes7/ConversosDivisas_UMG
