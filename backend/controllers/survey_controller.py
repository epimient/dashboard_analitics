"""
controllers/survey_controller.py — Endpoints para datos de la encuesta.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel

from models.survey import SurveyResponse, SurveyStats, FilterParams
from services.data_loader import DataLoader
from services.survey_service import SurveyService

router = APIRouter(prefix="/api/survey", tags=["Survey"])


class UploadResponse(BaseModel):
    ok: bool
    num_records: int
    message: str


class SheetsConnectRequest(BaseModel):
    url: str


# Dependencias para inyectar servicios en las rutas
def get_survey_service() -> SurveyService:
    from main import survey_service
    return survey_service


def get_data_loader() -> DataLoader:
    from main import data_loader
    return data_loader


@router.get("/responses", response_model=list[SurveyResponse])
async def get_responses(
    filters: Annotated[FilterParams, Depends()],
    svc: Annotated[SurveyService, Depends(get_survey_service)]
):
    """Devuelve todas las respuestas aplicando filtros opcionales."""
    if not svc.is_loaded:
        raise HTTPException(status_code=400, detail="Datos no cargados")
    return svc.get_all(filters)


@router.get("/stats", response_model=SurveyStats)
async def get_stats(
    filters: Annotated[FilterParams, Depends()],
    svc: Annotated[SurveyService, Depends(get_survey_service)]
):
    """Devuelve KPIs y distribuciones estadísticas."""
    if not svc.is_loaded:
        raise HTTPException(status_code=400, detail="Datos no cargados")
    return svc.get_stats(filters)


@router.post("/upload", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    loader: Annotated[DataLoader, Depends(get_data_loader)] = None,
    svc: Annotated[SurveyService, Depends(get_survey_service)] = None
):
    """Sube un archivo CSV y recarga los datos en memoria."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser .csv")

    try:
        content = await file.read()
        responses = loader.load_from_bytes(content, filename=file.filename)
        svc.load(responses)
        return UploadResponse(
            ok=True,
            num_records=len(responses),
            message=f"Se cargaron {len(responses)} registros exitosamente."
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/sheets", response_model=UploadResponse)
async def connect_sheets(
    payload: SheetsConnectRequest,
    loader: Annotated[DataLoader, Depends(get_data_loader)],
    svc: Annotated[SurveyService, Depends(get_survey_service)]
):
    """Conecta una URL de Google Sheets y carga los datos."""
    try:
        responses = await loader.load_from_sheets_url(payload.url)
        svc.load(responses)
        return UploadResponse(
            ok=True,
            num_records=len(responses),
            message=f"Conectado a Google Sheets: {len(responses)} registros cargados."
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Error al conectar Sheets: {str(exc)}")


@router.post("/apps-script", response_model=UploadResponse)
async def connect_apps_script(
    payload: SheetsConnectRequest,
    loader: Annotated[DataLoader, Depends(get_data_loader)],
    svc: Annotated[SurveyService, Depends(get_survey_service)]
):
    """
    Conecta un Google Apps Script Web App y carga los datos.
    La URL debe ser la del Web App publicado (termina en /exec).
    """
    try:
        responses = await loader.load_from_apps_script(payload.url)
        svc.load(responses)
        return UploadResponse(
            ok=True,
            num_records=len(responses),
            message=f"Conectado a Google Apps Script: {len(responses)} registros cargados."
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Error al conectar Apps Script: {str(exc)}")
