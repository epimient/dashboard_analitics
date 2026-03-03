"""
services/ai_service.py — Strategy pattern para proveedores de IA.

Clases:
  AIProvider (abc)   → interfaz común
  GroqProvider       → llama la API de Groq Cloud
  OllamaProvider     → llama un servidor Ollama local
  AIService          → orquesta el proveedor elegido y construye prompts
"""
from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from typing import Optional

import httpx

from config import OPEN_QUESTIONS, settings
from models.ai_analysis import AIAnalysisResult, AIRequest, Theme

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt del sistema reutilizable
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """Eres un analista experto en investigación educativa.
Se te entregarán respuestas abiertas de una encuesta universitaria sobre modalidades de clase.
Tu tarea es analizar todas las respuestas y devolver un JSON estructurado con exactamente estos campos:
{
  "themes": [{"name": "...", "description": "...", "count": N}],
  "sentiment": "positive|negative|neutral|mixed",
  "sentiment_score": float entre -1.0 y 1.0,
  "keywords": ["kw1", "kw2", ...],
  "patterns": ["patrón 1", "patrón 2", ...],
  "recommendations": ["recomendación 1", ...],
  "summary": "resumen ejecutivo en 2-3 oraciones"
}
Responde ÚNICAMENTE con el JSON, sin texto adicional."""


def _build_user_prompt(question_label: str, responses: list[str]) -> str:
    numbered = "\n".join(f"{i + 1}. {r}" for i, r in enumerate(responses))
    return (
        f"Pregunta analizada: {question_label}\n\n"
        f"Respuestas de los estudiantes:\n{numbered}"
    )


# ---------------------------------------------------------------------------
# Proveedores
# ---------------------------------------------------------------------------

class AIProvider(ABC):
    """Interfaz abstracta para proveedores de IA."""

    @abstractmethod
    async def complete(self, system: str, user: str) -> str:
        """Envía el prompt y retorna el texto generado."""


class GroqProvider(AIProvider):
    """Llama a la API REST de Groq Cloud."""

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    async def complete(self, system: str, user: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.3,
            "max_tokens": 1500,
        }
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(self.BASE_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
        return data["choices"][0]["message"]["content"]


class OllamaProvider(AIProvider):
    """Llama a un servidor Ollama local."""

    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def complete(self, system: str, user: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{system}\n\n{user}",
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.3},
        }
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                f"{self.base_url}/api/generate", json=payload
            )
            resp.raise_for_status()
            data = resp.json()
        return data.get("response", "")


# ---------------------------------------------------------------------------
# Servicio orquestador
# ---------------------------------------------------------------------------

class AIService:
    """
    Construye el provider adecuado, genera el prompt y parsea la respuesta JSON.
    """

    def __init__(self) -> None:
        self._provider: Optional[AIProvider] = None

    def _get_provider(self, request: AIRequest) -> AIProvider:
        if request.provider == "groq":
            # Usar API key del request o la de settings
            api_key = request.api_key or settings.groq_api_key
            if not api_key:
                raise RuntimeError("Groq API key no configurada. Usa Ollama o configura GROQ_API_KEY en .env")
            model = request.model or settings.groq_model
            return GroqProvider(api_key=api_key, model=model)
        # default: ollama
        model = request.model or settings.ollama_model
        return OllamaProvider(base_url=settings.ollama_base_url, model=model)

    async def analyze(self, request: AIRequest) -> AIAnalysisResult:
        """Analiza una columna abierta y devuelve el resultado estructurado."""
        column_label = OPEN_QUESTIONS.get(request.column_key, request.column_key)
        provider = self._get_provider(request)

        # Filtrar respuestas vacías
        valid_responses = [r.strip() for r in request.responses if r and r.strip()]
        if not valid_responses:
            return AIAnalysisResult(
                column_key=request.column_key,
                column_label=column_label,
                summary="No hay respuestas disponibles para analizar.",
                total_analyzed=0,
            )

        user_prompt = _build_user_prompt(column_label, valid_responses)

        try:
            raw = await provider.complete(SYSTEM_PROMPT, user_prompt)
            result_data = self._parse_json(raw)
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"Error de API [{exc.response.status_code}]: {exc.response.text}")
        except Exception as exc:
            logger.exception("Error al analizar con IA")
            raise RuntimeError(f"Error en análisis IA: {exc}")

        provider_name = request.provider
        model_name = request.model or (
            settings.groq_model if request.provider == "groq" else settings.ollama_model
        )

        return AIAnalysisResult(
            column_key=request.column_key,
            column_label=column_label,
            themes=[Theme(**t) for t in result_data.get("themes", [])],
            sentiment=result_data.get("sentiment", "neutral"),
            sentiment_score=float(result_data.get("sentiment_score", 0.0)),
            keywords=result_data.get("keywords", []),
            patterns=result_data.get("patterns", []),
            recommendations=result_data.get("recommendations", []),
            summary=result_data.get("summary", ""),
            total_analyzed=len(valid_responses),
            provider_used=provider_name,
            model_used=model_name,
        )

    # ------------------------------------------------------------------

    @staticmethod
    def _parse_json(raw: str) -> dict:
        """Extrae el JSON de la respuesta, ignorando texto extra."""
        text = raw.strip()
        # Buscar bloque JSON entre llaves
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            text = text[start:end]
        return json.loads(text)
