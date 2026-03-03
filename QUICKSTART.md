# ⚡ Quick Start Guide

Inicio rápido del Survey Analytics Dashboard en 5 minutos.

---

## 1️⃣ Instalar dependencias

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 2️⃣ Configurar variables de entorno

```bash
cd backend
cp .env.example .env
```

Edita `.env` y agrega:

```env
# Tu API Key de Groq (gratis en https://console.groq.com/keys)
GROQ_API_KEY=gsk_TU_API_KEY

# URL de tu Google Apps Script (ver paso 3)
APPS_SCRIPT_URL=https://script.google.com/macros/s/TU_ID/exec
```

---

## 3️⃣ Configurar Google Apps Script

1. Abre tu Google Sheet con las encuestas
2. **Extensiones** → **Apps Script**
3. Borra el código y pega el contenido de `google_apps_script/Code.gs`
4. Cambia `SHEET_NAME` por el nombre de tu hoja
5. **Implementar** → **Nueva implementación** → **Aplicación web**
6. **Quién tiene acceso:** `Cualquier usuario`
7. Copia la URL y pégala en `APPS_SCRIPT_URL` en el `.env`

---

## 4️⃣ Iniciar el servidor

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

---

## 5️⃣ Abrir el dashboard

Navega a: **http://localhost:8000**

---

## ✅ Verificar que funciona

### Test 1: Verificar datos

```bash
curl http://localhost:8000/api/survey/stats
```

Deberías ver JSON con `total_responses` y KPIs.

### Test 2: Verificar IA

```bash
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"column_key": "comments"}'
```

Deberías ver análisis con `summary`, `sentiment`, `keywords`, etc.

---

## 🆘 Problemas comunes

| Error | Solución |
|-------|----------|
| `ModuleNotFoundError` | Ejecuta `pip install -r requirements.txt` |
| `Groq API key no configurada` | Agrega tu key en `.env` |
| `Datos no cargados` | Verifica la URL de Apps Script |
| Puerto 8000 ocupado | Usa `--port 8001` |

---

## 📚 Más información

- [README completo](README.md)
- [Google Apps Script](google_apps_script/README.md)

---

**¡Listo!** Tu dashboard está funcionando. 🎉
