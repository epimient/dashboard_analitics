"""
main.py — Entry point de la aplicación FastAPI.
Configura routers, CORS, sirve estáticos del frontend y carga los datos al inicio.
"""
from contextlib import asynccontextmanager
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from services.data_loader import DataLoader
from services.survey_service import SurveyService
from services.ai_service import AIService
from controllers.survey_controller import router as survey_router
from controllers.ai_controller import router as ai_router

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Instancias Globales de Servicios
# ------------------------------------------------------------------
data_loader = DataLoader()
survey_service = SurveyService()
ai_service = AIService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de arranque y apagado del servidor."""
    logger.info("Iniciando Survey Analytics API...")

    # Intentar cargar desde Apps Script primero
    if settings.apps_script_url:
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            # Ejecutar en hilo separado para no bloquear
            responses = await data_loader.load_from_apps_script(settings.apps_script_url)
            survey_service.load(responses)
            logger.info("✓ Se cargaron %d respuestas desde Google Apps Script", len(responses))
        except Exception as e:
            logger.warning("No se pudo cargar desde Apps Script: %s. Usando CSV local.", e)
            try:
                csv_path = Path(__file__).parent / settings.default_csv_path
                responses = data_loader.load_from_path(csv_path)
                survey_service.load(responses)
                logger.info("Se cargaron %d respuestas desde %s", len(responses), csv_path)
            except Exception as e2:
                logger.warning("No se pudo cargar el CSV por defecto: %s", e2)
    else:
        # Fallback a CSV local
        try:
            csv_path = Path(__file__).parent / settings.default_csv_path
            responses = data_loader.load_from_path(csv_path)
            survey_service.load(responses)
            logger.info("Se cargaron %d respuestas desde %s", len(responses), csv_path)
        except Exception as e:
            logger.warning("No se pudo cargar el CSV por defecto: %s", e)

    yield
    logger.info("Apagando API.")


# ------------------------------------------------------------------
# Configuración de la App
# ------------------------------------------------------------------
app = FastAPI(
    title="Survey Analytics API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registramos routers
app.include_router(survey_router)
app.include_router(ai_router)

# ------------------------------------------------------------------
# Frontend Static Files
# ------------------------------------------------------------------
frontend_dir = Path(__file__).parent.parent / "frontend"

if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
else:
    logger.warning("La carpeta 'frontend' no existe en %s", frontend_dir)
