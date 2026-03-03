"""
models/ai_analysis.py — Modelos Pydantic para los resultados de análisis IA.
"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class Theme(BaseModel):
    """Tema identificado en respuestas abiertas."""
    name: str
    description: str
    count: int = 0


class AIAnalysisResult(BaseModel):
    """Resultado completo del análisis IA sobre una pregunta abierta."""
    column_key: str
    column_label: str
    themes: list[Theme] = Field(default_factory=list)
    sentiment: str = "neutral"           # "positive" | "negative" | "neutral" | "mixed"
    sentiment_score: float = 0.0         # -1.0 a 1.0
    keywords: list[str] = Field(default_factory=list)
    patterns: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    summary: str = ""
    total_analyzed: int = 0
    provider_used: str = ""
    model_used: str = ""


class AIRequest(BaseModel):
    """Solicitud de análisis IA enviada desde el frontend."""
    column_key: str
    responses: list[str] = Field(default_factory=list)  # Opcional, se autocompleta desde el backend
    provider: str = "groq"   # "groq" | "ollama"
    api_key: Optional[str] = None
    model: Optional[str] = None
