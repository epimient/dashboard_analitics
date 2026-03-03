"""
controllers/ai_controller.py — Endpoints para análisis con Inteligencia Artificial.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from models.ai_analysis import AIAnalysisResult, AIRequest
from services.ai_service import AIService
from services.survey_service import SurveyService

router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])


def get_survey_service() -> SurveyService:
    from main import survey_service
    return survey_service


def get_ai_service() -> AIService:
    from main import ai_service
    return ai_service


@router.post("/analyze", response_model=AIAnalysisResult)
async def analyze_responses(
    request: AIRequest,
    ai_svc: Annotated[AIService, Depends(get_ai_service)],
    survey_svc: Annotated[SurveyService, Depends(get_survey_service)]
):
    """
    Analiza las respuestas de una pregunta abierta usando el provider seleccionado.
    Si la lista request.responses viene vacía, intenta sacarla del SurveyService
    usando request.column_key.
    """
    try:
        if not request.responses:
            # Autocompletar con respuestas mapeadas
            if not survey_svc.is_loaded:
                raise HTTPException(status_code=400, detail="Datos no cargados y respuestas vacías en request")
            request.responses = survey_svc.get_open_responses(request.column_key)

        if not request.responses:
            # Retornar vacío si no hay respuestas
            return AIAnalysisResult(
                column_key=request.column_key,
                column_label=request.column_key,
                summary="No hay respuestas disponibles para esta pregunta.",
            )

        result = await ai_svc.analyze(request)
        return result

    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
