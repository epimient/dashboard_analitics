# 📊 Survey Analytics Dashboard

Dashboard interactivo para análisis de encuestas universitarias con Inteligencia Artificial.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Groq](https://img.shields.io/badge/Groq-LLM-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 Características

- **Conexión en tiempo real** a Google Sheets vía Google Apps Script
- **Dashboard interactivo** con gráficos de Chart.js
- **Análisis con IA** de respuestas abiertas usando Groq (Llama 3.1)
- **Interfaz limpia** y minimalista
- **KPIs automáticos** de tendencias y distribuciones

---

## 📁 Estructura del Proyecto

```
dashboard_analitics/
├── backend/                 # API FastAPI
│   ├── .env.example         # Plantilla de variables de entorno
│   ├── config.py            # Configuración global
│   ├── main.py              # Entry point
│   ├── models/              # Modelos Pydantic
│   ├── services/            # Lógica de negocio
│   │   ├── data_loader.py   # Carga de datos (CSV, Sheets, Apps Script)
│   │   ├── survey_service.py # Servicio de encuestas
│   │   └── ai_service.py    # Análisis con IA (Groq/Ollama)
│   └── controllers/         # Endpoints REST
│       ├── survey_controller.py
│       └── ai_controller.py
├── frontend/                # Interfaz web
│   ├── index.html           # HTML principal
│   ├── css/
│   │   └── style.css        # Estilos personalizados
│   └── js/
│       ├── app.js           # Lógica principal
│       ├── api.js           # Cliente HTTP
│       ├── charts.js        # Gráficos Chart.js
│       └── ai_panel.js      # Panel de análisis IA
├── data/                    # Datos locales
│   └── encuesta.csv         # CSV de respaldo
└── google_apps_script/      # Integración Google Sheets
    ├── Code.gs              # Script de Apps Script
    ├── README.md            # Documentación específica
    └── QUICKSTART.md        # Guía rápida
```

---

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/survey-analytics-dashboard.git
cd survey-analytics-dashboard
```

### 2. Configurar el Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Variables de Entorno

Crea un archivo `.env` en `backend/` basado en `.env.example`:

```bash
cp .env.example .env
```

Edita `.env` con tu configuración:

```env
# URL de Google Apps Script (obligatorio)
APPS_SCRIPT_URL=https://script.google.com/macros/s/TU_ID_DEL_WEB_APP/exec

# Proveedor de IA por defecto
DEFAULT_AI_PROVIDER=groq

# API Key de Groq (obténla en https://console.groq.com/keys)
GROQ_API_KEY=gsk_TU_API_KEY

# Modelo de Groq
GROQ_MODEL=llama-3.1-8b-instant

# Ollama (opcional, backup local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

### 4. Configurar Google Apps Script

Sigue las instrucciones en [`google_apps_script/README.md`](google_apps_script/README.md) para:

1. Abrir tu Google Sheet
2. Ir a **Extensiones → Apps Script**
3. Pegar el código de `Code.gs`
4. Implementar como Web App
5. Copiar la URL y ponerla en `APPS_SCRIPT_URL`

### 5. Iniciar el Servidor

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

Accede a **http://localhost:8000**

---

## 📊 Uso

### Dashboard Principal

- **KPIs**: Total de respuestas, asistencia presencial, preferencia virtual/híbrida, internet estable
- **Gráficos**: Distribución por modalidad, disposición a virtual, nivel de compromiso, equipamiento

### Análisis con IA

1. Haz clic en **"Análisis IA"** en la sidebar
2. Expande cualquier sección de respuestas abiertas:
   - Razones para preferir presencial
   - Razones para preferir virtual/híbrida
   - Comentarios adicionales
3. Haz clic en **"Generar Análisis IA"**
4. La IA devolverá:
   - **Resumen ejecutivo**
   - **Sentimiento** (positivo/negativo/neutral)
   - **Palabras clave**
   - **Temas identificados**
   - **Recomendaciones**

---

## 🔌 API Endpoints

### Encuestas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/survey/responses` | Obtener todas las respuestas |
| `GET` | `/api/survey/stats` | Obtener estadísticas y KPIs |
| `POST` | `/api/survey/upload` | Subir archivo CSV |
| `POST` | `/api/survey/sheets` | Conectar Google Sheets (export URL) |
| `POST` | `/api/survey/apps-script` | Conectar Google Apps Script |

### Inteligencia Artificial

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/ai/analyze` | Analizar respuestas con IA |

**Ejemplo de request:**

```json
{
  "column_key": "comments",
  "provider": "groq",
  "model": "llama-3.1-8b-instant"
}
```

**Ejemplo de response:**

```json
{
  "column_key": "comments",
  "column_label": "Comentarios adicionales",
  "themes": [
    {"name": "Modalidad presencial", "description": "...", "count": 3}
  ],
  "sentiment": "negative",
  "sentiment_score": -0.6,
  "keywords": ["presencial", "virtual"],
  "recommendations": ["Ofrecer opción presencial"],
  "summary": "Los estudiantes prefieren...",
  "total_analyzed": 4,
  "provider_used": "groq",
  "model_used": "llama-3.1-8b-instant"
}
```

---

## 🧠 Proveedores de IA Soportados

### Groq (Recomendado)

- **Velocidad**: 300+ tokens/segundo
- **Modelo**: `llama-3.1-8b-instant`
- **Costo**: Free tier disponible
- **Configuración**: Solo necesita API key

### Ollama (Local)

- **Privacidad**: Todo se ejecuta localmente
- **Modelo**: `llama3` (u otro que tengas instalado)
- **Requisito**: Tener Ollama instalado y corriendo
- **Configuración**: `OLLAMA_BASE_URL=http://localhost:11434`

---

## 🔒 Seguridad

- **No subas** el archivo `.env` a GitHub
- **API Keys**: Se cargan desde variables de entorno
- **CORS**: Configurado para permitir solo orígenes específicos
- **Google Apps Script**: Configura el acceso como "Solo yo" o "Dominio específico" en producción

---

## 🧪 Testing

```bash
# Probar carga de datos
curl http://localhost:8000/api/survey/stats

# Probar análisis IA
curl -X POST http://localhost:8000/api/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"column_key": "comments"}'
```

---

## 📦 Dependencias Principales

### Backend

- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `pydantic` - Validación de datos
- `pydantic-settings` - Variables de entorno
- `pandas` - Procesamiento de datos
- `httpx` - Cliente HTTP asíncrono

### Frontend

- `Bootstrap 5.3` - Framework CSS
- `Chart.js` - Gráficos
- `Bootstrap Icons` - Iconos

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push (`git push origin feature/nueva-funcionalidad`)
5. Pull Request

---

## 📄 Licencia

MIT License - ver archivo [LICENSE](LICENSE) para detalles.

---

## 👨‍💻 Autor

Desarrollado por **Eddy** como proyecto de análisis de encuestas universitarias.

---

## 🙏 Agradecimientos

- [Groq](https://groq.com/) por la API de inferencia rápida
- [FastAPI](https://fastapi.tiangolo.com/) por el framework web
- [Chart.js](https://www.chartjs.org/) por las visualizaciones
- [Google Apps Script](https://developers.google.com/apps-script) por la integración con Sheets

---

## 📞 Soporte

Para dudas o problemas, abre un issue en el repositorio o contacta al autor.
