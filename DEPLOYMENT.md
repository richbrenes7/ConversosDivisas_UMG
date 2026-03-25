# 🚀 Guía de Despliegue

## Arquitectura de Despliegue

- **Frontend (React)**: Netlify
- **Backend (FastAPI)**: Render

---

## 📦 Desplegar Backend en Render

### Opción 1: Despliegue Automático con render.yaml

1. Ve a [Render](https://render.com) y crea una cuenta
2. Click en **"New"** → **"Blueprint"**
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el archivo `render.yaml`
5. Click en **"Apply"** y espera a que se despliegue

### Opción 2: Despliegue Manual

1. Ve a [Render](https://render.com)
2. Click en **"New"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Name**: `conversor-divisas-backend`
   - **Region**: Oregon (U.S. West)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

5. Agrega las **Environment Variables**:
   ```
   API_KEY=demo
   CORS_ORIGINS=https://tu-app.netlify.app
   RATE_LIMIT_PER_MINUTE=60
   ENVIRONMENT=production
   ```

6. Click en **"Create Web Service"**
7. Espera a que se despliegue (toma 2-5 minutos)
8. Copia la URL generada (ej: `https://conversor-divisas-backend.onrender.com`)

---

## 🌐 Desplegar Frontend en Netlify

### Paso 1: Preparar el Repositorio

1. Asegúrate de que los archivos `netlify.toml` y `public/_redirects` estén creados
2. Actualiza `netlify.toml` con la URL del backend de Render:
   ```toml
   REACT_APP_API_URL = "https://tu-backend.onrender.com"
   ```

### Paso 2: Desplegar en Netlify

1. Ve a [Netlify](https://netlify.com) y crea una cuenta
2. Click en **"Add new site"** → **"Import an existing project"**
3. Conecta con GitHub y selecciona tu repositorio
4. Configura:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`
   
5. Agrega **Environment Variables**:
   ```
   REACT_APP_API_URL=https://tu-backend.onrender.com
   ```

6. Click en **"Deploy site"**
7. Espera a que se despliegue (toma 1-2 minutos)
8. Netlify te asignará un dominio (ej: `random-name-123.netlify.app`)

### Paso 3: Actualizar CORS en el Backend

1. Ve a tu servicio en Render
2. Actualiza la variable de entorno `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://tu-app-real.netlify.app
   ```
3. El servicio se reiniciará automáticamente

---

## 🔧 Configuración Post-Despliegue

### Personalizar Dominio de Netlify (Opcional)

1. En Netlify, ve a **"Site settings"** → **"Domain management"**
2. Click en **"Options"** → **"Edit site name"**
3. Cambia el nombre a algo más descriptivo (ej: `conversor-divisas-umg`)

### Habilitar HTTPS (Automático)

- Netlify y Render proporcionan HTTPS automáticamente
- No se requiere configuración adicional

---

## ✅ Verificar el Despliegue

1. Visita tu URL de Netlify
2. Prueba convertir una moneda
3. Abre las DevTools (F12) → Console para verificar que no haya errores
4. Verifica que las peticiones vayan a tu backend de Render

---

## 🐛 Solución de Problemas

### Error: "Failed to fetch" o CORS

- **Causa**: El backend no permite el origen del frontend
- **Solución**: Actualiza `CORS_ORIGINS` en Render con la URL exacta de Netlify

### Error: "API timeout"

- **Causa**: El backend en Render se durmió (plan gratuito)
- **Solución**: Espera 30-60 segundos para que el backend se despierte

### Error de Build en Netlify

- **Causa**: Falta `package-lock.json` o dependencias incorrectas
- **Solución**: Verifica que `package-lock.json` esté en el repositorio

---

## 💰 Costos

- **Netlify**: 100% Gratis (300 minutos de build/mes, 100 GB bandwidth)
- **Render**: 100% Gratis (750 horas/mes, se duerme después de 15 min de inactividad)

---

## 🔄 Actualizaciones Futuras

Después del primer despliegue, cualquier push a `main` activará:
- ✅ **Render**: Re-despliegue automático del backend
- ✅ **Netlify**: Re-despliegue automático del frontend

---

## 📝 Checklist Final

- [ ] Backend desplegado en Render
- [ ] URL del backend copiada
- [ ] Frontend desplegado en Netlify
- [ ] Variable `REACT_APP_API_URL` configurada en Netlify
- [ ] Variable `CORS_ORIGINS` actualizada en Render
- [ ] Aplicación probada y funcionando
- [ ] Dominio personalizado configurado (opcional)

---

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs en Render (pestaña "Logs")
2. Revisa los logs en Netlify (pestaña "Deploys" → click en el deploy → "Deploy log")
3. Verifica que todas las variables de entorno estén correctas
